import concurrent.futures
import random
import time

import requests

failed_urls = []


class BaseCrawler:
    def __init__(self, headers=None):
        if headers:
            self.headers = headers
        else:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"
            }

    def fetch_data(self, urls):
        results = []
        with concurrent.futures.ThreadPoolExecutor(8) as executor:
            # 提交每个URL的抓取任务到线程池中
            futures = [
                executor.submit(
                    requests_handler, "GET", url, headers=self.headers, timeout=8
                )
                for url in urls
            ]
            # 获取已完成的任务，并将结果保存到列表中
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        return results


def requests_handler(method, url, **kwargs):
    for i in range(3):
        try:
            if method == "GET":
                response = requests.get(url, **kwargs)
            elif method == "POST":
                response = requests.post(url, **kwargs)
            else:
                raise Exception("requests_handler()方法的method参数只能为GET或POST")
            if response.status_code == 200:
                print(f"请求{url}成功")
                return response.text
            else:
                raise Exception(f"请求{url}失败，状态码为{response.status_code}")
        except Exception as e:
            if "404" in str(e):
                raise e
            print(f"请求{url}失败，正在重试第{i + 1}次: {e}")
            time.sleep(2 + random.uniform(0, 2))

    global failed_urls
    failed_urls.append(url)
    print(f"failed_urls: {failed_urls}")
