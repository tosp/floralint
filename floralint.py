#!/usr/bin/python3

import urllib.request
import re

from bs4 import BeautifulSoup

from rules_data import better_as_null_en, better_as_null_es


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

    def test_wcag_f39(self):
        """ F39:
        Failure of Success Criterion 1.1.1 due to providing a
        text alternative that is not null (e.g., alt="spacer" or alt="image")
        for images that should be ignored by assistive technology.
        """
        images = self.soup.findAll('img')
        for image in images:
            if 'alt' in image:
                for description in better_as_null_en:
                    if image['alt'] == description:
                        print('The alt value {} is not very descriptive'
                              .format(description))
                        print('It would be better as a null value')
                for description in better_as_null_es:
                    if image['alt'] == description:
                        print('The alt value {} is not very descriptive'
                              .format(description))
                        print('It would be better as a null value')

    def test_wcag_f65(self):
        """ F65:
        Failure of Success Criterion 1.1.1 due to omitting
        the alt attribute or text alternative on img elements,
        area elements, and input elements of type "image".
        """

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
