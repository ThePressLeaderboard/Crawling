# Press 별로 journalists of_{press name}.csv 파일 생성후
# join_journalist.py 파일 사용해 한 journalist.csv 파일 생성
import pandas as pd
import os

# 작업 디렉토리 설정
directory_path = 'D:\coding_directory\Crawling_test'

# 빈 데이터프레임을 생성하여 컬럼명을 저장할 준비
combined_journalist = pd.DataFrame()

# 디렉토리 내의 모든 CSV 파일을 읽어서 데이터프레임으로 저장
for filename in os.listdir(directory_path):
    if filename.startswith("Journalists of") and filename.endswith('.csv'):
        with open(os.path.join(directory_path, filename), 'r', newline='', encoding='utf-8-sig') as file:
            df = pd.read_csv(file)
            # 컬럼명이 없으면 추가
            if combined_journalist.empty:
                combined_journalist = df
            else:
                # 컬럼명이 이미 있는 경우 컬럼명은 추가하지 않음
                combined_journalist = pd.concat([combined_journalist, df])

# "journalist.csv" 파일로 저장
combined_journalist.to_csv('journalist.csv', index=False)

print("CSV 파일이 합쳐져서 journalist.csv로 저장되었습니다.")
