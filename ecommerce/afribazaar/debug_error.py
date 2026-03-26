import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.forms import CustomerRegisterForm
from django.core.exceptions import ValidationError

form_data = {
    'username': 'testuser123',
    'email': 'test@example.com',
    'phone': '1234567890',
    'address': '123 Main St',
    'password1': 'testuser123',
    'password2': 'testuser123'
}

print("=" * 60)
print("Creating form...")
form = CustomerRegisterForm(data=form_data)

#Override add_error to trace where errors are added
original_add_error = form.add_error
def trace_add_error(field, error):
    print(f"[DEBUG] add_error called: field={field}, error={error}")
    traceback.print_stack()
    return original_add_error(field, error)
form.add_error = trace_add_error

print("\n" + "=" * 60)
print("Calling is_valid()...")
result = form.is_valid()
print(f"Result: {result}")

print("\n" + "=" * 60)
print(f"Final form.errors: {form.errors}")



