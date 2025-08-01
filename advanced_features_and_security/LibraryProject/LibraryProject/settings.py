# Disable debug mode in production
DEBUG = False

# Restrict allowed hosts (adjust to your domain or localhost if needed)
ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1']

# Enable browser-side security headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Secure cookies over HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
