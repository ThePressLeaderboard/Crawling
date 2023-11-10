from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from bs4 import BeautifulSoup
import re

class NaverJournalistScraper:
    def __init__(self):
        # Headless 모드 옵션 추가
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Headless 모드 활성화
        chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
        chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화

        self.service = Service(ChromeDriverManager().install())
        # chrome_options를 추가하여 WebDriver 초기화
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)  # WebDriverWait 초기화

    def scrape_journalist_by_press(self, press_id, category_id, press_name):
        self.driver.get(f'https://media.naver.com/journalists/whole?officeId={press_id}')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.journalist_list_content_name')))
        self.scroll_to_bottom()

        journalist_ids, journalist_links = self.collect_journalist_links()

        # 파일명을 변경하여 name을 포함하도록 합니다.
        csv_filename = f'Journalists of {press_name}_{press_id}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file, delimiter=',')  # 쉼표로 구분
            csv_writer.writerow(['press_id', 'journalist_id', 'name', 'subscribers_count', 'articles_count', 'cheer_counts'])

            for journalist_id, journalist_link in zip(journalist_ids, journalist_links):
                journalist_data = self.get_journalist_data(journalist_id, journalist_link, category_id, press_id)
                csv_writer.writerow(journalist_data[1:])

        print(f"CSV 파일 {csv_filename} 생성 완료")
        
    def scroll_to_bottom(self):
        # 페이지를 아래로 스크롤하여 모든 기사를 로드합니다.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 스크롤이 로딩될 때까지 대기
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def close(self):
        self.driver.quit()

    def collect_journalist_links(self):
        journalist_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.journalist_list_content_name')
        journalist_links = [element.get_attribute('href') for element in journalist_elements]

        # journalist_id 추출 (링크의 마지막 숫자)
        journalist_ids = [link.split('/')[-1] for link in journalist_links]

        return journalist_ids, journalist_links

    def get_journalist_data(self, journalist_id, journalist_link, category_id, press_id):
        self.driver.get(journalist_link)
        time.sleep(2)  # 페이지 로딩 대기

        # 처음 값 초기화
        journalist_name = "Unknown"  # 이름 못 찾으면 unknown
        subscribers_count = "0"
        articles_count = "0"
        cheer_counts = "0"

        try:
            journalist_name_element = self.driver.find_element(By.CSS_SELECTOR, 'h2.media_reporter_basic_name')
            journalist_name = journalist_name_element.text.replace(" ", "")  # 공백 제거
        except Exception as e:
            print(f"Error getting journalist name for journalist_id {journalist_id}: {e}")

        
        try:
            subscribers_count_element = self.driver.find_element(By.CSS_SELECTOR, 'em._journalist_subscribe_count').text
            subscribers_count = int(subscribers_count_element)  # 문자열을 정수로 변환
        except Exception as e:
            print(f"Error getting subscribers count for journalist_id {journalist_id}: {e}")
        
        try:
            articles_info = self.driver.find_element(By.CSS_SELECTOR, 'li.media_reporter_summary_item').text
            articles_count_match = re.search(r'(\d+)건의 기사를 작성했습니다', articles_info)
            if articles_count_match:
                articles_count = articles_count_match.group(1)
        except Exception as e:
            print(f"Error getting articles count for journalist_id {journalist_id}: {e}")

        try:
            cheer_counts_element = self.driver.find_element(By.CSS_SELECTOR, 'em.u_cnt._count._journalist_cheer_count')
            cheer_counts = cheer_counts_element.text.replace(",", "")  # 쉼표 제거
            cheer_counts = int(cheer_counts)  # 문자열을 정수로 변환
        except Exception as e:
            print(f"Error getting cheer count for journalist_id {journalist_id}: {e}")
        return [category_id, press_id, journalist_id, journalist_name, subscribers_count, articles_count, cheer_counts]

if __name__ == "__main__":
    # press_id와 category_id 목록 예시
    press_data = """
    press_id,category_id,name
    032,0,경향신문
    005,0,국민일보
    020,0,동아일보
    021,0,문화일보
    081,0,서울신문
    022,0,세계일보
    023,0,조선일보
    025,0,중앙일보
    028,0,한겨레
    469,0,한국일보
    437,1,JTBC
    056,1,KBS
    214,1,MBC
    057,1,MBN
    055,1,SBS
    374,1,SBSBiz
    448,1,TV조선
    052,1,YTN
    421,1,뉴스1
    003,1,뉴시스
    001,1,연합뉴스
    422,1,연합뉴스TV
    449,1,채널A
    215,1,한국경제TV
    009,2,매일경제
    008,2,머니투데이
    648,2,비즈워치
    011,2,서울경제
    277,2,아시아경제
    018,2,이데일리
    366,2,조선비즈
    123,2,조세일보
    014,2,파이낸셜뉴스
    015,2,한국경제
    016,2,헤럴드경제
    079,3,노컷뉴스
    629,3,더팩트
    119,3,데일리안
    138,3,디지털데일리
    029,3,디지털타임스
    417,3,머니S
    006,3,미디어오늘
    293,3,블로터
    031,3,아이뉴스24
    047,3,오마이뉴스
    030,3,전자신문
    092,3,지디넷코리아
    002,3,프레시안
    665,4,더스쿠프
    024,4,매경이코노미
    308,4,시사IN
    586,4,시사저널
    262,4,신동아
    094,4,월간산
    243,4,이코노미스트
    037,4,주간동아
    053,4,주간조선
    353,4,중앙SUNDAY
    036,4,한겨레21
    050,4,한경비즈니스
    127,5,기자협회보
    662,5,농민신문
    607,5,뉴스타파
    584,5,동아사이언스
    310,5,여성신문
    640,5,코리아중앙데일리
    044,5,코리아헤럴드
    296,5,코메디닷컴
    346,5,헬스조선
    655,6,CJB청주방송
    661,6,JIBS
    660,6,kbc광주방송
    654,6,강원도민일보
    087,6,강원일보
    666,6,경기일보
    658,6,국제신문
    657,6,대구MBC
    656,6,대전일보
    088,6,매일신문
    082,6,부산일보
    659,6,전주MBC
    """
    # Split the string into lines and then each line by spaces or commas
    press_category_list = [tuple(re.split(r',\s*', line.strip())) for line in press_data.strip().split('\n')[1:]]


    scraper = NaverJournalistScraper()
    start_time = time.time()  # 시작 시간 기록
    try:
        for press_id, category_id, name in press_category_list:
            scraper.scrape_journalist_by_press(press_id, category_id, name)
    finally:
        scraper.close()
    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 경과 시간 계산
    print(f"파일 생성에 걸린 총 시간: {elapsed_time:.2f}초")