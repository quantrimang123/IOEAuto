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


def ask_ai_for_answer(question_text):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Lỗi: Chưa cấu hình GROQ_API_KEY!")
        return None

    client = Groq(api_key=api_key)

    prompt = f"""
    Bạn là một máy farm thông minh chuyên giải các bài tập tiếng Anh trong cuộc thi IOE (Internet Olympiad of English).Làm hết từ vòng 1 đến 14 bỏ bài nói
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_completion_tokens=100,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Lỗi khi gọi AI API: {e}")
        return None


def run():
    username = os.environ.get("IOE_USERNAME")
    password = os.environ.get("IOE_PASSWORD")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        print("Đang truy cập trang đăng nhập IOE...")
        driver.get("https://ioe.vn/dang-nhap")

        wait = WebDriverWait(driver, 20)

        username_field = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[formcontrolname='account']")
            )
        )
        password_field = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[formcontrolname='password']")
            )
        )
        login_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn-login, button[type='submit']")
            )
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_btn.click()

        time.sleep(5)

        driver.get("https://ioe.vn/tu-luyen")
        time.sleep(4)
        print("Đã vào phòng tự luyện!")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
