# Code to collect Github repo's forks
# and compare the commit status with the original repos
# then export it to csv.
# In order to get a huge data, a github bearer token is required. Please find here: 
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


# Import library needed
import requests
import pandas as pd

# Input parameters
print('input owner name: ')
owner = input()
print('input repos name: ')
repository = input()
print('input csv result filename')
fname = input() + '.csv'
print('input github bearer token')
btoken = input()

# Initiate requests url based on input paramaeter
url = f"https://api.github.com/repos/{owner}/{repository}/forks" 
res = requests.get(url, headers = {"Authorization": f"Bearer {btoken}"})
repos = res.json()
db = []

# Traversing with pagination in order to get as much as forks
while 'next' in res.links.keys():
    res = requests.get(res.links['next']['url'], headers = {"Authorization": f"Bearer {btoken}"})
    repos.extend(res.json())
    print('next in res', res)

while 'next' not in res.links.keys():
    res = requests.get(url, headers = {"Authorization": f"Bearer {btoken}"})
    print('next not in res', res)
    
print('total repos: ', len(repos)) # Check total repos forks number
print('================================================================')


for i in repos:
    link = i['html_url']
    updated_at = i['updated_at']
    compare_url = i['compare_url']
    print(link)
    print('Last update: '+updated_at)
    #print(compare_url)
    urlcompare = compare_url.replace('{base}', f'{owner}:master').replace('{head}', 'master')
    #print(urlcompare)
    page = requests.get(urlcompare, headers = {'Accept': 'application/vnd.github+json', 
            'Authorization': f'Bearer {btoken}'})
    pagejson = page.json()
    print('urlcompare requests status: ', page)
    if page.status_code == 200: # To check request status. <Response [200]> = OK; 
        pagestatus = str(pagejson['status'])
        aheadby = str(pagejson['ahead_by'])
        behindby = str(pagejson['behind_by'])
        print('Status: '+pagestatus)
        print('Ahead by: '+aheadby)
        print('Behind by: '+behindby)
        print('-----')
        db.append(             # To append each element inside pandas dataframe
            {
                'Link' : link,
                'Updated at' : updated_at,
                'Status' : pagestatus,
                'Ahead by' : aheadby,
                'Behind by' : behindby
            }
        )
        df = pd.DataFrame(db)
        df.to_csv(fname)
    else:
        print("Page Not Found! Check urlcompare manually.")
        print('-----')
        continue
