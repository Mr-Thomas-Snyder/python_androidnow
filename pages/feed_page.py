import time
from pages.base_page import BasePage

class FeedPage(BasePage):
    def has_topic_chip(self, topic_name):
        return self.is_visible(text=topic_name)

    def click_first_news_card(self):
        # Wait for at least one card to appear
        print("Waiting for news cards to populate...")
        # The news cards often have 'newsResourceCard:' in their resource-id
        card = self.engine.find_element(resource_id="newsResourceCard:", timeout=15)
        if card:
            print(f"Found card at {card.bounds}. Tapping header (10% Rule)...")
            # Tapping the top 10% ensures we hit the title/image area, not the bottom chips
            self.click_safe(card) 
            return True
        print("No news cards found.")
        return False

    def toggle_bookmark_on_first_card(self):
        print("Attempting to toggle bookmark on first card...")
        # Find the bookmark icon (content-desc is usually 'Bookmark')
        el = self.engine.find_element(content_desc="Bookmark")
        if not el:
            el = self.engine.find_element(content_desc="Unbookmark")
        
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
