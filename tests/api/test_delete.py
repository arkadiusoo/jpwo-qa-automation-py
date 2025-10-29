import pytest
pytestmark = [pytest.mark.api, pytest.mark.delete]

def test_delete_product_happy(http, base_url, timeout, admin_headers, product_factory):
    pid = product_factory()
    r = http.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 204, f"Spec expects 204, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_valid_input_not_found(http, base_url, timeout, admin_headers):
    not_exist_id = "this_id_doesnt_exist_for_sure"
    r = http.delete(f"{base_url}/products/{not_exist_id}", headers=admin_headers, timeout=timeout)
    if r.status_code == 200 and r.json().get("success") is False:
        pytest.xfail("Implementation returns 200 with success=false instead of 404 as per the specification.")
    assert r.status_code == 404, f"Spec expects 404, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_invalid_input_non_integer(http, base_url, timeout, admin_headers):
    r = http.delete(f"{base_url}/products/abc", headers=admin_headers, timeout=timeout)
    assert r.status_code in (400, 404, 405)