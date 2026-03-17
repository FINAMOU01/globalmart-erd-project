@echo off
REM AfriBazaar Setup Script for Windows
REM Quick setup for development

echo ================================
echo AfriBazaar Setup Script
echo ================================

REM Step 1: Install dependencies
echo.
echo [1/7] Installing Python dependencies...
pip install -r requirements.txt

REM Step 2: Create migrations
echo [2/7] Creating migrations...
python manage.py makemigrations users
python manage.py makemigrations products

REM Step 3: Apply migrations
echo [3/7] Applying migrations...
python manage.py migrate

REM Step 4: Create media directories
echo [4/7] Creating media directories...
if not exist media\products mkdir media\products
if not exist media\artisans mkdir media\artisans
if not exist media\categories mkdir media\categories

REM Step 5: Collect static files
echo [5/7] Collecting static files...
python manage.py collectstatic --noinput

REM Step 6: Create superuser
echo [6/7] Creating superuser...
python manage.py createsuperuser

REM Step 7: Load sample data
echo [7/7] Loading sample data...
python manage.py loaddata products/fixtures/sample_data.json

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Run: python manage.py runserver
echo 2. Visit: http://localhost:8000/admin/
echo 3. Browse: http://localhost:8000/products/shop/
echo.
pause
