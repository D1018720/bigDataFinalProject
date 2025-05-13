# 消費者物價指數與薪資關係分析

## 專案概述
本專案旨在分析台灣民國103年至113年間消費者物價指數(CPI)與工業及服務業薪資的關係，並計算實質薪資增長率，進而探討通貨膨脹對民眾實質收入的影響。

## 數據來源
- 消費者物價指數銜接表:[消費者物價指數及其年增率](https://www.stat.gov.tw/cp.aspx?n=2665)
- 薪情平臺匯出資料:[薪資平台查詢系統](https://earnings.dgbas.gov.tw/query_payroll.aspx)

## 分析方法
1. **數據處理**：
   - 篩選民國103年至113年的CPI資料
   - 處理薪情平臺原始數據，提取工業及服務業薪資
   - 將兩組數據進行整合

2. **指標計算**：
   - CPI年增長率
   - 薪資名義增長率
   - 實質薪資增長率（薪資名義增長率減去CPI年增長率）

3. **視覺化分析**：
   - CPI與薪資趨勢對比圖
   - CPI與薪資年增長率比較
   - 實質薪資增長率柱狀圖

## 分析結果
透過視覺化圖表呈現了以下結果：

1. **CPI與薪資趨勢比較**：
   - 展示民國103至113年間CPI與工業及服務業薪資的變化趨勢
   - 分析兩者增長速度的關係

2. **增長率比較**：
   - 對比CPI與薪資的年增長率
   - 揭示通貨膨脹與薪資調整的關係

3. **實質薪資增長**：
   - 計算並視覺化實質薪資增長率
   - 評估通膨環境下的實際薪資購買力變化

## 使用技術
- Python
- Pandas (數據處理)
- Matplotlib (數據視覺化)
- NumPy (數值計算)

## 圖表輸出
本專案生成了三張高解析度圖表：
1. CPI_vs_Salary.png  ![消費者物價指數與工業及服務業薪資比較](https://github.com/D1018720/bigDataFinalProject/blob/main/CPI_vs_Salary.png)
2. Growth_Rate_Comparison.png  ![消費者物價指數與薪資年增長率比較](https://github.com/D1018720/bigDataFinalProject/blob/main/Growth_Rate_Comparison.png)
3. Real_Salary_Growth.png  ![工業及服務業實質薪資增長率](https://github.com/D1018720/bigDataFinalProject/blob/main/Real_Salary_Growth.png)

## 結論
通過分析消費者物價指數與薪資數據，我們可以更清楚地了解通貨膨脹對台灣勞工實質薪資的影響，為相關政策制定提供參考依據。
