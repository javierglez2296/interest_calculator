import os
import requests


class SupabaseClient:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not self.url or not self.key:
            raise ValueError("❌ Supabase env vars no configuradas")

        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    # =========================================================
    # INSERT / UPSERT COMPRA
    # =========================================================
    def upsert_purchase(self, payload):
        endpoint = f"{self.url}/rest/v1/purchases"

        response = requests.post(
            endpoint,
            headers={
                **self.headers,
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
            params={"on_conflict": "email,product_code"},
            json=payload,
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(
                f"Supabase REST upsert error {response.status_code}: {response.text}"
            )

        return response.json()

    # =========================================================
    # CHECK PREMIUM
    # =========================================================
    def check_premium(self, email, product_code):
        endpoint = f"{self.url}/rest/v1/purchases"

        params = {
            "select": "email,premium_active,product_code",
            "email": f"eq.{email}",
            "premium_active": "eq.true",
            "product_code": f"eq.{product_code}",
            "limit": "1",
        }

        response = requests.get(
            endpoint,
            headers=self.headers,
            params=params,
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(
                f"Supabase REST select error {response.status_code}: {response.text}"
            )

        data = response.json()
        return bool(data)


# =========================================================
# FACTORY
# =========================================================
def get_supabase_admin():
    return SupabaseClient()
