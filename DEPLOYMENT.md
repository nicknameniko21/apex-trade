# Deployment Guide - CTO Autonomous Brain

This guide provides detailed instructions for deploying and accessing the Swarm Intelligence Control Center.

## Quick Start

The application is configured for deployment to Vercel with minimal setup required.

## Deployment Options

### Option 1: Vercel Deployment (Recommended)

Vercel provides free hosting for Python applications with serverless functions.

#### Step 1: Prepare Your Repository

The repository already includes all necessary configuration files:
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `.vercelignore` - Files to exclude from deployment
- ✅ `api/index.py` - Serverless function entrypoint

#### Step 2: Deploy to Vercel

1. **Sign up/Login to Vercel**:
   - Visit https://vercel.com
   - Sign up with GitHub (recommended) or email
   - Authorize Vercel to access your GitHub repositories

2. **Import Your Project**:
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose `nicknameniko21/apex-trade` from the list
   - Click "Import"

3. **Configure Project**:
   - Vercel will automatically detect the Python configuration
   - Project Name: `apex-trade` (or customize)
   - Framework Preset: Other
   - Root Directory: `./` (default)
   - **No build command needed** - Vercel handles it automatically

4. **Deploy**:
   - Click "Deploy"
   - Wait 1-2 minutes for deployment to complete
   - You'll see a success screen with your deployment URL

#### Step 3: Access Your Application

Once deployed, you'll receive a URL like:
- Production: `https://apex-trade.vercel.app`
- Or custom: `https://your-custom-name.vercel.app`

**Available Endpoints**:
- `/` - Swarm Intelligence Control Center (Web UI)
- `/api/agents` - Agent management API
- `/api/tasks` - Task management API
- `/api/status` - System status
- `/api/chat` - Natural language interface

### Option 2: Local Development

Run the application locally for development and testing.

#### Requirements

- Python 3.8 or higher
- pip (Python package manager)

#### Setup Steps

```bash
# 1. Clone the repository (if not already done)
git clone https://github.com/nicknameniko21/apex-trade.git
cd apex-trade

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python ui_server.py
```

The server will start on `http://localhost:5000`

#### Local Testing

```bash
# Test the API endpoints
curl http://localhost:5000/api/status

# Test agent listing
curl http://localhost:5000/api/agents

# Open in browser
open http://localhost:5000  # macOS
start http://localhost:5000  # Windows
xdg-open http://localhost:5000  # Linux
```

### Option 3: Other Platforms

The application can be deployed to other Python-compatible platforms:

#### Heroku

```bash
# Install Heroku CLI
# Add Procfile:
echo "web: python ui_server.py" > Procfile

# Deploy
heroku create apex-trade-app
git push heroku main
```

#### Railway

1. Visit https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `apex-trade` repository
4. Railway will auto-detect Python and deploy

#### Google Cloud Run

```bash
# Create Dockerfile
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "ui_server.py"]
EOF

# Deploy
gcloud run deploy apex-trade --source .
```

## Troubleshooting

### Deployment Fails

**Issue**: Vercel deployment fails with module import error

**Solution**: Ensure `requirements.txt` includes all dependencies:
```
Flask>=2.3.0,<4.0.0
flask-cors>=4.0.0,<5.0.0
pytest>=7.4.4,<8.0.0
```

### Cold Start Timeout

**Issue**: First request after inactivity takes too long

**Solution**: This is normal for serverless functions. The application uses lazy initialization to minimize cold start impact.

### Templates Not Found

**Issue**: Error: `TemplateNotFound: index.html`

**Solution**: Ensure the `templates/` directory is included in deployment. Check `.vercelignore` doesn't exclude it.

### API Routes Return 404

**Issue**: API endpoints return 404 errors

**Solution**: Check `vercel.json` routing configuration:
```json
{
  "routes": [
    {"src": "/api/(.*)", "dest": "api/index.py"},
    {"src": "/(.*)", "dest": "api/index.py"}
  ]
}
```

## Monitoring & Maintenance

### Vercel Dashboard

Monitor your deployment at:
- https://vercel.com/dashboard
- View logs, analytics, and deployment history
- Configure custom domains
- Set environment variables

### Logs

**View Logs in Vercel**:
1. Go to your project dashboard
2. Click on a deployment
3. Click "View Function Logs"

**Local Logs**:
```bash
# Run with debug mode for detailed logs
python ui_server.py
# Check console output for errors
```

## Environment Variables

If needed, add environment variables in Vercel:

1. Go to Project Settings → Environment Variables
2. Add any required variables:
   - `FLASK_ENV=production`
   - Custom API keys or configuration

## Updating Your Deployment

### Automatic Deployments

Vercel automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update application"
git push origin main
```

Vercel will:
1. Detect the push
2. Build and deploy automatically
3. Provide a preview URL for testing
4. Deploy to production if successful

### Manual Redeployment

In Vercel dashboard:
1. Go to your project
2. Click "Deployments"
3. Find a previous deployment
4. Click "..." → "Redeploy"

## Security Considerations

- ✅ Sensitive files excluded via `.vercelignore`
- ✅ Logs and session data not deployed
- ✅ Auto-backup scripts excluded from deployment
- ⚠️ Add authentication if exposing publicly
- ⚠️ Consider rate limiting for API endpoints

## Next Steps

After deployment:

1. **Test the Application**: Visit all main endpoints
2. **Configure Custom Domain**: Set up in Vercel settings
3. **Add Monitoring**: Set up uptime monitoring (e.g., UptimeRobot)
4. **Enable Analytics**: Use Vercel Analytics
5. **Set Up CI/CD**: Configure GitHub Actions for testing

## Support

For issues:
- Check Vercel documentation: https://vercel.com/docs
- Review Flask documentation: https://flask.palletsprojects.com/
- Repository: https://github.com/nicknameniko21/apex-trade

---

**Generated by CTO Autonomous Brain System**
