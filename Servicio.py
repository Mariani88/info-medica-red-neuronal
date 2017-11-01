'''
Created on Oct 4, 2017

@author: martin
'''

import requests

r = requests.get('http://localhost:8080/greeting?name=hola')
print r.text
    