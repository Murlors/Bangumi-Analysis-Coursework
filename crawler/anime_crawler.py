import json
import os

import pandas as pd

from .base_crawler import BaseCrawler


class AnimeCrawler(BaseCrawler):
    def __init__(self, data_path, headers=None):
        """
        初始化AnimeCrawler对象

        Args:
            data_path (str): 数据保存路径
            headers (dict, optional): 请求头. Defaults to None.
        """
        self.data_path = data_path
        self.api = "https://api.bgm.tv/v0/subjects/{}"
        super().__init__(headers=headers)

    def save_anime_info(self, anime_infos):
        """
        将动画信息保存到CSV文件中

        Args:
            anime_infos (list): 包含动画信息的列表
        """
        file_name = os.path.join(self.data_path, "anime_infos.csv")
        anime_infos_df = pd.DataFrame(anime_infos)
        anime_infos_df.to_csv(file_name, index=False)

    def get_anime_info(self, subject_codes):
        """
        获取动画信息

        Args:
            subject_codes (list): 包含动画条目代码的列表

        Returns:
            list[dict]: 包含多个动画信息字典的列表，动画信息如：
            id, type, name, name_cn, summary, nsfw, locked, platform, images[large,common,medium,small,grid](cover),
            infobox, volumes, eps, total_episodes, rating(rank, total, count, score),
            collection(on_hold, dropped, wish, collect, doing), tags(name:count).
        """
        anime_infos = []
        truncate = 50
        for i in range(0, len(subject_codes), truncate):
            api = [
                self.api.format(subject_code)
                for subject_code in subject_codes[i : i + truncate]
            ]
            json_datas = super().fetch_data(api)
            self.process_anime_info(anime_infos, json_datas)
            print(f"已获取{len(anime_infos)}条动画信息")
            self.save_anime_info(anime_infos)
        return anime_infos

    def process_anime_info(self, anime_infos, json_datas):
        """
        处理动画信息

        Args:
            anime_infos (list): 包含动画信息的列表
            json_datas (list): 包含动画信息的JSON数据
        """
        for json_data in json_datas:
            anime_info = json.loads(json_data)

            # pop unwanted keys
            # for unwanted_key in ['nsfw', 'locked', ]:
            #     anime_info.pop(unwanted_key)
            # unpack images dict
            images = {
                f"{size}_cover": url for size, url in anime_info["images"].items()
            }
            anime_info.pop("images")
            anime_info.update(images)
            # unpack infobox dict
            anime_info["tags"] = {
                tag["name"]: tag["count"] for tag in anime_info["tags"]
            }

            infobox = {item["key"]: item["value"] for item in anime_info["infobox"]}
            anime_info.pop("infobox")
            anime_info.update(infobox)
            # unpack rating dict
            rank = anime_info["rating"]["rank"]
            votes = anime_info["rating"]["total"]
            ratings = anime_info["rating"]["count"]
            rating_score = (
                sum([int(rating) * count for rating, count in ratings.items()]) / votes
            )
            anime_info.pop("rating")
            anime_info["rank"] = rank
            anime_info["votes"] = votes
            anime_info["ratings"] = ratings
            anime_info["rating_score"] = rating_score

            anime_infos.append(anime_info)


if __name__ == "__main__":
    headers = {
        "User-Agent": "murlors/bangumi-analysis-coursework (https://github.com/murlors/Bangumi-Analysis-Coursework)"
    }
    anime_crawler = AnimeCrawler("data", headers)
    anime_info = anime_crawler.get_anime_info(["68812", "13677"])
