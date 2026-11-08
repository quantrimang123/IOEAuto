import os
import time
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def main():
    u = os.environ.get("IOE_USERNAME")
    p = os.environ.get("IOE_PASSWORD")
    proxy = os.environ.get("PROXY_SERVER", "")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    
    if proxy:
        opts.add_argument(f"--proxy-server={proxy}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    
    try:
        driver.get("https://ioe.vn/dang-nhap")
        w = WebDriverWait(driver, 25)
        
        w.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or contains(@class, 'form-control')]"))).send_keys(u)
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(p)
        driver.find_element(By.XPATH, "//button[contains(., 'Đăng nhập') or @type='submit']").click()
        
        time.sleep(5)
        
        for r in range(1, 15):
            print(f"Vòng {r}/14")
            driver.get("https://ioe.vn/tu-luyen")
            time.sleep(4)
            
        print("Xong")
    except Exception as e:
        print(f"Lỗi: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
