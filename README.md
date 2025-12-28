# Парсинг-бот для генерации кодов

### Виртуальное окружение
```bash
python -m venv your_venv_name

# Windows:
your_venv_name\Scripts\activate
# Linux/Mac:
source your_venv_name/bin/activate 
```

### Установка зависимостей
```bash
pip install flask selenium python-telegram-bot python-dotenv
```

### Установка chromedriver
#### Заходим на сайт (https://googlechromelabs.github.io/chrome-for-testing/#stable), скачиваем .zip архив и извлекаем из него .exe-файл. После скачивания, данный chromedriver.exe нужно положить в корень проекта
##### Если что-то идет не так, на Хабр есть более подробная инструкция по установке : https://habr.com/ru/companies/reksoft/articles/898386

### Настройка кредов в ENV файле
#### Создайте .env файл и, опираясь на .env.example, заполните его данными

### Запуск веб-сервиса (он будет доступен по адресу: http://localhost:5000)
```bash
python web_service.py
```

### Запуск веб-сервиса
```bash
python telegram_parser_bot.py
```

### Команды для бота
```bash
/start # Приветственное сообщение
/get_code # Получить сгенерированный код
```