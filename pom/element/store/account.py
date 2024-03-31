from selenium.webdriver.common.by import By
from frame.node import Node


class account(Node):

    self = (By.CSS_SELECTOR, ".list-group")
    login = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(1)")
    register = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(2)")
    forgotten_password = (
        By.CSS_SELECTOR, "#column-right > div > a:nth-child(3)")
    my_account = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(4)")
    address_book = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(5)")
    wish_list = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(6)")
    order_history = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(7)")
    downloads = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(8)")
    recurring_payments = (
        By.CSS_SELECTOR, "#column-right > div > a:nth-child(9)")
    reward_points = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(10)")
    returns = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(11)")
    transactions = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(12)")
    newsletters = (By.CSS_SELECTOR, "#column-right > div > a:nth-child(13)")
    logout = (By.CSS_SELECTOR,
              "#column-right > div > a[href$='account/logout']")
