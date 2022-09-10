import requests
import json
import datetime

from emoji import is_emoji


token = 'ffc52effffc52effffc52eff4ffcd5bb24fffc5ffc52eff9cd30b88d025ff0fd4cc37e2'
version = 5.131
domains = [
    #'almetnews',
    #'almetgo',
    'afisha.almet',
    'almet_news',
    'liga_almet'
]

# Сохраняем список постов в json файл
def set_to_json(obj):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"..\data\Posts_List_{cur_time}_.json", "w", encoding="utf-8") as file:
        json.dump(obj, file, indent=4, ensure_ascii=False)


def sort_posts(posts):
    """
    Сортировка списка словарей с данными о постах
    :param posts: array
    :return:
    """
    sorted_posts = []
    for post in posts:
        sorted_post = {}
        sorted_post['id'] = post['id']

        try:
            sorted_post['text'] = ''.join(char for char in post['text'] if not is_emoji(char))
        except:
            sorted_post['text'] = 'none'

        try:
            sorted_post['attachments'] = post['attachments']
        except:
            sorted_post['attachments'] = 'none'

        sorted_posts.append(sorted_post)
    return sorted_posts



def vk_parse(domains, count):
    """
    Парсинг групп Вконтакте
    :param domains: array - список id групп ВК
    :param count: int - количество скачиваемых постов.
    :return:
    """
    posts_list = {}

    for domain in domains:
        posts = requests.get(f'https://api.vk.com/method/wall.get?PARAMS'
                             f'&access_token={token}'
                             f'&v={version}'
                             f'&domain={domain}'
                             f'&count={count}')

        posts = posts.json()['response']['items']
        posts_list[f'{domain}'] = sort_posts(posts)
    set_to_json(posts_list)


vk_parse(domains, 20)
