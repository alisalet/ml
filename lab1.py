import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

api=KaggleApi()
api.authenticate()
dataset='norc/general-social-survey'
api.dataset_download_files(dataset, path='./data', unzip=True)

csv_files=[file for file in os.listdir('./data') if file.endswith('.csv')]
csv_path=os.path.join('./data', csv_files[0])

df=pd.read_csv(csv_path, low_memory=False)
print(f'Размер датасета: {df.shape}')

general_keywords=['general happy', 'satisfaction', 'life satisfaction', 'trust', 'confid']
specific_keywords=['happy', 'satisf', 'life', 'trust', 'moral']
target_column=None
for keyword in general_keywords:
    for col in df.columns:
        if keyword in col.lower() and df[col].count()>=1000 and df[col].nunique()>=3:
            target_column=col
            break
    if target_column:
        break

if target_column is None:
    for keyword in specific_keywords:
        for col in df.columns:
            if keyword in col.lower() and df[col].count()>=1000 and df[col].nunique()>=3:
                target_column=col
                break
        if target_column:
            break

print(f'Целевой признак: {target_column}')
print(f'Данных: {df[target_column].count()}')
print(f'Уникальных значений: {df[target_column].nunique()}')
print(f'Пример данных:\n{df[target_column].value_counts().head()}')
