from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('file:///C:/Users/hoqei/IdeaProjects/fullstack-gpt/case1.html')

# 사용자 question의 엘리먼트를 찾기
element = driver.find_element(By.XPATH, '//div[text()="중1(상)"]')

print(element)

# 엘리먼트 클릭
element.click()