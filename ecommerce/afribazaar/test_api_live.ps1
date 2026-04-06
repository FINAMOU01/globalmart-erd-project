#!/usr/bin/env powershell
# Test l'API de conversion de devises

Write-Host "======================================================================="
Write-Host " Testing Currency Conversion API"
Write-Host "======================================================================="
Write-Host ""
Write-Host "Server running at: http://localhost:8000"
Write-Host ""

# Function to test API endpoint
function Test-CurrencyConversion {
    param(
        [string]$FromCurrency = "USD",
        [string]$ToCurrency,
        [decimal]$Amount = 95.00
    )
    
    $url = "http://localhost:8000/payments/api/convert/?from=$FromCurrency&to=$ToCurrency&amount=$Amount"
    Write-Host "Test: $Amount $FromCurrency → $ToCurrency"
    Write-Host "URL: $url"
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -Headers @{"Accept"="application/json"}
        $data = $response.Content | ConvertFrom-Json
        
        if ($data.success) {
            Write-Host "  ✓ Success!"
            Write-Host "  Amount: $($data.formatted)"
            Write-Host "  Symbol: $($data.symbol)"
            Write-Host "  Rate: $($data.rate)"
            Write-Host ""
        } else {
            Write-Host "  ✗ Error: $($data.error)"
            Write-Host ""
        }
    } catch {
        Write-Host "  ✗ Connection error: $_"
        Write-Host ""
    }
}

# Test various conversions
Write-Host "Testing currency conversions..."
Write-Host ""

Test-CurrencyConversion -FromCurrency "USD" -ToCurrency "EUR" -Amount 95
Test-CurrencyConversion -FromCurrency "USD" -ToCurrency "NGN" -Amount 95
Test-CurrencyConversion -FromCurrency "USD" -ToCurrency "XAF" -Amount 95
Test-CurrencyConversion -FromCurrency "USD" -ToCurrency "ZAR" -Amount 95
Test-CurrencyConversion -FromCurrency "USD" -ToCurrency "GHS" -Amount 95

Write-Host "======================================================================="
Write-Host " Testing Complete!"
Write-Host "======================================================================="
Write-Host ""
Write-Host "Next: Open your browser and test the payment form:"
Write-Host "  → http://localhost:8000/payments/pay/"
Write-Host ""
Write-Host "Tips:"
Write-Host "  1. Open DevTools (F12) to see console messages"
Write-Host "  2. Select different payment methods"
Write-Host "  3. Change currencies and watch amounts update"
Write-Host "  4. Check the Network tab to see API calls"
Write-Host ""
Write-Host "======================================================================="
