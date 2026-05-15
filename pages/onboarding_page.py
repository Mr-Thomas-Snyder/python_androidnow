import time
from pages.base_page import BasePage

class OnboardingPage(BasePage):
    def follow_topic(self, topic_name):
        print(f"Following topic: {topic_name}")
        el = self.engine.find_element(text=topic_name, timeout=5)
        if not el:
            print(f"Topic {topic_name} not found, scrolling...")
            self.driver.swipe(500, 1500, 500, 800) # Scroll up
            el = self.engine.find_element(text=topic_name, timeout=5)
            
        if el:
            self.click(el)
            return True
        return False

    def wait_for_sync(self):
        """Poll logcat for topic_followed event."""
        print("Waiting for topic_followed sync in logcat...")
        return self.driver.poll_logcat("topic_followed", timeout=10)

    def click_done(self):
        # Wait for any follow animations to settle
        print("Waiting for UI to settle before clicking Done...")
        time.sleep(2)
        
        for attempt in range(3):
            print(f"Clicking Done button (Attempt {attempt+1})...")
            el = self.engine.find_element(resource_id="onboarding:done")
            if not el: el = self.engine.find_element(text="Done")
            
            if not el:
                print("Done button no longer visible.")
                break
                
            self.click(el)
            if self.engine.wait_until_gone(text="Done", timeout=5):
                print("Done button successfully dismissed.")
                break
            print("Warning: Done button still visible after click.")
        
        # Small nudge swipe to force feed render
        print("Nudging UI to force render...")
        self.driver.swipe(500, 1500, 500, 1300, duration=200)
        time.sleep(2)
        return True

    def is_on_screen(self):
        return self.is_visible(text="What are you interested in?")
