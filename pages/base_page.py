from core.adb_driver import ADBDriver
from core.ui_engine import UIEngine

class BasePage:
    def __init__(self, driver: ADBDriver, engine: UIEngine):
        self.driver = driver
        self.engine = engine

    def click(self, element):
        if element:
            x, y = element.center
            self.driver.tap(x, y)
    
    def click_safe(self, element):
        """Click using the 10% Rule for card headers."""
        if element:
            x, y = element.top_10_center
            self.driver.tap(x, y)

    def is_visible(self, text=None, resource_id=None, content_desc=None):
        return self.engine.find_element(text, resource_id, content_desc, timeout=5) is not None

    def navigate_to(self, tab_name):
        """Navigate via bottom nav."""
        print(f"Navigating to tab: {tab_name}")
        el = self.engine.find_element(text=tab_name)
        if el:
            self.click(el)
            return True
        return False
