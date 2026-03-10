import requests
import pandas as pd
from datetime import datetime
import os

def update_data():
    # 1. 获取当前年份，默认补全 2024 年至今
    current_year = datetime.now().year
    
    # 获取补全数据的起始日期 (例如从本年初开始)
    start_date = f"{current_year}-01-01"
    url = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{start_date}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    print(f"正在从 CNN API 获取 {current_year} 年最新数据...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"获取数据失败: {e}")
        return

    new_data = data.get('fear_and_greed_historical', {}).get('data', [])
    if not new_data:
        print("未获取到新数据。")
        return

    # 2. 解析新数据
    df_new = pd.DataFrame(new_data)
    df_new['date'] = pd.to_datetime(df_new['x'], unit='ms').dt.date
    df_new.rename(columns={'y': 'fear_and_greed_index'}, inplace=True)
    df_new = df_new[['date', 'fear_and_greed_index']]

    # 3. 按年份拆分并更新本地文件
    df_new['year'] = pd.to_datetime(df_new['date']).dt.year
    years_to_update = df_new['year'].unique()

    for year in years_to_update:
        file_path = f"fear-greed-{year}.csv"
        df_year_new = df_new[df_new['year'] == year][['date', 'fear_and_greed_index']]
        
        if os.path.exists(file_path):
            # 读取现有文件
            df_old = pd.read_csv(file_path)
            df_old['date'] = pd.to_datetime(df_old['date']).dt.date
            
            # 合并去重
            df_combined = pd.concat([df_old, df_year_new], ignore_index=True)
            df_combined = df_combined.drop_duplicates(subset=['date'], keep='last')
            df_combined = df_combined.sort_values(by='date')
            
            df_combined.to_csv(file_path, index=False)
            print(f"已成功更新 {file_path} (共 {len(df_combined)} 条记录)")
        else:
            # 创建新年份文件
            df_year_new.to_csv(file_path, index=False)
            print(f"已成功创建新年份文件 {file_path}")

    print("\n所有数据更新完成！")

if __name__ == "__main__":
    # 切换到脚本所在目录执行，确保路径正确
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    update_data()
