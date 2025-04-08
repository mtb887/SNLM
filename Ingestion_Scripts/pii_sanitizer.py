import hashlib

def hash_string(value):
    """Hash string with SHA-256 (can be used to pseudonymize usernames)."""
    return hashlib.sha256(value.encode()).hexdigest()

def sanitize_user(user_obj):
    """Remove or hash PII from a user object."""
    return {
        "id": user_obj.get("id"),  # OK to keep for internal mapping
        "username_hashed": hash_string(user_obj.get("username", "")) if "username" in user_obj else None
        # name, email, or real username are omitted for privacy
        # More fields can be added here if needed and should any laws change.
    }
