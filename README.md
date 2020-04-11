# HTTPserver
HTTP-сервер на чистом Python

## Описание

Сервис - конвертер валют, который обрабатывает запрос клиента для совершения обменных операций.
Асинхронный сервис корректно обрабатывает запрос, обращается к стороннему веб-ресурсу через API, и 
предоставляет информацию о результате обмена.

### Особенности:

* валидация запроса формату (Query-компоненту URI):

/currency?<из валюты>_<в валюту>=<сумма к обмену>
* вывод лога в консоль с кастомным форматированием

### Примеры работы:

Корректный GET-запрос

![f](https://github.com/Padking/HTTPserver/blob/master/screenshots/pass_get.jpg)

Некорректный GET-запрос

![s](https://github.com/Padking/HTTPserver/blob/master/screenshots/fail_get.jpg)

Некорректный GET-запрос (неверный код валюты)

![t](https://github.com/Padking/HTTPserver/blob/master/screenshots/fail_get_invalid_currency.jpg)

Лог

![fo](https://github.com/Padking/HTTPserver/blob/master/screenshots/log.jpg)

### Требования к окружению:

* Python 3.7+;
* Linux/Windows;

### Запуск:

1. Получить APIKEY на [сайте](https://www.currencyconverterapi.com),
2. Присвоить APIKEY одноимённой переменной в `server.py`,
3. `$ python server.py`,
4. Выполнить [запрос](http://127.0.0.1:8000/currency?usd_rub=10)
