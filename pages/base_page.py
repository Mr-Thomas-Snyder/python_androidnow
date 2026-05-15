from core.adb_driver import ADBDriver
import time
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
        """Navigate via bottom nav with coordinate and ID safety."""
        print(f"Navigating to tab: {tab_name}")
        
        # 1. Try text/content-desc search in the nav area
        el = self.engine.find_element(content_desc=tab_name)
        if not el: el = self.engine.find_element(text=tab_name)
            
        if el and el.center[1] > 1800:
            self.click(el)
        else:
            # 2. Fallback to hardcoded coordinates if text-search is ambiguous
            print(f"  [DEBUG] Nav icon '{tab_name}' not found by text, using coordinate fallback.")
            coords = {
                "For you": (172, 2088),
                "Saved": (540, 2088),
                "Interests": (907, 2088)
            }
            if tab_name in coords:
                x, y = coords[tab_name]
                self.driver.tap(x, y)
            else:
                print(f"  [ERROR] No fallback for {tab_name}")
                return False

        print("  [DEBUG] Navigating... waiting for transition.")
        time.sleep(2) 
        return True
