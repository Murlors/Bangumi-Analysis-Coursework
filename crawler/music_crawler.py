import json
import os

import pandas as pd

from .base_crawler import BaseCrawler


class MusicCrawler(BaseCrawler):
    def __init__(self, data_path, headers=None):
        self.data_path = data_path
        self.api = "https://api.bgm.tv/v0/subjects/{}"
        super().__init__(headers=headers)

    # def get_music_info(self):
    #     url = f'https://bgm.tv/subject/{subject_code}/'
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

    def save_music_info(self, music_infos):
        file_name = os.path.join(self.data_path, "music_infos.csv")
        music_infos_df = pd.DataFrame(music_infos)
        music_infos_df.to_csv(file_name, index=False)

    def get_music_info(self, subject_codes):
        """
        :param subject_codes: list of subject_code
        :return: a dict of music info containing:
        id, type, name, name_cn, summary, nsfw, locked, platform, images[large,common,medium,small,grid](cover),
        infobox, volumes, eps, total_episodes, rating(rank, total, count, score),
        collection(on_hold, dropped, wish, collect, doing), tags(name:count).
        """
        music_infos = []
        truncate = 50
        # 每次截取50个subject_code
        for i in range(0, len(subject_codes), truncate):
            api = [
                self.api.format(subject_code)
                for subject_code in subject_codes[i : i + truncate]
            ]
            json_datas = super().fetch_data(api)
            self.process_music_info(music_infos, json_datas)
            print(f"已获取{len(music_infos)}条音乐信息")
            self.save_music_info(music_infos)
        return music_infos

    def process_music_info(self, music_infos, json_datas):
        for json_data in json_datas:
            music_info = json.loads(json_data)

            # pop unwanted keys
            # for unwanted_key in ['nsfw', 'locked', ]:
            #     music_info.pop(unwanted_key)
            # unpack images dict
            images = {
                f"{size}_cover": url for size, url in music_info["images"].items()
            }
            music_info.pop("images")
            music_info.update(images)
            # unpack infobox dict
            music_info["tags"] = {
                tag["name"]: tag["count"] for tag in music_info["tags"]
            }

            infobox = {item["key"]: item["value"] for item in music_info["infobox"]}
            music_info.pop("infobox")
            music_info.update(infobox)
            # unpack rating dict
            rank = music_info["rating"]["rank"]
            votes = music_info["rating"]["total"]
            ratings = music_info["rating"]["count"]
            rating_score = (
                sum([int(rating) * count for rating, count in ratings.items()]) / votes
            )
            music_info.pop("rating")
            music_info["rank"] = rank
            music_info["votes"] = votes
            music_info["ratings"] = ratings
            music_info["rating_score"] = rating_score

            music_infos.append(music_info)


if __name__ == "__main__":
    headers = {
        "User-Agent": "murlors/bangumi-analysis-coursework (https://github.com/murlors/Bangumi-Analysis-Coursework)"
    }
    music_crawler = MusicCrawler("data", headers)
    music_info = music_crawler.get_music_info(["163164", "238923"])
