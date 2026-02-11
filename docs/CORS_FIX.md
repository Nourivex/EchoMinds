# 🔧 CORS Configuration Fix

## Problem

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://localhost:8000/api/config. 
(Reason: CORS header 'Access-Control-Allow-Origin' missing).
```

Frontend (http://localhost:5173) tidak bisa mengakses backend endpoint `/api/config`.

---

## Root Cause Analysis

### 1. CORS Middleware Configuration

**Current Setup** (`backend/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Settings** (`backend/config/settings.py`):
```python
cors_origins: List[str] = Field(
    default=["http://localhost:5173"],
    env="CORS_ORIGINS"
)
```

### 2. Possible Issues

**Issue A: Route Ordering**
- CORS middleware harus dipasang **sebelum** routes
- Jika routes di-include dulu, CORS tidak applied

**Issue B: Preflight Request**
- Browser mengirim OPTIONS request sebelum PUT/POST
- Jika OPTIONS tidak handled → CORS error

**Issue C: Environment Variable**
- `CORS_ORIGINS` di `.env` tidak terbaca
- Fallback ke default value

---

## Solutions

### Solution 1: Verify CORS Origins

**Check di startup logs:**
```python
# Tambahkan di main.py setelah app initialization
logger.info(f"CORS Origins: {settings.cors_origins}")
```

**Expected output:**
```
CORS Origins: ['http://localhost:5173']
```

### Solution 2: Explicit OPTIONS Handler

**Add to `routes_models.py`:**
```python
@router.options("/config")
async def config_options():
    """Handle preflight request"""
    return Response(status_code=200)
```

### Solution 3: Development Wildcard (Temporary)

**Only for development**, allow all origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ NOT for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Solution 4: Check .env File

**Ensure `.env` has:**
```bash
CORS_ORIGINS=http://localhost:5173
```

**Or for multiple origins:**
```bash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

---

## Testing Steps

### 1. Backend Startup Check

```bash
cd backend
python -m uvicorn main:app --reload
```

**Look for:**
```
INFO:     CORS Origins: ['http://localhost:5173']
INFO:     Application startup complete.
```

### 2. Browser DevTools Check

**Request Headers:**
```
Origin: http://localhost:5173
```

**Response Headers (Expected):**
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

### 3. CURL Test

```bash
# Test OPTIONS (preflight)
curl -X OPTIONS http://localhost:8000/api/config \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Test GET
curl -X GET http://localhost:8000/api/config \
  -H "Origin: http://localhost:5173" \
  -v
```

---

## Frontend Verification

**Current code** (`SettingsPage.svelte`):
```typescript
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const response = await fetch(`${apiBase}/api/config`, {
  method: 'GET',
  headers: { 'Content-Type': 'application/json' }
});
```

**Add CORS debugging:**
```typescript
try {
  const response = await fetch(`${apiBase}/api/config`);
  console.log('Response headers:', response.headers);
  
  if (!response.ok) {
    console.error('Response status:', response.status);
    console.error('Response text:', await response.text());
  }
} catch (err) {
  console.error('Fetch error:', err);
}
```

---

## Implementation Checklist

- [ ] Add CORS logging to `main.py`
- [ ] Verify `.env` file has correct `CORS_ORIGINS`
- [ ] Add OPTIONS handler to `/api/config` endpoint (if needed)
- [ ] Test with browser DevTools Network tab
- [ ] Test with CURL
- [ ] Verify preflight request (OPTIONS) succeeds
- [ ] Verify actual request (GET/PUT) succeeds
- [ ] Test from Settings page
- [ ] Remove debug logs after fixing

---

## Quick Fix (Immediate)

**Add to `backend/main.py` after CORS middleware:**

```python
@app.middleware("http")
async def log_cors(request: Request, call_next):
    logger.info(f"Request from: {request.headers.get('origin', 'no-origin')}")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"Response headers: {response.headers}")
    return response
```

This will help diagnose where CORS headers are missing.

---

## Related Issues

- Settings page cannot load backend configuration
- All `/api/config` endpoints blocked (GET, PUT)
- Might affect other endpoints if CORS is globally broken

---

## Status

**Priority:** High (blocking Settings page functionality)  
**Estimated Fix Time:** 10-15 minutes  
**Next Steps:** Add logging → Identify missing header → Apply fix → Test → Commit

---

**Created:** 2025-01-XX  
**Status:** Pending Fix
