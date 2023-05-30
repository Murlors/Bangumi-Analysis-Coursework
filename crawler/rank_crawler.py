import csv
import os

from bs4 import BeautifulSoup

from .base_crawler import BaseCrawler


class RankCrawler(BaseCrawler):
    def __init__(self, type, data_path, start_page, end_page, headers=None):
        assert type in ["anime", "book", "music", "game", "real"]
        self.type = type
        self.data_path = data_path
        self.start_page = start_page
        self.end_page = end_page
        self.url = f"https://bgm.tv/{self.type}/browser?sort=rank"
        super().__init__(headers=headers)

    def save_subject_codes(self, subject_codes):
        file_name = os.path.join(
            self.data_path,
            f"{self.type}_subject_codes_{self.start_page}_{self.end_page}.csv",
        )
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["subject_code"])
            writer.writerows([code] for code in subject_codes)

    def get_subject_codes(self):
        subject_codes = set()
        for page in range(self.start_page, self.end_page + 1):
            url = self.url + f"&page={page}"
            html = super().fetch_data(url)
            if html:
                soup = BeautifulSoup(html, "lxml")
                
                subjects = soup.select(".subjectCover")
                subject_codes.update(
                    (subject["href"].split("/")[-1] for subject in subjects)
                )
            else:
                break
        self.save_subject_codes(subject_codes)
        return subject_codes


if __name__ == "__main__":
    rank_crawler = RankCrawler("music", "data", 1, 2)
    subject_codes = rank_crawler.get_subject_codes()
