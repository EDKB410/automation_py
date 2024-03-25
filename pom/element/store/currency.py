from frame.node import Node
from selenium.webdriver.common.by import By


class currency(Node):

    form = (By.CSS_SELECTOR, "#form-currency")
    button = (By.CSS_SELECTOR, "button.btn.btn-link.dropdown-toggle")
    self = (By.CSS_SELECTOR, "ul.dropdown-menu")
    usd = (By.CSS_SELECTOR, "button[name=USD]")
    eur = (By.CSS_SELECTOR, "button[name=EUR]")
    gbp = (By.CSS_SELECTOR, "button[name=GBP]")
    selected = (By.CSS_SELECTOR, "strong")
