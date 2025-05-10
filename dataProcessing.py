import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 檔案路徑
cpi_file_path = "c:/Users/user/OneDrive/Desktop/大數據期末/消費者物價指數銜接表.csv"
salary_file_path = "c:/Users/user/OneDrive/Desktop/大數據期末/薪情平臺匯出資料.csv"

# --- 處理消費者物價指數資料 ---
# 讀取CSV檔案
df_cpi = pd.read_csv(cpi_file_path, encoding="utf-8", header=1, nrows=66)

# 將民國年轉換為數值類型
df_cpi["民國年"] = pd.to_numeric(df_cpi["民國年"], errors="coerce")

# 篩選出民國103年到113年的資料
filtered_cpi_df = df_cpi[(df_cpi["民國年"] >= 103) & (df_cpi["民國年"] <= 113)]

# 只保留「民國年」和「累計平均」兩列
cpiResult = filtered_cpi_df[["民國年", "累計平均"]]

# 使用.loc進行賦值
cpiResult.loc[:, "累計平均"] = pd.to_numeric(cpiResult["累計平均"], errors="coerce")

# 重設索引，從0開始
cpiResult = cpiResult.reset_index(drop=True)

print("消費者物價指數資料：")
print(cpiResult)
print("\n")

# --- 處理薪情平臺資料 ---
# 讀取CSV檔案，但跳過第一列到第二列，header跳過前三行
df_raw = pd.read_csv(salary_file_path, encoding='utf-8', header=2, nrows=11, usecols=range(1, 3))

# 準備存放資料的列表
salary_data = []

# 遍歷每一行尋找資料
for i in range(len(df_raw)):
    row = df_raw.iloc[i]
    
    # 檢查第一欄是否包含年份（修正使用.iloc[]）
    first_col = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
    
    # 從第一欄找年份
    if "年" in first_col:
        try:
            year = int(first_col.replace("年", ""))
            
            # 只處理民國103年到113年
            if 103 <= year <= 113:
                # 提取工業及服務業薪資（第二欄）
                if pd.notna(row.iloc[1]):
                    salary_str = str(row.iloc[1])
                    if salary_str != "nan" and salary_str != "-":
                        industry_salary = int(salary_str.replace(",", "").replace('"', ''))
                        salary_data.append([year, industry_salary])
                        #print(f"找到年份: {year}, 工業及服務業薪資: {industry_salary}")
        except ValueError:
            pass

# 建立薪資資料DataFrame
salaryResult = pd.DataFrame(salary_data, columns=["民國年", "工業及服務業薪資"])

# 重設索引並排序
salaryResult = salaryResult.sort_values(by="民國年").reset_index(drop=True)

print("\n薪情平臺資料（工業及服務業薪資）：")
print(salaryResult)

# --- 計算增長率 ---
# 計算CPI年增長率
cpiResult['CPI年增長率'] = cpiResult['累計平均'].pct_change() * 100

# 計算薪資名義增長率
salaryResult['薪資名義增長率'] = salaryResult['工業及服務業薪資'].pct_change() * 100

# 合併兩個資料集
merged_df = pd.merge(
    cpiResult[['民國年', '累計平均', 'CPI年增長率']], 
    salaryResult[['民國年', '工業及服務業薪資', '薪資名義增長率']], 
    on='民國年'
)

# 計算實質薪資增長率
merged_df['實質薪資增長率'] = merged_df['薪資名義增長率'] - merged_df['CPI年增長率']

print("\n合併後的資料（含增長率）：")
print(merged_df)

# --- 繪製圖表 ---
# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 設定微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 圖表1：消費者物價指數與工業及服務業薪資比較
plt.figure(figsize=(12, 6))
fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = 'tab:blue'
ax1.set_xlabel('民國年')
ax1.set_ylabel('消費者物價指數', color=color1)
ax1.plot(merged_df['民國年'], merged_df['累計平均'], color=color1, marker='o', label='消費者物價指數')
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('工業及服務業薪資 (元)', color=color2)
ax2.plot(merged_df['民國年'], merged_df['工業及服務業薪資'], color=color2, marker='s', label='工業及服務業薪資')
ax2.tick_params(axis='y', labelcolor=color2)

# 設定X軸刻度
ax1.set_xticks(np.arange(103, 114, 1))

# 添加網格線
ax1.grid(True, linestyle='--', alpha=0.7)

# 添加標題
plt.title('民國103-113年消費者物價指數與工業及服務業薪資比較', fontsize=16)

# 添加圖例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# 優化佈局
fig.tight_layout()

# 顯示圖表1
plt.savefig('CPI_vs_Salary.png', dpi=300, bbox_inches='tight')
plt.show()

# 圖表2：增長率比較
plt.figure(figsize=(12, 6))

# 移除第一年（因為沒有增長率）
growth_df = merged_df.dropna()

plt.plot(growth_df['民國年'], growth_df['CPI年增長率'], marker='o', color='blue', label='消費者物價指數年增長率')
plt.plot(growth_df['民國年'], growth_df['薪資名義增長率'], marker='s', color='red', label='薪資名義增長率')

plt.grid(True, linestyle='--', alpha=0.7)
plt.title('民國104-113年消費者物價指數與工業及服務業薪資年增長率比較', fontsize=16)
plt.xlabel('民國年')
plt.ylabel('年增長率(%)')
plt.legend()
plt.xticks(growth_df['民國年'])

plt.tight_layout()
plt.savefig('Growth_Rate_Comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 圖表3：實質薪資增長率
plt.figure(figsize=(12, 6))

bars = plt.bar(growth_df['民國年'], growth_df['實質薪資增長率'], color='green', alpha=0.7)

# 在每個柱子上方或下方加上數值標籤
for bar in bars:
    height = bar.get_height()
    position = height / abs(height) * 0.5 if height != 0 else 0.5  # 根據正負值決定標籤位置
    va = 'bottom' if height >= 0 else 'top'
    plt.text(bar.get_x() + bar.get_width()/2, height + position, 
             f'{height:.2f}%', ha='center', va=va)

plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)  # 添加零線
plt.title('民國104-113年工業及服務業實質薪資增長率', fontsize=16)
plt.xlabel('民國年')
plt.ylabel('實質薪資增長率(%)')
plt.xticks(growth_df['民國年'])

plt.tight_layout()
plt.savefig('Real_Salary_Growth.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n分析完成，已生成三張圖表。")
