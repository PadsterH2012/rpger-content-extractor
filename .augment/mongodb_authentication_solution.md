# MongoDB Authentication Configuration Solution

## Problem
MongoDB requires authentication but the application is not configured with username/password credentials, resulting in:
```
Error: Command dbStats requires authentication
{'ok': 0.0, 'errmsg': 'Command dbStats requires authentication', 'code': 13, 'codeName': 'Unauthorized'}
```

## Current State Analysis

### ✅ Good News: Infrastructure Already Exists!

The application **already has full support** for MongoDB authentication:

#### 1. Backend Support (Modules/mongodb_manager.py)
- **Lines 35-36**: Environment variables for credentials
  ```python
  MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
  MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
  ```
- **Lines 40-44**: Connection string builder with auth support
  ```python
  if MONGODB_USERNAME and MONGODB_PASSWORD:
      MONGODB_CONNECTION_STRING = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}"
  ```
- **Lines 116-120**: Client authentication configuration
  ```python
  if self.config and self.config.get("username") and self.config.get("password"):
      client_kwargs["username"] = self.config["username"]
      client_kwargs["password"] = self.config["password"]
  ```

#### 2. Environment Configuration (.env.sample)
- **Lines 13-15**: Already documented
  ```
  # Optional: Authentication (uncomment if needed)
  # MONGODB_USERNAME=your_username
  # MONGODB_PASSWORD=your_password
  ```

#### 3. UI Settings Modal (ui/templates/index.html)
- **Lines 515-525**: MongoDB connection settings exist
  - Host, Port, Database fields are present
  - **BUT: Username and Password fields are MISSING**

### ❌ What's Missing

The UI Settings Modal lacks MongoDB authentication fields:
- No `MONGODB_USERNAME` input field
- No `MONGODB_PASSWORD` input field
- No `MONGODB_AUTH_SOURCE` field (optional, defaults to "admin")

## Solution

### Step 1: Add UI Fields to Settings Modal
**File**: `ui/templates/index.html` (after line 525)

Add MongoDB authentication fields:
```html
<div class="mb-3">
    <label class="form-label">MongoDB Username</label>
    <input type="text" class="form-control" id="mongodb-username" placeholder="mongodb_user">
    <small class="text-muted">Leave empty for no authentication</small>
</div>
<div class="mb-3">
    <label class="form-label">MongoDB Password</label>
    <div class="input-group">
        <input type="password" class="form-control" id="mongodb-password" placeholder="••••••••">
        <button class="btn btn-outline-secondary" type="button" onclick="togglePasswordVisibility('mongodb-password')">
            <i class="fas fa-eye"></i>
        </button>
    </div>
    <small class="text-muted">Leave empty for no authentication</small>
</div>
<div class="mb-3">
    <label class="form-label">MongoDB Auth Source</label>
    <input type="text" class="form-control" id="mongodb-auth-source" placeholder="admin">
    <small class="text-muted">Database for authentication (usually "admin")</small>
</div>
```

### Step 2: Update JavaScript Handler
**File**: `ui/static/js/app.js`

Update `loadSettings()` and `saveSettings()` functions to handle:
- `MONGODB_USERNAME`
- `MONGODB_PASSWORD`
- `MONGODB_AUTH_SOURCE`

### Step 3: Update .env.sample
**File**: `.env.sample`

Uncomment and document the authentication fields.

## Implementation Checklist

- [ ] Add MongoDB username/password/auth_source fields to HTML settings modal
- [ ] Update JavaScript to load/save MongoDB auth credentials
- [ ] Test MongoDB connection with credentials
- [ ] Update .env.sample with authentication examples
- [ ] Document in deployment guide

## Testing

After implementation:
1. Open Settings modal
2. Enter MongoDB credentials
3. Save settings
4. Verify .env file contains credentials
5. Restart application
6. Check MongoDB connection status
7. Verify collections are accessible

## Security Notes

- Credentials stored in .env file (should be in .gitignore)
- Password field uses type="password" for UI masking
- Consider environment variable override for production
- Never commit .env file to version control

