import os

import matplotlib.pyplot as plt
import pandas as pd


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
        year_counts.plot(kind="line", color="steelblue", alpha=0.8)
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

        company_counts.plot(kind="pie", autopct="%1.1f%%")
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
        plt.barh(
            most_common.index,
            most_common.values,
            color="steelblue",
            alpha=0.8,
        )
        plt.title("作曲家数量统计")
        plt.xlabel("数量")
        plt.ylabel("作曲家")
        plt.savefig(os.path.join(self.save_path, "composer_counts.png"))
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
    music_analysis = MusicAnalysis("data/music_infos.csv")

    year_counts = music_analysis.count_year_music()
    music_analysis.plot_year_music_trend(year_counts)

    company_counts = music_analysis.count_company_music()
    music_analysis.pie_company_music(company_counts)

    composer_counts = music_analysis.count_composer_frequency()
    music_analysis.plot_composer_counts(composer_counts, top_n=30)
