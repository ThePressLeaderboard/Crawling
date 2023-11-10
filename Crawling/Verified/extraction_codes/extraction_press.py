from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

# 웹드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 웹 페이지로 이동
driver.get('https://media.naver.com/journalists/whole?officeId=009')

# 페이지가 완전히 로드될 때까지 기다림
time.sleep(5)

# 카테고리 정보를 가져옴
category_elements = driver.find_elements(By.CSS_SELECTOR, '.journalist_all_category_item_link._journalist_whole_category_item')

# 카테고리 ID와 이름의 매핑을 생성
category_mapping = {}
for element in category_elements:
    category_id = element.get_attribute('data-categoryid')
    category_name = element.get_attribute('data-categoryname')
    category_mapping[category_name] = category_id

# 모든 신문사 정보를 가져옴
press_elements = driver.find_elements(By.CSS_SELECTOR, 'a._office_item')

# press.csv 파일 생성 및 데이터 쓰기
with open('press.csv', 'w', newline='', encoding='utf-8-sig') as file:
    csv_writer = csv.writer(file, delimiter=' ')
    # 컬럼명 작성
    csv_writer.writerow(['press_id', 'category_id', 'name'])

    # 추출된 데이터를 CSV 파일에 작성
    for press_element in press_elements:
        name = press_element.get_attribute('data-officename')
        category_name = press_element.get_attribute('data-categoryname')
        # 카테고리 이름을 숫자 ID로 매핑
        category_id = category_mapping.get(category_name, 'Unknown')  # 매핑에서 찾지 못한 경우 'Unknown'을 사용
        press_id = press_element.get_attribute('data-officeid')
        csv_writer.writerow([press_id, category_id, name])

# 드라이버 종료
driver.quit()

print("CSV 파일이 생성되었습니다.")
