import sys
import time
from playwright.sync_api import sync_playwright, expect


def handle_critical_failure(step_description, error):
    print(f"🔥 CRITICAL FAILURE at step: '{step_description}'")
    print(f"⚠️ Error details: {error}")
    sys.exit(1)


def run_test(page):

    overall_result = True

    print("\n--- Critical verifications ---")

    try:
        page.goto("https://bsky.app", timeout=30000)
        print("✅ Navigated to bsky.app homepage")
    except Exception as e:
        handle_critical_failure("Navigating to homepage", e)

    try:
        page.click('button[aria-label="Sign in"]', timeout=30000)
        print('✅ "Sign In" button clicked')
    except Exception as e:
        handle_critical_failure('Click on the "Sign In" button', e)

    try:
        page.get_by_placeholder("Username or email address").fill("qatest.06082025@gmail.com", timeout=5000)
        print(f'✅ Email "qatest.06082025@gmail.com" entered')
    except Exception as e:
        handle_critical_failure("Entering email", e)

    try:
        page.get_by_placeholder("Password").fill("123459_BlueSky", timeout=30000)
        print('✅ Password entered')
    except Exception as e:
        handle_critical_failure("Entering password", e)

    try:
        page.click('button[aria-label="Next"]', timeout=30000)
        print('✅ "Next" button clicked')
    except Exception as e:
        handle_critical_failure('Click on the "Next" button', e)


    print("\n--- Non-critical verifications ---")


    try:
        a = page.locator('button[aria-label="Compose new post"]')
        expect(a).to_be_visible(timeout=5000)
        print("✅ 1/3 Verification PASSED: 'Compose post' button is visible.")
    except:
        print("❌ 1/3 Verification FAILED: 'Compose post' button was NOT found.")
        overall_result = False

    try:
        a = page.locator('div[data-testid="homeScreenFeedTabs-Discover"]')
        expect(a).to_be_visible(timeout=5000)
        print("✅ 2/3 Verification PASSED: 'Search' link is visible.")
    except:
        print("❌ 2/3 Verification FAILED: 'Search' link was NOT found.")
        overall_result = False

    try:
        a = page.locator('button[aria-label="Find people to follow"]')
        expect(a).to_be_visible(timeout=5000)
        print("✅ 3/3 Verification PASSED: 'Profile' link is visible.")
    except:
        print("❌ 3/3 Verification FAILED: 'Profile' link was NOT found.")
        overall_result = False

    return overall_result


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        try:
            final_status = run_test(page)
        except SystemExit:
            print("\n--- Test execution was halted due to a critical failure ---")
            final_status = False

        except Exception as e:
            print(f"\n🔥 AN UNEXPECTED CRITICAL ERROR OCCURRED: {e}")
            final_status = False

        finally:
            print("\n" + "=" * 40)
            if final_status:
                print("🎉 OVERALL TEST RESULT: PASSED 🎉")
            else:
                print("🔥 OVERALL TEST RESULT: FAILED 🔥")
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                screenshot_path = f"failure_screenshot_{timestamp}.png"
                try:
                    page.screenshot(path=screenshot_path)
                    print(f"📸 Screenshot saved to '{screenshot_path}'")
                except Exception as screenshot_error:
                    print(f"Could not save screenshot: {screenshot_error}")
            print("=" * 40)

            context.close()
            browser.close()
            print("\nBrowser closed.")

if __name__ == "__main__":
    main()
