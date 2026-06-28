# constants/status_codes.py

class StatusCode:
    # ── 2xx Success ────────────────────────────
    OK            = 200    # GET success
    CREATED       = 201    # POST success (new resource created)

    # ── 4xx Client Errors ──────────────────────
    BAD_REQUEST   = 400    # Invalid input / validation failed
    UNAUTHORIZED  = 401    # Login required / token invalid
    FORBIDDEN     = 403    # Logged in but no permission
    NOT_FOUND     = 404    # Resource nahi mila
    CONFLICT      = 409    # Already exists (duplicate email)

    # ── 5xx Server Errors ──────────────────────
    SERVER_ERROR  = 500    # Unexpected server side error


# 200 → data mila, kaam ho gaya
# 201 → naya user/record bana
# 400 → form validation fail (missing fields, weak password)
# 401 → token nahi hai ya expire ho gaya
# 403 → token hai but permission nahi (role mismatch)
# 404 → user/record exist nahi karta
# 409 → email already registered
# 500 → database down, unexpected crash