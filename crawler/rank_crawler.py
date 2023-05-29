from bs4 import BeautifulSoup
from base_crawler import BaseCrawler
import csv


class RankCrawler(BaseCrawler):
    def __init__(self, type, max_page, headers=None):
        assert type in ['anime', 'book', 'music', 'game', 'real']
        self.type = type
        self.max_page = max_page
        self.url = f'https://bgm.tv/{self.type}/browser?sort=rank'
        super().__init__(headers=headers)

    def save_subject_codes(self, subject_codes):
        file_name = f'./data/{self.type}_subject_codes.csv'
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['subject_code'])
            writer.writerows([code] for code in subject_codes)

    def get_subject_codes(self):
        subject_codes = set()
        for page in range(1, self.max_page + 1):
            url = self.url + f'&page={page}'
            html = super().fetch_data(url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                # items = soup.select('.browserFull .item')
                # subject_codes = [item['id'].split('_')[-1] for item in items]
                subjects = soup.select('.subjectCover')
                subject_codes.update((subject['href'].split('/')[-1] for subject in subjects))
            else:
                break
        self.save_subject_codes(subject_codes)
        return subject_codes


if __name__ == '__main__':
    rank_crawler = RankCrawler('music', 2)
    subject_codes = rank_crawler.get_subject_codes()
