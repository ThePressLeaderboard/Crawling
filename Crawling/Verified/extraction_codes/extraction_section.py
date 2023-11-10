from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

class NaverJournalistScraper:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.wait = WebDriverWait(self.driver, 5)

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait to load the page
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrape_journalist_by_press(self, press_id, category_id, press_name, writer):
        self.driver.get(f'https://media.naver.com/journalists/whole?officeId={press_id}')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.journalist_list_content_name')))
        self.scroll_to_bottom()

        journalist_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.journalist_list_content_name')
        journalist_links = [element.get_attribute('href') for element in journalist_elements]
        journalist_ids = [link.split('/')[-1] for link in journalist_links]

        section_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.journalist_list_content_info')
        sections = []

        for section_element in section_elements:
            section_span = section_element.find_element(By.XPATH, './span[contains(@class, "journalist_list_content_info_item")][2]')
            section = section_span.text if section_span else None
            sections.append(section)

        for section, journalist_id in zip(sections, journalist_ids):
            if section:  # section이 None이 아닌 경우에만 CSV 파일에 기록
                writer.writerow([section, journalist_id])
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    press_data = """
    665 4 더스쿠프
    024 4 매경이코노미
    308 4 시사IN
    586 4 시사저널
    262 4 신동아
    094 4 월간산
    243 4 이코노미스트
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

    press_category_list = [line.split() for line in press_data.strip().split('\n')]

    with open('journalist_section2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=' ')  # 공백으로 데이터 구분

        writer.writerow(['section_id', 'journalist_id'])

        scraper = NaverJournalistScraper()
        try:
            for press_id, category_id, name in press_category_list:
                scraper.scrape_journalist_by_press(press_id, category_id, name, writer)
        finally:
            scraper.close()