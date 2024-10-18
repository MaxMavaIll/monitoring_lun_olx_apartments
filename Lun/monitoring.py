import requests
import logging 
import time

from bs4 import BeautifulSoup
from tb_bot.api_bot import send_message


BASE_URL = 'https://lun.ua/uk/search?currency=UAH&floor_max=15&geo_id=10009580&has_eoselia=false&insert_date_min=2024-10-16&is_without_fee=false&price_max=16500&price_min=14000&price_sqm_currency=UAH&room_count=1&room_count=2&section_id=2&sort=price-desc&sub_geo_id=10026621&with_renovation=yes'
URL_LINK = "https://lun.ua/realty/"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter2)
log.addHandler(log_s)



def check_flat_with_filter(token, chain_id, data):
    try:
        if "LUN" not in data:
            data["LUN"] = []

        response = requests.get(BASE_URL)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            apartments = soup.find_all('article')  # Знайти всі блоки з оголошеннями

            log.info(f"Len apartments {len(apartments)}")
            for index, apartment in enumerate(apartments):
                # Отримуємо id з атрибута id тега <article>
                article_id = apartment.get('id')
                
                if article_id:
                    full_link = URL_LINK + article_id  # Створюємо повне посилання
                else:
                    full_link = "Посилання немає"

                # Пошук тексту опису квартири
                description = apartment.find('p').get_text(strip=True) if apartment.find('p') else "Опису немає"

                # Пошук параметра за правильним CSS-селектором (використовуємо :nth-child)
                param_element1 = apartment.select_one('button > div > div > div > div:nth-child(1) > span')
                rooms = param_element1.get_text(strip=True) if param_element1 else "Параметра немає"

                param_element2 = apartment.select_one('button > div > div > div > div:nth-child(2) > span')
                areas = param_element2.get_text(strip=True) if param_element2 else "Параметра немає"

                param_element3 = apartment.select_one('button > div > div > div > div:nth-child(3) > span')
                floor = param_element3.get_text(strip=True) if param_element3 else "Параметра немає"

                price_element = apartment.select_one('button > div > div:nth-child(1) > div')
                price = price_element.get_text(strip=True) if price_element else "Ціни немає"

                street_element = apartment.select_one('article > div > div > h3 > button')
                street = street_element.get_text(strip=True) if street_element else "Ціни немає"
                
                message = f"""
    <strong>LUN</strong>

    Ціна: {price}
    Вулиця: <code>{street}</code> 
    Опис: 
    <b>{description}</b>

    Кімнати: {rooms}
    Площа: {areas}
    Поверх: {floor}
    <a href="{full_link}">Перейти на сайт</a>
    """
                
                if article_id not in data["LUN"]:
                    send_message(message, token, chain_id)
                    data["LUN"].append(article_id)
                    time.sleep(1)

        else:
            log.error("LUN | Помилка при доступі до сторінки:", response.status_code)
    except Exception as e:
        log.error(e)