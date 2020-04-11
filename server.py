import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from utils import construct_url, get_rate, parse_string


APIKEY = "f5c4f3ea68441c75bdd1"
BASE_URL = "https://free.currconv.com/api/v7/convert"
hostname = "127.0.0.1"
port = 8000
server_address = hostname, port


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        path_part_URI = self.path
        print(path_part_URI)
        if path_part_URI == "/favicon.ico":
            print("Отработан запрос к серверу favicon")
            print()
        else:
            try:
                from_currency, to_currency, ante = parse_string(path_part_URI)
            except:  # любые ошибки вызова .parse_string
                print()
                print("Ошибка парсинга Query-компонента URI")
                report = {
                        "response code": "0",
                        "error": "URI parsing error"
                    }
            else:
                absolute_URL = construct_url(BASE_URL, APIKEY, from_currency, (
                                                                to_currency))
                print()
                print(f"Приложение запрашивает ресурс: \n{absolute_URL}")
                rate = get_rate(absolute_URL, from_currency, to_currency)
                if isinstance(rate, float):
                    total = ante*rate
                    report = {
                        "response code": "200",
                        "currency exchange": f"{from_currency} to {to_currency}",
                        "requested value": f"{ante}",
                        "rate": f"{rate}",
                        "exchange result": f"{total:.2f}",
                        "error": ""
                    }
                else:  # возникла ошибка при запросе к API обмена валют
                    code = rate[0]
                    text = rate[1]
                    report = {
                        "response code": f"{code}",
                        "error": f"{text}"
                    }
            finally:  # при любых ошибках отправляет ответ пользователю
                print()
                print("Результат запроса ресурса:")
                response = json.dumps(report, ensure_ascii=False).encode("utf-8")
                print(response.decode())
                print()
                self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(server_address, Server)
    print()
    print(f"Сервер запущен http://{hostname}:{port}")
    server.serve_forever()
