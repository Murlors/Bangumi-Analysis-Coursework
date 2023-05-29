from base_crawler import BaseCrawler
import json
import pandas as pd


class MusicCrawler(BaseCrawler):
    def __init__(self, headers=None):
        # url = f'https://bgm.tv/subject/{subject_code}/'
        self.api = 'https://api.bgm.tv/v0/subjects/{}'
        super().__init__(headers=headers)

    # def get_music_info(self):
    #     html = super().fetch_data()
    #     if html:
    #         soup = BeautifulSoup(html, 'lxml')
    #         info = {}
    #         info['title'] = soup.select_one('#headerSubject h1 span').text.strip()
    #         info['cover'] = soup.select_one('#bangumiInfo .infobox img')['src']
    #         info['rating'] = soup.select_one('#bangumiInfo .global_score .number').text.strip()
    #         info['rank'] = soup.select_one('#subjectPanel .global_score .rank').text.strip()
    #         info['tags'] = [tag.text.strip() for tag in soup.select('#subject_detail .subject_tag_section .inner a')]
    #         return info
    #     else:
    #         return None

    @staticmethod
    def save_music_info(music_infos):
        file_name = './data/music_infos.csv'
        df = pd.DataFrame(music_infos)
        df.to_csv(file_name, index=False)

    def get_music_info(self, subject_codes):
        """
        :param subject_codes: list of subject_code
        :return: a dict of music info containing:
        id, type, name, name_cn, summary, nsfw, locked, platform, images[large,common,medium,small,grid](cover),
        infobox, volumes, eps, total_episodes, rating(rank, total, count, score),
        collection(on_hold, dropped, wish, collect, doing), tags(name:count).
        """
        music_infos = []
        for subject_code in subject_codes:
            api = self.api.format(subject_code)
            json_data = super().fetch_data(api)
            if json_data:
                music_info = json.loads(json_data)

                # pop unwanted keys
                for unwanted_key in ['nsfw', 'locked', ]:
                    music_info.pop(unwanted_key)
                # unpack images dict
                images = {f'{size}_cover': url for size, url in music_info['images'].items()}
                music_info.pop('images')
                music_info.update(images)
                # unpack infobox dict
                music_info['tags'] = {tag['name']: tag['count'] for tag in music_info['tags']}

                infobox = {item['key']: item['value'] for item in music_info['infobox']}
                music_info.pop('infobox')
                music_info.update(infobox)
                # unpack rating dict
                rank = music_info['rating']['rank']
                votes = music_info['rating']['total']
                ratings = music_info['rating']['count']
                rating_score = sum([int(rating) * count for rating, count in ratings.items()]) / votes
                music_info.pop('rating')
                music_info['rank'] = rank
                music_info['votes'] = votes
                music_info['ratings'] = ratings
                music_info['rating_score'] = rating_score

                music_infos.append(music_info)
            else:
                break
        self.save_music_info(music_infos)
        return music_infos


if __name__ == '__main__':
    headers = {
        'User-Agent': 'murlors/bangumi-analysis-coursework (https://github.com/murlors/Bangumi-Analysis-Coursework)'
    }
    music_crawler = MusicCrawler(headers)
    music_info = music_crawler.get_music_info(['163164', '238923'])
