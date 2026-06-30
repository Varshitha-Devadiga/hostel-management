import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

ARTIFACT_DIR = r"C:\Users\admin\.gemini\antigravity-ide\brain\1e8d1c63-bf5e-4e1d-b49b-31cb881617c8"

def capture_ui():
    print("Setting up Chrome Headless Driver...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,800')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 1. Load login page (via root redirect)
        print("Loading root page (should redirect to login)...")
        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)  # Wait for load and render
        
        login_screenshot_path = os.path.join(ARTIFACT_DIR, "login_page_checked.png")
        driver.save_screenshot(login_screenshot_path)
        print(f"Saved login page screenshot to: {login_screenshot_path}")

        # 2. Perform Login
        print("Entering credentials and logging in...")
        driver.find_element(By.ID, "email").send_keys("student@123.com")
        driver.find_element(By.ID, "password").send_keys("123456")
        
        # Click login button
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(3)  # Wait for redirect and render

        dashboard_screenshot_path = os.path.join(ARTIFACT_DIR, "dashboard_page_checked.png")
        driver.save_screenshot(dashboard_screenshot_path)
        print(f"Saved dashboard page screenshot to: {dashboard_screenshot_path}")
        print("Current URL after login:", driver.current_url)

    except Exception as e:
        print("An error occurred during UI automation:")
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_ui()
