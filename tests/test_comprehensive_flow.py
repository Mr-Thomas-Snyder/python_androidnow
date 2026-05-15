import pytest
import time

def test_1_comprehensive_onboarding_flow(onboarding, feed):
    """
    Scenario 1: Complete onboarding and verify feed content.
    """
    assert onboarding.is_on_screen(), "Should be on Onboarding screen"
    
    topic = "UI"
    print(f"Attempting to follow: {topic}")
    assert onboarding.follow_topic(topic), f"Should follow {topic}"
    assert onboarding.wait_for_sync(), "Logcat should show topic_followed event"
    assert onboarding.click_done(), "Should click Done and transition"
    
    assert feed.is_on_screen(), "Should be on Feed screen"
    assert feed.has_topic_chip(topic), f"Feed should have {topic} chip"

def test_2_interests_sync_loop(feed, interests):
    """
    Scenario 2: Verify topic following syncs from Interests to For You.
    Run this BEFORE card clicks to ensure a clean feed.
    """
    assert feed.is_on_screen()
    feed.navigate_to("Interests")
    assert interests.is_on_screen()
    
    # Toggle UI off, Follow Compose
    interests.follow_topic("UI")
    time.sleep(1)
    topic = "Compose"
    interests.follow_topic(topic)
    time.sleep(1)
    
    interests.navigate_to("For you")
    assert feed.is_on_screen()
    
    # Refresh and verify
    feed.refresh()
    assert feed.has_topic_chip(topic), f"Feed should now show {topic} chip"

def test_3_feed_interaction_fast_transition(feed, driver):
    """
    Scenario 3: Verify news card interaction using the 10% Rule.
    Uses Fast Polling to catch the quick < 0.5s browser swap.
    """
    assert feed.is_on_screen(), "Should be on Feed screen"
    
    # 1. Click card header (10% Rule)
    assert feed.click_first_news_card(), "Should click news card header"
    
    # 2. FAST POLLING for transition
    print("Polling for browser transition (Fast Mode)...")
    found_transition = False
    start_time = time.time()
    while time.time() - start_time < 4: # Watch for 4 seconds
        focused = driver.get_focused_window().lower()
        if any(x in focused for x in ["chrome", "browser", "webview"]):
            found_transition = True
            print(f"SUCCESS: Captured browser transition: {focused}")
            break
        # No sleep or very tiny sleep to stay fast
    
    assert found_transition, "Did not capture the fast browser transition"
    
    # 3. Return to app if still in browser
    driver.keyevent(4) # BACK
    time.sleep(1)
    assert feed.is_on_screen(), "Should be back on Feed screen"
