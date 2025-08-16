# 🚀 Railway Deployment Guide for Audify Music Bot

This guide will help you deploy your Audify Music Bot to Railway successfully.

## 📋 Prerequisites

1. **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather)
2. **Telegram API Credentials**: Get from [my.telegram.org](https://my.telegram.org)
3. **MongoDB Database**: Create a free MongoDB Atlas cluster
4. **Railway Account**: Sign up at [railway.app](https://railway.app)

## 🔧 Setup Steps

### 1. Fork/Clone the Repository
```bash
git clone https://github.com/yourusername/Alphabot.git
cd Alphabot
```

### 2. Configure Environment Variables

Copy the sample environment file and configure it:
```bash
cp sample.env .env
```

Edit `.env` with your actual values:
- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `BOT_TOKEN`: Your bot token from @BotFather
- `OWNER_ID`: Your Telegram user ID
- `MONGO_DB_URI`: Your MongoDB connection string
- `STRING_SESSION`: Pyrogram session string for assistant

### 3. Generate String Sessions

For assistant accounts, generate Pyrogram session strings:

```python
from pyrogram import Client

# Generate session for assistant
app = Client(
    "my_account",
    api_id=YOUR_API_ID,
    api_hash=YOUR_API_HASH
)

with app:
    print(app.export_session_string())
```

### 4. Deploy to Railway

#### Option A: Using Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Option B: Using Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway will automatically detect the configuration

### 5. Configure Environment Variables in Railway

In your Railway project dashboard:
1. Go to "Variables" tab
2. Add all variables from your `.env` file
3. Make sure to set `RAILWAY_URL` to your app's URL

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails with Git Checkout Error**
   - ✅ Fixed: Updated `requirements.txt` to use PyPI packages instead of git repositories

2. **Python Version Mismatch**
   - ✅ Fixed: Updated Dockerfile to use Python 3.11

3. **Missing Dependencies**
   - ✅ Fixed: Added all required packages to requirements.txt

4. **Health Check Failures**
   - ✅ Fixed: Added web server for Railway health checks

5. **Dependency Conflicts (pytgcalls/tgcalls)**
   - ✅ Fixed: Using simplified requirements with fixed versions
   - ✅ Fixed: Using `requirements-simple.txt` with minimal dependencies

6. **Build Timeout (apt-get install fails)**
   - ✅ Fixed: Optimized Dockerfile with minimal system dependencies
   - ✅ Fixed: Reduced build context size with improved .dockerignore
   - ✅ Fixed: Using only essential packages to avoid timeouts

7. **tgcalls Version Not Found**
   - ✅ Fixed: Updated to use `tgcalls==3.0.0.dev6` (available version)
   - ✅ Fixed: Added fallback requirements with alternative versions
   - ✅ Fixed: Dockerfile now tries alternative requirements if main fails

8. **pytgcalls Version Not Found**
   - ✅ Fixed: Using `pytgcalls>=2.0.0` to let pip choose available version
   - ✅ Fixed: Removed problematic alternative requirements
   - ✅ Fixed: Simplified Dockerfile to avoid fallback issues

9. **Dependency Resolution Conflicts**
   - ✅ Fixed: Using compatible versions (`pytgcalls==2.1.0`, `tgcalls==2.0.0`)
   - ✅ Fixed: Added basic requirements fallback without pytgcalls
   - ✅ Fixed: Smart Dockerfile with fallback options

10. **ModuleNotFoundError: No module named 'pytgcalls'**
    - ✅ Fixed: Made pytgcalls imports optional with graceful fallback
    - ✅ Fixed: Bot can now run without pytgcalls (voice features disabled)
    - ✅ Fixed: Added proper error handling for missing voice dependencies

11. **ModuleNotFoundError: No module named 'config'**
    - ✅ Fixed: Created multiple config import locations
    - ✅ Fixed: Added fallback config in Audify package
    - ✅ Fixed: Updated start command with better error handling
    - ✅ Fixed: Created simple start script with debugging

### Debugging Steps

1. **Check Build Logs**
   - Go to Railway dashboard → Deployments → View logs

2. **Check Application Logs**
   - Go to Railway dashboard → Deployments → HTTP Logs

3. **Test Health Endpoint**
   - Visit: `https://your-app.up.railway.app/health`

4. **Check Environment Variables**
   - Ensure all required variables are set in Railway dashboard

5. **Test Package Versions**
   - Run: `python3 test_requirements.py` to check available versions

6. **Test Basic Requirements**
   - Run: `python3 test_basic.py` to test imports

7. **Test Config Import**
   - Run: `python3 test_config.py` to test config import

8. **Test Start Process**
   - Run: `python3 test_start.py` to test complete start process

## 📊 Monitoring

### Health Check Endpoints
- **Main Page**: `https://your-app.up.railway.app/`
- **Health API**: `https://your-app.up.railway.app/health`

### Logs
- Railway automatically provides logs in the dashboard
- Check "Deploy Logs" for build issues
- Check "HTTP Logs" for runtime issues

## 🔄 Updates

To update your bot:
1. Push changes to your GitHub repository
2. Railway will automatically redeploy
3. Monitor the deployment logs for any issues

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Railway deployment logs
3. Ensure all environment variables are correctly set
4. Contact support at [@devforgekush](https://t.me/devforgekush)

## 📝 Notes

- The bot includes a web server for Railway health checks
- Automatic pinging is enabled if `RAILWAY_URL` is set
- All dependencies are now from PyPI to avoid git checkout issues
- Python 3.11 is used for better compatibility
- Using simplified requirements to avoid dependency conflicts
- Fixed pytgcalls/tgcalls version conflicts
- Optimized for Railway's build constraints and timeouts
- Multiple requirements files for fallback options
- Using flexible version ranges to avoid specific version issues
- Smart fallback system for dependency resolution
- **pytgcalls is now optional** - bot works without voice features if pytgcalls fails
- **Multiple config locations** - config can be imported from root or Audify package
- **Simple start script** - better error handling and debugging

## 🔧 Recent Fixes

### Dependency Conflict Resolution
- **Issue**: `pytgcalls` and `tgcalls` version conflicts
- **Solution**: Using compatible versions (`pytgcalls==2.1.0`, `tgcalls==2.0.0`)
- **Result**: Eliminates pip dependency resolution errors

### Simplified Requirements
- Created `requirements-working.txt` with minimal dependencies
- Created `requirements-basic.txt` as fallback without pytgcalls
- Reduces build time and potential conflicts
- Ensures core functionality works reliably

### Build Optimization
- **Issue**: Railway build timeouts during apt-get install
- **Solution**: Minimal Dockerfile with only essential system packages
- **Result**: Faster, more reliable builds
- **Additional**: Improved .dockerignore to reduce build context size

### Version Availability Fix
- **Issue**: Specific pytgcalls versions not available on PyPI
- **Solution**: Using compatible version pairs and fallback options
- **Result**: Successful package installation
- **Fallback**: Basic requirements without pytgcalls if needed

### Optional pytgcalls Support
- **Issue**: ModuleNotFoundError when pytgcalls not available
- **Solution**: Made pytgcalls imports optional with graceful fallback
- **Result**: Bot can run without voice features
- **Benefit**: More reliable deployment with degraded functionality

### Config Import Fix
- **Issue**: ModuleNotFoundError when config not available
- **Solution**: Multiple config locations and fallback imports
- **Result**: Config can be imported from root or Audify package
- **Benefit**: More reliable config loading

### Git Dependency Fix
- **Issue**: ModuleNotFoundError when git module not available
- **Solution**: Added gitpython==3.1.42 to all requirements files
- **Result**: Git operations work correctly
- **Additional**: Added git system dependency to Dockerfile
- **Test**: Created test_git.py to verify gitpython and git command

### Alternative Dockerfiles
- `Dockerfile.minimal` - Ultra-minimal version
- `Dockerfile.alpine` - Alpine Linux alternative
- Use these if the main Dockerfile still has issues

### Alternative Start Commands
- `Procfile` - Uses simple start script with debugging
- `Procfile.alternative` - Uses direct Python command
- Use these if the main start command has issues

---

**Happy Deploying! 🎵**
