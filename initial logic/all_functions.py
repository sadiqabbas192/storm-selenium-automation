from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import pdfplumber

# Set up user data directory for Chrome profiles
user_data_dir = r"C:\\Users\\Famekeeda\\AppData\\Local\\Google\\Chrome\\User Data"     # update the path as per your system
chrome_profiles = [
    "Profile 4", "Profile 4", "Profile 5", "Profile 6", "Profile 8",
    "Profile 3", "Profile 9", "Profile 10", "Profile 12", "Default"
]


def launch_chrome(profile_name):
    """Launches Chrome with the specified profile."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_name}")
    
    prefs = {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    service = Service("chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://storm.genie.stanford.edu/")
    return driver


def submit_title_form(driver, title_str):
    """Submits the title form on STORM."""
    title_textarea = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-lg')]"))
    )
    title_textarea.clear()
    title_textarea.send_keys(title_str)
    
    title_submit_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-tip='Start']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", title_submit_btn)
    title_submit_btn.click()


def detect_and_switch_profile(driver, profile_index, title_str):
    """Detects error and switches to next profile if needed."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'You have reached the daily limit of article creation')]"))
        )
        
        driver.quit()
        next_profile_index = (profile_index + 1) % len(chrome_profiles)
        new_driver = launch_chrome(chrome_profiles[next_profile_index])
        submit_title_form(new_driver, title_str)
        return new_driver, next_profile_index
    except:
        return driver, profile_index


def submit_response_form(driver, response_str):
    """Submits the response form on STORM."""
    purpose_textarea = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-primary')]"))
    )
    purpose_textarea.clear()
    purpose_textarea.send_keys(response_str)
    
    purpose_submit_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'self-end')]"))
    )
    purpose_submit_btn.click()


def download_pdf(driver):
    """Downloads the response PDF from STORM."""
    WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.ID, "summary"))
    )
    
    pdf_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'tooltip') and contains(@data-tip, 'Show as PDF')]"))
    )
    pdf_button.click()
    
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Download')]"))
    )
    download_button.click()
    
    download_path = os.getcwd()
    for _ in range(30):
        pdf_files = [f for f in os.listdir(download_path) if f.endswith(".pdf")]
        if pdf_files:
            pdf_file = max(pdf_files, key=lambda f: os.path.getctime(os.path.join(download_path, f)))
            os.rename(os.path.join(download_path, pdf_file), os.path.join(download_path, "response.pdf"))
            return "response.pdf"
        time.sleep(1)
    return None


def extract_text_from_pdf(pdf_path):
    """Extracts text from the PDF starting from 'Summary' section onwards."""
    with pdfplumber.open(pdf_path) as pdf:
        extracted_text = []
        summary_found = False
        for page in pdf.pages[1:]:
            lines = page.extract_text().split("\n")
            for line in lines:
                if summary_found:
                    extracted_text.append(line)
                elif line.strip().lower() == "summary":
                    summary_found = True
                    extracted_text.append("\nSUMMARY\n")
        return "\n".join(extracted_text).strip()


def delete_pdf(pdf_path):
    """Deletes the PDF after extracting text."""
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


def run_storm_automation(title_str, response_str):
    """Runs the full automation and returns extracted text."""
    current_profile_index = 0
    driver = launch_chrome(chrome_profiles[current_profile_index])
    
    while True:
        submit_title_form(driver, title_str)
        driver, current_profile_index = detect_and_switch_profile(driver, current_profile_index, title_str)
        if driver:
            break
    
    submit_response_form(driver, response_str)
    pdf_path = download_pdf(driver)
    driver.quit()
    
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
        delete_pdf(pdf_path)
        return extracted_text
    return None

    

text = run_storm_automation("Bajaj Finserv Ltd Marketing Campaigns 2025","i want Bajaj Finserv Ltd Campaigns 2025 to generate brand profiling")
print('------------------------------------------------------')
print(text)