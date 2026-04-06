"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

views.py – All views for the payments module.

Views:
    payment_page          – GET: show form  | POST: process payment
    payment_confirmation  – success landing page
    payment_failed        – failure landing page
    currency_rates        – public page listing all active exchange rates
    set_currency          – AJAX/form POST to save chosen currency in session
    api_convert           – JSON endpoint: convert amount between currencies
"""

import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.utils import timezone

from .models import Currency, ExchangeRate, Payment, Transaction
from .forms import PaymentForm, CurrencySelectForm
from .utils import convert_to_usd, get_active_currencies, get_latest_rate


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT PAGE  (main checkout payment step)
# ─────────────────────────────────────────────────────────────────────────────

def payment_page(request):
    """
    GET  → Display the payment form.
    POST → Validate the form, create Payment + Transaction, redirect to
           confirmation or failure page.

    URL: /payments/pay/
    Template: payments/payment_page.html
    """

    # ── Determine the order details ───────────────────────────────────────────
    # In a full integration Randy's cart/order system would set
    # session['pending_order_id'] and session['order_amount_usd'].
    # For now we fall back to demo values if the session keys are absent.
    order_id = request.session.get("pending_order_id", 0)
    order_amount_usd = Decimal(str(request.session.get("order_amount_usd", "25.00")))

    # ── Resolve the customer's preferred currency ─────────────────────────────
    chosen_code = request.session.get("selected_currency", "USD")
    try:
        chosen_currency = Currency.objects.get(currency_code=chosen_code, is_active=True)
    except Currency.DoesNotExist:
        chosen_currency = Currency.objects.filter(is_active=True).first()

    # Convert the USD amount into the customer's preferred currency
    if chosen_currency and chosen_currency.currency_code != "USD":
        rate_obj = get_latest_rate(chosen_currency.currency_code)
        if rate_obj and rate_obj.rate_to_usd > 0:
            display_amount = (order_amount_usd / rate_obj.rate_to_usd).quantize(
                Decimal("0.01")
            )
        else:
            display_amount = order_amount_usd
    else:
        display_amount = order_amount_usd

    if request.method == "GET":
        form = PaymentForm(
            initial={
                "order_id": order_id,
                "currency_code": chosen_currency,
                "payment_method": Payment.METHOD_CARD,
            }
        )
        context = {
            "form": form,
            "order_id": order_id,
            "order_amount_usd": order_amount_usd,
            "display_amount": display_amount,
            "chosen_currency": chosen_currency,
            "active_currencies": get_active_currencies(),
        }
        return render(request, "payments/payment_form.html", context)

    # ── POST: process the payment ─────────────────────────────────────────────
    form = PaymentForm(request.POST)
    if not form.is_valid():
        context = {
            "form": form,
            "order_id": order_id,
            "order_amount_usd": order_amount_usd,
            "display_amount": display_amount,
            "chosen_currency": chosen_currency,
            "active_currencies": get_active_currencies(),
        }
        return render(request, "payments/payment_form.html", context)

    # Extract validated data
    currency = form.cleaned_data["currency_code"]
    method = form.cleaned_data["payment_method"]

    # Recalculate display amount using the submitted currency (may differ)
    amount_in_chosen = order_amount_usd
    if currency.currency_code != "USD":
        rate_obj = get_latest_rate(currency.currency_code)
        if rate_obj and rate_obj.rate_to_usd > 0:
            amount_in_chosen = (order_amount_usd / rate_obj.rate_to_usd).quantize(
                Decimal("0.01")
            )

    # Create the Payment record
    payment = Payment.objects.create(
        order_id=form.cleaned_data["order_id"] or order_id,
        currency=currency,
        amount_in_currency=amount_in_chosen,
        amount_in_usd=order_amount_usd,
        payment_method=method,
        payment_status=Payment.STATUS_PENDING,
    )

    # Log the INITIATED transaction
    Transaction.objects.create(
        payment=payment,
        event_type=Transaction.EVENT_INITIATED,
        notes=f"Customer initiated payment via {method}.",
    )

    # ── Simulate payment processing ───────────────────────────────────────────
    # In production this is where you call an actual payment gateway API.
    # We simulate: card payments succeed, cash-on-delivery always succeeds,
    # bank transfer is left pending.
    if method in (Payment.METHOD_CARD, Payment.METHOD_MOBILE_MONEY):
        payment.mark_completed(reference=f"AFRI-{payment.pk:06d}")
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_SUCCESS,
            notes="Simulated payment gateway: approved.",
        )
        # Store payment id in session for the confirmation page
        request.session["last_payment_id"] = payment.pk
        # Clear the pending order from session
        request.session.pop("pending_order_id", None)
        request.session.pop("order_amount_usd", None)
        return redirect("payments:payment_confirmation")

    elif method == Payment.METHOD_CASH_ON_DELIVERY:
        payment.mark_completed(reference=f"COD-{payment.pk:06d}")
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_SUCCESS,
            notes="Cash on delivery – order confirmed.",
        )
        request.session["last_payment_id"] = payment.pk
        request.session.pop("pending_order_id", None)
        request.session.pop("order_amount_usd", None)
        return redirect("payments:payment_confirmation")

    else:
        # Bank transfer stays PENDING
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_INITIATED,
            notes="Bank transfer pending bank confirmation.",
        )
        request.session["last_payment_id"] = payment.pk
        return redirect("payments:payment_confirmation")


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT CONFIRMATION
# ─────────────────────────────────────────────────────────────────────────────

def payment_confirmation(request):
    """
    Shown after a successful (or pending) payment.

    URL: /payments/confirmation/
    Template: payments/payment_confirmation.html
    """
    payment_id = request.session.get("last_payment_id")
    payment = None
    if payment_id:
        payment = get_object_or_404(Payment, pk=payment_id)

    context = {"payment": payment}
    return render(request, "payments/payment_confirmation.html", context)


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT FAILED
# ─────────────────────────────────────────────────────────────────────────────

def payment_failed(request):
    """
    Shown when a payment could not be processed.

    URL: /payments/failed/
    Template: payments/payment_failed.html
    """
    payment_id = request.session.get("last_payment_id")
    payment = None
    if payment_id:
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            pass

    context = {"payment": payment}
    return render(request, "payments/payment_failed.html", context)


# ─────────────────────────────────────────────────────────────────────────────
# CURRENCY RATES PAGE
# ─────────────────────────────────────────────────────────────────────────────

def currency_rates(request):
    """
    Public page that lists all active currencies and their latest rates vs USD.

    URL: /payments/currencies/
    Template: payments/currency_rates.html
    """
    currencies = get_active_currencies()

    # For each currency, attach its latest rate
    currency_data = []
    for curr in currencies:
        rate_obj = get_latest_rate(curr.currency_code)
        currency_data.append(
            {
                "currency": curr,
                "rate": rate_obj,
            }
        )

    context = {
        "currency_data": currency_data,
        "last_updated": timezone.now(),
    }
    return render(request, "payments/currency_rates.html", context)


# ─────────────────────────────────────────────────────────────────────────────
# SET CURRENCY (session-based currency selector)
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def set_currency(request):
    """
    Saves the user's preferred currency in their session.
    Called when the navbar currency selector changes.

    POST body (form or JSON): { "currency_code": "XAF" }
    Redirects back to the referring page (or home).

    URL: /payments/set-currency/
    """
    code = request.POST.get("currency_code", "")
    if Currency.objects.filter(currency_code=code, is_active=True).exists():
        request.session["selected_currency"] = code

    # Redirect back to where the user was
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")
    return redirect(next_url)


# ─────────────────────────────────────────────────────────────────────────────
# API: CURRENCY CONVERSION  (JSON endpoint for frontend JS)
# ─────────────────────────────────────────────────────────────────────────────

@require_GET
def api_convert(request):
    """
    Converts an amount from one currency to another.

    Query params:
        amount   – the numeric amount to convert
        from     – source currency code (e.g. USD)
        to       – target currency code (e.g. XAF)

    Returns JSON:
        { 
            "success": true, 
            "amount": 1234.56, 
            "rate": 655.957,
            "symbol": "FCFA",
            "formatted": "FCFA 1,234.56" 
        }
    or on error:
        { "success": false, "error": "..." }

    URL: /payments/api/convert/?amount=10&from=USD&to=XAF
    """
    try:
        amount = Decimal(request.GET.get("amount", "0"))
        from_code = request.GET.get("from", "USD").upper()
        to_code = request.GET.get("to", "USD").upper()

        # Convert: from_code → USD → to_code
        usd_amount = convert_to_usd(amount, from_code)

        if to_code == "USD":
            result = usd_amount
            rate = Decimal("1.0")
        else:
            rate_obj = get_latest_rate(to_code)
            if rate_obj is None or rate_obj.rate_to_usd == 0:
                return JsonResponse(
                    {"success": False, "error": f"No exchange rate for {to_code}"}
                )
            result = (usd_amount / rate_obj.rate_to_usd).quantize(Decimal("0.01"))
            rate = rate_obj.rate_to_usd

        try:
            target_currency = Currency.objects.get(currency_code=to_code)
            formatted = f"{target_currency.symbol} {float(result):,.2f}"
            symbol = target_currency.symbol
        except Currency.DoesNotExist:
            formatted = f"{to_code} {float(result):,.2f}"
            symbol = to_code

        return JsonResponse(
            {
                "success": True, 
                "amount": float(result), 
                "rate": float(rate),
                "symbol": symbol,
                "formatted": formatted,
                "currency_code": to_code
            }
        )

    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)})


# ─────────────────────────────────────────────────────────────────────────────
# ORDER PAYMENT FLOW (for checkout integration)
# ─────────────────────────────────────────────────────────────────────────────

from django.contrib.auth.decorators import login_required
from orders.models import Order


@login_required(login_url='accounts:login')
def order_payment_view(request, order_id):
    """
    Display payment form for a specific order.
    Customer selects payment method and currency, then proceeds to pay.
    
    URL: /payments/order/<order_id>/pay/
    Template: payments/order_payment.html
    """
    # Get the order - ensure it belongs to the logged-in customer
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # If order is already paid, redirect to confirmation
    if order.status != 'pending':
        messages.info(request, "This order has already been processed.")
        return redirect('orders:order_detail', order_id=order.id)
    
    # Get customer's preferred currency or default to USD
    chosen_code = request.session.get("selected_currency", "USD")
    try:
        chosen_currency = Currency.objects.get(currency_code=chosen_code, is_active=True)
    except Currency.DoesNotExist:
        try:
            chosen_currency = Currency.objects.filter(is_active=True).first()
            if not chosen_currency:
                chosen_currency = Currency.objects.get(currency_code="USD")
        except Currency.DoesNotExist:
            messages.error(request, "Currency configuration error. Please contact support.")
            return redirect('orders:cart_view')
    
    # Calculate order total
    order_total_usd = order.get_items_total()
    
    # Convert to customer's currency for display
    if chosen_currency.currency_code != "USD":
        rate_obj = get_latest_rate(chosen_currency.currency_code)
        if rate_obj and rate_obj.rate_to_usd > 0:
            display_amount = (order_total_usd / rate_obj.rate_to_usd).quantize(Decimal("0.01"))
        else:
            display_amount = order_total_usd
    else:
        display_amount = order_total_usd
    
    if request.method == "GET":
        form = PaymentForm(
            initial={
                "order_id": order_id,
                "currency_code": chosen_currency,
                "payment_method": Payment.METHOD_CARD,
            }
        )
        context = {
            "form": form,
            "order": order,
            "order_total_usd": order_total_usd,
            "display_amount": display_amount,
            "chosen_currency": chosen_currency,
            "active_currencies": get_active_currencies(),
        }
        return render(request, "payments/order_payment.html", context)
    
    # ── POST: Process the payment ─────────────────────────────────────────────
    form = PaymentForm(request.POST)
    if not form.is_valid():
        context = {
            "form": form,
            "order": order,
            "order_total_usd": order_total_usd,
            "display_amount": display_amount,
            "chosen_currency": chosen_currency,
            "active_currencies": get_active_currencies(),
        }
        return render(request, "payments/order_payment.html", context)
    
    # Extract validated data
    currency = form.cleaned_data["currency_code"]
    method = form.cleaned_data["payment_method"]
    
    # Calculate amount in chosen currency
    amount_in_chosen = order_total_usd
    if currency.currency_code != "USD":
        rate_obj = get_latest_rate(currency.currency_code)
        if rate_obj and rate_obj.rate_to_usd > 0:
            amount_in_chosen = (order_total_usd / rate_obj.rate_to_usd).quantize(Decimal("0.01"))
    
    # Create Payment record
    payment = Payment.objects.create(
        order_id=order_id,
        currency=currency,
        amount_in_currency=amount_in_chosen,
        amount_in_usd=order_total_usd,
        payment_method=method,
        payment_status=Payment.STATUS_PENDING,
    )
    
    # Log INITIATED transaction
    Transaction.objects.create(
        payment=payment,
        event_type=Transaction.EVENT_INITIATED,
        notes=f"Customer initiated payment for Order #{order_id} via {method}.",
    )
    
    # ── Simulate payment processing ───────────────────────────────────────────
    # Simulate: Card & Mobile Money succeed, Cash on Delivery is pending
    if method in (Payment.METHOD_CARD, Payment.METHOD_MOBILE_MONEY):
        payment.mark_completed(reference=f"AFRI-{payment.pk:06d}")
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_SUCCESS,
            notes="Simulated payment gateway: approved.",
        )
        
        # Update order status to confirmed and set total price
        order.status = 'confirmed'
        order.total_price = order_total_usd
        order.save()
        
        messages.success(request, f"Payment successful! Order #{order_id} confirmed.")
        return redirect('payments:order_payment_confirmation', order_id=order_id)
    
    elif method == Payment.METHOD_CASH_ON_DELIVERY:
        payment.mark_completed(reference=f"COD-{payment.pk:06d}")
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_SUCCESS,
            notes="Cash on Delivery: payment pending delivery.",
        )
        
        # Update order status to confirmed and set total price
        order.status = 'confirmed'
        order.total_price = order_total_usd
        order.save()
        
        messages.success(request, f"Order #{order_id} confirmed! We'll collect payment on delivery.")
        return redirect('payments:order_payment_confirmation', order_id=order_id)
    
    elif method == Payment.METHOD_BANK_TRANSFER:
        Transaction.objects.create(
            payment=payment,
            event_type=Transaction.EVENT_INITIATED,
            notes="Bank Transfer: awaiting payment.",
        )
        
        messages.warning(request, "Bank transfer initiated. Your order will be confirmed once we receive your payment.")
        return redirect('payments:order_payment_failed', order_id=order_id)


@login_required(login_url='accounts:login')
def order_payment_confirmation_view(request, order_id):
    """
    Show payment confirmation for a completed order.
    
    URL: /payments/order/<order_id>/confirmation/
    Template: payments/order_payment_confirmation.html
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Get payment for this order
    payment = Payment.objects.filter(order_id=order_id).first()
    
    # Get transactions for the payment
    transactions = payment.transactions.all() if payment else None
    
    context = {
        'order': order,
        'payment': payment,
        'transactions': transactions,
        'order_items': order.items.all(),
    }
    return render(request, 'payments/order_payment_confirmation.html', context)


@login_required(login_url='accounts:login')
def order_payment_failed_view(request, order_id):
    """
    Show payment failed/pending page for an order.
    
    URL: /payments/order/<order_id>/failed/
    Template: payments/order_payment_failed.html
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Get payment for this order
    payment = Payment.objects.filter(order_id=order_id).first()
    
    context = {
        'order': order,
        'payment': payment,
    }
    return render(request, 'payments/order_payment_failed.html', context)
