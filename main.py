import argparse

import yaml

import crawler


def get_hparams():
    parser = argparse.ArgumentParser()
    # use local saved info? (local path)
    parser.add_argument('-l', '--local', action='store_true', help='是否使用本地保存的信息')
    parser.add_argument('-p', '--path', type=str, default='./data', help='本地保存的信息路径')

    parser.add_argument('-cfg', '--config', type=str, help='配置文件路径')

    parser.add_argument('-t', '--type', type=str, help='爬取的条目类型')
    parser.add_argument('-s', '--start', type=int, help='爬取的开始页数')
    parser.add_argument('-e', '--end', type=int, help='爬取的结束页数')
    parser.add_argument('-ua', '--user-agent', type=str, help='User-Agent')

    return parser


def get_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def parse_args(parser):
    args = parser.parse_args()
    if args.config:
        config = get_config(args.config)
        args.type = config['crawler']['type']
        args.start = config['crawler']['start']
        args.end = config['crawler']['end']
        args.user_agent = config['crawler']['user_agent']
        args.path = config['data']['path']
    return args


def main():
    parser = get_hparams()
    args = parse_args(parser)

    if args.local:
        # use local saved info
        pass
    else:
        # get music subject codes
        rank_crawler = crawler.RankCrawler(args.type, args.path, args.start, args.end)
        subject_codes = rank_crawler.get_subject_codes()
        # get music subject info
        headers = {
            'User-Agent': args.user_agent
        }
        music_crawler = crawler.MusicCrawler(args.path, headers)
        music_infos = music_crawler.get_music_info(subject_codes)
