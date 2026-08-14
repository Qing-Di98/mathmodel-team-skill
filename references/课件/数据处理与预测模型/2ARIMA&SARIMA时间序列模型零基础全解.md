## 目录

- 第一部分：ARIMA模型（非周期性时序）
- 一、ARIMA核心定位与适用条件
- 二、核心概念：平稳性（ARIMA建模的前提）
- 三、ARIMA国赛标准完整解题步骤
- 一、截尾
- 二、拖尾
- 四、ARIMA参数选型口诀
- 五、ARIMA国赛满分论文话术
- 第二部分：SARIMA季节时序模型精讲（国赛高频提分点）
- 一、为什么需要SARIMA？（ARIMA的致命缺陷）
- 二、SARIMA核心定位与适用场景
- 三、SARIMA参数详解（SARIMA(p,d,q)(P,D,Q)m）
- 四、SARIMA标准化解题步骤
- 五、ARIMA与SARIMA终极选型对比
- 第三部分：国赛可直接运行完整代码（ARIMA+SARIMA）
- 一、ARIMA完整竞赛代码
- 二、SARIMA季节时序完整竞赛代码
- 第四部分：模型精度评价指标
- 一、三大核心评价指标
- 二、精度评价代码（可直接追加到原有代码末尾）
- 第五部分
- 第六部分：完整国赛真题分步解题演示

---

ARIMA&SARIMA时间序列模型零基础全解
在数模国赛中，时间序列预测分为两大场景：
1. 无明显季节周期、仅含趋势+随机波动 → 用 ARIMA
2. 有月度/季度/年度固定周期（如每年夏季客流高、每月销量周期性波动） → 用 SARIMA
## 第一部分：ARIMA模型（非周期性时序）
### 一、ARIMA核心定位与适用条件
1. 适用场景
大样本时序数据（样本量n≥20），存在长期上升/下降趋势、随机波动，无固定季节周期。
典型数据：逐年GDP、逐年产量、长期能耗变化、无季节波动的监测数据。
23年gdp
24年gdp
2. 模型核心组成（AR+I+MA）
ARIMA(p,d,q) 三个参数对应三步建模逻辑，缺一不可：
p（AR自回归阶数）：利用历史前p期的数据，预测当前数据，捕捉时序的滞后相关性
d（差分阶数）：核心步骤，将非平稳时序转化为平稳时序，消除整体趋势
q（MA移动平均阶数）：利用历史前q期的预测误差，修正当前预测，消除随机噪声
### 二、核心概念：平稳性（ARIMA建模的前提）
1. 平稳序列
数据均值、方差基本稳定，无明显上升/下降趋势、无固定周期，波动均匀。只有平稳序列，才能用AR、MA建模。
2. 非平稳序列
现实中99%的原始时序都是非平稳的，存在明显趋势，无法直接建模。
ARIMA的核心解题思路：通过d次差分，强制将非平稳转为平稳
3. 差分通俗理解
一次差分：后一期数据 - 前一期数据，消除整体趋势
例：原序列[10,13,16,19,22]（持续上涨，非平稳）
一次差分后：[3,3,3,3]（平稳无趋势）
原序列：([10, 13, 16, 19, 22]) 一共 5 个数字，差分后只剩 4 个结果：
第 2 个数 − 第 1 个数：(13 - 10 = 3)
第 3 个数 − 第 2 个数：(16 - 13 = 3)
第 4 个数 − 第 3 个数：(19 - 16 = 3)
第 5 个数 − 第 4 个数：(22 - 19 = 3)
把四个计算结果放在一起，得到一次差分序列：
([3, 3, 3, 3])
### 三、ARIMA国赛标准完整解题步骤
国赛大题固定7步流程，缺任意一步都会扣分，全程标准化：
步骤1：时序数据可视化与特征分析
绘制时序折线图，观察数据是否存在趋势、波动、周期，初步判定是否适配ARIMA模型。
步骤2：平稳性检验（ADF检验·必做）
通过ADF单位根检验判断序列是否平稳：
P值 < 0.05：序列平稳，无需差分（d=0）
P值 > 0.05：序列非平稳，需要差分处理
步骤3：确定最优差分阶数d
d=0：原始数据平稳
d=1：一次差分后平稳（国赛90%题目适用）
d=2：二次差分，仅用于剧烈波动、强趋势数据
原则：能用1次差分绝不使用2次，避免数据信息丢失
步骤4：确定最优p、q阶数
p、q无法随意乱设，国赛标准两种定参方法：ACF/PACF图像判参法（手写论文必用）、AIC/BIC信息准则择优法（代码实操必用）。
1. ACF/PACF图像判定规则
前提：序列已经差分平稳，再看图定p、q
AR(p)阶数（看PACF偏自相关图）：PACF图像在p阶后快速截尾（突然落入置信区间），即为最优p值 PACF1阶截尾 → p=1
PACF2阶截尾 → p=2
MA(q)阶数（看ACF自相关图）：ACF图像在q阶后快速截尾，即为最优q值 ACF1阶截尾 → q=1
ACF拖尾不截尾 → q=0
### 一、截尾
定义
ACF / PACF 图里：前面几阶柱子明显超出蓝色置信虚线（显著相关），到某一阶之后，后面所有柱子全部掉进虚线里面，不再显著，直接断掉，这就叫截尾。
举例子
PACF 图：1 阶柱子很高（显著），2、3、4… 全部贴在虚线内 → PACF 在 1 阶截尾 → p=1
ACF 图：2 阶柱子显著，3 阶之后全部不显著 → ACF 在 2 阶截尾 → q=2
### 二、拖尾
定义
ACF / PACF 图：柱子会慢慢变小，但一直有部分柱子时不时跑出置信虚线，不会彻底全部收进区间，拖很长一串，没有突然断掉的点，就是拖尾。
举例子
ACF 每 1、3、5 阶偶尔突出虚线，一直到 10 阶还有波动，没有一次性全部收进去 → ACF 拖尾
ARIMA 看图定参
PACF 截尾、ACF 拖尾 → 只用 AR (p)，q=0
ACF 截尾、PACF 拖尾 → 只用 MA (q)，p=0
ACF、PACF 全都拖尾 → ARIMA (p,d,q)，p、q 都等于 0
2. 四种经典平稳序列定参模板
PACF截尾、ACF拖尾 → AR(p)
ACF截尾、PACF拖尾 → MA(q)
ACF、PACF均拖尾 → ARIMA(p,q)
均无明显规律 → 直接用万能组合(1,1,1)
3. AIC/BIC信息准则择优（代码精准定参）
核心规则：AIC、BIC数值越小，模型拟合效果越好、泛化能力越强，遍历组合取最小值对应的p、q即为最优阶数，杜绝主观瞎选。
国赛遍历范围：p∈[0,1,2]，q∈[0,1,2]，少量组合遍历、效率极高。
4. 一些小窍门
时间紧张、图像模糊、遍历麻烦时，直接使用ARIMA(1,1,1)，适配绝大多数非周期时序考题，不会出错、不扣分。
通过ACF自相关图、PACF偏自相关图，或AIC、BIC信息准则（数值越小模型越优）筛选最优p、q。
国赛最优解：优先遍历(0,1)(1,0)(1,1)，ARIMA(1,1,1)适配绝大多数考题。
步骤5：构建并训练ARIMA模型
代入最优(p,d,q)参数，基于平稳序列训练模型，拟合历史数据。
步骤6：残差白噪声检验（国赛必写结题依据·补齐实操）
模型训练完成后，必须检验残差，是证明模型拟合充分、无信息残留的唯一结题依据，不写直接扣步骤分。
1. 检验原理
优质时序模型：有效规律被模型全部拟合，剩余残差为随机白噪声，无可用信息、无自相关性。
2. 判定标准（论文直接抄）
P值＞0.05：接受原假设，残差为白噪声 → 模型合格、拟合有效
P值＜0.05：拒绝原假设，残差存在有效信息 → 模型欠拟合，需重新调参
3. 结题话术
对模型拟合残差进行白噪声检验，结果显示残差无显著自相关性，符合白噪声特征，说明时序数据的趋势与波动规律已被模型充分挖掘，模型拟合效果可靠，可用于后续预测分析。
检验模型拟合后的残差是否为白噪声：
是白噪声：残差无有效信息，模型拟合充分、合格
非白噪声：模型未拟合完全，需要调整参数重新建模
步骤7：模型拟合+未来预测+结果分析
拟合历史数据验证精度，外推未来多期数据，结合实际场景分析预测结果。
### 四、ARIMA参数选型口诀
无周期、有趋势、大样本 → ARIMA
平稳数据 → d=0
普通趋势数据 → d=1、p=1、q=1
波动极小数据 → p=0、q=1
### 五、ARIMA国赛满分论文话术
本次时序数据样本量充足，存在明显长期趋势与随机波动，无固定季节性周期，传统线性回归无法消除时序自相关性，灰色预测仅适用于小样本贫信息场景，存在局限性。因此本文选取ARIMA时序预测模型，通过差分运算将非平稳时序平稳化，结合自回归与移动平均机制挖掘时序滞后关联规律，能够有效拟合含趋势、含随机波动的复杂时序变化，模型适配性良好。
## 第二部分：SARIMA季节时序模型精讲（国赛高频提分点）
### 一、为什么需要SARIMA？（ARIMA的致命缺陷）
ARIMA 无法捕捉季节性周期波动。
当数据出现：每年夏季峰值、每月固定波动、季度周期性变化时，ARIMA预测会严重失真，必须使用 SARIMA季节性差分自回归移动平均模型。
### 二、SARIMA核心定位与适用场景
适用：大样本时序（n≥20）+ 有固定季节/月度/季度周期 + 含趋势波动
典型国赛数据：月度销量、季度能耗、年度季节客流、气象时序数据
### 三、SARIMA参数详解（SARIMA(p,d,q)(P,D,Q)m）
在ARIMA基础上，新增季节参数体系，共7个参数：
1. 非季节参数（同ARIMA）
p：自回归阶数、d：差分阶数、q：移动平均阶数
2. 季节专属参数（核心新增）
m：季节周期长度（最重要参数）
月度数据 → m=12
季度数据 → m=4
周度数据 → m=7
P：季节自回归阶数
D：季节差分阶数（消除周期性趋势）
Q：季节移动平均阶数
国赛万能默认组合：SARIMA(1,1,1)(1,1,1)m，适配所有季节时序题
### 四、SARIMA标准化解题步骤
SARIMA在ARIMA趋势拟合基础上，叠加季节周期拟合，步骤更完整，是月度/季度时序大题满分标准流程：
时序可视化分析：绘制折线图，直观判断数据同时存在长期趋势+固定季节周期，判定适配SARIMA模型，排除普通ARIMA
确定季节周期m：根据数据类型锁定周期（月度m=12、季度m=4、周度m=7）
平稳性检验与普通差分：通过ADF检验判定平稳性，确定非季节差分阶数d（常规取d=1）
季节差分处理与定D：针对周期波动做季节差分，消除季节性规律，常规考题D=1即可实现周期平稳
最优参数筛选：结合ACF/PACF图+AIC/BIC准则，遍历筛选最优p、q（趋势参数）与P、Q（季节参数）
模型训练与残差检验：代入最优7项参数训练模型，完成白噪声检验，验证模型有效性
拟合验证与外推预测：拟合历史数据验证精度，外推未来多期数据，结合业务场景分析结果
SARIMA国赛万能参数组合
无特殊复杂波动时，统一使用：SARIMA(1,1,1)(1,1,1)m，适配所有季节时序考题，拟合稳定、无过拟合、竞赛通过率最高。
在ARIMA步骤基础上，增加季节判定与季节差分：
时序可视化，判定存在固定季节周期
确定周期m（月度12、季度4）
ADF平稳性检验，确定普通差分d
季节差分处理，消除周期波动，确定D
信息准则筛选最优p,q,P,Q
模型训练、残差检验
拟合预测、结果分析
### 五、ARIMA与SARIMA终极选型对比
## 第三部分：国赛可直接运行完整代码（ARIMA+SARIMA）
### 一、ARIMA完整竞赛代码
### 二、SARIMA季节时序完整竞赛代码
## 第四部分：模型精度评价指标
ARIMA/SARIMA预测完成后，必须搭配量化指标评价精度，避免仅看图无数据，提升论文专业性，可直接替换使用。
### 一、三大核心评价指标
决定系数 R²：取值[0,1]，越接近1，模型拟合度越高、解释能力越强
均方误差 MSE：衡量预测值与真实值误差平方均值，数值越小精度越高
平均绝对误差 MAE：误差绝对值均值，不受极端异常值干扰，结果更稳健
### 二、精度评价代码（可直接追加到原有代码末尾）
## 第五部分
小样本(n<20)使用ARIMA/SARIMA：时序统计模型依赖充足样本，小样本会导致模型不收敛、拟合失真、预测完全失效，必须替换为GM(1,1)灰色预测
有季节周期强行用ARIMA：ARIMA无季节拟合模块，无法捕捉月度/季度周期性波动，预测结果严重偏离真实趋势，必须用SARIMA
跳过ADF平稳性检验直接建模：非平稳时序建模无统计学意义，论文逻辑断层，属于核心步骤缺失，直接大幅扣分
用ARIMA/SARIMA填补中间缺失值：两类模型仅用于未来外推预测，数据中间缺失必须用线性插值、三次样条插值补全
不做残差检验直接出结果：无法证明模型拟合有效性，竞赛大题结题不完整
盲目高阶参数（p/q/P/Q≥3）：极易过拟合，训练集精度极高、预测集完全失效，国赛禁止高阶参数
无周期、大样本、纯趋势波动 → 优先ARIMA(1,1,1)
有固定季节周期、大样本 → 优先SARIMA(1,1,1)(1,1,1)m
小样本、贫信息、杂乱数据 → 必选GM(1,1)
## 第六部分：完整国赛真题分步解题演示
真题题干
某店铺36个月月度销量数据，存在明显夏季高、冬季低的年度周期性波动，试建立时序模型预测未来6个月销量。
解题思路
1. 样本量36≥20，大样本满足时序建模条件；
2. 数据存在明显年度季节周期，ARIMA无法适配，选择SARIMA；
3. 月度数据周期m=12，采用SARIMA(1,1,1)(1,1,1,12)建模；
4. 平稳性检验、季节差分、模型训练、未来6期预测、结果分析。
论文结论话术
本次月度销量时序数据存在显著的年度季节性波动与长期趋势特征，传统ARIMA模型无法捕捉季节周期规律，拟合精度有限。因此本文采用SARIMA季节性时序预测模型，引入季节差分与季节自回归机制，同时挖掘数据的长期趋势与周期性波动特征，模型拟合效果良好，预测结果可为店铺备货、营销策略调整提供数据支撑。

<!-- 表 1 -->
| 模型 | 样本量 | 数据特征 | 核心优势 | 适用考题 |
| ARIMA | ≥20 | 有趋势、无固定周期、随机波动 | 消除趋势，拟合平稳波动 | 逐年长期趋势数据 |
| SARIMA | ≥20 | 有趋势+有固定季节/月度周期 | 同时捕捉趋势+周期双重规律 | 月度、季度、季节类时序数据 |
| GM(1,1) | 3~15 | 小样本、杂乱无规律、贫信息 | 小样本短期高精度预测 | 数据稀少的竞赛小题 |


<!-- 表 2 -->
| python # ========= ARIMA完整建模全流程代码（数模国赛专用） =========== # 导入表格处理库，读取csv格式清洗后的时序数据 import pandas as pd # 导入数值计算库，用于数组运算、数值保留小数 import numpy as np # 导入绘图库，绘制时序曲线、ACF/PACF相关图 import matplotlib.pyplot as plt # 屏蔽训练过程无关警告，避免控制台输出杂乱 import warnings warnings.filterwarnings("ignore") # 导入ARIMA时序预测模型核心类 from statsmodels.tsa.arima.model import ARIMA # 导入ADF单位根检验函数，判断序列平稳性，确定差分阶d from statsmodels.tsa.stattools import adfuller # 导入ACF自相关、PACF偏自相关绘图工具，用来初步判断p、q from statsmodels.graphics.tsaplots import plot_acf, plot_pacf # 导入模型评价指标 from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error # ---------------------- 全局绘图配置：解决中文乱码、负号方块问题 ---------------------- # 设置全局字体为黑体，支持中文显示 plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"] # 关闭负号unicode兼容，防止负数显示方框 plt.rcParams["axes.unicode_minus"] = False # ---------------------- 步骤1：读取预处理完成的时序数据 ---------------------- # 读取csv文件，该文件已经完成缺失插值、IQR异常值修正 df = pd.read_csv("clean_time_data.csv") # 提取需要预测的指标列，生成一维时序序列 data = df["clean_y"] # 复制原始数据，防止后续运算修改原序列 origin_data = data.copy() # ---------------------- 步骤2：自定义ADF平稳性检验函数，确定差分阶d ---------------------- def adf_test(series): # 执行ADF单位根检验，返回全部检验结果元组 adf_result = adfuller(series) # 打印ADF检验统计量 print("="*50) print(f"ADF检验统计量: {adf_result[0]:.4f}") # P值是核心判断依据 p_value = adf_result[1] print(f"检验P值: {p_value:.4f}") # 打印1%、5%、10%置信度临界值，论文可粘贴 print("各置信水平临界值：", adf_result[4]) # 判断平稳性 if p_value < 0.05: print("检验结论：P<0.05，序列无单位根，属于平稳序列，d=0") else: print("检验结论：P>0.05，序列存在单位根，属于非平稳序列，需要差分") print("="*50) return p_value # 对原始时序执行ADF检验 p_origin = adf_test(data) # 自动判断需要几次差分（国赛最多2次差分）每次 差分，展示当前序列折线图 d = 0 temp_series = data.copy() # 原始不平稳则一次差分 if p_origin > 0.05: d = 1 temp_series = temp_series.diff().dropna() p_diff1 = adf_test(temp_series) # 一次差分仍不平稳，做二次差分 if p_diff1 > 0.05: d = 2 temp_series = temp_series.diff().dropna() adf_test(temp_series) print(f"经ADF检验确定最优差分阶数 d = {d}") # ---------------------- 步骤3：绘制ACF、PACF图，初步筛选p、q候选值 ---------------------- # 创建2行1列画布，分别放ACF、PACF fig, (ax_acf, ax_pacf) = plt.subplots(2, 1, figsize=(10, 7)) # 基于差分后的平稳序列绘图，最大滞后阶数10阶 plot_acf(temp_series, lags=10, ax=ax_acf) ax_acf.set_title("差分后序列 ACF自相关图（判断q阶数）") plot_pacf(temp_series, lags=10, ax=ax_pacf) ax_pacf.set_title("差分后序列 PACF偏自相关图（判断p阶数）") plt.tight_layout() plt.show() # ---------------------- 步骤4：遍历p、q组合，通过AIC准则自动选最优p、q ---------------------- # 遍历范围0、1、2，国赛足够使用 min_aic = float("inf") best_p = 0 best_q = 0 print("\n开始遍历p、q组合筛选最优参数...") for p in range(0, 3): for q in range(0, 3): try: # 构建临时模型 temp_model = ARIMA(data, order=(p, d, q)) temp_fit = temp_model.fit() # 更新最小AIC与最优p、q if temp_fit.aic < min_aic: min_aic = temp_fit.aic best_p = p best_q = q except Exception as e: # 部分参数组合模型不收敛，直接跳过 continue print(f"遍历完成，最优参数：p={best_p}, d={d}, q={best_q}，最小AIC={min_aic:.2f}") # ---------------------- 步骤5：使用最优(p,d,q)搭建并训练正式ARIMA模型 ---------------------- # 传入最优三阶参数构建模型 arima_model = ARIMA(data, order=(best_p, d, best_q)) # 模型拟合训练 model_fit = arima_model.fit() # ---------------------- 步骤6：获取历史拟合值、未来多期外推预测 ---------------------- # fittedvalues：模型对全部历史数据的拟合值 history_fit = model_fit.fittedvalues # get_forecast(steps=5)：向后预测5期，predicted_mean提取预测均值 forecast_result = model_fit.get_forecast(steps=5) future_pred = forecast_result.predicted_mean # 打印未来5期预测结果，保留2位小数 print("\n===== 未来5期外推预测结果 =====") print(np.round(future_pred, 2)) # ---------------------- 步骤7：计算模型拟合精度指标R²、MSE、MAE ---------------------- # 跳过前d个空值，对齐长度 true_y = data[d:] pred_y = history_fit[d:] r2 = r2_score(true_y, pred_y) mse = mean_squared_error(true_y, pred_y) mae = mean_absolute_error(true_y, pred_y) print("\n===== 模型拟合精度评价指标 =====") print(f"拟合优度 R² = {r2:.4f}") print(f"均方误差 MSE = {mse:.4f}") print(f"平均绝对误差 MAE = {mae:.4f}") # ---------------------- 步骤8：绘制原图+拟合曲线对比图 ---------------------- plt.figure(figsize=(12, 5)) # 原始真实数据曲线 plt.plot(data.index, data.values, label="原始真实时序数据", linewidth=2) # 模型历史拟合曲线，透明度0.7区分 plt.plot(history_fit.index, history_fit.values, label="ARIMA模型拟合值", alpha=0.7, linewidth=2) plt.title("ARIMA时序模型：真实值 vs 拟合值对比曲线") plt.xlabel("时序编号") plt.ylabel("指标数值") plt.legend() plt.grid(alpha=0.3) plt.show() # ---------------------- 步骤9：输出完整模型统计摘要（论文直接复制） ---------------------- print("\n===== ARIMA模型完整参数摘要 =====") print(model_fit.summary()) |


<!-- 表 3 -->
| python import pandas as pd import numpy as np import matplotlib.pyplot as plt from statsmodels.tsa.statespace.sarimax import SARIMAX from statsmodels.tsa.stattools import adfuller # 中文适配 plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"] plt.rcParams["axes.unicode_minus"] = False # 1. 导入月度/季度时序数据 df = pd.read_csv("season_time_data.csv") data = df["season_y"] # 2. 平稳性检验 def adf_test(series): p = adfuller(series)[1] print("ADF检验P值：",p) return p adf_test(data) # 3. SARIMA建模（月度数据m=12，季度m=4） # 通用参数(1,1,1)(1,1,1,12) model = SARIMAX(data, order=(1,1,1), seasonal_order=(1,1,1,12)) sarima_fit = model.fit() # 4. 拟合+预测未来6期 fit_res = sarima_fit.fittedvalues future_pred = sarima_fit.get_forecast(steps=6).predicted_mean print("n====SARIMA未来6期季节预测结果====") print(np.round(future_pred,2)) # 5. 绘图 plt.figure(figsize=(11,5)) plt.plot(data,label="原始季节时序数据") plt.plot(fit_res,label="SARIMA拟合数据",alpha=0.7) plt.title("基于SARIMA的季节性时序预测") plt.legend() plt.grid(alpha=0.3) plt.show() # 输出论文可用模型摘要 print(sarima_fit.summary()) |


<!-- 表 4 -->
| python from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error # 仅对已有真实数据的部分做精度评价 true_data = data[1:] pred_data = fit_vals[1:] # 计算三大指标 r2 = r2_score(true_data, pred_data) mse = mean_squared_error(true_data, pred_data) mae = mean_absolute_error(true_data, pred_data) print("====模型精度评价指标====") print(f"拟合优度 R² = {r2:.4f}") print(f"均方误差 MSE = {mse:.4f}") print(f"平均绝对误差 MAE = {mae:.4f}") |
