
import requests
from bs4 import BeautifulSoup

def main():
    r = requests.get('https://drachenchronik.com/')
    soup = BeautifulSoup(r.content, 'html-parser')
    d = {}

    d['0'] = soup.select('.container .box .color .half')


    print(d)

if __name__ == '__main__':
    main()
