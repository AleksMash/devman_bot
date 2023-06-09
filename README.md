# Описание

Это простой Telegram бот, который монторит [API Devman](https://dvmn.org/api/docs/)  и позволяет получать уведомление о факте окончания проверки  работы, которую вы сдали на ревью.

# Установка

Python3 должен быть уже установлен.
Затем используйте `pip` для установки зависимостей:

```
pip install -r requirements.txt
```

## Переменные окружения

Скрипт использует чувствительные данные - токен вашего Telegram бота и ваш токен для доступа к [API DevMan](https://dvmn.org/api/docs/), которые необходимо сохранить в файле `.env` каталоге проекта.

```
DVMN_TOKEN=<токен API Devman>  
TG_CLIENTS_TOKEN=<токен бота>
```

# Использование

- задайте переменные окружения (см. выше)
- запустите скрпит `python bot.py <chat_id>`
  - chat_id - ID вашего чата с ботом
    - как узнать chat_id читайте здесь: [Как узнать свой ID в Telegram Bot и получить адрес канала: get chat user и где посмотреть группу](https://stelegram.ru/ispolzovanie/kak-uznat-id-chata-polzovatelya-i-kanala)

Если запуск прошел успешно бот перейдет в режим "прослушивания" [API DevMan](https://dvmn.org/api/docs) в режиме long-polling. В случае, если работа будет проверена в ваш чат c ботом придет соответствующее сообщение.