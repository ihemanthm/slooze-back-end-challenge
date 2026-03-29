# ☁️ Cloud Deployment Guide - Free Platforms

## 🎯 Quick Comparison

| Platform | Database | Auto-Deploy | Free Tier | Best For |
|----------|----------|-------------|-----------|----------|
| **Render** | ✅ PostgreSQL | ✅ GitHub | 750 hrs/month | Easiest setup |
| **Railway** | ✅ PostgreSQL | ✅ GitHub | $5 credit/month | Docker support |
| **Fly.io** | ⚠️ Separate setup | ✅ GitHub | Limited free | Global edge |

---

## 🚀 Option 1: Render.com (Recommended)

### Step 1: Create Account
1. Go to https://render.com
2. Sign up with your GitHub account (`ihemanthm`)

### Step 2: Create PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Name: `slooze-db`
3. Database: `slooze_db`
4. User: `slooze_user`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click **"Create Database"**
8. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 3: Deploy FastAPI Application
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `ihemanthm/slooze-back-end-challenge`
3. Configure:
   - **Name:** `slooze-api`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Environment:** `Docker`
   - **Plan:** `Free`

4. **Environment Variables** (click "Add Environment Variable"):
   ```
   DATABASE_URL = <paste Internal Database URL from Step 2>
   SECRET_KEY = <generate random string>
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

5. **Build Command:**
   ```bash
   alembic upgrade head && python scripts/seed_data.py
   ```

6. **Start Command:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

7. Click **"Create Web Service"**

### Step 4: Wait for Deployment
- First deploy takes 5-10 minutes
- Watch the logs for any errors
- Once deployed, you'll get a URL like: `https://slooze-api.onrender.com`

### Step 5: Test Your API
```bash
# Health check
curl https://slooze-api.onrender.com/health

# Swagger UI
open https://slooze-api.onrender.com/docs
```

---

## 🚂 Option 2: Railway.app

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
# or
brew install railway
```

### Step 2: Login and Initialize
```bash
# Login
railway login

# Initialize project
railway init
```

### Step 3: Add PostgreSQL
```bash
railway add --database postgresql
```

### Step 4: Deploy
```bash
# Deploy from current directory
railway up

# Set environment variables
railway variables set SECRET_KEY=$(openssl rand -base64 32)
railway variables set ALGORITHM=HS256
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 5: Run Migrations
```bash
railway run alembic upgrade head
railway run python scripts/seed_data.py
```

### Step 6: Get URL
```bash
railway domain
```

---

## ✈️ Option 3: Fly.io

### Step 1: Install Fly CLI
```bash
# macOS
brew install flyctl

# Or download from https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Login and Launch
```bash
# Login
flyctl auth login

# Launch app (uses fly.toml)
flyctl launch --no-deploy

# When prompted:
# - App name: slooze-api
# - Region: Choose closest
# - PostgreSQL: Yes
# - Redis: No
```

### Step 3: Set Secrets
```bash
# Generate and set secret key
flyctl secrets set SECRET_KEY=$(openssl rand -base64 32)

# Get database URL
flyctl postgres attach <postgres-app-name>
```

### Step 4: Deploy
```bash
# Deploy application
flyctl deploy

# Run migrations
flyctl ssh console -C "alembic upgrade head"
flyctl ssh console -C "python scripts/seed_data.py"
```

### Step 5: Open App
```bash
flyctl open
```

---

## 🔧 Post-Deployment Setup

### Update CORS Origins
After deployment, update `app/main.py` to include your production URL:

```python
origins = [
    "http://localhost:3000",
    "https://slooze-api.onrender.com",  # Add your Render URL
    "https://your-frontend-domain.com",
]
```

### Test All Endpoints
```bash
# Replace with your deployed URL
export API_URL="https://slooze-api.onrender.com"

# Test login
curl -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=nick.fury@slooze.com&password=admin123"

# Test restaurants
curl "$API_URL/api/v1/restaurants"
```

---

## 📊 Monitoring & Logs

### Render
```bash
# View logs in dashboard
# Or use Render CLI
render logs -s slooze-api
```

### Railway
```bash
railway logs
```

### Fly.io
```bash
flyctl logs
```

---

## 💰 Free Tier Limits

### Render
- 750 hours/month (enough for 1 app running 24/7)
- 512 MB RAM
- Sleeps after 15 min inactivity
- 100 GB bandwidth/month

### Railway
- $5 credit/month
- ~500 hours of usage
- 512 MB RAM
- 100 GB bandwidth

### Fly.io
- 3 shared-cpu-1x VMs
- 160GB outbound data transfer
- PostgreSQL: 3GB storage

---

## 🎯 Recommended: Render.com

**Why Render?**
- ✅ Easiest setup (no CLI needed)
- ✅ Free PostgreSQL included
- ✅ Auto-deploys from GitHub
- ✅ Free SSL certificates
- ✅ Good for demos/portfolios

**Limitations:**
- ⚠️ Sleeps after 15 min inactivity (first request takes ~30s to wake)
- ⚠️ 512 MB RAM (sufficient for this app)

---

## 🔄 Auto-Deploy from GitHub

All platforms support automatic deployment when you push to GitHub:

1. **Render:** Enable in dashboard → Settings → Build & Deploy
2. **Railway:** Automatic by default
3. **Fly.io:** Setup GitHub Actions workflow

---

## 📝 Quick Start Checklist

- [ ] Choose platform (Render recommended)
- [ ] Create account and link GitHub
- [ ] Create PostgreSQL database
- [ ] Deploy web service
- [ ] Set environment variables
- [ ] Run migrations and seed data
- [ ] Test API endpoints
- [ ] Update CORS settings
- [ ] Share your live API URL!

---

**Your API will be live at a URL like:**
- Render: `https://slooze-api.onrender.com`
- Railway: `https://slooze-api.up.railway.app`
- Fly.io: `https://slooze-api.fly.dev`

🎉 **Ready to deploy!**
