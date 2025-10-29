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

def _login(base_url: str, email: str, password: str, timeout: int) -> str | None:
    # POST /users/login -> returns {"access_token": "..."}
    # Known demo accounts exist in the upstream project.
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
def unique_brand_name() -> str:
    return f"brand_{uuid.uuid4().hex[:10]}"

@pytest.fixture()
def brand_factory(base_url, timeout, admin_headers):
    created_ids = []

    def _create(name: str) -> int:
        resp = requests.post(f"{base_url}/brands", json={"name": name},
                             headers=admin_headers, timeout=timeout)
        assert resp.status_code in (200, 201), f"create brand failed: {resp.status_code} {resp.text}"
        bid = resp.json().get("id")
        assert isinstance(bid, int)
        created_ids.append(bid)
        return bid

    yield _create

    # cleanup
    for bid in created_ids:
        requests.delete(f"{base_url}/brands/{bid}", headers=admin_headers, timeout=timeout)


@pytest.fixture()
def product_payload_valid():
    def _make(name=None, price=9.99, description="Test product", is_location_offer=1, is_rental=0,
              category_id="01K8RRWYDKG0WYG384PJGVNREM", brand_id="01K8RRWY347SKPMYHMDFJGPN9X", product_image_id="01K8RRWYE05YD87QMN91R7EWQ6", co2_rating="A"):
        return {
            "name": name or f"prod_{uuid.uuid4().hex[:8]}",
            "description": description,
            "price": price,
            "category_id": category_id,
            "brand_id": brand_id,
            "product_image_id": product_image_id,
            "is_location_offer": is_location_offer,
            "is_rental": is_rental,
            "co2_rating": co2_rating
        }
    return _make

@pytest.fixture()
def product_factory(base_url, timeout, admin_headers, product_payload_valid):
    created_ids = []

    def _create(payload=None):
        data = payload or product_payload_valid()
        r = requests.post(f"{base_url}/products", json=data, headers=admin_headers, timeout=timeout)
        assert r.status_code in (200, 201), f"create product failed: {r.status_code} {r.text}"
        pid = r.json().get("id")
        assert isinstance(pid, int)
        created_ids.append(pid)
        return pid

    yield _create

    for pid in created_ids:
        requests.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)