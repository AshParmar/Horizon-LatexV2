# OAuth Integration Guide - Based on Composio Official Docs

This guide shows how to implement OAuth authentication for Google services using Composio's official methods.

**Reference:** https://docs.composio.dev/docs/custom-auth-configs

---

## 🔐 OAuth Flow (Official Composio Method)

### Step 1: Initiate Connection

```python
from composio import Composio

composio = Composio(api_key="your_api_key")

# Initiate OAuth connection
connection_request = composio.connected_accounts.initiate(
    user_id="user_123",        # Your user's ID
    auth_config_id="ac_1234",  # Optional: Custom auth config (uses default if None)
)

print(connection_request.redirectUrl)  # Send this URL to frontend
```

### Step 2: Redirect User to OAuth URL

```python
# Frontend redirects user to the redirect_url
# User completes OAuth on Google's site
# Composio handles the callback automatically
```

### Step 3: Wait for Connection (Optional)

```python
# Backend can wait for user to complete OAuth
connected_account = connection_request.wait_for_connection()
print(f"Connected: {connected_account.id}")
```

---

## 🚀 Implementation in Our System

### Using OAuthManager

```python
from modules.integrations.oauth import OAuthManager

# Initialize
oauth = OAuthManager()

# Initiate connection for Gmail
result = oauth.initiate_connection(
    service='gmail',
    user_id='test_user_001',
    redirect_url='http://localhost:3000/callback'  # Optional
)

print(result['redirect_url'])  # Send to frontend
# User visits this URL and grants permissions
```

---

## 📡 API Endpoints

### 1. Get OAuth URL

```bash
POST /api/v1/integrations/connect/google?service=gmail

Body:
{
  "entity_id": "test_user_001",
  "redirect_url": "http://localhost:3000/callback"
}

Response:
{
  "auth_url": "https://accounts.google.com/o/oauth2/auth?...",
  "message": "Visit URL to connect gmail"
}
```

### 2. Check Connection Status

```bash
GET /api/v1/integrations/status/test_user_001

Response:
{
  "entity_id": "test_user_001",
  "connections": {
    "gmail": {
      "connected": true,
      "service": "gmail",
      "entity_id": "test_user_001"
    },
    "calendar": {
      "connected": false,
      "service": "calendar"
    },
    "sheets": {
      "connected": false,
      "service": "sheets"
    }
  },
  "total": 1
}
```

---

## 🎨 Frontend Integration

### React Example

```javascript
import React, { useState } from 'react';

function GoogleConnectButton({ service, userId }) {
  const [loading, setLoading] = useState(false);
  
  const connectService = async () => {
    setLoading(true);
    
    try {
      // Step 1: Get OAuth URL from backend
      const response = await fetch(
        `/api/v1/integrations/connect/google?service=${service}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            entity_id: userId,
            redirect_url: `${window.location.origin}/oauth/callback`
          })
        }
      );
      
      const data = await response.json();
      
      // Step 2: Redirect user to OAuth URL
      window.location.href = data.auth_url;
      
    } catch (error) {
      console.error('Failed to connect:', error);
      setLoading(false);
    }
  };
  
  return (
    <button onClick={connectService} disabled={loading}>
      {loading ? 'Connecting...' : `Connect ${service}`}
    </button>
  );
}

// Usage
<GoogleConnectButton service="gmail" userId="user_123" />
<GoogleConnectButton service="calendar" userId="user_123" />
<GoogleConnectButton service="sheets" userId="user_123" />
```

### OAuth Callback Handler

```javascript
// pages/oauth/callback.jsx
import { useEffect } from 'react';
import { useRouter } from 'next/router';

function OAuthCallback() {
  const router = useRouter();
  
  useEffect(() => {
    // Composio handles the callback automatically
    // Just show success message and redirect
    
    const checkConnection = async () => {
      const userId = localStorage.getItem('userId');
      
      // Verify connection was established
      const response = await fetch(
        `/api/v1/integrations/status/${userId}`
      );
      const status = await response.json();
      
      if (status.total > 0) {
        // Success! Redirect to dashboard
        router.push('/dashboard?connected=true');
      } else {
        // Connection failed
        router.push('/settings?error=connection_failed');
      }
    };
    
    setTimeout(checkConnection, 2000); // Wait 2 seconds for Composio to process
  }, []);
  
  return (
    <div>
      <h1>Connecting your account...</h1>
      <p>Please wait while we verify your connection.</p>
    </div>
  );
}

export default OAuthCallback;
```

### Check Connection Status

```javascript
import React, { useEffect, useState } from 'react';

function IntegrationStatus({ userId }) {
  const [status, setStatus] = useState(null);
  
  useEffect(() => {
    const checkStatus = async () => {
      const response = await fetch(
        `/api/v1/integrations/status/${userId}`
      );
      const data = await response.json();
      setStatus(data);
    };
    
    checkStatus();
  }, [userId]);
  
  if (!status) return <div>Loading...</div>;
  
  return (
    <div>
      <h2>Connected Services ({status.total})</h2>
      
      {Object.entries(status.connections).map(([service, info]) => (
        <div key={service} className="service-item">
          <span>{service}</span>
          <span className={info.connected ? 'connected' : 'disconnected'}>
            {info.connected ? '✅ Connected' : '❌ Not Connected'}
          </span>
          {!info.connected && (
            <GoogleConnectButton service={service} userId={userId} />
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## 🔧 Custom Auth Config (Optional)

If you want to use your own Google OAuth app instead of Composio's default:

### 1. Create Google OAuth App

1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID
3. Set Authorized Redirect URI to:
   ```
   https://backend.composio.dev/api/v3/toolkits/auth/callback
   ```
4. Copy Client ID and Client Secret

### 2. Create Auth Config in Composio Dashboard

1. Go to https://app.composio.dev
2. Navigate to "Authentication management" → "Manage authentication with custom credentials"
3. Click "Create Auth Config"
4. Select OAuth2 scheme
5. Add Client ID and Client Secret
6. Copy the `auth_config_id` (e.g., `ac_1234`)

### 3. Use Custom Auth Config

```python
# In .env file
AC_GMAIL=ac_1234567890abcdef
AC_GOOGLE_CALENDAR=ac_0987654321fedcba
AC_GOOGLE_SHEETS=ac_abcdef1234567890

# In code
oauth = OAuthManager()
result = oauth.initiate_connection(
    service='gmail',
    user_id='user_123',
    auth_config_id='ac_1234567890abcdef'  # Use custom config
)
```

---

## 🎯 Complete Flow Diagram

```
┌─────────────┐
│  Frontend   │
│   User      │
└──────┬──────┘
       │ 1. Click "Connect Gmail"
       ↓
┌─────────────────────────────────────────────┐
│  POST /api/v1/integrations/connect/google  │
│  Body: {entity_id, redirect_url}           │
└──────────────┬──────────────────────────────┘
               │ 2. composio.connected_accounts.initiate()
               ↓
        ┌──────────────┐
        │   Composio   │
        │   Backend    │
        └──────┬───────┘
               │ 3. Returns OAuth URL
               ↓
        ┌──────────────┐
        │   Response   │
        │  {auth_url}  │
        └──────┬───────┘
               │ 4. Frontend redirects user
               ↓
┌────────────────────────────────────┐
│  https://accounts.google.com/...   │
│  User grants permissions           │
└────────────┬───────────────────────┘
             │ 5. User clicks "Allow"
             ↓
┌─────────────────────────────────────────────┐
│  https://backend.composio.dev/.../callback  │
│  Composio handles callback automatically   │
└────────────┬────────────────────────────────┘
             │ 6. Connection established
             ↓
┌─────────────────────────────────────────────┐
│  User redirected to: redirect_url           │
│  http://localhost:3000/oauth/callback       │
└────────────┬────────────────────────────────┘
             │ 7. Frontend verifies connection
             ↓
┌─────────────────────────────────────────────┐
│  GET /api/v1/integrations/status/{user_id} │
│  Response: {connections: {gmail: connected}}│
└─────────────────────────────────────────────┘
             │ 8. Show success message
             ↓
        ┌──────────────┐
        │  Dashboard   │
        │  Gmail ✅    │
        └──────────────┘
```

---

## ✅ Testing

### Test OAuth Initiation

```bash
# Start server
uvicorn main:app --reload

# Test Gmail connection
curl -X POST "http://localhost:8000/api/v1/integrations/connect/google?service=gmail" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "test_user_001",
    "redirect_url": "http://localhost:3000/callback"
  }'

# Response:
# {
#   "auth_url": "https://accounts.google.com/o/oauth2/auth?...",
#   "message": "Visit URL to connect gmail"
# }

# Visit the auth_url in your browser
# Complete OAuth flow
# Then check status:

curl "http://localhost:8000/api/v1/integrations/status/test_user_001"

# Response:
# {
#   "entity_id": "test_user_001",
#   "connections": {
#     "gmail": {"connected": true, ...}
#   }
# }
```

---

## 📚 Key Takeaways

1. ✅ Use `composio.connected_accounts.initiate()` for OAuth (official method)
2. ✅ Composio handles OAuth callback automatically
3. ✅ Custom auth configs optional (use for production with many users)
4. ✅ Frontend gets OAuth URL and redirects user
5. ✅ After OAuth, check connection status to verify
6. ✅ All services (Gmail, Calendar, Sheets) use same flow

**The OAuth implementation is now aligned with Composio's official documentation!** 🎉
