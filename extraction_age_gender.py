import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re


class NaverJournalistScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=options)
 
    def scrape_journalist_by_press(self, press_id, category_id, press_name):
        self.driver.get(f'https://media.naver.com/journalists/whole?officeId={press_id}')
        time.sleep(2)
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        journalist_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.journalist_list_content_name')
        journalist_links = [element.get_attribute('href') for element in journalist_elements]

        for journalist_link in journalist_links:
            journalist_id = journalist_link.split('/')[-1]
            
            age_data, gender_data = self.scrape_age_and_gender(journalist_link)
            
            with open(f'{press_id}_age.csv', 'a', newline='', encoding='utf-8-sig') as age_file:
                age_writer = csv.writer(age_file, delimiter=' ')
                if not age_data:
                    age_data = {f'{10*(i+1)}': '0' for i in range(6)}
                for age_label, age_percent in age_data.items():
                    age_writer.writerow([journalist_id, age_label, age_percent])

            with open(f'{press_id}_gender.csv', 'a', newline='', encoding='utf-8-sig') as gender_file:
                gender_writer = csv.writer(gender_file, delimiter=' ')
                if not gender_data:
                    gender_data = {'M': '0', 'F': '0'}
                for gender_label, gender_percent in gender_data.items():
                    gender_label = 'M' if gender_label == '남자' else 'F' if gender_label == '여자' else gender_label
                    gender_writer.writerow([journalist_id, gender_label, gender_percent])

    def scrape_age_and_gender(self, journalist_link):
        self.driver.get(journalist_link)
        time.sleep(2)
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        age_data = {}
        gender_data = {}

        age_dl = soup.find('dl', class_='group_barchart')
        
        if age_dl:
            age_groups = age_dl.find_all('div', class_='group')
            for age_group in age_groups:
                age_label = age_group.find('dt', class_='label').text.strip()
                age_percent = age_group.find('span', class_='percent').text.strip().replace(',', '').replace('%', '')
                age_label = ''.join(filter(str.isdigit, age_label))
                age_data[age_label] = age_percent

        gender_dl = soup.find('div', class_='_gender_chart_area')
        
        if gender_dl:
            gender_items = gender_dl.find_all('dt', class_='legend')
            for gender_item in gender_items:
                gender_label = gender_item.text.strip()
                gender_percent = gender_item.find_next('dd').text.strip().replace(',', '').replace('%', '')
                gender_label = 'M' if gender_label == '남자' else 'F' if gender_label == '여자' else gender_label
                gender_data[gender_label] = gender_percent

        return age_data, gender_data
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    press_data = """
    press_id,category_id,name    
    032 0 경향신문
    005 0 국민일보
    020 0 동아일보
    021 0 문화일보
    081 0 서울신문
    022 0 세계일보
    023 0 조선일보
    025 0 중앙일보
    028 0 한겨레
    469 0 한국일보
    437 1 JTBC
    056 1 KBS
    214 1 MBC
    057 1 MBN
    055 1 SBS
    374 1 SBSBiz
    448 1 TV조선
    052 1 YTN
    421 1 뉴스1
    003 1 뉴시스
    001 1 연합뉴스
    422 1 연합뉴스TV
    449 1 채널A
    215 1 한국경제TV
    009 2 매일경제
    008 2 머니투데이
    648 2 비즈워치
    011 2 서울경제
    277 2 아시아경제
    018 2 이데일리
    366 2 조선비즈
    123 2 조세일보
    014 2 파이낸셜뉴스
    015 2 한국경제
    016 2 헤럴드경제
    079 3 노컷뉴스
    629 3 더팩트
    119 3 데일리안
    138 3 디지털데일리
    029 3 디지털타임스
    417 3 머니S
    006 3 미디어오늘
    293 3 블로터
    031 3 아이뉴스24
    047 3 오마이뉴스
    030 3 전자신문
    092 3 지디넷코리아
    002 3 프레시안
    665 4 더스쿠프
    145 4 레이디경향
    024 4 매경이코노미
    308 4 시사IN
    586 4 시사저널
    262 4 신동아
    094 4 월간산
    243 4 이코노미스트
    033 4 주간경향
    037 4 주간동아
    053 4 주간조선
    353 4 중앙SUNDAY
    036 4 한겨레21
    050 4 한경비즈니스
    127 5 기자협회보
    662 5 농민신문
    607 5 뉴스타파
    584 5 동아사이언스
    310 5 여성신문
    007 5 일다
    640 5 코리아중앙데일리
    044 5 코리아헤럴드
    296 5 코메디닷컴
    346 5 헬스조선
    655 6 CJB청주방송
    661 6 JIBS
    660 6 kbc광주방송
    654 6 강원도민일보
    087 6 강원일보
    666 6 경기일보
    658 6 국제신문
    657 6 대구MBC
    656 6 대전일보
    088 6 매일신문
    082 6 부산일보
    659 6 전주MBC
"""
    press_category_list = [tuple(re.split(r',\s*|\s+', line.strip())) for line in press_data.strip().split('\n')[1:]]
    scraper = NaverJournalistScraper()
    try:
        for press_id, category_id, name in press_category_list:
            start_time = time.time()  # 작업 시작 시간 측정
            scraper.scrape_journalist_by_press(press_id, category_id, name)
            end_time = time.time()  # 작업 종료 시간 측정
            elapsed_time = end_time - start_time  # 작업 소요 시간 계산
            print(f"{name}의 CSV 파일 생성에 걸린 시간: {elapsed_time}초")
    finally:
        scraper.close()
