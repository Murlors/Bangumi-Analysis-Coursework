import requests


class BaseCrawler:
    def __init__(self, headers=None):
        if headers:
            self.headers = headers
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
            }

    def fetch_data(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
