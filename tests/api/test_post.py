import pytest
pytestmark = [pytest.mark.api, pytest.mark.post]

def test_post_product_happy(http, base_url, timeout, admin_headers, product_payload_valid):
    payload = product_payload_valid()
    print(payload)
    r = http.post(f"{base_url}/products", json=payload, headers=admin_headers, timeout=timeout)
    assert r.status_code in (200,201), r.text
    body = r.json()
    # cleanup
    http.delete(f"{base_url}/products/{body['id']}", headers=admin_headers, timeout=timeout)

@pytest.mark.negative
def test_post_product_negative_valid_input_unauthorized(http, base_url, timeout, product_payload_valid):
    payload = product_payload_valid()
    r = http.post(f"{base_url}/products", json=payload, timeout=timeout)
    assert r.status_code in (401, 403)

@pytest.mark.negative
def test_post_product_negative_invalid_input_schema(http, base_url, timeout, admin_headers):
    r = http.post(f"{base_url}/products", json={"name": ""}, headers=admin_headers, timeout=timeout)
    assert r.status_code in (400, 422)