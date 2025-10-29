import os
import uuid
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://api.practicesoftwaretesting.com")

@pytest.fixture(scope="session")
def timeout() -> int:
    return int(os.getenv("TIMEOUT", "10"))

@pytest.fixture(scope="session")
def http() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s

@pytest.fixture()
def product_relations(http, base_url, timeout):
    r_list = http.get(f"{base_url}/products", timeout=timeout)
    assert r_list.status_code == 200, f"list failed: {r_list.status_code} {r_list.text}"
    data = r_list.json()
    items = data if isinstance(data, list) else data.get("data", [])
    if not items:
        pytest.skip("No products in the catalog - cannot derive relation IDs.")
    item = items[0]
    brand_id = item.get("brand_id") or (item.get("brand") or {}).get("id")
    category_id = item.get("category_id") or (item.get("category") or {}).get("id")
    image_id = item.get("product_image_id") or (item.get("product_image") or {}).get("id")
    return {"brand_id": brand_id, "category_id": category_id, "product_image_id": image_id}

def _login(base_url: str, email: str, password: str, timeout: int) -> str | None:
    resp = requests.post(
        f"{base_url}/users/login",
        json={"email": email, "password": password},
        timeout=timeout,
    )
    if resp.status_code == 200 and "access_token" in resp.json():
        return resp.json()["access_token"]
    return None

@pytest.fixture(scope="session")
def admin_token(base_url, timeout) -> str | None:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        return None
    return _login(base_url, email, password, timeout)

@pytest.fixture(scope="session")
def customer_token(base_url, timeout) -> str | None:
    email = os.getenv("CUSTOMER_EMAIL")
    password = os.getenv("CUSTOMER_PASSWORD")
    if not email or not password:
        return None
    return _login(base_url, email, password, timeout)

@pytest.fixture()
def admin_headers(admin_token):
    if not admin_token:
        pytest.skip("admin token not configured - set ADMIN_EMAIL/ADMIN_PASSWORD in .env")
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture()
def product_payload_valid(product_relations):
    def _make(
        name=None,
        price=9.99,
        description="Test product",
        brand_id=None,
        category_id=None,
        product_image_id=None,
        is_location_offer=False,
        is_rental=False,
        co2_rating="A",
    ):
        rel = product_relations
        return {
            "name": name or f"prod_{uuid.uuid4().hex[:8]}",
            "description": description,
            "price": price,
            "brand_id": brand_id if brand_id is not None else rel["brand_id"],
            "category_id": category_id if category_id is not None else rel["category_id"],
            "product_image_id": product_image_id if product_image_id is not None else rel["product_image_id"],
            "is_location_offer": is_location_offer,  # bool
            "is_rental": is_rental,                  # bool
            "co2_rating": co2_rating,
        }
    return _make

@pytest.fixture()
def product_factory(http, base_url, timeout, admin_headers, product_payload_valid):
    created_ids = []

    def _create(payload=None):
        data = payload or product_payload_valid()
        r = http.post(f"{base_url}/products", json=data, headers=admin_headers, timeout=timeout)
        assert r.status_code in (200, 201), f"create product failed: {r.status_code} {r.text}"
        pid = r.json().get("id")
        assert pid, "No product id in response"
        created_ids.append(pid)
        return pid

    yield _create

    for pid in created_ids:
        http.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)