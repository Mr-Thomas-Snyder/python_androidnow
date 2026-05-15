# 📊 NiA Pure Python Test Report
**Generated at**: `2026-05-14 23:14:13`

## 📈 Summary
| Total | ✅ Passed | ❌ Failed | Pass Rate |
| :--- | :--- | :--- | :--- |
| 5 | 3 | 2 | 60.0% |

## 📋 Test Details
| Test Name | Status | Duration | Screenshot |
| :--- | :--- | :--- | :--- |
| `test_comprehensive_onboarding_flow` | ✅ PASSED | 13.13s | N/A |
| `test_feed_interaction_25_percent_rule` | ❌ FAILED | 8.46s | [View Image](screenshot_test_feed_interaction_25_percent_rule_225622.png) |
| `test_interests_sync_loop` | ❌ FAILED | 24.7s | [View Image](screenshot_test_interests_sync_loop_225647.png) |
| `test_bookmarking_flow` | ✅ PASSED | 30.29s | N/A |
| `test_exclusive_topic_propagation` | ✅ PASSED | 18.57s | N/A |

## 🔍 Failure Analysis
### ❌ `test_feed_interaction_25_percent_rule`
**Error Message**:
```text
feed = <pages.feed_page.FeedPage object at 0x0000020055024910>, driver = <core.adb_driver.ADBDriver object at 0x0000020054FCB770>

    def test_feed_interaction_25_percent_rule(feed, driver):
        """
        Scenario: Verify news card interaction using the 25% Rule.
        """
        assert feed.is_on_screen(), "Should be on Feed screen"
    
        # Click card
        assert feed.click_first_news_card(), "Should click news card using 25% rule"
    
        # Verify transition to browser/detail (Standard check)
        time.sleep(2)
        focused = driver.get_focused_window()
>       assert "chrome" in focused.lower() or "browser" in focused.lower() or "webview" in focused.lower(), \
            f"Expected browser/webview in focus, but got: {focused}"
E       AssertionError: Expected browser/webview in focus, but got: mFocusedWindow=Window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.MainActivity}
E       assert ('chrome' in 'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}' or 'browser' in 'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}' or 'webview' in 'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}')
E        +  where 'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}' = <built-in method lower of str object at 0x000002005501C7C0>()
E        +    where <built-in method lower of str object at 0x000002005501C7C0> = 'mFocusedWindow=Window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.MainActivity}'.lower
E        +  and   'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}' = <built-in method lower of str object at 0x000002005501C7C0>()
E        +    where <built-in method lower of str object at 0x000002005501C7C0> = 'mFocusedWindow=Window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.MainActivity}'.lower
E        +  and   'mfocusedwindow=window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.mainactivity}' = <built-in method lower of str object at 0x000002005501C7C0>()
E        +    where <built-in method lower of str object at 0x000002005501C7C0> = 'mFocusedWindow=Window{9afba6e u0 com.google.samples.apps.nowinandroid.demo.debug/com.google.samples.apps.nowinandroid.MainActivity}'.lower

tests\test_comprehensive_flow.py:43: AssertionError
```
![Failure Screenshot](screenshot_test_feed_interaction_25_percent_rule_225622.png)
---
### ❌ `test_interests_sync_loop`
**Error Message**:
```text
feed = <pages.feed_page.FeedPage object at 0x0000020055024410>, interests = <pages.interests_page.InterestsPage object at 0x0000020054FCB8C0>

    def test_interests_sync_loop(feed, interests):
        """
        Scenario: Verify topic following syncs from Interests to For You.
        """
        # 1. Start on Feed, navigate to Interests
        assert feed.is_on_screen()
        feed.navigate_to("Interests")
        assert interests.is_on_screen()
    
        # 2. Follow a new topic
        topic = "Compose"
        interests.follow_topic(topic)
        time.sleep(1)
    
        # 3. Return to Feed
        interests.navigate_to("For you")
        assert feed.is_on_screen()
    
        # 4. Verify topic chip is present
>       assert feed.has_topic_chip(topic), f"Feed should now show {topic} chip"
E       AssertionError: Feed should now show Compose chip
E       assert False
E        +  where False = has_topic_chip('Compose')
E        +    where has_topic_chip = <pages.feed_page.FeedPage object at 0x0000020055024410>.has_topic_chip

tests\test_extended_scenarios.py:23: AssertionError
```
![Failure Screenshot](screenshot_test_interests_sync_loop_225647.png)
---