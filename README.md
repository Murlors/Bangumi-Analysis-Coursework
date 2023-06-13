# Bangumi数据分析器

[English](README.en.md) | 简体中文

这是一个基于Bangumi网站的数据分析工具，可以帮助您分析ACG相关数据的发展趋势和流行程度。

## 安装

1. 克隆本仓库到本地：

```bash
git clone https://github.com/murlors/Bangumi-Analysis-Coursework.git
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

如果你使用的是conda，可以使用以下命令安装依赖：

```bash
conda env create -f environment.yml
```

## 使用

1. 运行爬虫：

```bash
python crawler.py -cfg config.yml
```

2. 运行分析器：

```bash
python analysis.py -cfg config.yml
```

## 配置文件

您可以使用`config.yml`文件来配置爬虫和数据分析的参数。以下是一个示例配置文件：

```yaml
# config.yml
type: music # anime, book, music, game, real

crawler:
  start: 1 # start page
  end: 50 # end page
  user-agent: your_name/bangumi-analysis (https://github.com/your_name/bangumi-analysis)
  access-token: # access token

data:
  path: 'data' # data path

figure:
  path: 'figures' # figure path
  rcParams: # matplotlib rcParams
    font.family: 'Microsoft YaHei' # font family
    savefig.dpi: 300 # dpi
    figure.figsize: [12, 8] # figure size
    figure.autolayout: True # auto layout
```

`type`参数指定了爬虫的类型，可以是`anime`、`book`、`music`、`game`或者`real`。
在`crawler`部分，您可以配置爬虫的参数。`start`和`end`参数指定了爬虫爬取的页面范围。`user-agent`参数指定了爬虫的User-Agent。
在`data`部分，您可以配置数据的保存路径。
在`figure`部分，您可以配置图像的保存路径和matplotlib的rcParams。

需要注意的是，`analysis.py`数据分析的部分需要使用`crawler.py`爬取的数据，因此请确保您已经运行了`crawler.py`再运行`analysis.py`。

由于本项目原本只用于分析音乐相关数据，若您需要分析其他类型的数据，您需要自行修改`crawler.py`和`analysis.py`中的代码。

## 贡献

如果您发现了任何问题或者有任何改进意见，请随时提交issue或者pull request。

## 许可证

本项目使用MIT许可证。详情请参阅LICENSE文件。
