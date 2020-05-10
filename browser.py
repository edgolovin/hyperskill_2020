import requests
import sys
import os
from bs4 import BeautifulSoup, SoupStrainer

wanted_tags = ['a', 'p', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
saved_tabs = []
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
proxy = {'http': 'http://' + '212.56.218.90:40572'}
tabs_folder = sys.argv[1]


try:
    os.mkdir(tabs_folder)
except FileExistsError:
    # print(f'The folder {tabs_folder} already exists')
    pass


def make_valid_url(url: str):
    if '.' not in url:
        if 'com' in url:
            url = url[:-3] + '.com'
        else:
            url += '.com'
    if 'https://' in url:
        pass
    else:
        url = 'https://' + url
    return url


def make_file_name(url: str):
    url = url.strip('https://')
    url_split = url.split('.')
    url_split.pop()
    file_name = '.'.join(url_split)
    return file_name


def show_site(url):
    r = requests.get(url)
    strainer = SoupStrainer(wanted_tags)
    strained_soup = BeautifulSoup(r.text, 'html.parser', parse_only=strainer)
    site = [st for st in strained_soup.stripped_strings]
    text = '\n'.join(site)
    print(text)
    file_name = make_file_name(url)
    with open(os.path.join(tabs_folder, file_name), 'w', encoding='utf-8') as f:
        f.write(text)
    saved_tabs.append(file_name)


def main():
    user_input = ''
    while user_input != 'exit':
        user_input = input()
        if user_input == 'exit':
            break
        elif user_input in saved_tabs:
            with open(os.path.join(tabs_folder, user_input), 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            url = make_valid_url(user_input)
            show_site(url)


if __name__ == '__main__':
    main()
