# Test Project: Robust Login Automation for bsky.app with Playwright

This educational project demonstrates skills in building reliable UI test automation using Python and the Playwright library.

## 🚀 What Does This Test Do?

The script performs a robust test of the user login scenario on bsky.app. It is designed with a **"fail fast"** approach for critical steps.

### Test Flow:
1.  **Critical Steps:** The test first navigates to the website and performs the entire login sequence. If any of these core steps fail (e.g., website unreachable, login fails), the test is **immediately terminated** to prevent misleading follow-up errors.
2.  **Non-Critical Verifications:** Only after a successful login, the script proceeds to verify the presence of key UI elements on the post-login page (e.g., "Compose Post" button, "Home" feed, "Profile" link). A failure at this stage is logged, but does not stop other verifications.
3.  **Environment Control:** The test runs in a controlled browser context with the `en-US` locale to ensure consistency.

## 🛠️ How to Run

### Prerequisites:
*   **Python 3.x** installed.
*   **Playwright** installed.

### Installation:
To install Playwright and its required browsers, run the following commands in your terminal:
```pip install playwright
playwright install

### Running the Test:
To run the test, execute the following command from your terminal:
python Translated_BlueSky.py
