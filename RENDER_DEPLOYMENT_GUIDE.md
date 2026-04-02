# 🚀 AfriBazaar Deployment Guide - Render.com

## ✅ Priority 1 - COMPLETED
- [x] Moved SECRET_KEY to environment variable
- [x] Moved DB credentials to environment variables
- [x] Fixed ALLOWED_HOSTS (now uses environment variable)
- [x] Created Procfile
- [x] Created runtime.txt
- [x] Added WhiteNoise middleware for static files

---

## 📝 Step-by-Step Deployment Instructions

### 1. **Push to GitHub**

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

⚠️ **Important**: Make sure `.env` is in `.gitignore` (not committed)

### 2. **Create Render Account**
- Go to https://render.com
- Sign up with GitHub

### 3. **Create New Web Service**
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select the branch (main)

### 4. **Configure Environment**

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn afribazaar.wsgi
```

**Environment Variables** (Add these in Render Dashboard):

```
SECRET_KEY=generate-a-new-secret-key-using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=your-neon-database-password
DB_HOST=your-neon-host.us-east-1.aws.neon.tech
DB_PORT=5432

ALLOWED_HOSTS=yourdomain.onrender.com

DEBUG=False
```

### 5. **Generate New Secret Key**

Run locally and copy the output:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Paste into `SECRET_KEY` environment variable on Render.

### 6. **Get Your Neon Credentials**

From your Neon Console:
1. Go to Connection String
2. Copy: host, user, password, database
3. Set as environment variables on Render

### 7. **Deploy**
- Click "Create Web Service"
- Render will automatically deploy
- Watch the build logs for any errors

### 8. **Test Your App**
- Visit `https://yourdomain.onrender.com`
- Admin: `/admin/`
- Products should load from Neon database

---

## 📂 Project Structure for Deployment

```
ecommerce/afribazaar/
├── manage.py
├── Procfile                    ✓ NEW (tells Render how to run)
├── runtime.txt                 ✓ NEW (specifies Python version)
├── requirements.txt            ✓ Has 45+ dependencies
├── .env.example                ✓ NEW (reference for env vars)
├── afribazaar/
│   ├── settings.py             ✓ UPDATED (uses env variables)
│   ├── wsgi.py
│   └── urls.py
├── products/
├── orders/
├── payments/
├── accounts/
├── users/
├── staticfiles/                ✓ Will be collected by Render
├── media/                      ⚠️ TODO: Use S3 for production
└── templates/
```

---

## 🔧 Troubleshooting

### **Build Fails**
1. Check "Logs" tab in Render Dashboard
2. Make sure all environment variables are set
3. Verify `requirements.txt` has all dependencies

### **500 Error After Deploy**
- Check Render logs: https://dashboard.render.com
- Run: `python manage.py check --deploy` locally to verify settings

### **Database Connection Error**
- Verify `DB_HOST`, `DB_USER`, `DB_PASSWORD` environment variables
- Check Neon is not in sleep mode
- Test connection locally with those credentials first

### **Static Files Not Loading** 
- Run: `python manage.py collectstatic --noinput` locally to verify
- WhiteNoise is now in middleware, should handle it automatically

### **Media Files Upload Issues**
- Local `media/` folder won't persist on Render
- Solution: Use AWS S3 or similar cloud storage (Priority 2)

---

## ✅ Pre-Deployment Checklist

- [x] SECRET_KEY moved to environment variable
- [x] Database credentials moved to environment variables
- [x] ALLOWED_HOSTS configured dynamically
- [x] Procfile created
- [x] runtime.txt created
- [x] WhiteNoise added to middleware
- [ ] .env variables set in Render Dashboard
- [ ] Neon database populated with data
- [ ] GitHub repository pushed
- [ ] First deployment test completed

---

## 🎯 Next Steps (Priority 2)

- [ ] Set up AWS S3 for media file uploads
- [ ] Configure error tracking (Sentry)
- [ ] Set up email notifications
- [ ] Configure production logging
- [ ] Set up SSL certificate (automatic on Render)
- [ ] Create custom domain mapping

---

**Status**: 🟢 Ready for deployment (with environment variables configured on Render)
