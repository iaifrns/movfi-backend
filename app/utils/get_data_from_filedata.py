from sqlalchemy.orm import Session
import app.model.model as models
from app.config.database import sessionLocal

def fetch_data_point(data, count, page = 1):
    keys = []
    newData = []
    start = (page - 1) * count
    print(start)
    print('='*80)
 
    for key in data[0].keys():
        if key[-1:] == 'x':
            keys.append(key[:-1])

    end = count+start

    if end > len(keys):
        end = len(keys)

    for i in range(len(data)):
        obj = {}
        for j in range(start, (end)):
            obj[f'{keys[j]}x'] = data[i][f'{keys[j]}x']
            obj[f'{keys[j]}y'] = data[i][f'{keys[j]}y']

        newData.append(obj)
    
    return newData