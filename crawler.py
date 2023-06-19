import argparse
import csv
import os

import yaml

import crawler


def get_hparams():
    """
    获取命令行参数

    Returns:
        ArgumentParser: 命令行参数解析器
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--path", type=str, default="data", help="本地保存的信息路径")
    parser.add_argument("-t", "--type", type=str, default="music", help="爬取的条目类型")

    parser.add_argument("-cfg", "--config", type=str, help="配置文件路径")

    parser.add_argument("-s", "--start", type=int, default=1, help="爬取的开始页数")
    parser.add_argument("-e", "--end", type=int, default=50, help="爬取的结束页数")

    parser.add_argument("-ua", "--user-agent", type=str, help="User-Agent")
    parser.add_argument("-at", "--access-token", type=str, help="Access Token")
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
        args.start = config["crawler"]["start"]
        args.end = config["crawler"]["end"]
        args.user_agent = config["crawler"]["user-agent"]
        args.path = config["data"]["path"]
    if not os.path.exists(args.path):
        os.makedirs(args.path)
    return args


def main():
    """
    主函数，用于爬取数据
    """
    parser = get_hparams()
    args = parse_args(parser)

    subject_codes_path = os.path.join(
        args.path, f"{args.type}_subject_codes_{args.start}_{args.end}.csv"
    )
    if not os.path.exists(subject_codes_path):
        rank_crawler = crawler.RankCrawler(args.type, args.path, args.start, args.end)
        subject_codes = list(rank_crawler.get_subject_codes())
    else:
        with open(subject_codes_path, "r") as f:
            # skip header
            csv_reader = csv.reader(f)
            next(csv_reader)
            subject_codes = [row[0] for row in csv_reader]
    # get music subject info
    headers = {
        "User-Agent": args.user_agent,
        "Authorization": f"Bearer {args.access_token}",
    }

    if args.type == "music":
        music_crawler = crawler.MusicCrawler(args.path, headers)
        music_crawler.get_music_info(subject_codes)
    elif args.type == "anime":
        anime_crawler = crawler.AnimeCrawler(args.path, headers)
        anime_crawler.get_anime_info(subject_codes)


if __name__ == "__main__":
    main()
