import os
from supabase import create_client

def get_supabase_admin():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # 👈 ESTA ES LA CLAVE

    if not url:
        raise ValueError("SUPABASE_URL no configurada")

    if not key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY no configurada")

    return create_client(url, key)
