def test_pass(driver, base_url):
    driver.get(base_url)
    assert "Your Store" in driver.title
