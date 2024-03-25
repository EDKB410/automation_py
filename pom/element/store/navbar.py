from frame.node import Node
from selenium.webdriver.common.by import By

class navbar(Node):

    self = (By.CSS_SELECTOR, '#menu')

    class desktops(Node):
        self = (By.LINK_TEXT, 'Desktops')
        pc = (By.PARTIAL_LINK_TEXT, 'PC')
        mac = (By.PARTIAL_LINK_TEXT, 'Mac')
        all = (By.LINK_TEXT, 'Show All Desktops')

    class laptops(Node):
        self = (By.LINK_TEXT, 'Laptops & Notebooks')
        macs = (By.PARTIAL_LINK_TEXT, 'Macs')
        windows = (By.PARTIAL_LINK_TEXT, 'Windows')
        all = (By.LINK_TEXT, 'Show All Laptops & Notebooks')

    class components(Node):
        self = (By.LINK_TEXT, 'Components')
        mice = (By.PARTIAL_LINK_TEXT, 'Mice and Trackballs')
        monitors = (By.PARTIAL_LINK_TEXT, 'Monitors')
        printers = (By.PARTIAL_LINK_TEXT, 'Printers')
        scanners = (By.PARTIAL_LINK_TEXT, 'Scanners')
        webcameras = (By.PARTIAL_LINK_TEXT, 'Web Cameras')
        all = (By.LINK_TEXT, 'Show All Components')

    class tablets(Node):
        self = (By.LINK_TEXT, 'Tablets')

    class software(Node):
        self = (By.LINK_TEXT, 'Software')

    class phones(Node):
        self = (By.LINK_TEXT, 'Phones & PDAs')

    class cameras(Node):
        self = (By.LINK_TEXT, 'Cameras')

    class mp3(Node):
        self = (By.LINK_TEXT, 'MP3 Players')
    