#!/usr/bin/python
import re, requests
from bs4 import BeautifulSoup
import credentials

base_url = "https://www.packtpub.com"
url = base_url + '/packt/offers/free-learning'

payload = {'email': credentials.login, 'password': credentials.password, 'op': 'Login', 'form_id': 'packt_user_login_form'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with requests.Session() as c:
    c.post(url, data=payload, headers=headers)
    r = c.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    #print(soup)
    #url2 = "https://www.packtpub.com" + str(soup.findAll('a', attrs={'href': re.compile("claim")}))
    #print(url2)
    button_url = base_url + str(soup.findAll('a', attrs={'href': re.compile("claim")})[0].get('href'))
    r = c.get(button_url, headers=headers)
    #f = open('out.html', 'w')
    #f.write(str((r.content)))
    #f.close()
