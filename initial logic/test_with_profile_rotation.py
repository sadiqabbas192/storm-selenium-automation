# %% [markdown]
# # **storm selenium automation**

# %% [markdown]
# ## **Generating PDF Link**

# %%
# Step 1 : importing Librarys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

# %%
# Step 2: Profile Rotation Setup

# List of available Chrome profiles
chrome_profiles = [
    r"Profile 4",  # Shraddha
    r"Profile 3",  # Pratham
    r"Profile 5",  # Application
    r"Profile 6",  # Business Tools
    r"Profile 8",  # Search Affiliate
    r"Profile 1",  # Strategy
    r"Profile 9",  # Team Affiliate
    r"Profile 10", # Team Account
    r"Profile 12", # Business Development
    r"Default"     # Karthik
]

# Set the user data directory
user_data_dir = r"C:\\Users\\Karthik\\AppData\\Local\\Google\\Chrome\\User Data"

#-------------------------------------------------------------------------------------------------------------
# karthik - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Default
# shraddha - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 4
# Pratham - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 3
# Application - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 5
# businesstools - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 6
# searchffiliate - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 8
# strategy - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 1
# team affiliate - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 9
# team account - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 10
# business devv - C:\Users\Karthik\AppData\Local\Google\Chrome\User Data\Profile 12

# %%
company_name = "Bajaj Finserv Ltd"
title_str = f"{company_name} Marketing Campaigns 2025"
response_str = f"i want {company_name} Campaigns 2025 to generate brand profiling"

# %%
def launch_chrome(profile_name):
    """Launch Chrome with a specific user profile and go to the Storm page."""
    
    chrome_options = webdriver.ChromeOptions()
    
    # ✅ Attach existing profile
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_name}")  

    # ✅ Set Chrome preferences for downloads
    prefs = {
        "download.default_directory": os.getcwd(),  # ✅ Save in project directory
        "download.prompt_for_download": False,  # ✅ Disable "Save As" prompt
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # ✅ Other Chrome options
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    # ✅ Initialize WebDriver
    service = Service("chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"✅ Chrome Launched Successfully with Profile: {profile_name}")

    # ✅ Always start at STORM homepage
    driver.get("https://storm.genie.stanford.edu/")
    print("✅ STORM website loaded successfully!")

    return driver  # Return WebDriver instance

# %%
def submit_title_form(driver):
    """Submits the title form and checks for error."""
    
    # ✅ Wait for the first textarea (Title Form)
    title_textarea = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-lg')]"))
    )

    # ✅ Clear the field before entering text
    title_textarea.clear()
    title_textarea.send_keys(title_str)
    print("✅ Title entered successfully!")

    # ✅ Wait for the submit button
    title_submit_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-tip='Start']"))
    )

    # ✅ Ensure button is visible before clicking
    driver.execute_script("arguments[0].scrollIntoView(true);", title_submit_btn)

    # ✅ Click using JavaScript if normal click fails
    try:
        title_submit_btn.click()
        print("✅ Clicked using normal .click()")
    except:
        print("⚠️ Normal click failed. Trying JavaScript click...")
        driver.execute_script("arguments[0].click();", title_submit_btn)

    print("✅ Title form submitted successfully!")

# %%
def detect_and_switch_profile(driver, profile_index):
    """Detects daily limit error and switches profile if needed."""
    
    try:
        # ✅ Check for the error message after title form submission
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'You have reached the daily limit of article creation')]"))
        )
        
        print("❌ Daily Limit Reached! Switching to next profile...")

        # Close the current browser window
        driver.quit()
        print("🚪 Closed current Chrome instance.")

        # Rotate to the next profile
        next_profile_index = (profile_index + 1) % len(chrome_profiles)  # Cycle through profiles
        next_profile = chrome_profiles[next_profile_index]

        print(f"🔄 Switching to profile: {next_profile}")

        # ✅ Launch new profile
        new_driver = launch_chrome(next_profile)

        # ✅ Immediately restart title form submission
        submit_title_form(new_driver)  # This ensures submission continues after switching
        
        return new_driver, next_profile_index  

    except:
        print("✅ No limit detected. Proceeding to next steps...")
        return driver, profile_index  # Continue with the same driver if no error

# %%
# ✅ Start with the first profile
current_profile_index = 0
driver = launch_chrome(chrome_profiles[current_profile_index])

while True:
    # ✅ Submit the title form
    submit_title_form(driver)  

    # ✅ Check if the error appears AFTER form submission & switch if needed
    driver, current_profile_index = detect_and_switch_profile(driver, current_profile_index)

    # ✅ If no error found, break loop and continue automation
    if driver:  # Ensures that driver is valid after switching
        break

# %%
# Step 6 : Response form submission

# Wait for the Purpose Form textarea to be visible
purpose_textarea = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'textarea-primary')]"))
)

# Clear the field before entering text
purpose_textarea.clear()

purpose_textarea.send_keys(response_str)
print("Writing purpose entered successfully!")
 
# ------------------------------------------------------------------------------
# Wait for the submit button using a more precise XPath
try:
    purpose_submit_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'self-end')]"))
    )
    print("Submit button found!")
except:
    print("Submit button NOT found!")
    raise

# Ensure the button is interactable before clickingc
if not purpose_submit_btn.is_enabled():
    print("Submit button is disabled. Waiting longer...")
    time.sleep(3)  # Wait a few seconds for any potential JavaScript changes

# Scroll into view (to ensure it's visible before clicking)
driver.execute_script("arguments[0].scrollIntoView(true);", purpose_submit_btn)

# Try clicking using ActionChains first
try:
    ActionChains(driver).move_to_element(purpose_submit_btn).click().perform()
    print("Clicked using ActionChains!")
except:
    print("ActionChains click failed. Trying JavaScript click...")
    driver.execute_script("arguments[0].click();", purpose_submit_btn)

print("Purpose form submitted successfully!")

# %%
# Step 7 : Generate Response and download the PDF

# Wait for the result page to fully load (Check for h1 with id='summary')
WebDriverWait(driver, 180).until(
    EC.presence_of_element_located((By.ID, "summary"))
)
print("✅ Result page fully loaded (Summary section detected)!")

# Wait for the "Show as PDF" button
pdf_button = WebDriverWait(driver, 0).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'tooltip') and contains(@data-tip, 'Show as PDF')]"))
)
pdf_button.click()
print("✅ Clicked 'Show as PDF' button!")

# Wait for the PDF dialog to appear and locate the "Download" button
download_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-primary') and contains(text(), 'Download')]"))
)
print("✅ Download button is visible!")

# Click the "Download" button
download_button.click()
print("✅ Clicked the 'Download' button!")

# ✅ Ensure correct project directory for download
download_path = os.getcwd()  # Save file in the project directory
print(f"📂 Expected Download Path: {download_path}")

# ✅ Check for the file in the directory
timeout = 30  # Max wait time in seconds
pdf_file = None

for _ in range(timeout):
    pdf_files = [f for f in os.listdir(download_path) if f.endswith(".pdf")]
    
    if pdf_files:
        pdf_file = max(pdf_files, key=lambda f: os.path.getctime(os.path.join(download_path, f)))  # Get latest PDF
        print(f"✅ Detected PDF: {pdf_file}")
        break
    
    time.sleep(1)  # Wait before checking again

# ✅ Rename the file if found
if pdf_file:
    response_pdf_path = os.path.join(download_path, "response.pdf")
    os.rename(os.path.join(download_path, pdf_file), response_pdf_path)
    print(f"✅ PDF downloaded and saved as 'response.pdf' in {download_path}!")
else:
    print("❌ Error: Downloaded PDF not found in expected directory!")

# ✅ Close the browser
driver.quit()
print("🚪 Browser window closed successfully!")


# %% [markdown]
# ## **Cleaning the PDF**

# %%
# Step 8 : Generate Text from PDF using pdfplumber

import pdfplumber

def extract_text_from_summary_onwards(pdf_path, target_heading="summary"):
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        if total_pages < 2:
            raise ValueError("The PDF does not contain enough pages.")

        extracted_text = []
        summary_found = False

        # Start from page 2 (index 1) to the last page
        for page_num in range(1, total_pages):
            page_text = pdf.pages[page_num].extract_text()

            if not page_text:
                continue  # Skip pages with no text
            
            lines = page_text.split("\n")

            for i, line in enumerate(lines):
                if summary_found:
                    extracted_text.append(line)
                elif line.strip().lower() == target_heading.lower():
                    summary_found = True
                    extracted_text.append(f"\n{target_heading.upper()}\n")  # Keep the heading

        if not extracted_text:
            raise ValueError(f"Heading '{target_heading}' not found in the document.")

        return "\n".join(extracted_text).strip()


# %%
# Path to the PDF in the project directory
pdf_path = "response.pdf"

# Extract the text from "summary" heading onward
try:
    summary_text = extract_text_from_summary_onwards(pdf_path)
    
    print("Extracted Text:\n")
    print(summary_text)

    # Delete the PDF after extraction
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"\nFile '{pdf_path}' has been successfully deleted.")
    else:
        print(f"\nFile '{pdf_path}' not found.")

except Exception as e:
    print(f"Error: {e}")


