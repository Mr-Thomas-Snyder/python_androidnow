import time
from pages.base_page import BasePage

class SavedPage(BasePage):
    def has_bookmarked_item(self, title_part=None):
        if title_part:
            return self.is_visible(text=title_part)
        # Check if there are any news cards in the saved list
        return self.is_visible(resource_id="newsResourceCard:")

    def is_on_screen(self):
        return self.engine.find_element(text="Saved", timeout=10) or self.engine.find_element(text="Nothing saved", timeout=10)
