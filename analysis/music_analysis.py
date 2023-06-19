import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class MusicAnalysis:
    def __init__(self, file_path, save_path="figures"):
        """
        初始化函数

        Args:
            file_path (str): 数据文件路径
            save_path (str, optional): 图片保存路径. Defaults to "figures".
        """
        self.data = pd.read_csv(file_path, parse_dates=["date"])
        self.data = self.data.dropna(subset=["date"])
        self.data[["year", "month", "day"]] = (
            self.data["date"].dt.strftime("%Y-%m-%d").str.split("-", expand=True)
        )
        self.data["company"] = self.data["厂牌"]
        self.data["composers"] = self.data["作曲"].str.replace("、", "|").str.split("|")
        self.save_path = save_path

    def count_year_music(self):
        """
        计算每年优秀音乐数量

        Returns:
            pandas.Series: 包含每年优秀音乐数量的Series
        """
        year_counts = self.data["year"].value_counts(sort=False).sort_index()
        return year_counts

    def plot_year_music_trend(self, year_counts):
        """
        绘制每年优秀音乐数量趋势图

        Args:
            year_counts (pandas.Series): 包含每年优秀音乐数量的Series
        """
        sns.barplot(x=year_counts.index, y=year_counts.values)
        plt.xticks(rotation=45)
        plt.xlabel("年份")
        plt.ylabel("优秀音乐数量")
        plt.title("每年优秀音乐数量趋势")
        plt.savefig(os.path.join(self.save_path, "year_music_trend.png"))
        plt.clf()

    def count_company_music(self):
        """
        计算每个公司的优秀音乐数量

        Returns:
            pandas.Series: 包含每个公司优秀音乐数量的Series
        """
        company_counts = self.data["company"].value_counts()
        return company_counts

    def pie_company_music(self, company_counts):
        """
        绘制每个公司优秀音乐数量的饼图

        Args:
            company_counts (pandas.Series): 包含每个公司优秀音乐数量的Series
        """
        # 计算其他公司的音乐数量
        threshold = 0.01 * company_counts.sum()
        other_count = company_counts[company_counts < threshold].sum()

        # 选择需要展示的公司
        company_counts = company_counts[company_counts >= threshold]
        company_counts["其他"] = other_count

        plt.pie(
            company_counts.values,
            labels=company_counts.index,
            autopct="%1.1f%%",
            colors=sns.color_palette("pastel", len(company_counts)),
        )
        plt.title("每公司优秀音乐数量", pad=20)
        plt.xlabel("")
        plt.ylabel("")
        plt.axis("equal")
        plt.savefig(os.path.join(self.save_path, "company_music_pie.png"))
        plt.clf()

    def count_composer_frequency(self):
        """
        计算每个作曲家的出现次数

        Returns:
            pandas.Series: 包含每个作曲家出现次数的Series
        """
        composer_counts = self.data["composers"].explode().value_counts()
        return composer_counts

    def plot_composer_counts(self, composer_counts, top_n):
        """
        绘制作曲家数量统计图

        Args:
            composer_counts (pandas.Series): 包含每个作曲家出现次数的Series
            top_n (int): 统计出现次数最多的前n个作曲家
        """
        most_common = composer_counts.nlargest(top_n)
        sns.barplot(x=most_common.values, y=most_common.index)
        plt.title("作曲家数量统计")
        plt.xlabel("数量")
        plt.ylabel("作曲家")
        plt.savefig(os.path.join(self.save_path, "composer_music_counts.png"))
        plt.clf()

    def facet_composer_counts(self, layout):
        """
        绘制作曲家数量统计图

        Args:
            top_n (int): 统计出现次数最多的前n个作曲家
        """
        composer_year_data = (
            self.data[["composers", "year"]]
            .explode("composers")
            .dropna(subset=["composers"])
        )
        composer_year_counts = (
            composer_year_data.groupby(["composers", "year"])
            .size()
            .unstack(level=0, fill_value=0)
        )
        top_composers = (
            composer_year_counts.sum().nlargest(layout[0] * layout[1]).index.tolist()
        )
        composer_year_counts = composer_year_counts[top_composers]
        composer_year_counts.plot(
            subplots=True, layout=layout, sharex=True, sharey=True
        )
        plt.savefig(os.path.join(self.save_path, "composer_year_counts.png"))


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
            "figure.autolayout": True,
        }
    )
    music_analysis = MusicAnalysis("data/music_infos.csv")

    year_counts = music_analysis.count_year_music()
    music_analysis.plot_year_music_trend(year_counts)

    company_counts = music_analysis.count_company_music()
    music_analysis.pie_company_music(company_counts)

    composer_counts = music_analysis.count_composer_frequency()
    music_analysis.plot_composer_counts(composer_counts, top_n=32)

    music_analysis.facet_composer_counts((4, 4))
