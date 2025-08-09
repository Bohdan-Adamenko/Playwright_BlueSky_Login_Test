import sys
import time
from playwright.sync_api import sync_playwright, expect
timestamp = time.strftime("%Y.%m.%d-%H;%M;%S")


# --- HELPER FUNCTIONS ---
def handle_critical_failure(step_description, e):
    print(f"🔥 CRITICAL FAILURE at step: '{step_description}'")
    print(f"⚠️ Error details: {e}")
    sys.exit(1)

def verification(page, value, element_name):
    try:
        expect(page.locator(value)).to_be_visible(timeout=5000)
        print(f'✅ Verification PASSED: Button "{element_name}" is visible')
        return True
    except:
        print(f'❌ Verification FAILED: Button "{element_name}" was NOT found')
        return False

def assertion(page, value, name):
    try:
        page(f"{value}", timeout=30000)
        print(f'✅ Assertion PASSED: {name}')
    except Exception as e:
        handle_critical_failure(name, e)

def assertion_fill(page, value, fill,  name):
    try:
        page(value).fill(fill, timeout=5000)
        print(f'✅ Assertion PASSED: {name}')
    except Exception as e:
        handle_critical_failure(name, e)


# --- MAIN TEST FUNCTION ---
def run_test(page):
    overall_result = True

    # --- STEP 1: LOGIN ---
    print("\n--- Assertions ---")

    assertion(page.goto, "https://bsky.app", 'Navigated to "bsky.app" homepage')
    assertion(page.click, 'button[aria-label="Sign in"]', 'Button "Sign In" clicked')
    assertion_fill(page.get_by_placeholder, "Username or email address", "qatest.06082025@gmail.com", 'Email "qatest.06082025@gmail.com" entered')
    assertion_fill(page.get_by_placeholder, "Password", "123459_BlueSky", 'Password entered')
    assertion(page.click, 'button[aria-label="Next"]', 'Button "Next" clicked')

    # --- STEP 2: LOGIN VERIFICATION ---
    print("\n--- Verifications ---")

    overall_result &= verification(page, 'button[aria-label="Compose new post"]', 'Compose post')
    overall_result &= verification(page, 'div[data-testid="homeScreenFeedTabs-Discover"]', 'Discover')
    overall_result &= verification(page, 'button[aria-label="Find people to follow"]', 'Find people to follow')

    return overall_result


# --- EXECUTION BLOCK ---
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        final_status = False

        try:
            final_status = run_test(page)
        except SystemExit:
            final_status = False
        except Exception as e:
            print(f"\n🔥 AN UNEXPECTED CRITICAL ERROR OCCURRED: {e}")
            final_status = False

        finally:
            print("\n" + "=" * 40)
            if final_status:
                print("🎉 OVERALL TEST RESULT: PASSED 🎉")
            else:
                screenshot_path = f"failure_screenshot_{timestamp}.png"
                try:
                    print("🔥 OVERALL TEST RESULT: FAILED 🔥")
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
