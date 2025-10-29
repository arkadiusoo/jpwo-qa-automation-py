import pytest
pytestmark = [pytest.mark.api, pytest.mark.put]

def test_put_product_happy(http, base_url, timeout, admin_headers, product_factory, product_payload_valid):
    pid = product_factory()
    update = product_payload_valid(name="updated_name")
    r = http.put(f"{base_url}/products/{pid}", json=update, headers=admin_headers, timeout=timeout)
    assert r.status_code in (200, 204), r.text
    gr = http.get(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    if gr.status_code == 200:
        assert gr.json().get("name") == "updated_name"

@pytest.mark.negative
def test_put_product_negative_valid_input_not_found(http, base_url, timeout, admin_headers, product_payload_valid):
    payload = product_payload_valid(name="whatever")
    r = http.put(f"{base_url}/products/999999999", json=payload, headers=admin_headers, timeout=timeout)
    assert r.status_code == 404

@pytest.mark.negative
def test_put_product_negative_invalid_input_schema(http, base_url, timeout, admin_headers, product_factory):
    pid = product_factory()
    payload = {"name": ""}
    r = http.put(f"{base_url}/products/{pid}", json=payload, headers=admin_headers, timeout=timeout)
    assert r.status_code in (400, 422)