# Bangumi Analysis

English | [简体中文](README.md)

This is a data analysis tool based on the Bangumi website that can help you analyze the development trends and popularity of ACG-related data.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/murlors/Bangumi-Analysis-Coursework.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

If you are using conda, you can install the dependencies using the following command:

```bash
conda env create -f environment.yml
```

## Usage

1. Run the crawler:

```bash
python crawler.py -cfg config.yml
```

2. Run the analysis:

```bash
python analysis.py -cfg config.yml
```

## Configuration

You can use the `config.yml` file to configure the parameters for the crawler and data analysis. Here is an example configuration file:

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

The `type` parameter specifies the type of crawler, which can be `anime`, `book`, `music`, `game`, or `real`.

In the `crawler` section, you can configure the parameters for the crawler. The `start` and `end` parameters specify the range of pages to crawl. The `user-agent` parameter specifies the User-Agent for the crawler.

In the `data` section, you can configure the path to save the data.
In the `figure` section, you can configure the path to save the figures and the matplotlib rcParams.

Please note that the `analysis.py` part of the tool requires the data crawled by `crawler.py`, so make sure you have run `crawler.py` before running `analysis.py`.

Since this project was originally designed to analyze music-related data, if you need to analyze other types of data, you will need to modify the code in `crawler.py` and `analysis.py` yourself.

## Contributing

If you find any issues or have any suggestions for improvement, please feel free to submit an issue or pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
