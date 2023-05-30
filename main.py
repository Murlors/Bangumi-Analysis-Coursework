import argparse
import csv
import os

import yaml
from matplotlib import pyplot as plt

import analysis
import crawler


def get_hparams():
    parser = argparse.ArgumentParser()
    # use local saved info? (local path)
    parser.add_argument("-l", "--local", action="store_true", help="是否使用本地保存的信息")
    parser.add_argument("-p", "--path", type=str, help="本地保存的信息路径")
    parser.add_argument("-fig", "--figure", type=str, help="本地保存的图片路径")
    parser.add_argument("-t", "--type", type=str, help="爬取的条目类型")

    parser.add_argument(
        "-cfg", "--config", type=str, default="config.yml", help="配置文件路径"
    )

    parser.add_argument("-s", "--start", type=int, help="爬取的开始页数")
    parser.add_argument("-e", "--end", type=int, help="爬取的结束页数")
    parser.add_argument("-ua", "--user-agent", type=str, help="User-Agent")

    return parser


def get_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def parse_args(parser):
    args = parser.parse_args()
    if args.config and os.path.exists(args.config):
        config = get_config(args.config)
        args.type = config["crawler"]["type"]
        args.start = config["crawler"]["start"]
        args.end = config["crawler"]["end"]
        args.user_agent = config["crawler"]["user-agent"]
        args.path = config["data"]["path"]
        args.figure = config["figure"]["path"]
        args.rcParams = config["figure"]["rcParams"]
    else:
        args.type = "music"
        args.start = 1
        args.end = 1
        args.path = "data"
        args.figure = "figures"
        args.rcParams = {
            "font.family": "SimHei",
            "savefig.dpi": 300,
            "figure.figsize": [12, 8],
        }
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    if not os.path.exists(args.figure):
        os.makedirs(args.figure)
    return args


def main():
    parser = get_hparams()
    args = parse_args(parser)
    plt.rcParams.update(args.rcParams)

    if not args.local:
        # get music subject codes
        subject_codes_path = os.path.join(
            args.path, f"{args.type}_subject_codes_{args.start}_{args.end}.csv"
        )
        if not os.path.exists(subject_codes_path):
            rank_crawler = crawler.RankCrawler(
                args.type, args.path, args.start, args.end
            )
            subject_codes = rank_crawler.get_subject_codes()
        else:
            with open(subject_codes_path, "r") as f:
                # skip header
                csv_reader = csv.reader(f)
                next(csv_reader)
                subject_codes = [row[0] for row in csv_reader]

        # get music subject info
        headers = {"User-Agent": args.user_agent}
        music_crawler = crawler.MusicCrawler(args.path, headers)
        music_infos = music_crawler.get_music_info(subject_codes)

    tag_analysis = analysis.TagAnalysis(
        os.path.join(args.path, f"{args.type}_infos.csv")
    )

    tag_counts = tag_analysis.count_tag_frequency(min_count=10)
    tag_analysis.plot_tag_counts(tag_counts, top_n=30)

    tag_analysis.generate_wordcloud(tag_counts)

    tag_year_counts = tag_analysis.count_tag_year_frequency(min_count=100, top_n=30)
    tag_analysis.plot_tag_year_counts_heatmap(tag_year_counts)

    if args.type == "music":
        music_analysis = analysis.MusicAnalysis(
            os.path.join(args.path, f"music_infos.csv")
        )
        year_counts = music_analysis.count_year_music()
        music_analysis.plot_year_music_trend(year_counts)


if __name__ == "__main__":
    main()
