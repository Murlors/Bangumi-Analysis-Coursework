import collections
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud


class TagAnalysis:
    def __init__(self, type, file_path, save_path="figures"):
        """
        初始化TagAnalysis对象

        Args:
            file_path (str): 数据文件路径
            save_path (str, optional): 图片保存路径. Defaults to "figures".
        """
        self.type = type
        self.data = pd.read_csv(file_path, parse_dates=["date"], low_memory=False)
        self.data["tags"] = self.data["tags"].apply(eval)
        self.data = self.data.dropna(subset=["date"])
        self.data[["year", "month", "day"]] = [
            (date.year, date.month, date.day) for date in self.data["date"]
        ]
        self.save_path = save_path

    def count_tag_frequency(self, min_count):
        """
        统计选择量>=min_count的tag数量

        Args:
            min_count (int): 最小选择量

        Returns:
            Counter: tag数量统计结果
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
        使用水平柱状图降序展示前top_n个tag的数量

        Args:
            tag_counts (Counter): tag数量统计结果
            top_n (int): 展示的tag数量
        """
        tag_counts_df = (
            pd.DataFrame(tag_counts.most_common(top_n * 2), columns=["tag", "count"])
            .loc[lambda df: ~df["tag"].str.match(r"\d{4}")]
            .head(top_n)
        )
        sns.barplot(x="count", y="tag", data=tag_counts_df)
        plt.title("tag数量统计")
        plt.xlabel("数量")
        plt.ylabel("tag")
        plt.savefig(os.path.join(self.save_path, f"tag_{self.type}_counts.png"))
        plt.clf()

    def generate_wordcloud(self, tag_counts):
        """
        使用词云展示tag的词频

        Args:
            tag_counts (Counter): tag数量统计结果
        """
        wordcloud = WordCloud(
            background_color="white",
            max_words=1000,
            # font_path="xiaolaisc-regular.ttf",
            font_path="msyh.ttc",
            width=3840,
            height=2160,
            max_font_size=500,
        ).generate_from_frequencies(tag_counts)
        wordcloud.to_file(
            os.path.join(self.save_path, f"tag_{self.type}_wordcloud.png")
        )

    def count_tag_year_frequency(self, min_count=100):
        """
        计算不同年份和不同tag之间的关系

        Args:
            min_count (int, optional): 最小选择量. Defaults to 100.

        Returns:
            DataFrame: 不同年份和不同tag之间的关系
        """
        tag_df = pd.json_normalize(self.data["tags"]).fillna(0).astype(int)
        tag_year_df = tag_df.groupby(self.data["year"]).sum()
        tag_counts = (
            tag_year_df.sum(axis=0)
            .loc[lambda s: s > min_count]
            .sort_values(ascending=False)
        )
        tag_year_counts_df = tag_year_df[tag_counts.index]
        return tag_year_counts_df

    def plot_tag_year_counts_heatmap(self, tag_year_counts_df, top_n=32):
        """
        使用热力图展示不同年份和不同tag之间的关系

        Args:
            tag_year_counts_df (DataFrame): 不同年份和不同tag之间的关系
            top_n (int, optional): 展示的tag数量. Defaults to 32.
        """
        plt.figure(figsize=(16, 8))
        sns.heatmap(tag_year_counts_df.T.head(top_n), cmap="Blues", vmax=10000)
        plt.xlabel("年份")
        plt.ylabel("tag")
        plt.xticks(rotation=45)
        plt.savefig(
            os.path.join(self.save_path, f"tag_year_counts_{self.type}_heatmap.png")
        )
        plt.clf()

    def wordcloud_subplots(self, tag_year_counts_df, layout):
        """
        使用词云展示不同年份和不同tag之间的关系

        Args:
            tag_year_counts_df (DataFrame): 不同年份和不同tag之间的关系
            layout (tuple): 子图布局
        """
        top_years = (
            tag_year_counts_df.sum(axis=1)
            .nlargest(layout[0] * layout[1])
            .sort_index()
            .index.tolist()
        )

        fig, axes = plt.subplots(
            nrows=layout[0],
            ncols=layout[1],
            figsize=(20, 20),
            dpi=300,
        )

        for i, ax in enumerate(axes.flat):
            if i < len(top_years):
                year = top_years[i]
                tag_counts = tag_year_counts_df.loc[year].nlargest(200)
                wordcloud = WordCloud(
                    background_color="white",
                    # max_words=1000,
                    # font_path="xiaolaisc-regular.ttf",
                    font_path="msyh.ttc",
                    width=1600,
                    height=1600,
                    max_font_size=400,
                ).generate_from_frequencies(tag_counts)
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.set_title(year, fontdict={"fontsize": 20})
                ax.axis("off")

        fig.suptitle(f"Top 9 Years with Most Tags", fontsize=30, y=0.99)

        plt.savefig(
            os.path.join(self.save_path, f"tag_year_counts_{self.type}_wordcloud.png")
        )


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
            "figure.autolayout": True,
        }
    )
    tag_analysis = TagAnalysis("anime", "data/anime_infos.csv")

    tag_counts = tag_analysis.count_tag_frequency(100)
    tag_analysis.plot_tag_counts(tag_counts, 32)

    tag_analysis.generate_wordcloud(tag_counts)

    tag_year_counts_df = tag_analysis.count_tag_year_frequency(100)
    tag_analysis.plot_tag_year_counts_heatmap(tag_year_counts_df, 32)

    tag_analysis.wordcloud_subplots(tag_year_counts_df, (3, 3))
