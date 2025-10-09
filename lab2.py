import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

url='https://ria.ru/'
headers={'User-Agent': 'Mozilla/5.0'}
response=requests.get(url,headers=headers)
response.raise_for_status()
soup=BeautifulSoup(response.text,'html.parser')
news=soup.find_all('a', class_='cell-list__item-link color-font-hover-only', limit=10)
data=[]

for new in news:
    title_raw=new.get_text(' ',strip=True)
    title=re.sub(r'\s+',' ',title_raw).strip()
    link=new.get('href')

    article_response=requests.get(link,headers=headers)
    article_soup=BeautifulSoup(article_response.text,'html.parser')

    date_tag=article_soup.find('div',class_='article__info-date')
    if date_tag:
        date_text=date_tag.get_text(strip=True).split()[0]
        try:
            date=datetime.strptime(date_text,'%d.%m.%Y')
        except ValueError:
            date=None
    else:
        date=None

    text_parts=article_soup.find_all('div',class_='article__text')
    full_text=' '.join([p.get_text(' ',strip=True) for p in text_parts])

    data.append({'title': title,'link': link,'date': date,'text': full_text})

df=pd.DataFrame(data)
print(f'Вывод первых 10 новостных заголовков:\n{df[['title']]}')
print(f'Вывод текста новостей:\n{df[['text']]}')
