import os
import json
import urllib.request
from tqdm import tqdm

from PIL import Image
from googleapiclient.discovery import build

"""
Change config.json. queries.txt should have each query on a new line. Then, simply run python -i query_images.py
Note: currently bug with num, cannot go above 10. This is due to the number of results on a search page? (intended on GoogleAPI,
# but to enable more results, i should 
"""

config = []
with open('config.json') as f:
    config = json.load(f)

api_key = config['api_key']
custom_search_id = config['custom_search_id']
dir_name = config['dir_name']
query_file = config['query_file']
num = config['num']

def search(query, num=10):
    service = build("customsearch", "v1",
            developerKey=api_key)

    results = []
    start = 1
    while num > 0:
        res = service.cse().list(
            q=query,
            cx=custom_search_id,
            searchType='image',
            num=min(10, num),
            start=start
        ).execute()

        start += 10
        num -= 10
        results.extend(res['items'])    

    return results

queries = []
with open(query_file, 'r', encoding="utf8") as f:
    for line in f:
        queries.append(line.strip())

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print("Directory" , dir_name,  "created ")
    
i = config['i']
pbar = tqdm(queries)
for query in pbar:
    pbar.set_description(f"{query}")
    result = search(query, num)
    for item in result:
        link = item['link']
        try:
            with urllib.request.urlopen(link) as url:
                with open(os.path.join(dir_name, f'{i}.{link.split(".")[-1]}'), 'wb') as f:
                    f.write(url.read())
                    i += 1
        except:
            pass