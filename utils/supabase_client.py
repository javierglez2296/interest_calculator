import os
import requests


class SupabaseRestAdmin:
    def __init__(self):
        self.url = (os.getenv("SUPABASE_URL") or "").strip().rstrip("/")
        self.key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()

        if not self.url:
            raise ValueError("SUPABASE_URL no configurada")

        if not self.key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY no configurada")

        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def check_premium(self, email):
        endpoint = f"{self.url}/rest/v1/purchases"

        params = {
            "select": "email,premium_active,product_code",
            "email": f"eq.{email}",
            "premium_active": "eq.true",
            "limit": "1",
        }

        response = requests.get(
            endpoint,
            headers=self.headers,
            params=params,
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(f"Supabase REST error {response.status_code}: {response.text}")

        return response.json()

    def upsert_purchase(self, payload):
        endpoint = f"{self.url}/rest/v1/purchases"

        response = requests.post(
            endpoint,
            headers={**self.headers, "Prefer": "resolution=merge-duplicates,return=representation"},
            params={"on_conflict": "email"},
            json=payload,
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(f"Supabase REST upsert error {response.status_code}: {response.text}")

        return response.json()


def get_supabase_admin():
    return SupabaseRestAdmin()
