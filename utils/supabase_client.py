import os
from supabase import create_client


def get_supabase_admin():
    url = (os.getenv("SUPABASE_URL") or "").strip()
    key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()

    print("SUPABASE_URL_DEBUG:", repr(url))
    print("SUPABASE_KEY_DEBUG_START:", key[:12])

    if not url:
        raise ValueError("SUPABASE_URL no configurada")

    if not key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY no configurada")

    return create_client(url, key)
