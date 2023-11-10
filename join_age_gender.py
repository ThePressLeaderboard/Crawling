import pandas as pd
import os

# 작업 디렉토리를 변경하려면 아래 경로를 변경하십시오.
directory_path = 'D:\coding_directory\DataCrawling_news'

# 빈 데이터프레임을 생성하여 컬럼명을 저장할 준비
combined_age = pd.DataFrame()
combined_gender = pd.DataFrame()

# 디렉토리 내의 모든 _age.csv 파일을 읽어서 데이터프레임으로 저장
for filename in os.listdir(directory_path):
    if filename.endswith('_age.csv'):
        with open(os.path.join(directory_path, filename), 'r', newline='', encoding='utf-8-sig') as file:
            df = pd.read_csv(file, delimiter=' ', header=None)  # 컬럼명을 지정하지 않음
            # 컬럼명이 없으면 추가
            if combined_age.empty:
                combined_age = df
            else:
                # 컬럼명이 이미 있는 경우 컬럼명은 추가하지 않음
                combined_age = pd.concat([combined_age, df])

# 새로운 age.csv 파일로 저장
combined_age.to_csv('age.csv', index=False, header=False, sep=' ')

# 디렉토리 내의 모든 _gender.csv 파일을 읽어서 데이터프레임으로 저장
for filename in os.listdir(directory_path):
    if filename.endswith('_gender.csv'):
        with open(os.path.join(directory_path, filename), 'r', newline='', encoding='utf-8-sig') as file:
            df = pd.read_csv(file, delimiter=' ', header=None)  # 컬럼명을 지정하지 않음
            # 컬럼명이 없으면 추가
            if combined_gender.empty:
                combined_gender = df
            else:
                # 컬럼명이 이미 있는 경우 컬럼명은 추가하지 않음
                combined_gender = pd.concat([combined_gender, df])

# 새로운 gender.csv 파일로 저장
combined_gender.to_csv('gender.csv', index=False, header=False, sep=' ')
