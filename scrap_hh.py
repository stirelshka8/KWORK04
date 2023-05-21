from bs4 import BeautifulSoup as bs
from random import choice
import requests
import os


def getting_user_agents():
    user_agents = []
    with open('user_agents.txt', 'r') as file:
        for line in file.readlines():
            user_agents.append(line.replace('\n', ''))

    return {'User-Agent': choice(user_agents)}


def read_file():
    search_terms = []
    with open('search_terms.txt', 'r') as file:
        for line in file.readlines():
            search_terms.append(line.replace('\n', ''))

    return search_terms


def read_name_file():
    list_files = []
    name_file = 1
    matching_names = []
    for x in os.listdir():
        if x.endswith(".a"):
            # Prints only text file present in My Folder
            list_files.append(x)

    for one_file in list_files:
        matching_names.append(one_file.split('.a')[0].split('_')[-1])
        if len(list_files) is None:
            pass
        else:
            name_file = int(max(matching_names)) + 1

    if len(list_files) >= 2:
        os.remove(f'found_vacancies_{int(min(matching_names))}.a')


    print(name_file)

    return name_file


def scrap_hh(set_search, name_file):
    counter = 0

    pag_urls = []
    start_page = 0
    session = requests.Session()
    preffix_url = f'https://hh.ru/search/vacancy?area=113&industry=29&search_field=name&search_field=company_name' \
                  f'&search_field=description&enable_snippets=false&text={set_search}&from=suggest_post'
    suffix_url = f'&page={start_page}'
    url_hh = preffix_url + suffix_url
    request = session.get(url_hh, headers=getting_user_agents())
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count_pages = int(pagination[-1].text)
            for i in range(count_pages):
                url = preffix_url + f'&page={i}'
                if url not in pag_urls:
                    pag_urls.append(url)
        except:
            pass
    for one_pag_urls in pag_urls:
        request = session.get(one_pag_urls, headers=getting_user_agents())  # ответ от сервера
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', class_="serp-item")

        for div in divs:
            try:
                title = div.find('a', class_="serp-item__title")
                salary = div.find('span', class_="bloko-header-section-3")

                with open(f"found_vacancies_{name_file}.a", "a") as f:
                    f.write(f'{title.text} >>>> {salary.text} >>>> {title["href"]}\n')
                counter += 1

            except AttributeError:
                pass

    print(counter)
    print(set_search)


def startup():

    nemeson = read_name_file()

    for one_search_terms in read_file():
        scrap_hh(one_search_terms, nemeson)

    # read_name_file()

