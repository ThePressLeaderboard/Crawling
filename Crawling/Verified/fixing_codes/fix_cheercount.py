# cheer_counts 칼럼 데이터 Null 값일 경우, 0으로 대체
import pandas as pd

# CSV 파일을 읽어옵니다.
df = pd.read_csv('journalist_without_zero.csv')

# 'cheer_counts' 열의 값을 처리합니다.
for i, value in enumerate(df['cheer_counts']):
    try:
        df.at[i, 'cheer_counts'] = int(value)
    except ValueError:
        df.at[i, 'cheer_counts'] = 0

# 변경된 DataFrame을 다시 CSV 파일로 저장합니다.
df.to_csv('journalist.csv', index=False)
