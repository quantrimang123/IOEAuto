import os
import time
from groq import Groq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def ask_ai_for_answer(question_text):
    """Hàm gửi nội dung câu hỏi tiếng Anh tới Groq API để lấy đáp án chuẩn"""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Lỗi: Chưa cấu hình GROQ_API_KEY!")
        return None

    client = Groq(api_key=api_key)

    prompt = f"""
    Bạn là một trợ lý thông minh chuyên giải các bài tập tiếng Anh trong cuộc thi IOE (Internet Olympiad of English).
    Dưới đây là đề bài của một câu hỏi. Hãy phân tích và chọn ra đáp án đúng nhất (hoặc đưa ra câu trả lời ngắn gọn, chính xác để điền/chọn vào ô trống).
    
    Câu hỏi: {question_text}
    
    Chỉ trả về đáp án chính xác, không giải thích dài dòng rườm rà.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Model AI tốc độ cao, thông minh của Groq
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

    # Cấu hình Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        print("Đang đăng nhập vào IOE...")
        driver.get("https://ioe.vn/dang-nhap")
        time.sleep(3)

        driver.find_element(By.ID, "Account").send_keys(username)
        driver.find_element(By.ID, "Password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        driver.get("https://ioe.vn/tu-luyen")
        time.sleep(4)
        print("Đã vào phòng tự luyện!")

        # -------------------------------------------------------------
        # VÍ DỤ MÔ PHỎNG LẤY CÂU HỎI VÀ GỌI AI:
        # (Bạn cần điều chỉnh CSS Selector / XPATH dựa theo giao diện thực tế của câu hỏi)
        # -------------------------------------------------------------
        # question_element = driver.find_element(By.CLASS_NAME, "class-chua-cau-hoi")
        # question_text = question_element.text
        #
        # print(f"Đã đọc câu hỏi: {question_text}")
        # answer = ask_ai_for_answer(question_text)
        # print(f"AI gợi ý đáp án: {answer}")
        #
        # # Sau đó viết logic code click vào đáp án tương ứng trên màn hình...

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
