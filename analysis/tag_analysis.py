import collections
import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


class TagAnalysis:
    def __init__(self, file_path, save_path="figures"):
        self.data = pd.read_csv(file_path)
        self.data["tags"] = self.data["tags"].apply(eval)
        self.data["year"] = self.data["date"].apply(lambda x: int(x.split("-")[0]))
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
            max_words=500,
            font_path="msyh.ttc",
            width=1920,
            height=1080,
            max_font_size=500,
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
            .sort_values(by=self.data["year"].max(), ascending=False)
            .iloc[:top_n]
        )
        return tag_year_counts

    def plot_tag_year_counts_heatmap(self, tag_year_counts):
        """
        使用热力图展示不同年份和不同tag之间的关系
        """
        sns.heatmap(tag_year_counts, cmap="Blues", xticklabels=True)
        plt.xlabel("年份")
        plt.ylabel("tag")
        plt.savefig(os.path.join(self.save_path, "tag_year_counts_heatmap.png"))
        plt.clf()


if __name__ == "__main__":
    tag_analysis = TagAnalysis("data/music_infos.csv")

    tag_counts = tag_analysis.count_tag_frequency(10)
    tag_analysis.plot_tag_counts(tag_counts, 20)

    tag_analysis.generate_wordcloud(tag_counts)

    tag_year_counts = tag_analysis.count_tag_year_frequency(100, 30)
    tag_analysis.plot_tag_year_counts_heatmap(tag_year_counts)
