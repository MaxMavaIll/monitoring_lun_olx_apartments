import requests
import logging
import time

from bs4 import BeautifulSoup
from tb_bot.api_bot import send_message


BASE_URL = 'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/q-%D0%9E%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B8/?currency=UAH&search%5Bdistrict_id%5D=1&search%5Bfilter_enum_number_of_rooms_string%5D%5B0%5D=dvuhkomnatnye&search%5Bfilter_enum_number_of_rooms_string%5D%5B1%5D=odnokomnatnye&search%5Bfilter_float_floor%3Ato%5D=15&search%5Bfilter_float_price%3Afrom%5D=14000&search%5Bfilter_float_price%3Ato%5D=16500'
URL_LINK = 'https://www.olx.ua'

floor_filter = 'Поверх: '
areas_filter = 'Загальна площа: '
areas_kitchen_filter = 'Загальна кухні: '
room_filter = 'Кількість кімнат: '




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
    
        if "OLX" not in data:
            data["OLX"] = []

        response = requests.get(BASE_URL)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            apartments = soup.find_all("div", class_="css-1sw7q4x")  

            log.info(f"Len apartments {len(apartments)}")
            for index, apartment in enumerate(apartments):
                article_id = apartment.get('id')

                if article_id not in data["OLX"]:

                    link = apartment.find('a') if apartment.find('a') else "Опису немає"
                    
                    full_link = URL_LINK + link['href'] if article_id else None

                    if full_link is None:
                        continue

                    response = requests.get(full_link)
                    if response.status_code == 200:

                        soup = BeautifulSoup(response.content, 'html.parser')
                        info_about_apartment = soup.find_all('li', class_="css-1r0si1e")
                        text = "Опису немає"
                        floor = "Опису немає"
                        areas = "-"
                        areas_kit = "-"
                        rooms = "Опису немає"

                        for index, info in enumerate(info_about_apartment):
                            
                            text = info.find('p').get_text(strip=True) if info.find('p') else "Опису немає"

                            if floor_filter in text:
                                floor = text[len(floor_filter):] 

                            if areas_filter in text:
                                areas = text[len(areas_filter):] 

                            if areas_kitchen_filter in text:
                                areas_kit = text[len(areas_kitchen_filter):] 

                            if room_filter in text:
                                rooms = text[len(room_filter):] 
                            
                        description = soup.find('div', class_="css-1o924a9").get_text(strip=True) if soup.find('div', class_="css-1o924a9") else "Опису немає"

                        price = soup.find('h3', class_='css-90xrc0').get_text(strip=True) if soup.find('h3', class_='css-90xrc0') else "Опису немає"
                        street = soup.find('h4', class_='css-1kc83jo').get_text(strip=True) if soup.find('h4', class_='css-1kc83jo') else "Опису немає"
                        
                        message = f"""
    <strong>OLX</strong>
                    
    Ціна: {price}
    Вулиця: <code>{street}</code> 
    Опис: 
    <b>{description}</b>

    Кімнати: {rooms}
    Площа: {areas}/-/{areas_kit}
    Поверх: {floor}
        <a href="{full_link}">Перейти на сайт</a>
        """
                        
                        send_message(message, token, chain_id)
                        data["OLX"].append(article_id)
                        time.sleep(5)

        else:
            log.error("LUN | Помилка при доступі до сторінки:", response.status_code)
    except Exception as e:
        log.error(e)

# check_flat_with_filter()