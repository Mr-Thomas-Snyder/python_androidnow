import subprocess
import time
import os

class EmulatorManager:
    def __init__(self):
        self.sdk_path = r"C:\Users\saiko\AppData\Local\Android\Sdk"
        self.emulator_path = f'"{self.sdk_path}\\emulator\\emulator.exe"'
        self.adb_path = f'"{self.sdk_path}\\platform-tools\\adb.exe"'

    def list_avds(self):
        result = subprocess.run(f"{self.emulator_path} -list-avds", shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')

    def is_device_connected(self):
        result = subprocess.run(f"{self.adb_path} devices", shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        # Filter out the header and empty lines
        devices = [line for line in lines[1:] if line.strip() and 'device' in line]
        return len(devices) > 0

    def start_emulator(self, avd_name=None):
        if self.is_device_connected():
            print("Device already connected. Skipping emulator start.")
            return True

        if not avd_name:
            avds = self.list_avds()
            if not avds or not avds[0]:
                print("No AVDs found!")
                return False
            avd_name = avds[0]

        print(f"Starting emulator: {avd_name}...")
        # Start emulator in the background
        subprocess.Popen(f"{self.emulator_path} -avd {avd_name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for device to appear in 'adb devices'
        print("Waiting for device to connect...")
        start_time = time.time()
        while time.time() - start_time < 60:
            if self.is_device_connected():
                print("Device connected!")
                # Wait for system to be ready
                self.wait_for_boot()
                return True
            time.sleep(2)
        
        print("Timed out waiting for emulator.")
        return False

    def wait_for_boot(self):
        print("Waiting for boot to complete...")
        while True:
            result = subprocess.run(f"{self.adb_path} shell getprop sys.boot_completed", shell=True, capture_output=True, text=True)
            if result.stdout.strip() == "1":
                print("Boot completed!")
                break
            time.sleep(2)
