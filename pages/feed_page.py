import time
from pages.base_page import BasePage

class FeedPage(BasePage):
    def has_topic_chip(self, topic_name):
        # Increased timeout to 15s for the initial sync after onboarding
        el = self.engine.find_element(text=topic_name, timeout=15)
        if not el:
            # Safe print for Windows terminals
            try:
                elements = self.engine.get_elements()
                texts = [e.text[:20] for e in elements if e.text] # Truncate and safe
                print(f"DEBUG: Topic chip '{topic_name}' not found. Visible: {texts}")
            except:
                print("DEBUG: Could not print visible text due to encoding.")
        return el is not None

    def click_first_news_card(self):
        # Wait for at least one card to appear
        print("Waiting for news cards to populate...")
        # The news cards often have 'newsResourceCard:' in their resource-id
        card = self.engine.find_element(resource_id="newsResourceCard:", timeout=10)
        
        if not card:
            print("No cards visible, attempting to nudge the feed...")
            self.driver.swipe(500, 1500, 500, 500, duration=1000) # Long slow swipe up
            card = self.engine.find_element(resource_id="newsResourceCard:", timeout=10)

        if card:
            print(f"Found card at {card.bounds}. Tapping header (10% Rule)...")
            # Tapping the top 10% ensures we hit the title/image area, not the bottom chips
            self.click_safe(card) 
            return True
        print("No news cards found.")
        return False

    def toggle_bookmark_on_first_card(self):
        # Ensure cards are present
        if not self.engine.find_element(resource_id="newsResourceCard:", timeout=10):
             print("No cards visible for bookmarking, nudging...")
             self.driver.swipe(500, 1500, 500, 1000, duration=500)
             
        print("Attempting to toggle bookmark on first card...")
        # Find the bookmark icon (content-desc is usually 'Bookmark')
        el = self.engine.find_element(content_desc="Bookmark", timeout=10)
        if not el:
            el = self.engine.find_element(content_desc="Unbookmark", timeout=5)
        
        if el:
            self.click(el)
            return True
        return False

    def refresh(self):
        """Perform a pull-to-refresh swipe."""
        print("Refreshing feed...")
        # Swipe from middle to bottom
        self.driver.swipe(500, 500, 500, 1500, duration=500)
        time.sleep(2)

    def is_on_screen(self):
        # Look for the bottom nav or feed container
        return self.is_visible(text="For you") or self.is_visible(resource_id="forYou:feed")
