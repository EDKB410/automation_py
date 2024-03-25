from frame.node import Node
from selenium.webdriver.common.by import By


class navigation(Node):

    class dashboard(Node):

        self = (By.PARTIAL_LINK_TEXT, 'Dashboard')

    class catalog(Node):

        self = (By.PARTIAL_LINK_TEXT, 'Catalog')
        categories = (By.PARTIAL_LINK_TEXT, 'Categories')
        products = (By.PARTIAL_LINK_TEXT, 'Products')
    
