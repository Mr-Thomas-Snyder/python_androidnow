import subprocess
import time
import os
import re

class ADBDriver:
    def __init__(self, package_name="com.google.samples.apps.nowinandroid.demo.debug"):
        self.package_name = package_name
        self.sdk_path = r"C:\Users\saiko\AppData\Local\Android\Sdk"
        self.adb_path = f'"{self.sdk_path}\\platform-tools\\adb.exe"'

    def shell(self, cmd):
        """Execute a shell command via ADB."""
        result = subprocess.run(f"{self.adb_path} shell {cmd}", shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stdout.strip()

    def tap(self, x, y):
        """Perform a tap at coordinates."""
        print(f"  [ADB] Tapping at ({x}, {y})")
        self.shell(f"input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2, duration=300):
        """Perform a swipe/scroll."""
        print(f"  [ADB] Swiping from ({x1}, {y1}) to ({x2}, {y2})")
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")

    def keyevent(self, code):
        """Send a keyevent (e.g., 4 for BACK)."""
        self.shell(f"input keyevent {code}")

    def get_hierarchy(self):
        """Dump the UI hierarchy and return the local path to the XML file."""
        xml_path = "window_dump.xml"
        self.shell("uiautomator dump /sdcard/view.xml")
        subprocess.run(f"{self.adb_path} pull /sdcard/view.xml {xml_path}", shell=True, capture_output=True)
        return xml_path

    def clear_logcat(self):
        """Clear the logcat buffer."""
        subprocess.run(f"{self.adb_path} logcat -c", shell=True)

    def poll_logcat(self, pattern, timeout=15):
        """Poll logcat for a specific pattern."""
        print(f"  [Logcat] Polling for pattern: '{pattern}' (timeout={timeout}s)")
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = subprocess.run(f"{self.adb_path} logcat -d", shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            logs = result.stdout
            if pattern in logs:
                print(f"  [Logcat] Found pattern '{pattern}'!")
                return True
            time.sleep(1)
        print(f"  [Logcat] Timed out waiting for '{pattern}'")
        return False

    def get_focused_window(self):
        """Get the currently focused window package."""
        output = self.shell("dumpsys activity activities | grep mFocusedWindow")
        return output

    def reset_app(self):
        """Force stop and clear app data."""
        self.shell(f"am force-stop {self.package_name}")
        self.shell(f"pm clear {self.package_name}")
        # Grant permissions to avoid blocking popups
        self.shell(f"pm grant {self.package_name} android.permission.POST_NOTIFICATIONS")

    def start_app(self):
        """Start the app's main activity."""
        # Ensure permission is granted again just in case
        self.shell(f"pm grant {self.package_name} android.permission.POST_NOTIFICATIONS")
        activity = f"{self.package_name}/com.google.samples.apps.nowinandroid.MainActivity"
        self.shell(f"am start -n {activity}")
        time.sleep(5) # Give it 5 seconds to stabilize
