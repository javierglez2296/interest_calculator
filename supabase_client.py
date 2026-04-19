from supabase import create_client
from utils.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY


def get_supabase_admin():
    if not SUPABASE_URL:
        raise ValueError("SUPABASE_URL no configurada")

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY no configurada")

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
