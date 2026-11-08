import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def run():
    # Lấy thông tin tài khoản từ biến môi trường của GitHub Actions Secrets
    username = os.environ.get("IOE_USERNAME")
    password = os.environ.get("IOE_PASSWORD")

    if not username or not password:
        print("Lỗi: Chưa cấu hình tài khoản trong GitHub Secrets!")
        return

    # Cấu hình Chrome chạy ở chế độ không giao diện (Headless) cho Linux Server
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        print("Đang truy cập trang đăng nhập IOE...")
        driver.get("https://ioe.vn/dang-nhap")
        time.sleep(4)

        # Điền tài khoản, mật khẩu (Thay thế ID thực tế nếu giao diện IOE thay đổi)
        username_field = driver.find_element(By.ID, "Account")
        password_field = driver.find_element(By.ID, "Password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Click nút đăng nhập
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_btn.click()

        time.sleep(5)
        print(f"Đang đăng nhập với tài khoản: {username}")

        # Điều hướng đến trang tự luyện hoặc làm bài
        driver.get("https://ioe.vn/tu-luyen")
        time.sleep(4)
        print("Đã vào trang tự luyện thành công!")

        # --- Thêm logic tự động giải bài hoặc luyện tập của bạn ở đây ---

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình chạy bot: {e}")
    finally:
        driver.quit()
        print("Đã đóng trình duyệt.")


if __name__ == "__main__":
    run()
