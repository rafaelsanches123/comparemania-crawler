import urllib.request
import bs4 as bs
import re
import pandas as pd
from datetime import datetime

df_comparemania = pd.DataFrame(
                   columns=[
                       'Loja','Melhor_Ganho','Latam','Azul','GOL','Livelo','Esfera'
                   ])


for i in range(1,13):

    url = f"https://www.comparemania.com.br/pontosmilhas/maispopular/{i}"
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = urllib.request.Request(url,headers=hdr)
    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce,'html.parser') #Beautiful Soup object
    table = soup.find("table")

    # Collecting Ddata
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
        
        if(columns != []):
            row = [columns[0].text.strip(), columns[1].text.strip(),columns[2].text.strip(),columns[3].text.strip(),columns[4].text.strip(),columns[5].text.strip(),columns[6].text.strip()]
            new_df = pd.DataFrame([row],columns=[
                        'Loja','Melhor_Ganho','Latam','Azul','GOL','Livelo','Esfera'
                    ])
            df_comparemania = pd.concat([df_comparemania, new_df], axis=0, ignore_index=True)

dt_ingestion = datetime.today().strftime('%Y-%m-%d')
print(dt_ingestion)
df_comparemania['dt_ingestion']= dt_ingestion
file_name = f'data/dataset-comparemania-{dt_ingestion}.csv'
df_comparemania.to_csv(file_name, index=False)