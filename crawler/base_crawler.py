import concurrent.futures
import random
import time

import requests


class BaseCrawler:
    def __init__(self, headers=None):
        """
        初始化BaseCrawler对象

        Args:
            headers (dict, optional): 请求头. Defaults to None.
        """
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
        }

    def fetch_data(self, urls):
        """
        获取数据

        Args:
            urls (list): 包含URL的列表

        Returns:
            list: 包含数据的列表
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [
                executor.submit(
                    requests_handler, "GET", url, headers=self.headers, timeout=8
                )
                for url in urls
            ]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]
        return results


def requests_handler(method, url, **kwargs):
    """
    请求处理函数
    
    Args:
        method (str): 请求方法
        url (str): 请求URL
        **kwargs: 其他参数
        
    Returns:
        str: 包含请求结果的字符串
    """
    for i in range(3):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            print(f"请求{url}成功")
            return response.text
        except requests.exceptions.RequestException as e:
            if (
                isinstance(e, requests.exceptions.HTTPError)
                and e.response.status_code == 404
            ):
                raise e
            print(f"请求{url}失败，正在重试第{i + 1}次: {e}")
            time.sleep(2 + random.uniform(0, 2))
    else:
        print(f"请求{url}失败，已重试3次，放弃请求")
        save_failed_urls(url)
        return None


def save_failed_urls(url):
    """
    将请求失败的URL保存到文件中
    
    Args:
        url (str): 请求失败的URL
    """
    with open("failed_urls.txt", "a", encoding="utf-8") as f:
        f.write(url + "\n")
