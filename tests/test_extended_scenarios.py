import pytest
import time

def test_4_bookmarking_flow(feed, saved):
    """
    Scenario 4: Verify bookmarking a news item.
    """
    # 1. Ensure we are on Feed
    assert feed.is_on_screen()
    
    # 2. Bookmark the first item
    assert feed.toggle_bookmark_on_first_card(), "Should toggle bookmark"
    time.sleep(1)
    
    # 3. Navigate to Saved tab
    feed.navigate_to("Saved")
    assert saved.is_on_screen()
    
    # 4. Verify item is in saved list
    assert saved.has_bookmarked_item(), "Should see bookmarked item in Saved tab"
    
    # 5. Cleanup: Unbookmark
    feed.navigate_to("For you")
    assert feed.toggle_bookmark_on_first_card(), "Should unbookmark item"

def test_5_exclusive_topic_propagation(onboarding, feed, driver):
    """
    Scenario 5: Verify feed filters correctly for a specific topic.
    """
    # Reset to onboarding to ensure a clean topic state
    driver.reset_app()
    driver.start_app()
    
    topic = "Headlines"
    onboarding.follow_topic(topic)
    onboarding.wait_for_sync()
    onboarding.click_done()
    
    time.sleep(2)
    assert feed.is_on_screen()
    assert feed.has_topic_chip(topic)
