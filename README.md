# CNN Fear & Greed Index 历史数据集

本仓库包含了 CNN 恐惧与贪婪指数（Fear & Greed Index）自 2011 年至今的每日历史数据。数据按年份拆分存储，方便检索和分析。

## 📂 目录结构
- `fear-greed-YYYY.csv`: 对应年份的每日数据（包含 `date` 和 `fear_and_greed_index` 两列）。
- `update_fng.py`: 自动更新脚本，用于获取最新数据并同步到对应的 CSV 文件中。

## 📊 数据来源
1. **历史数据 (2011-2023)**: 整合自 GitHub 开源项目 [whit3rabbit/fear-greed-data](https://github.com/whit3rabbit/fear-greed-data)。
2. **实时数据 (2024至今)**: 通过 CNN 官方数据接口实时抓取：
   `https://production.dataviz.cnn.io/index/fearandgreed/graphdata/YYYY-MM-DD`

## 🚀 如何更新数据
项目提供了一个 Python 脚本，可以自动识别当前日期并补全缺失的数据。

### 前提条件
确保已安装 Python 3 以及必要的库：
```bash
pip install requests pandas
```

### 执行更新
在终端中运行以下命令：
```bash
python3 update_fng.py
```
脚本会自动执行以下操作：
1. 获取当前年份及最近的指数数据。
2. 读取本地对应的 `fear-greed-YYYY.csv` 文件。
3. 将新获取的数据与本地数据合并、去重并按日期排序。
4. 如果进入了新的一年，脚本会自动创建新的年份文件。

## 🛠 注意事项
- CNN 的 API 具有一定的反爬机制，脚本已内置 `User-Agent` 模拟真实浏览器访问。
- 建议每周或每月运行一次脚本以保持数据最新。
