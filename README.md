# Now in Android (NiA) - Pure Python ADB Harness

This project is a high-performance, zero-framework-dependency automation suite for the "Now in Android" app. It demonstrates how to achieve 100% test coverage using only Python and ADB, bypassing the overhead of Appium or Karate.

## 🚀 Key Features
- **Zero Heavyweight Dependencies**: No Appium server, no Node.js, no Java (except for ADB).
- **Extreme Speed**: Direct communication with ADB via subprocess for sub-second interactions.
- **Smart UI Parsing**: Custom XML engine that implements the **25% Rule** for precise Compose UI targeting.
- **Logcat Synchronization**: Uses logcat polling to detect internal app events (like topic following) when UI state is opaque.

## 📋 Test Scenarios
1. **App Launch & Onboarding**: Verify initial state and transition to the feed.
2. **Comprehensive App Flow**: Full journey from onboarding to topic selection and feed verification.
3. **Interests Sync**: Verify that following topics in the Interests tab reflects in the "For You" feed.
4. **Browser Transition**: Verify external intent handling (Chrome Custom Tabs).

## 🛠️ Implementation Strategy
- **Interaction**: `adb shell input tap/swipe/keyevent`.
- **Observation**: `uiautomator dump` + `xml.etree.ElementTree`.
- **Synchronization**: Multi-threaded logcat monitoring and element polling.

## 🚧 Challenges Overcome
- **Compose Obscuration**: Overcoming the "unclickable" Done button by monitoring `topic_followed` log events.
- **Overlapping Elements**: Using the **25% Rule** to ensure clicks land on the card container and not the bookmark toggle.
- **Dynamic Content**: Implementing robust wait-for-disappearance logic during screen transitions.

## 🏗️ Getting Started

### 1. Environment Setup
If you don't have an emulator running, the harness can start one for you automatically. It looks for available AVDs and picks the first one.

```bash
# Install dependencies
pip install -r requirements.txt

# Bootstrap the environment (Starts emulator & checks for app)
# If you have the APK:
python bootstrap.py C:\path\to\nowinandroid.apk
# Otherwise:
python bootstrap.py
```

### 2. Run Tests & Generate Reports
We have provided a one-click script that executes all tests and generates a visual Markdown report with screenshots.

```bash
# Run all tests and generate REPORT.md
.\run_and_report.ps1
```

## 📊 Reporting
After running the script, a `REPORT.md` file will be generated in the root directory. It includes:
- **Summary Table**: Pass/Fail counts and durations.
- **Failure Analysis**: Detailed stack traces for failed tests.
- **Visual Evidence**: Automatic screenshots captured at the moment of failure.
