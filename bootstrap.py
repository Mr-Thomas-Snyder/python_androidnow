import sys
import os
from core.emulator_manager import EmulatorManager
from core.adb_driver import ADBDriver

def bootstrap(apk_path=None):
    mgr = EmulatorManager()
    
    # 1. Start Emulator
    if not mgr.is_device_connected():
        print("Ensuring emulator is running...")
        mgr.start_emulator()
    
    # 2. Check for App
    driver = ADBDriver()
    print(f"Checking for package: {driver.package_name}")
    output = driver.shell(f"pm list packages | grep {driver.package_name}")
    
    if driver.package_name not in output:
        print("App not found on device.")
        if apk_path and os.path.exists(apk_path):
            print(f"Installing app from: {apk_path}...")
            driver.shell(f"install -g {apk_path}")
        else:
            print("Warning: APK path not provided or not found. Please install the NiA app manually or provide a path.")
    else:
        print("App is already installed.")

    print("\n[SUCCESS] Environment is ready for testing!")
    print("Run tests with: pytest tests/")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    bootstrap(path)
