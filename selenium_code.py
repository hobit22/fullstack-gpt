from selenium import webdriver

# Selenium 드라이버 초기화
driver = webdriver.Chrome()

# HTML 파일 로드
file_path = "/case1.html"
driver.get("file://" + file_path)

# 사용자 question 엘리먼트 찾기
question_element = driver.find_element_by_xpath("//div[contains(text(), '중1(상)')]")

# question 엘리먼트 클릭
question_element.click()

# 실행 코드 작성
# ...

# 드라이버 종료
driver.quit()