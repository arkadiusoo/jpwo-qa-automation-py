import pytest
pytestmark = [pytest.mark.api, pytest.mark.post]

def test_post_product_happy(http, base_url, timeout, admin_headers, product_factory, product_payload_valid):
    pid = product_factory(product_payload_valid())
    r = http.get(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 200, f"Spec expects 200, got {r.status_code}: {r.text}"


@pytest.mark.negative
def test_post_product_negative_invalid_input(http, base_url, timeout):
    r = http.post(f"{base_url}/products", json={"name": ""}, timeout=timeout)
    assert r.status_code == 422, f"Spec expects 422, got {r.status_code}: {r.text}"