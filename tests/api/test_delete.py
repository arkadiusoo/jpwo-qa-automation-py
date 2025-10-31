import pytest
pytestmark = [pytest.mark.api, pytest.mark.delete]


def test_delete_brand_happy(http, base_url, timeout, admin_headers, brand_factory):
    bid = brand_factory()
    r = http.delete(f"{base_url}/brands/{bid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 204, f"Spec expects 204, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_brand_negative_invalid_input_non_uuid(http, base_url, timeout, admin_headers):
    r = http.delete(f"{base_url}/brands/abc", headers=admin_headers, timeout=timeout)
    assert r.status_code == 422, f"Spec expects 422, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_brand_negative_product_used_elsewhere(http, base_url, timeout, admin_headers):
    r_list = http.get(f"{base_url}/brands", timeout=timeout)
    assert r_list.status_code == 200, f"list failed: {r_list.status_code} {r_list.text}"
    data = r_list.json()

    items = data if isinstance(data, list) else data.get("data", [])
    if not items:
        pytest.skip("No brands in the catalog.")
    brand_id = items[0]["id"]
    r = http.delete(f"{base_url}/brands/{brand_id}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 409, f"Spec expects 409, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_brand_negative_valid_input_not_found(http, base_url, timeout, admin_headers, brand_factory):
    # get brand id
    bid = brand_factory()

    # delete product
    r = http.delete(f"{base_url}/brands/{bid}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 204, f"Spec expects 204, got {r.status_code}: {r.text}"

    # use the same id to delete again
    r = http.delete(f"{base_url}/brands/{bid}", headers=admin_headers, timeout=timeout)
    if r.status_code == 200 and r.json().get("success") is False:
        pytest.xfail("Implementation returns 200 with success=false instead of 404 as per the specification.")
    if r.status_code == 422:
        pytest.xfail("Implementation returns 422 instead of 404 as per the specification, the id is correct for sure.")
    assert r.status_code == 404, f"Spec expects 404, got {r.status_code}: {r.text}"


@pytest.mark.negative
def test_delete_brand_negative_unauthorized(http, base_url, timeout, brand_factory):
    bid = brand_factory()
    r = http.delete(f"{base_url}/brands/{bid}", timeout=timeout)
    assert r.status_code == 401, f"Spec expects 401, got {r.status_code}: {r.text}"



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
def test_delete_product_negative_invalid_input_non_uuid(http, base_url, timeout, admin_headers):
    r = http.delete(f"{base_url}/products/abc", headers=admin_headers, timeout=timeout)
    assert r.status_code == 422, f"Spec expects 422, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_product_used_elsewhere(http, base_url, timeout, admin_headers):
    r_list = http.get(f"{base_url}/products", timeout=timeout)
    assert r_list.status_code == 200, f"list failed: {r_list.status_code} {r_list.text}"
    data = r_list.json()

    items = data if isinstance(data, list) else data.get("data", [])
    if not items:
        pytest.skip("No products in the catalog.")
    product_id = items[0]["id"]
    r = http.delete(f"{base_url}/products/{product_id}", headers=admin_headers, timeout=timeout)
    assert r.status_code == 409, f"Spec expects 409, got {r.status_code}: {r.text}"

@pytest.mark.negative
def test_delete_product_negative_unauthorized(http, base_url, timeout, product_factory):
    pid = product_factory()
    r = http.delete(f"{base_url}/products/{pid}", timeout=timeout)
    assert r.status_code == 401, f"Spec expects 401, got {r.status_code}: {r.text}"