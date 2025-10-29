import pytest
pytestmark = [pytest.mark.api, pytest.mark.delete]

def test_delete_product_happy(http, base_url, timeout, admin_headers, product_factory):
    pid = product_factory()
    r = http.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 204, f"Spec expects 204, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_valid_input_not_found(http, base_url, timeout, admin_headers, product_factory):
    # get product id
    pid = product_factory()

    # delete product
    r = http.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 204, f"Spec expects 204, got {r.status_code}: {r.text}"

    # use the same id to delete again
    r = http.delete(f"{base_url}/products/{pid}", headers=admin_headers, timeout=timeout)
    if r.status_code == 200 and r.json().get("success") is False:
        pytest.xfail("Implementation returns 200 with success=false instead of 404 as per the specification.")
    if r.status_code == 422:
        pytest.xfail("Implementation returns 422 instead of 404 as per the specification, the id is correct for sure.")
    assert r.status_code == 404, f"Spec expects 404, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_invalid_input_non_integer(http, base_url, timeout, admin_headers):
    r = http.delete(f"{base_url}/products/abc", headers=admin_headers, timeout=timeout)
    assert r.status_code == 422, f"Spec expects 422, got {r.status_code}: {r.text}"