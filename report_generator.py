import json
import os
from datetime import datetime

def generate_markdown_report():
    if not os.path.exists("test_results.json"):
        print("Error: test_results.json not found.")
        return

    with open("test_results.json", "r") as f:
        results = json.load(f)

    total = len(results)
    passed = len([r for r in results if r["status"] == "PASSED"])
    failed = total - passed
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = [
        f"# 📊 NiA Pure Python Test Report",
        f"**Generated at**: `{timestamp}`",
        f"",
        f"## 📈 Summary",
        f"| Total | ✅ Passed | ❌ Failed | Pass Rate |",
        f"| :--- | :--- | :--- | :--- |",
        f"| {total} | {passed} | {failed} | {round((passed/total)*100, 1) if total > 0 else 0}% |",
        f"",
        f"## 📋 Test Details",
        f"| Test Name | Status | Duration | Screenshot |",
        f"| :--- | :--- | :--- | :--- |"
    ]

    for r in results:
        status_icon = "✅" if r["status"] == "PASSED" else "❌"
        screenshot_link = f"[View Image]({r['screenshot']})" if r["screenshot"] else "N/A"
        md.append(f"| `{r['name']}` | {status_icon} {r['status']} | {r['duration']}s | {screenshot_link} |")

    if failed > 0:
        md.append(f"\n## 🔍 Failure Analysis")
        for r in results:
            if r["status"] == "FAILED":
                md.append(f"### ❌ `{r['name']}`")
                md.append(f"**Error Message**:")
                md.append(f"```text\n{r['error']}\n```")
                if r["screenshot"]:
                    md.append(f"![Failure Screenshot]({r['screenshot']})")
                md.append(f"---")

    with open("REPORT.md", "w", encoding='utf-8') as f:
        f.write("\n".join(md))
    
    print(f"\n[SUCCESS] Markdown report generated: REPORT.md")

if __name__ == "__main__":
    generate_markdown_report()
