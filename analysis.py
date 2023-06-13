import argparse
import os

import yaml
from matplotlib import pyplot as plt

import analysis


def get_hparams():
    """
    获取命令行参数

    Returns:
        ArgumentParser: 命令行参数解析器
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", type=str, default="data", help="本地保存的信息路径")
    parser.add_argument(
        "-fig", "--figure", type=str, default="figures", help="本地保存的图片路径"
    )
    parser.add_argument("-t", "--type", type=str, default="anime", help="分析的数据类别")

    parser.add_argument("-cfg", "--config", type=str, help="配置文件路径")
    return parser


def get_config(config_path):
    """
    读取配置文件

    Args:
        config_path (str): 配置文件路径

    Returns:
        dict: 包含配置信息的字典
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def parse_args(parser):
    """
    解析命令行参数

    Args:
        parser (ArgumentParser): 命令行参数解析器

    Returns:
        Namespace: 包含命令行参数的命名空间
    """
    args = parser.parse_args()
    if args.config and os.path.exists(args.config):
        config = get_config(args.config)
        args.type = config["crawler"]["type"]
        args.path = config["data"]["path"]
        args.figure = config["figure"]["path"]
        args.rcParams = config["figure"]["rcParams"]
    else:
        args.rcParams = {
            "font.family": "Microsoft YaHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
            "figure.autolayout": True,
        }
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"路径{args.path}不存在")
    if not os.path.exists(args.figure):
        os.makedirs(args.figure)
    return args


def main():
    """
    主函数，用于数据分析
    """
    parser = get_hparams()
    args = parse_args(parser)
    plt.rcParams.update(args.rcParams)

    tag_analysis = analysis.TagAnalysis(
        args.type, os.path.join(args.path, f"{args.type}_infos.csv")
    )

    tag_counts = tag_analysis.count_tag_frequency(min_count=10)
    tag_analysis.plot_tag_counts(tag_counts, top_n=32)

    tag_analysis.generate_wordcloud(tag_counts)

    tag_year_counts = tag_analysis.count_tag_year_frequency(min_count=100, top_n=32)
    tag_analysis.plot_tag_year_counts_heatmap(tag_year_counts)

    if args.type == "music":
        music_analysis = analysis.MusicAnalysis(
            os.path.join(args.path, f"music_infos.csv")
        )
        year_counts = music_analysis.count_year_music()
        music_analysis.plot_year_music_trend(year_counts)

        company_counts = music_analysis.count_company_music()
        music_analysis.pie_company_music(company_counts)

        composer_counts = music_analysis.count_composer_frequency()
        music_analysis.plot_composer_counts(composer_counts, top_n=30)


if __name__ == "__main__":
    main()
