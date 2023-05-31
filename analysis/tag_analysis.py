import collections
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud


class TagAnalysis:
    def __init__(self, file_path, save_path="figures"):
        self.data = pd.read_csv(file_path, parse_dates=["date"])
        self.data["tags"] = self.data["tags"].apply(eval)
        self.data = self.data.dropna(subset=["date"])
        self.data[["year", "month", "day"]] = (
            self.data["date"].dt.strftime("%Y-%m-%d").str.split("-", expand=True)
        )
        self.save_path = save_path

    def count_tag_frequency(self, min_count):
        """
        统计每个tag的数量, 并返回一个Counter对象, 仅统计选择量>=min_count的tag
        """
        tag_counts = collections.Counter(
            tag
            for tags in self.data["tags"]
            for tag, count in tags.items()
            if count >= min_count
        )
        return tag_counts

    def plot_tag_counts(self, tag_counts, top_n):
        """
        使用竖向柱状图降序展示前top_n个tag的数量
        """
        most_common = dict(tag_counts.most_common(top_n))
        plt.barh(
            list(most_common.keys()),
            list(most_common.values()),
            color="steelblue",
            alpha=0.8,
        )
        plt.title("tag数量统计")
        plt.xlabel("数量")
        plt.ylabel("tag")
        plt.savefig(os.path.join(self.save_path, "tag_counts.png"))
        plt.clf()

    def generate_wordcloud(self, tag_counts):
        """
        使用词云图展示tag的词频
        """
        wordcloud = WordCloud(
            background_color="white",
            max_words=1000,
            font_path="msyh.ttc",
            width=3840,
            height=2160,
            max_font_size=800,
        ).generate_from_frequencies(tag_counts)
        wordcloud.to_file(os.path.join(self.save_path, "tag_wordcloud.png"))

    def count_tag_year_frequency(self, min_count=100, top_n=30):
        """
        计算不同年份和不同tag之间的关系, 并返回一个DataFrame对象
        """
        tag_year_counts = (
            pd.json_normalize(self.data["tags"])
            .fillna(0)
            .astype(int)
            .assign(year=self.data["year"])
            .groupby("year")
            .sum()
            .T.loc[lambda df: df.sum(axis=1) > min_count]
            .nlargest(top_n, columns="2020")
        )
        return tag_year_counts

    def plot_tag_year_counts_heatmap(self, tag_year_counts):
        """
        使用热力图展示不同年份和不同tag之间的关系
        """
        sns.heatmap(tag_year_counts, cmap="Blues", vmax=500)
        plt.xlabel("年份")
        plt.ylabel("tag")
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(self.save_path, "tag_year_counts_heatmap.png"))
        plt.clf()


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
            "figure.autolayout": True,
        }
    )
    tag_analysis = TagAnalysis("data/music_infos.csv")

    tag_counts = tag_analysis.count_tag_frequency(10)
    tag_analysis.plot_tag_counts(tag_counts, 20)

    tag_analysis.generate_wordcloud(tag_counts)

    tag_year_counts = tag_analysis.count_tag_year_frequency(100, 30)
    tag_analysis.plot_tag_year_counts_heatmap(tag_year_counts)
