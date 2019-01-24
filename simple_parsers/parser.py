# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


class Soup:
    def __init__(self, response):
        """
        A wrapper over BeautifulSoup class.
        :param response: is a response of from a http request (request library).
        """
        self.html = ""
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.html = response.text
        self.external_links = set()
        self.internal_links = set()
        self.absolute_internal_links = set()
        self.url = response.url
        self._all_links = set()

    def get_pretty_soup(self):
        if self.soup:
            return self.soup.prettify()
        else:
            return 'Sorry! The soup was nasty.'

    def get_all_p(self):
        if self.soup:
            return self.soup.find_all('p')

    def get_all_p_text(self):
        p_contents = []
        if self.soup:
            for p in self.get_all_p():
                p_contents.append(p.get_text())
        return p_contents

    def get_external_links(self):
        if not self.external_links:
            current_urlparsed_obj = urlparse(self.url)
            for link in self.get_all_links():

                urlparsed_obj = urlparse(link)
                if current_urlparsed_obj.netloc != urlparsed_obj.netloc and urlparsed_obj.netloc != "":
                    self.external_links.add(link)
        return self.external_links

    def get_internal_links(self):
        if not self.internal_links:
            current_urlparsed_obj = urlparse(self.url)

            for link in self.get_all_links():
                urlparsed_obj = urlparse(link)
                if urlparsed_obj.netloc == "" or urlparsed_obj.netloc == current_urlparsed_obj.netloc:
                    self.internal_links.add(link)
        return self.internal_links

    def get_all_links(self):
        if self.soup and not self._all_links:
            links = set(map(lambda a_element: a_element.get("href", ""), self.soup.find_all('a', href=True)))
            self._all_links = list(filter(lambda x: "mailto:" not in x, links))
        return self._all_links

    def get_absolute_internal_links(self):
        if not self.absolute_internal_links:
            for link in self.get_internal_links():
                if not self._is_media_resource(link):
                    self.absolute_internal_links.add(urljoin(self.url, link))
        return self.absolute_internal_links

    def _is_media_resource(self, url):
        media_identifier_tokens = ['.jpg', '.png', 'jpeg', '.js', '.css', '.gif', '.pdf', '.doc', '.docx', '.svg', '.zip']
        for token in media_identifier_tokens:
            if url.lower().endswith(token):
                return True
        return False

