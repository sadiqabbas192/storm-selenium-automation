from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
import pdfplumber
import time, os
import re

# Set up user data directory for Chrome profiles
user_data_dir = r"C:\\Users\\Karthik\\AppData\\Local\\Google\\Chrome\\User Data"
chrome_profiles = [
    "Profile 13",
    "Profile 14",
    "Profile 21",
    "Profile 19",
    "Default",
    "Profile 3",
    "Profile 2",
    "Profile 20",
    "Profile 4",
    "Profile 1",
    "Profile 22",
    "Profile 9",
    "Profile 16",
    "Profile 12"
]
 
# Aakash - Profile 13
# Melwyn - Profile 14
# Aditya - Profile 21
# Abhishek - Profile 19
# Karthik - Default
# Pratham - Profile 3
# Robin - Profile 2
# Sagar - Profile 20
# Sharddha - Profile 4
# Stretegy - Profile 1
# Suraj Patil - Profile 22
# Team Affiliate - Profile 9
# try1 - Profile 16
# Business - Profile 12
 

# Rotating profile index to ensure different profiles get used sequentially
profile_rotation_index = 0

# --------------------------------------------------------------------- Chrome Profile Rotation ---------------------------------------------------------------- 

# This function returns the next Chrome profile name from the list, rotating sequentially
def get_next_profile():
    """Returns the next profile in sequence for rotation."""
    global profile_rotation_index
    profile = chrome_profiles[profile_rotation_index]
    profile_rotation_index = (profile_rotation_index + 1) % len(chrome_profiles)  # Cycle through profiles
    return profile


# ------------------------------------------------------------ Launch Chrome Browser with Selenium ------------------------------------------------------------ 

# This function launches a new Chrome browser instance with the specified profile using Selenium
def launch_chrome(profile_name):
    """Launches Chrome with the specified profile."""
    profile_name = get_next_profile()
    print(f"🚀 Launching Chrome with profile: {profile_name}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_name}")

    # if want to test in GUI uncomment the below lines 13 lines with blank lines and comments
    chrome_options.add_argument("--headless=new")  # Run Chrome in headless mode
    
    # ✅ Fast mode optimizations
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--remote-debugging-port=9222")  # Allows reusing sessions

    prefs = {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    # ✅ Suppress Chrome logs
    chrome_options.add_argument("--log-level=3")  # Suppresses most logs
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppresses DevTools logs

    service = Service("chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(3)  # ✅ Implicit wait to reduce redundant explicit waits
    driver.get("https://storm.genie.stanford.edu/")
    print("✅ STORM website loaded successfully!")
    return driver


# ------------------------------------------------------------ Parallel Execution of Multiple Tasks ------------------------------------------------------------ 

 # This function runs multiple automation tasks in parallel using threads
def run_parallel_tasks(titles, responses):
    """Runs STORM automation in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=2) as executor:  # Adjust max_workers as needed
        results = executor.map(run_storm_automation, titles, responses)
    return list(results)


# ------------------------------------------------------------------ Submit Title Form on STORM --------------------------------------------------------------------- 

# This function submits the response form on the STORM website using Selenium
def submit_title_form(driver, title_str):
    """Submits the title form on STORM."""
    print("📝 Submitting Title Form...")
    try:
        # Wait for the textarea to be present and interactable
        title_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-lg')]"))
        )
        title_textarea.clear()
        title_textarea.send_keys(title_str)
        print("✅ Title entered successfully!")

        # Wait for and click the submit button
        title_submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tip='Start']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", title_submit_btn)
        title_submit_btn.click()
        print("✅ Title form submitted successfully!")

    except Exception as e:
        print(f"❌ Error during title submission: {e}")
        driver.save_screenshot("title_form_error.png")
        raise e  # Raise the exception for handling upstream


# ------------------------------------------------------------ Switch Chrome Profile if Daily Limit Reached ------------------------------------------------------------ 

 # This function handles downloading the generated PDF from the STORM site
def detect_and_switch_profile(driver, profile_index, title_str):
    """Detects error and switches to next profile if needed."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'You have reached the daily limit of article creation')]"))
        )
        print("❌ Daily Limit Reached! Switching to next profile...")
        driver.quit()
        next_profile_index = (profile_index + 1) % len(chrome_profiles)
        new_profile = chrome_profiles[next_profile_index]
        print(f"🔄 Switching to profile: {new_profile}")
        new_driver = launch_chrome(new_profile)
        # Wait for page to fully load
        WebDriverWait(new_driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-lg')]"))
        )
        submit_title_form(new_driver, title_str)
        return new_driver, next_profile_index
    except:
        print("✅ No limit detected. Proceeding...")
        return driver, profile_index


# ------------------------------------------------------------ Submit Response Form on STORM ------------------------------------------------------------ 

# This function submits the response form on the STORM website using Selenium
def submit_response_form(driver, response_str):
    """Submits the response form on STORM."""
    print("📝 Submitting Response Form...")
    purpose_textarea = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-primary')]"))
    )
    purpose_textarea.clear()
    purpose_textarea.send_keys(response_str)
    
    purpose_submit_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'self-end')]"))
    )
    purpose_submit_btn.click()
    print("✅ Response form submitted successfully!")


# ------------------------------------------------------------ Download PDF File from STORM ------------------------------------------------------------ 

# This function handles downloading the generated PDF from the STORM site
def download_pdf(driver):
    """Downloads the response PDF from STORM."""
    print("📥 Downloading PDF...")
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
            print("✅ PDF downloaded successfully!")
            return "response.pdf"
        time.sleep(1)
    print("❌ PDF download failed!")
    return None


 # ------------------------------------------------------------ Text Extraction from PDF through pdfplumber ------------------------------------------------------------

# This function extracts text from the downloaded PDF between 'Summary' and 'References'
# and collects hyperlinks only after the 'References' section
def extract_text_from_pdf(pdf_path):
    """Extracts text from the PDF, starting from 'Summary' section onwards and retrieving hyperlinks under 'References'."""
    with pdfplumber.open(pdf_path) as pdf:
        extracted_text = []
        summary_found = False
        references_found = False
        hyperlinks = []

        for page in pdf.pages[1:]:  # Start reading from the second page
            extracted_data = page.extract_text()
            
            # # ✅ Extract hyperlinks from annotations
            # if hasattr(page, "annots") and page.annots:
            #     for annot in page.annots:
            #         if annot.get("uri"):  # Check if annotation contains a hyperlink
            #             hyperlinks.append(annot["uri"])

            # ✅ Extract text & detect 'Summary' and 'References' sections
            if extracted_data:
                lines = extracted_data.split("\n")
                for line in lines:
                    if references_found:
                        continue  # Skip regular text after references start
                    elif line.strip().lower() == "summary":
                        summary_found = True
                        extracted_text.append("\nSUMMARY\n")
                    elif summary_found and line.strip().lower() == "references":
                        references_found = True
                        extracted_text.append("\nReferences\n")
            elif summary_found:
                        extracted_text.append(line)

        # ✅ Append extracted hyperlinks under 'References'
        extracted_text.extend(f"[{i + 1}]: {url}" for i, url in enumerate(hyperlinks))

        return "\n".join(extracted_text).strip()

# ------------------------below code is try code---------------------------------
# def extract_text_from_pdf(pdf_path):
#     """Extracts text from a PDF, starting from 'Summary' section onwards, retrieving all hyperlinks under 'References'."""
#     extracted_text = []
#     hyperlinks = []
#     summary_found = False
#     references_found = False

#     # ✅ Extract text using pdfplumber
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages[1:]:  # Start from the second page
#             page_text = page.extract_text()
#             if page_text:
#                 lines = page_text.split("\n")
#                 for line in lines:
#                     if references_found:
#                         extracted_text.append(line)  # ✅ Keep collecting all references
#                     elif line.strip().lower().startswith("summary"):
#                         summary_found = True
#                         extracted_text.append("\nSUMMARY\n")
#                     elif summary_found and line.strip().lower().startswith("references"):
#                         references_found = True
#                         extracted_text.append("\nReferences\n")
#                     elif summary_found:
#                         extracted_text.append(line)

#                 # ✅ Extract hyperlinks from visible text
#                 hyperlinks.extend(re.findall(r'https?://\S+', page_text))

#     # ✅ Ensure 'References' section exists before adding hyperlinks
#     if hyperlinks and "references" not in "\n".join(extracted_text).lower():
#         extracted_text.append("\nReferences:")

#     extracted_text.extend(f"[{i + 1}]: {url}" for i, url in enumerate(sorted(set(hyperlinks))))  # ✅ Removes duplicates & sorts

#     return "\n".join(extracted_text).strip()
# ------------------------above code is try code---------------------------------


# ------------------------------------------------------------ Delete Downloaded PDF File ------------------------------------------------------------

# This function deletes the downloaded PDF file from disk
def delete_pdf(pdf_path):
    """Deletes the PDF after extracting text."""
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


# ------------------------------------------------------------ Main STORM Automation Pipeline ------------------------------------------------------------ 

# This is the main automation function that runs all steps:
# launching Chrome, submitting forms, downloading PDF, extracting text, and cleaning up
def run_storm_automation(title_str, response_str):
    """Runs the full automation and returns extracted text."""
    print("🚀 Starting STORM automation...")
    current_profile_index = 0
    driver = launch_chrome(chrome_profiles[current_profile_index])
    
    while True:
        submit_title_form(driver, title_str)
        driver, current_profile_index = detect_and_switch_profile(driver, current_profile_index, title_str)
        if driver:
            break
    
    # Proceed with response submission using the valid driver
    try:
        submit_response_form(driver, response_str)
        pdf_path = download_pdf(driver)
    except Exception as e:
        print(f"❌ Error occurred during response submission: {e}")
        driver.quit()
        return None
    driver.quit()
    
    if pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
        delete_pdf(pdf_path)
        print("✅ Extracted text successfully!")
        return extracted_text
    return None