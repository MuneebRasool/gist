"""
Constants for auth module
"""

# Password related constants
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 50


# Authentication related constants
ACCESS_TOKEN_EXPIRE_DAYS = 30
JWT_ALGORITHM = "HS256"
BEARER_TOKEN_PREFIX = "Bearer"

# Error messages
EMAIL_EXISTS_ERROR = "Email already registered"
USER_NOT_FOUND_ERROR = "User not found"
INVALID_CREDENTIALS_ERROR = "Invalid credentials"
REQUIRE_GOOGLE_AUTH_ERROR = "Please login with Google"
INACTIVE_USER_ERROR = "No user account found"
UNVERIFIED_USER_ERROR = "User account is not verified"
UNAUTHORIZED_ERROR = "Not authenticated"
INVALID_TOKEN_ERROR = "Could not validate credentials"
