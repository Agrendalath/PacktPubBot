#!/usr/sbin/python
import re
import requests
import shutil
import os.path
import sys
from bs4 import BeautifulSoup
import credentials

payload = {
    'email': credentials.login,
    'password': credentials.password,
    'op': 'Login',
    'form_id': 'packt_user_login_form'
}
base_url = 'https://www.packtpub.com'
url = base_url + '/packt/offers/free-learning'
url2 = base_url + '/account/my-ebooks'
target_dir = 'books/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with requests.Session() as c:
    print("Logging in...")
    c.post(url, data=payload, headers=headers)
    print("Logged in successfully...")
    print("Downloading books' list...")
    r = c.get(url2, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    books = soup.findAll('a', attrs={'href': re.compile("epub")})
    titles = soup.findAll(
        'div',
        attrs = {
            'class': re.compile("product-line"),
            'class': re.compile("unseen")
        }
    )
    amount = len(books)
    print("Books' list downloaded successfully...")
    print("Downloading books...")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for counter, i in enumerate(books):
        name = str(titles[counter].get('title')).replace(' [eBook]','').replace('/','')
        filename = target_dir + name + '.epub'
        if os.path.exists(target_dir + name + '.epub'):
            print(name, "already downloaded.")
            continue
        try:
            download = c.get(str(base_url + i.get('href')), stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(download.raw, out_file)
            del download
        except KeyboardInterrupt:
            print("Exiting...")
            if os.path.isfile(filename):
                print("Removing incomplete downloads...")
                os.remove(filename)
            print("Bye.")
            sys.exit()
        print("Downloaded", name, str(counter+1) + "/" + str(amount))
    print("Finished downloading.")
    print("Bye.")

