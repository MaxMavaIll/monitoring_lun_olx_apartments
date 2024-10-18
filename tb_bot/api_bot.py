import requests
import toml
import logging as log


def send_message(message, token=None, chain_id=None):
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    data = {'chat_id': chain_id, 'text': message, 'parse_mode': 'HTML'}
        
    response = requests.post(url=url, data=data, timeout=5)

    if response.status_code == 200:
        log.info(f"Повідомлення було відправиленно успішно код {response.status_code}")
        log.debug(f"Отримано через папит:\n{response.text}")
        return True
    else:
        log.error(f"Повідомлення отримало код {response.status_code}")
        log.error(response.text)
        log.debug(f"url: {url}")
        return False