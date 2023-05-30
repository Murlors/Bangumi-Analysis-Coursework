import os

import pandas as pd
import matplotlib.pyplot as plt


class MusicAnalysis:
    def __init__(self, file_path, save_path="figures"):
        self.data = pd.read_csv(file_path)
        self.data["year"] = self.data["date"].apply(lambda x: int(x.split("-")[0]))
        self.save_path = save_path

    def count_year_music(self):
        """
        计算排行榜中每年的音乐数量, 并返回一个Series对象
        """
        year_counts = self.data["year"].value_counts().sort_index()
        return year_counts

    def plot_year_music_trend(self, year_counts):
        """
        使用折线图展示每年排行榜中的音乐数量
        """
        plt.plot(year_counts.index, year_counts.values)
        plt.xlabel("年份")
        plt.ylabel("优秀音乐数量")
        plt.title("每年优秀音乐数量趋势")
        plt.savefig(os.path.join(self.save_path, "year_music_trend.png"))


if __name__ == "__main__":
    music_analysis = MusicAnalysis("data/music_infos.csv")

    year_counts = music_analysis.count_year_music()
    music_analysis.plot_year_music_trend(year_counts)
