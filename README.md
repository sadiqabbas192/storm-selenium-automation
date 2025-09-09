# Storm Selenium Automation

A robust automation framework leveraging Selenium and Jupyter Notebooks to streamline browser-based testing and automation tasks.

## Overview

**Storm Selenium Automation** is designed for developers and testers who want to automate web application testing with ease. Built with the flexibility of Jupyter Notebook and the power of Selenium, this framework enables interactive development, rapid prototyping, and efficient debugging.

## Features

- **Jupyter Notebook Integration:** Write and run your automation scripts interactively.
- **Selenium WebDriver Support:** Automate browsers such as Chrome, Firefox, Edge, etc.
- **Easy Customization:** Extend and adapt test scenarios as needed.
- **Open Source:** Publicly available for modification and collaboration.

## Getting Started

### Prerequisites

- Python 3.7+
- Jupyter Notebook
- Selenium (`pip install selenium`)
- Browser driver (e.g., ChromeDriver for Chrome)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sadiqabbas192/storm-selenium-automation.git
   cd storm-selenium-automation
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *(If there is no requirements.txt, manually install the required packages:)*

   ```bash
   pip install selenium notebook
   ```

3. **Download the appropriate browser driver:**
   - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   - [GeckoDriver (Firefox)](https://github.com/mozilla/geckodriver/releases)

4. **Start Jupyter Notebook:**

   ```bash
   jupyter notebook
   ```

## Usage

- Open the provided notebook files.
- Modify or add your test scripts as needed.
- Run code cells to execute automation steps interactively.

### Example

```python
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
driver.get('https://www.example.com')

# Interact with the page
element = driver.find_element("id", "some-id")
element.click()

driver.quit()
```

## Supported Browsers

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- (Others supported by Selenium WebDriver)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is open source. Add your license details here.

## Contact

For questions or suggestions, please contact [sadiqabbas192](https://github.com/sadiqabbas192).

---

*Happy Testing!*
