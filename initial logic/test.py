from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time

driver_path = r"C:\Users\Karthik\Documents\storm_selenium_automation\chromedriver-win64\chromedriver.exe"
user_data_dir = r"C:\Users\Karthik\AppData\Local\Google\Chrome\User Data"
profiles = ["Profile 13", "Profile 14", "Profile 21", "Profile 16", "Profile 12"]  # include or exclude as needed

def try_profile(profile_name):
    print(f"\n🚀 Trying profile: {profile_name}")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    prefs = {
        "profile.exit_type": "Normal",
        "profile.exited_cleanly": True,
        "session.restore_on_startup": 0
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(driver_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(2)
        driver.get("https://storm.genie.stanford.edu/")
        print(f"✅ STORM loaded successfully with {profile_name}")
        time.sleep(10)
        driver.quit()
        return True
    except WebDriverException as e:
        print(f"❌ {profile_name} failed to launch: {e.msg}")
        return False

# Loop through and use first successful profile
for profile in profiles:
    if try_profile(profile):
        break
