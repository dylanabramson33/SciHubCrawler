from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import argparse

class SciHubCrawler:
    def __init__(self, download_dir="./Downloads"):
        self.download_dir = os.path.abspath(download_dir)
        self.options = self._setup_chrome_options()
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def _setup_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        return options

    def navigate_to(self, url):
        self.driver.get(url)

    def enter_reference(self, reference):
        textarea = self.driver.find_element(By.ID, "request")
        textarea.send_keys(reference)

    def submit_form(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

    def click_save_button(self):
        save_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '⇣ save')]")))
        save_button.click()

    def wait_for_download(self, timeout=5):
        time.sleep(timeout)

    def check_download(self):
        return any(file.endswith('.pdf') for file in os.listdir(self.download_dir))

    def download_pdf(self, url, reference):
        try:
            self.navigate_to(url)
            self.enter_reference(reference)
            self.submit_form()
            self.click_save_button()
            self.wait_for_download()

            if self.check_download():
                print("PDF file was successfully downloaded")
            else:
                print("File download failed")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Download PDF from a specified URL using a given reference.")
    parser.add_argument("url", help="The URL of the website to navigate to", default="https://sci-hub.scrongyao.com/")
    parser.add_argument("reference", help="The reference to enter in the textarea")
    parser.add_argument("-d", "--download_dir", default="./Downloads", help="The directory to save the downloaded PDF (default: ./Downloads)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    downloader = SciHubCrawler(download_dir=args.download_dir)
    downloader.download_pdf(args.url, args.reference)