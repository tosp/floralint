import urllib.request
from bs4 import BeautifulSoup

raw = urllib.request.urlopen('https://tosp.io')
html = raw.read()
#print(html)
soup = BeautifulSoup(html, "html.parser")
images = soup.findAll('img')

for image in images:
    if 'alt' not in image:
        print('Shitty code, no alt html value')
    print(image.attrs)
    