from selenium.webdriver.common.by import By
from frame.node import Node

class account_dropdown(Node):

    self = (By.CSS_SELECTOR, "a[title='My Account']")
    login = (By.LINK_TEXT, "Login")
    register = (By.LINK_TEXT, "Register")
    my_account = (By.LINK_TEXT, "My Account")
    order_history = (By.LINK_TEXT, "Order History")
    transactions = (By.LINK_TEXT, "Transactions")
    downloads = (By.LINK_TEXT, "Downloads")
    logout = (By.LINK_TEXT, "Logout")

