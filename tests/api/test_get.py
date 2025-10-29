import pytest
pytestmark = [pytest.mark.api, pytest.mark.get]

def test_get_product_happy(http, base_url, timeout):
    product_id = "01K8RNF12GMV72X9QZ1ADWMBX2"
    r = http.get(f"{base_url}/products/{product_id}", timeout=timeout)
    assert r.status_code == 200
    body = r.json()
    assert body.get("id") == product_id
    assert "name" in body and "price" in body

@pytest.mark.negative
def test_get_product_negative_valid_input_not_found(http, base_url, timeout):
    missing_product_id = "1"
    r = http.get(f"{base_url}/products/{missing_product_id}", timeout=timeout)
    assert r.status_code == 404

# Explanation for commenting out: how can we trigger a 405 error for this method
# if everyone can view the products and GET accepts a string value?

# @pytest.mark.negative
# def test_get_product_negative_invalid_input_non_integer(http, base_url, timeout):
#     r = http.get(f"{base_url}/products/null", timeout=timeout)
#     assert r.status_code == 405
