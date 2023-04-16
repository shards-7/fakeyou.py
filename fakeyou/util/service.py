from requests import Session, Response

from . import handle_response


class Service:
    def __init__(self, proxies: dict = None):
        self.api = "https://api.fakeyou.com{}".format
        self.__session = Session()
        self.__session.headers = {"accept": "application/json", "content-Type": "application/json"}
        self.proxies = proxies

    def clear_cookies(self):
        return self.__session.cookies.clear()

    def post(self, path: str, data: dict = None, params: dict = None, files: dict = None) -> Response:
        response = self.__session.post(
            self.api(path),
            json=data,
            params=params,
            proxies=self.proxies,
            files=files
        )
        return handle_response(response)

    def get(self, path: str, params: dict = None) -> Response:
        response = self.__session.get(
            self.api(path),
            params=params,
            proxies=self.proxies
        )
        return handle_response(response)

    def delete(self, path: str, params: dict = None) -> Response:
        response = self.__session.delete(
            self.api(path),
            params=params,
            proxies=self.proxies
        )
        return handle_response(response)
