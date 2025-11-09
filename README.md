# Подготовка к запуску проекта

## Клонирование репозитория
git clone https://github.com/sashkevski/esoft-test

cd ESOFT-test

## Создание виртуального окружения
python -m venv .venv

source .venv/bin/activate  # Linux/Mac

.venv\Scripts\activate  # Windows

## Установка зависимостей
pip install -r requirements.txt

## Добавление пути в PYTHONPATH

setx PYTHONPATH "%PYTHONPATH%;<путь>"

где <путь> - путь до директории расположения проекта

# Сценарии работы

NOTE: для дополнительной информации используйте python main.py -h

## Основная стратегия
python main.py strategy main

## Стратегия парсинга
python main.py strategy parse

## Очистка логов
python main.py clean

NOTE: Если скрипт не запускается с ошибкой "ModuleNotFoundError", попробуйте ввести следующие команды:

$env:PYTHONPATH=$pwd # Windows

export PYTHONPATH=$(pwd) # Linux

# Запуск тестов

## Запуск всех тестов
python -m pytest /tests
## Запуск unit-тестов
python -m pytest /tests/unit
## Запуск интеграционных тестов
python -m pytest /tests/integrations
## Запуск end-to-end тестов
python -m pytest /tests/e2e