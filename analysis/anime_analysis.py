import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class AnimeAnalysis:
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
        self.data["anime_product"] = (
            self.data["动画制作"]
            .str.replace("、", "|")
            .str.replace("&amp;", "|")
            .str.split("|")
        )
        self.save_path = save_path

    def count_year_anime(self):
        """
        计算每年优秀动画数量

        Returns:
            pandas.Series: 包含每年优秀动画数量的Series
        """
        year_counts = self.data["year"].value_counts(sort=False).sort_index()
        return year_counts

    def plot_year_anime_trend(self, year_counts):
        """
        绘制每年优秀动画数量趋势图

        Args:
            year_counts (pandas.Series): 包含每年优秀动画数量的Series
        """
        sns.barplot(x=year_counts.index, y=year_counts.values)
        plt.xticks(rotation=45)
        plt.xlabel("年份")
        plt.ylabel("优秀动画数量")
        plt.title("每年优秀动画数量趋势")
        plt.savefig(os.path.join(self.save_path, "year_anime_trend.png"))
        plt.clf()

    def count_company_anime(self):
        """
        计算每个公司的优秀动画数量

        Returns:
            pandas.Series: 包含每个公司优秀动画数量的Series
        """
        company_counts = self.data["anime_product"].value_counts()
        return company_counts

    def facet_company_anime(self, layout):
        """
        绘制每个公司优秀动画数量的饼图

        Args:
            company_counts (pandas.Series): 包含每个公司优秀动画数量的Series
        """
        company_year_data = (
            self.data[["anime_product", "year"]]
            .explode("anime_product")
            .dropna(subset=["anime_product"])
        )
        company_year_counts = (
            company_year_data.groupby(["anime_product", "year"])
            .size()
            .unstack(level=0, fill_value=0)
        )
        top_company = (
            company_year_counts.sum().nlargest(layout[0] * layout[1]).index.tolist()
        )
        company_year_counts = company_year_counts[top_company]
        company_year_counts.plot(
            subplots=True, layout=layout, sharex=True, sharey=True
        )
        plt.savefig(os.path.join(self.save_path, "company_year_anime.png"))

if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
            "figure.autolayout": True,
        }
    )
    anime_analysis = AnimeAnalysis("data/anime_infos.csv")

    year_counts = anime_analysis.count_year_anime()
    anime_analysis.plot_year_anime_trend(year_counts)

    company_counts = anime_analysis.count_company_anime()
    anime_analysis.facet_company_anime((4,4))
