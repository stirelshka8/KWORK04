# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from random import choice
import configparser
import requests
import time
import os


config = configparser.ConfigParser()
config.read('config.cfg')


def message_generation_and_sending():
    list_files = []
    for x in os.listdir():
        if x.endswith(".a"):
            list_files.append(x)

    if int(len(list_files)) == 1:
        with open(list_files[0], 'r', encoding='utf-8') as file:
            for line in file.readlines():
                print(line.split(' >>>> '))
                message_telegram = f"Вакансия - {line.split(' >>>> ')[0]}\n" \
                                   f"Зарплата - {line.split(' >>>> ')[1]}\n\n" \
                                   f"[ПОДРОБНЕЕ]({line.split(' >>>> ')[2]})"
                send_telegram(message_telegram)
                time.sleep(3)
    else:
        vacancy_list = repetition_check()
        try:
            for line in vacancy_list[0]:
                format_url = line.split(' >>>> ')[2].split('\n')[0]
                message_telegram = f"Вакансия - {line.split(' >>>> ')[0]}\n" \
                                   f"Зарплата - {line.split(' >>>> ')[1]}\n\n" \
                                   f"[ПОДРОБНЕЕ]({line.split(' >>>> ')[2]})"
                send_telegram(message_telegram)
                time.sleep(3)
        except TypeError:
            print('Вакансии не найдены!')


def send_telegram(text: str):
    token = config.get("SET", "token")
    url = "https://api.telegram.org/bot"
    channel_id = config.get("SET", "channel")
    method = url + token + "/sendMessage" + f"?text={text}&chat_id={channel_id}&parse_mode=markdown"
    print(method)
    r = requests.post(method)


    if r.status_code != 200:
        raise ConnectionError(f"Ошибка отправки сообщения! Статус код - {r.status_code}")


def getting_user_agents():
    user_agents = []
    with open('user_agents.txt', 'r') as file:
        for line in file.readlines():
            user_agents.append(line.replace('\n', ''))

    return {'User-Agent': choice(user_agents)}


def export_search_terms():
    terms = []
    with open('terms.txt', 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            terms.append(line.replace('\n', ''))

    return terms


def read_name_file():
    list_files = []
    for x in os.listdir():
        if x.endswith(".a"):
            list_files.append(int(x.split('.a')[0].split('_')[-1]))

    if len(list_files) == 0:
        name_file = 1
    else:
        name_file = max(list_files) + 1

    return name_file


def del_old_file():
    list_files = []
    for x in os.listdir():
        if x.endswith(".a"):
            list_files.append(int(x.split('.a')[0].split('_')[-1]))

    if len(list_files) >= 2:
        os.remove(f"found_vacancies_{min(list_files)}.a")
    else:
        pass


def repetition_check():
    list_files = []
    old_list = []
    new_list = []
    finish_list = []

    for x in os.listdir():
        if x.endswith(".a"):
            list_files.append(int(x.split('.a')[0].split('_')[-1]))

    if len(list_files) >= 2:

        with open(f"found_vacancies_{list_files[1]}.a", encoding='UTF-8') as old_file:
            for old_line in old_file.readlines():
                old_list.append(old_line)

        with open(f"found_vacancies_{list_files[0]}.a", encoding='UTF-8') as new_file:
            for new_line in new_file.readlines():
                new_list.append(new_line)

        finish_list.append(list(set(new_list) - set(old_list)))
        return finish_list


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
        soup = bs(request.content, 'html.parser')

        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count_pages = int(pagination[-1].text)
            for i in range(count_pages):
                url = preffix_url + f'&page={i}'
                if url not in pag_urls:
                    pag_urls.append(url)
        except Exception as e:
            print(e)
    for one_pag_urls in pag_urls:
        request = session.get(one_pag_urls, headers=getting_user_agents())  # ответ от сервера
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', class_="serp-item")

        for div in divs:
            try:
                title = div.find('a', class_="serp-item__title")
                salary = div.find('span', class_="bloko-header-section-3")

                with open(f"found_vacancies_{name_file}.a", "a", encoding='utf-8') as f:
                    f.write(f'{title.text} >>>> {salary.text} >>>> {title["href"]}\n')
                counter += 1

            except AttributeError:
                pass

    print(counter)
    print(set_search)


def startup():
    nemeson = read_name_file()

    for one_search_terms in export_search_terms():
        scrap_hh(one_search_terms, nemeson)

    time.sleep(1)
    del_old_file()
    time.sleep(1)
    message_generation_and_sending()


if __name__ == '__main__':
    startup()
    # message_generation_and_sending()