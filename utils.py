import json
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def parse_string(query_string: str):
    """ Анализирует строку на наличие параметров для запроса к API обмена валют

    :param query_string: Query-компонент URI

    >>> parse_string("/currency?usd_rub=10")
    ('USD', 'RUB', 10)

    """

    payload = query_string.split("?")[1]
    currencies, ante = [item.upper() if "_" in item else int(item) for item in payload.split("=")]
    from_currency, to_currency = currencies.split("_")
    return from_currency, to_currency, ante


def construct_url(base: str, apikey: str, *args, data=None):
    """ Формирует URL к API обмена валют

    :param base: Scheme & Path-компоненты URI
    :param apikey: ключ доступа к API
    :param args: валютная пара
    :param data: значения параметров Query-компонента URI

    """

    data = data or {}
    pair = "{}_{}".format(*args)
    data["q"] = pair
    data["compact"] = "ultra"
    data["apiKey"] = apikey
    url_values = urlencode(data)
    full_url = f"{base}?{url_values}"
    return full_url


def get_rate(url: str, *args):
    """ Получает курс из JSON API обмена валют

    :param args: валютная пара

    """

    try:
        r = urlopen(url)
    except HTTPError as e:
        print(f"Сервер не смог выполнить запрос. \nКод ошибки: {e.code}")
        return e.code, str(e.reason)
    except URLError as e:
        print(f"Не удаётся связаться с сервером. \nПричина: {e.reason}")
        fail = str(e.reason)
        return 0, fail
    else:
        exchange_str = r.read().decode(r.info().get_param("charset") or (
                                                                "utf-8"))
        exchange_dict = json.loads(exchange_str)
        currency_pair = "{}_{}".format(*args)
        try:
            rate = exchange_dict[currency_pair]
            return rate
        except KeyError:  # при запросе введён неверный код валюты
            return 0, "Invalid currency code entered"


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
