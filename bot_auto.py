from time import sleep

import telegram
import argparse
from environs import Env

import requests


def main():
    env = Env()
    env.read_env()
    chat_id = env.str('CHAT_ID')
    headers = {'Authorization': f'Token {env.str("DVMN_TOKEN")}'}
    params = {}
    bot = telegram.Bot(token=env.str('TG_CLIENTS_TOKEN'))
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                params=params
            )
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            sleep(3)
        else:
            response.raise_for_status()
            checks: dict = response.json()
            if not checks.get('status') == 'found':
                params = {'timestamp': checks['timestamp_to_request']}
            else:
                lesson_info = checks['new_attempts'][0]
                msg_text = f'У вас проверили работу "{lesson_info["lesson_title"]}"\n\n'
                if lesson_info['is_negative']:
                    msg_text += 'К сожалению в работе нашлись ошибки\n'
                else:
                    msg_text += f'Ваша работа принята! Можно приступать к следующему уроку.\n\n'
                msg_text += f'Cсылка на работу: {lesson_info["lesson_url"]}'
                bot.send_message(chat_id=chat_id, text=msg_text)


if __name__ == "__main__":
    main()