#server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os


hostName = "localhost"
serverPort = 8080
ROOT_DIR = "."   # Папка с HTML‑файлами (где лежит server.py).


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        # Путь html страницы.
        url_path = urlparse(self.path).path

        # index.html -> главная и т.д.
        if url_path in ["/", "/index.html"]:
            filename = "index.html"
        elif url_path == "/catalog.html":
            filename = "catalog.html"
        elif url_path == "/category.html":
            filename = "category.html"
        elif url_path == "/contacts.html":
            filename = "contacts.html"
        else:
            # Любые другие пути 404 ошибка.
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
            return

        # Полный путь к файлу.
        filepath = os.path.join(ROOT_DIR, filename)

        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
            return

        # Читаем файл.
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Отдаём браузеру инфу.
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер стартовал, и доступен по адресу http://{hostName} порт:{serverPort} слушает запросы.")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер ОСТАНОВЛЕН.")
