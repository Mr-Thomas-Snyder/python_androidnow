from pages.base_page import BasePage

class OnboardingPage(BasePage):
    def follow_topic(self, topic_name):
        print(f"Following topic: {topic_name}")
        el = self.engine.find_element(text=topic_name)
        if el:
            self.click(el)
            return True
        return False

    def wait_for_sync(self):
        """Poll logcat for topic_followed event."""
        print("Waiting for topic_followed sync in logcat...")
        return self.driver.poll_logcat("topic_followed", timeout=10)

    def click_done(self):
        print("Clicking Done button...")
        el = self.engine.find_element(text="Done")
        if el:
            self.click(el)
            # Wait for onboarding to disappear
            self.engine.wait_until_gone(text="Done")
            return True
        return False

    def is_on_screen(self):
        return self.is_visible(text="What are you interested in?")
