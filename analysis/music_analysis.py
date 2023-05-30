import os

import matplotlib.pyplot as plt
import pandas as pd


class MusicAnalysis:
    def __init__(self, file_path, save_path="figures"):
        self.data = pd.read_csv(file_path, parse_dates=["date"])
        self.data = self.data.dropna(subset=["date"])
        self.data[["year", "month", "day"]] = (
            self.data["date"].dt.strftime("%Y-%m-%d").str.split("-", expand=True)
        )
        self.data["company"] = self.data["厂牌"]
        self.save_path = save_path

    def count_year_music(self):
        """
        计算排行榜中每年的音乐数量, 并返回一个Series对象
        """
        year_counts = self.data["year"].value_counts(sort=False).sort_index()
        return year_counts

    def plot_year_music_trend(self, year_counts):
        """
        使用折线图展示每年排行榜中的音乐数量
        """
        year_counts.plot(kind="line", color="steelblue", alpha=0.8)
        plt.xlabel("年份")
        plt.ylabel("优秀音乐数量")
        plt.title("每年优秀音乐数量趋势")
        plt.savefig(os.path.join(self.save_path, "year_music_trend.png"))
        plt.clf()

    def count_company_music(self):
        """
        计算排行榜中每公司的音乐数量, 并返回一个Series对象
        """
        company_counts = self.data["company"].value_counts()
        return company_counts

    def pie_company_music(self, company_counts):
        """
        使用饼图展示每公司的音乐数量
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
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_path, "company_music_pie.png"))
        plt.clf()


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
        }
    )
    music_analysis = MusicAnalysis("data/music_infos.csv")

    year_counts = music_analysis.count_year_music()
    music_analysis.plot_year_music_trend(year_counts)

    company_counts = music_analysis.count_company_music()
    music_analysis.pie_company_music(company_counts)
