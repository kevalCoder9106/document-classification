"""

* This web scraping project is designed to fetch articles from https://hbswk.hbs.edu
* Using this code for any other purpose, might not work

"""

import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class WebScrap:
    """
        1. Add the url
        2. Connect
        3. Parse

        ...missing any of above stage will lead to an error
    """
    def __init__(self) -> None:
        url = ""
        content = ""
        parsed_content = ""

    def show_content(self):
        print(self.parsed_content)

    """
    connect(self)
        will fetch the web page from the url
    """

    def connect(self):
        page = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(page).read()
        self.content = web_byte.decode('utf-8')
    
    """
        parse_content(self)
            will convert the web page to generic html hierarchy
    """

    def parse_content(self):
        self.parsed_content = BeautifulSoup(self.content, 'html.parser')

    """
        get_elements_content(self, element, element_class)
            will fetch the element present in the page
    """

    def get_elements_content(self, element, element_class):
        return self.parsed_content.find_all(element, {"class": element_class})

    def get_c_element_content(self, element, element_class, sub_element):
        el = self.parsed_content.find_all(element, {"class": element_class})
        return el.findChildren(sub_element)

def get_articles_links(main_page_url, page_url, total_page_num):
    total_links = 0
    _ws = WebScrap()
    
    for i in range(1, total_page_num + 1):
        url = page_url + str(i)
        print("[+] URL: ", url, end='\r')

        try:
            _ws.url = url
            _ws.connect()
            _ws.parse_content()

            elements_content = _ws.get_elements_content('a', 'hbsred')
            for element in elements_content:
                article_url = main_page_url + element.get('href')

                with open('links.txt', 'a') as file:
                    file.write(article_url + '\n')
                total_links += 1

        except Exception:
            print("[-] Something wrong happend at page number ", i)
            continue

    return total_links

def store_articles_content(path, total_links):
    _ws = WebScrap()
    
    link_count = 1
    with open('links.txt', 'r') as f:
        for link in f:
            print("[+] Total link parsed: ", link_count, ' / ', total_links, end='\r')
                
            try:
                _ws.url = link
                _ws.connect()
                _ws.parse_content()
            except:
                print("[-] Page at index ", link_count, ", is not available.")
                continue

            text = ''
            elements_content = _ws.get_elements_content('p', '')
            for element in elements_content:
                text = text + element.get_text() + ' '
                
            file_name = str(link_count) + '.txt'
            file_path = os.path.join(path,file_name)
            if os.path.exists(file_path):
                link_count += 1
                continue
            else:
                with open(file_path, 'w') as file:
                    file.write(text)
                link_count += 1

def get_articles_links_specific_1(page_url, element, element_class,limit):
    _ws = WebScrap()
    
    total_links = 0
    i = 1
    while True:
        url = page_url + str(i) + '/'
        try:
            _ws.url = url
            _ws.connect()
            _ws.parse_content()
        except:
            print("[-] Page at index ", i, ", is not available.")
            if i > limit:
                break
            else:
                continue

        print("[+] Link: ", url, end='\r')
    
        el = _ws.get_elements_content(element, element_class)
        for e in el:
            link = e.find('a').get('href')
            with open('links.txt', 'a', errors='ignore') as f:
                f.write(link + '\n')
            total_links += 1
        i += 1

        if i > limit:
            break
        else:
            continue
    
    return total_links

"""
    clear()
        clear outs the link folder
"""
def clear():
    with open('links.txt', 'w') as f:
        f.write("")

if __name__ == '__main__':
    category = 'Science & Technology'
    page_url = 'https://hbswk.hbs.edu/Pages/browse.aspx?HBSIndustry=Food%20%26%20Beverage&page='
    
    path = '../ws_data/' + category
    if os.path.exists(path) == False:
        os.mkdir(path)

    total_page_num = 29
    main_page_url = 'https://hbswk.hbs.edu'
    
    clear()

    # For harvard buisness school
    # os.system('clear')
    # total_links = get_articles_links(main_page_url, page_url, total_page_num)

    # For harvard school of arts and science (specific)
    os.system('clear')
    total_links = get_articles_links_specific_1('https://news.harvard.edu/gazette/section/science-technology/page/', 'h2', 'tz-article-image__title', 30)

    # Storing articles
    os.system('clear')
    store_articles_content(path, total_links)