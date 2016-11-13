#!/usr/bin/python3

import urllib.request
import re

import tinycss
from bs4 import BeautifulSoup

from js_data import js_events


class FloraLint:

    def __init__(self, url='https://tosp.io'):
        print("Initializing...")
        self.url = url
        self.html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.css_list = []
        self.css_rules = []
        self.css_errors = []

    def get_css_files(self):
        css_links = self.soup.findAll('link')
        http_re = re.compile(r'https:.?')
        for link in css_links:
            if not re.match(http_re,link['href']):
                self.css_list.append(self.url+link['href'])
        print(self.css_list)

    def parse_css_links(self):
        css_parser = tinycss.make_parser('page3')
        for css_url in self.css_list:
            raw = urllib.request.urlopen(css_url)
            style = css_parser.parse_stylesheet_bytes(raw.read())
            for rule in style.rules:
                self.css_rules.append(rule)
            for err in style.errors:
                self.css_errors.append(err)

    def get_js_functions(self):
        for line in self.soup:
            print("GIGIGI",line)

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
        self.parse_css_links()
        self.test_all()
        # self.get_js_functions()





lint = FloraLint('http://127.0.0.1:8000')
lint.main()