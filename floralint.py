#!/usr/bin/python3

import urllib.request
import re

from bs4 import BeautifulSoup


class FloraLint:

    def __init__(self, url='https://tosp.io'):
        print("Initializing...")
        self.url = url
        raw = urllib.request.urlopen(url)
        self.html = raw.read()
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.css_list = []

    def get_css_files(self):
        css_links = self.soup.findAll('link')
        http_re = re.compile(r'https:.?')
        for link in css_links:
            if not re.match(http_re, link['href']):
                self.css_list.append(self.url+link['href'])
        print(self.css_list)

    # Images with no alt
    def test_wcag_f65(self):
        images = self.soup.findAll('img')
        for image in images:
            if 'alt' not in image:
                print('Shitty code, no alt html value')
                print(image.attrs)

    def test_all(self):
        self.test_wcag_f65()

    def main(self):
        self.get_css_files()
        self.test_all()


lint = FloraLint('https://tosp.io')
lint.main()
