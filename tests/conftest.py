import pytest
import os
import subprocess
import json
from datetime import datetime
from core.adb_driver import ADBDriver
from core.ui_engine import UIEngine
from core.emulator_manager import EmulatorManager
from pages.onboarding_page import OnboardingPage
from pages.feed_page import FeedPage
from pages.interests_page import InterestsPage
from pages.saved_page import SavedPage

@pytest.fixture(scope="session", autouse=True)
def ensure_device():
    mgr = EmulatorManager()
    if not mgr.is_device_connected():
        print("\n[Setup] No device connected. Attempting to start emulator...")
        success = mgr.start_emulator()
        if not success:
            pytest.exit("Could not start emulator and no device connected.")
    else:
        print("\n[Setup] Device already connected.")

@pytest.fixture(scope="session")
def driver():
    drv = ADBDriver()
    drv.reset_app()
    drv.clear_logcat()
    drv.start_app()
    yield drv
    drv.shell("am force-stop com.google.samples.apps.nowinandroid.demo.debug")

@pytest.fixture(scope="session")
def engine(driver):
    return UIEngine(driver)

@pytest.fixture
def onboarding(driver, engine):
    return OnboardingPage(driver, engine)

@pytest.fixture
def feed(driver, engine):
    return FeedPage(driver, engine)

@pytest.fixture
def interests(driver, engine):
    return InterestsPage(driver, engine)

@pytest.fixture
def saved(driver, engine):
    return SavedPage(driver, engine)

# --- Reporting Logic ---
RESULTS = []

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        result = {
            "name": item.name,
            "status": "PASSED" if rep.passed else "FAILED",
            "duration": round(rep.duration, 2),
            "error": str(rep.longrepr) if rep.failed else "",
            "screenshot": None
        }
        
        if rep.failed:
            driver = item.funcargs.get('driver')
            if driver:
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"screenshot_{item.name}_{timestamp}.png"
                driver.shell(f"screencap -p /sdcard/{filename}")
                # Pull using absolute adb path from driver
                subprocess.run(f"{driver.adb_path} pull /sdcard/{filename} .", shell=True, capture_output=True)
                result["screenshot"] = filename
        
        RESULTS.append(result)

def pytest_sessionfinish(session, exitstatus):
    # Save results to a JSON for the markdown generator
    with open("test_results.json", "w") as f:
        json.dump(RESULTS, f, indent=4)
    print(f"\n[INFO] Results saved to test_results.json")
