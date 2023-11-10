from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기
driver.get('https://media.naver.com/journalists/whole?officeId=009')  # HTML 페이지의 URL을 설정합니다.

# 클래스명 = 'journalist_all_category_item_link _journalist_whole_category_item'인 요소들을 가져오기
elements = driver.find_elements(By.CSS_SELECTOR, '.journalist_all_category_item_link._journalist_whole_category_item')


# 추출 데이터를 CSV 파일로 저장 (UTF-8 인코딩)
with open('category.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:  # utf-8-sig를 사용하여 BOM 문자를 추가합니다.
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['id', 'name'])  # 헤더 작성

    for idx, element in enumerate(elements):
        category_name = element.get_attribute('data-categoryname')
        csv_writer.writerow([idx, category_name])

# 웹 드라이버 종료
driver.quit()

print("CSV 파일이 생성되었습니다.")
