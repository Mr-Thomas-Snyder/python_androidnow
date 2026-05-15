import time
from pages.base_page import BasePage

class InterestsPage(BasePage):
    def follow_topic(self, topic_name):
        print(f"Interests: Following {topic_name}")
        # Look for the topic and click its follow button (usually a checkbox or icon next to it)
        # For simplicity in this showcase, we'll click the text itself if it acts as a toggle
        el = self.engine.find_element(text=topic_name)
        if el:
            self.click(el)
            return True
        return False

    def is_on_screen(self):
        # Increased flexibility for header detection
        return self.engine.find_element(text="Topics", timeout=10) or self.engine.find_element(text="Interests", timeout=10)
