import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from datetime import date, datetime
from collections import Counter


def main():
    
    dict = Counter()

    id = 30
    url = "https://intera.bossdesk.io/api/v1/tickets/" + str(id)
    headers={'Authorization': 'Token token=""', 
            'Content-Type':'application/json'}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    data = pd.json_normalize(response.json())
    entry = data['created_at'].values[0]
    utc_dt = entry.replace("Z", "UTC")
    dt = datetime.strptime(utc_dt, "%Y-%m-%dT%H:%M:%S.%f%Z")
    dict[(dt.month, dt.year)] += 1
    print(dt)
    # print(datetime.today().month)
    
    while dt <= datetime.today():
        try: 
            id += 1
            url = "https://intera.bossdesk.io/api/v1/tickets/" + str(id)
            response = requests.get(url, headers=headers)
            print(response.status_code)
            data = pd.json_normalize(response.json())
            entry = data['created_at'].values[0] 
            utc_dt = entry.replace("Z", "UTC")
            dt = datetime.strptime(utc_dt, "%Y-%m-%dT%H:%M:%S.%f%Z")
            print(dt)
            dict[(dt.month, dt.year)] += 1
        except:
            continue
        
        
    print(dict)
    # dict = sorted(dict.keys)
    dates = pd.to_datetime(['{}-{}'.format(y, m) for (m, y) in dict.keys()])
    
    
    plt.bar(dates, dict.values())
    
    for i in range(len(dates)):
        plt.text(i, list(dict.values())[0], list(dict.values())[0], ha = 'center')
    
    plt.title("Tickets Submitted Over Time")
    plt.xlabel("Month")
    plt.ylabel("Tickets submitted")
    plt.gcf().autofmt_xdate()
    plt.show()
    

if __name__ == "__main__":
    main()