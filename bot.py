from time import sleep

import telegram
from environs import Env

import requests


def main(bot_token, chat_id):
    headers = {'Authorization': f'Token {bot_token}'}
    params = {}
    bot = telegram.Bot(token=env.str('TG_CLIENTS_TOKEN'))
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                params=params
            )
        except requests.exceptions.ReadTimeout as e:
            print('Посылаем запрос еще раз')
        except requests.exceptions.ConnectionError as e:
            print('Пропал интернет, подождем 3 сек')
            sleep(3)
        else:
            response.raise_for_status()
            checks: dict = response.json()
            if not checks.get('status') == 'found':
                params = {'timestamp': checks['timestamp_to_request']}
            else:
                updates = bot.get_updates()
                lesson_info = checks['new_attempts'][0]
                msg_parts = [None for i in range(3)]
                msg_parts[0] = f'У вас проверили работу "{lesson_info["lesson_title"]}"\n'
                if lesson_info['is_negative']:
                    msg_parts[1] = 'К сожалению в работе нашлись ошибки'
                else:
                    msg_parts[1] = 'Ваша работа принята! Можно приступать к следующему уроку.'
                msg_parts[2] = f'Cсылка на работу: {lesson_info["lesson_url"]}'
                bot.send_message(chat_id=chat_id, text='\n'.join(msg_parts))
            print(checks)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    chat_id = input('Введите ваш chat_id: ')
    if not chat_id:
        print('Вы не указали chat_id')
    else:
        main(env.str('DVMN_TOKEN'))