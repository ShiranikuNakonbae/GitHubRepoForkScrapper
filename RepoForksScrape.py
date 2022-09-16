import requests
import pandas as pd

url = "https://api.github.com/repos/blynkkk/blynk-library/forks?per_page=100&page=1"
res = requests.get(url, headers = {"Authorization": "Bearer <YOUR-TOKEN-HERE>"})
repos = res.json()
db = []

while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers = {"Authorization": "Bearer <YOUR-TOKEN-HERE>"})
    repos.extend(res.json())
    #print(repos)
    
for i in repos:
    link = i['html_url']
    updated_at = i['updated_at']
    compare_url = i['compare_url']
    print(link)
    print('Last update: '+updated_at)
    #print(compare_url)
    urlcompare = compare_url.replace('{base}', 'blynkkk:master').replace('{head}', 'master')
    #print(urlcompare)
    page = requests.get(urlcompare, headers = {'Accept': 'application/vnd.github+json', 
            'Authorization': 'Bearer <YOUR-TOKEN-HERE>'})
    pagejson = page.json()
    if page.status_code == 200:
        pagestatus = pagejson['status']
        aheadby = str(pagejson['ahead_by'])
        behindby = str(pagejson['behind_by'])
        print('Status: '+pagestatus)
        print('Ahead by: '+aheadby)
        print('Behind by: '+behindby)
        print('-----')
        db.append(
            {
                'Link' : link,
                'Updated at' : updated_at,
                'Status' : pagestatus,
                'Ahead by' : aheadby,
                'Behind by' : behindby
            }
        )
        df = pd.DataFrame(db)
        df.to_csv('filename.csv')
    else:
        continue
