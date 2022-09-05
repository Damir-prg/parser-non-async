import json
import requests
import datetime
from bs4 import BeautifulSoup


url = 'https://www.culture.ru/afisha/respublika-tatarstan-almetevsk'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.0.0 Safari/537.36',
    'accept': '*/*'
}

event_list = []

counter = 0


def get_html(url, params=None):
    try:
        # Получить веб-страницу с помощью get-запроса
        req = requests.get(url, headers=HEADERS, params=params)
        return req
    except Exception as e:
        print(repr(e))
        print('ОШИБКА В ПОЛУЧЕНИЕ ДОКУМЕНТА HTML_main_URL')


def get_last_page(html):
    # Инициализируем soup
    soup = BeautifulSoup(html, 'html.parser')
    # Получем элементы с цифрами из нижнего блока пагинации сайта, чтобы узнать количество страниц
    pages = soup.find_all('div', class_='vt1mg')
    last_page = 0

    for page in pages:
        # Добавляем в константу количество страниц на сайте
        last_page = int(page.get_text()[-1])

    return last_page

# Сохраняем массив мероприятий в json файл
def set_to_json():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"Event_List_{cur_time}_.json", "w", encoding="utf-8") as file:
        json.dump(event_list, file, indent=4, ensure_ascii=False)


def get_content(html):
    global url
    try:
        # Инициализируем soup
        soup = BeautifulSoup(html, 'html.parser')

        # Получаем все элементы с карточками мероприятий
        cards = soup.find_all('div', class_='CHPy6')

        # Пробегаясь по каждому элементу массива, получаем из него текст
        for card in cards:
            # Из блока div достаём блок script
            # преобразуем данные в json
            json_object = json.loads(card.find('script').contents[0])
            card_page_url = json_object['url']
            card_img_url = json_object['image']['url']
            card_price = json_object['offers']['price']
            card_name = json_object['name']
            card_place = ''
            card_date = card.find('div', class_='r8tBP').get_text()

            for k, v in json_object['location'].items():
                if k == 'name':
                    card_place = v

            # Проблемное место
            card_name.replace("\\xa0", " ")

            # Добавляем данные в массив мероприятий
            event_list.append(
                {
                    "event_url": card_page_url,
                    "event_img_url": card_img_url,
                    "event_price": card_price,
                    "event_name": card_name,
                    "event_place": card_place,
                    "event_address": parse_page_place(card_page_url),
                    "event_date": card_date
                }
            )
    except Exception as e:
        print(repr(e))
        print('ОШИБКА В ЗАПИСЕ В БД')


def parse():
    try:
        # Получаем ответ от request
        html = get_html(url)

        # "The HTTP 200 OK" указывает, что запрос выполнен успешно
        if html.status_code == 200:
            # Получаем кол-во страниц
            last_page = get_last_page(html.text)

            # Проходим по каждой странице и парсим её
            for page in range(1, last_page+1):
                html = get_html(url + f"?page={page}")

                if html.status_code == 200:
                    get_content(html.text)
            set_to_json()
            print(event_list)
        else:
            print('Error')
    except Exception as e:
        print(repr(e))
        print('ОШИБКА В ЧТЕНИЕ main_URL')


def parse_page_place(url):
    """
    Функцияя нужна для получения адреса проведения мероприятия
    url каждого отдельного мероприятя
    :param url: string
    :return: string
    """
    global counter
    try:
        counter += 1
        print(f"отработано {counter}")
        html = get_html(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            place = soup.find('div', class_="uMrgA")
            # Возвращаем в текстовом формате кажое мероприятие
            return place.get_text()
    except Exception as e:
        print(repr(e))
        print('ОШИБКА В ЧТЕНИЕ АДРЕСА МЕРОПРИЯТИЯ')


parse()
