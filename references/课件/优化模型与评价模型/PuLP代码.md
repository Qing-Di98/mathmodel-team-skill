PuLP 三段代码
LP + 0-1 背包 + 指派问题
这份稿子怎么用
PuLP 是一个 Python 库，专门用来写线性规划 (LP)、整数规划 (IP)、0-1 规划这类 "最优化问题" 的。
预备:先认识 PuLP 的 5 大零件
零件 作用 LpProblem 建"问题"的容器,装目标和约束 LpMaximize / LpMinimize 告诉求解器是要"最大化"还是"最小化" LpVariable 造一个决策变量(可连续、可整数、可 0-1) prob += 表达式 第一次 += 是加"目标",之后 += 都是加"约束" prob.solve() 喊求解器开工,算出所有变量的值
通俗理解: PuLP 写法都是"5 步走":建问题 → 定变量 → 写目标 → 加约束 → 求解读结果。下面 3 个例子全部按这 5 步来,套路一模一样,只是变量和约束不同。
from pulp import * 是什么意思?
from pulp import * 就是把 pulp 库里所有工具都拿到当前文件里用,这样后面直接写 LpProblem、LpVariable 就行,不用写 pulp.LpProblem。正规写法是 import pulp,但教学里用 * 更简洁。
例子 1:工厂生产问题(线性规划 LP)
题目回顾
生产 A、B 两种产品:
A 每件用 1 小时工时、4 单位材料,利润 6 元
B 每件用 2 小时工时、3 单位材料,利润 5 元
每天最多 8 小时工时、12 单位材料
问:A、B 各生产多少利润最大?
完整代码
from pulp import * # ① 创建问题:目标是最大化 prob = LpProblem("工厂利润", LpMaximize) # ② 定义决策变量(非负) x1 = LpVariable("A产品数量", lowBound=0) x2 = LpVariable("B产品数量", lowBound=0) # ③ 写目标函数 prob += 6*x1 + 5*x2 # ④ 写约束条件 prob += x1 + 2*x2 <= 8, "工时约束" prob += 4*x1 + 3*x2 <= 12, "材料约束" # ⑤ 求解 + 打印 prob.solve() print("A =", x1.varValue, ", B =", x2.varValue) print("最大利润 =", value(prob.objective))
逐行讲解
第 1 行:from pulp import *
把 PuLP 库里所有工具搬进来。这行永远写在第一行。
第 3 行:prob = LpProblem("工厂利润", LpMaximize)
新建一个空的'问题容器',名字叫'工厂利润'。LpMaximize 告诉求解器我要'最大化'目标。如果要'最小化'(比如成本最小),就换成 LpMinimize。
通俗理解: 把 prob 想成一个空篮子,后面往里装目标和约束。
第 6 行:x1 = LpVariable("A产品数量", lowBound=0)
造一个决策变量 x1,代表 A 产品的生产数量。第一个参数是这个变量的名字(打印时会用到),lowBound=0 意思是"最小值是 0"——不能生产负数件。x2 同理,代表 B 产品数量。
通俗理解: LpVariable 默认是"连续变量",没写上限就默认无穷大。这就是为啥算出来 A=1.8、B=1.6 是小数。
第 10 行:prob += 6*x1 + 5*x2
给 prob 加东西——第一次 += 加的一定是'目标函数'。6*x1 + 5*x2 就是'总利润 = A数量×6 + B数量×5'。PuLP 会拿这个式子去最大化。
通俗理解: 这里没有等号,是因为目标函数不需要"等于什么"——就是一个要被最大化的表达式。
第 13 行:prob += x1 + 2*x2 <= 8, "工时约束"
第二次以后的 += 都是加'约束'。这条约束的意思是:A 数量 × 1 小时 + B 数量 × 2 小时 ≤ 8 小时。后面那个字符串 '工时约束' 是给这条约束起个名字,方便打印和 Debug,可以省略,但建议写上。
第 14 行:prob += 4*x1 + 3*x2 <= 12, "材料约束"
同理:A 用 4 单位材料 + B 用 3 单位材料 ≤ 12。
第 17 行:prob.solve()
喊求解器开始算。这一行运行完,所有变量的 varValue 属性就有值了。
第 18–19 行:打印结果
x1.varValue 就是求解器给 x1 算出来的最优值。value(prob.objective) 就是目标函数在最优解处的值,也就是最大利润。
运行输出
A = 1.8 , B = 1.6 最大利润 = 18.8
A 生产 1.8 单位、B 生产 1.6 单位,利润 18.8 元。
A、B 都是小数——如果题目要求整数(比如生产多少台机器),在 LpVariable 里加一个 cat="Integer" 就变成整数规划。一行代码的差别,从 LP 变成 IP。
例子 2:0-1 背包问题
题目回顾
5 件宝物,背包容量 10:
物品编号 0 1 2 3 4 重量 2 3 4 5 6 价值 3 4 5 8 9
每件宝物只有"装"或"不装"两种选择,问怎么选价值最大?
完整代码
weights = [2, 3, 4, 5, 6] values = [3, 4, 5, 8, 9] n = len(weights) prob = LpProblem("背包", LpMaximize) # 关键:cat="Binary" 就是 0-1 变量 x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)] prob += lpSum(values[i]*x[i] for i in range(n)) prob += lpSum(weights[i]*x[i] for i in range(n)) <= 10 prob.solve() for i in range(n): print(f"物品{i}:{'装' if x[i].varValue==1 else '不装'}") print("总价值 =", value(prob.objective))
逐行讲解
第 1–3 行:weights / values / n
weights 和 values 是两个列表,把 5 件宝物的重量和价值分别存起来。n = len(weights) 就是"一共有几件",这里等于 5。后面所有 for i in range(n) 都是从 0 循环到 4。
第 5 行:prob = LpProblem("背包", LpMaximize)
和例 1 一模一样,新建一个求最大值的问题容器。
第 8 行:x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
这行最关键,分两部分看。
★ 第一部分:cat="Binary"
cat 是 category(类别)的缩写。Binary 就是"二元变量",只能取 0 或 1,天然表达"选/不选"。这就是从 LP 升级到 0-1 规划的唯一改动。
★ 第二部分:列表推导式 [... for i in range(n)]
这是 Python 的"列表推导式",一次性造出 5 个变量,相当于下面这 5 行的合体写法
# 展开就是这样(等价写法): x = [] x.append(LpVariable("x0", cat="Binary")) x.append(LpVariable("x1", cat="Binary")) x.append(LpVariable("x2", cat="Binary")) x.append(LpVariable("x3", cat="Binary")) x.append(LpVariable("x4", cat="Binary"))
f"x{i}" 是 Python 的"f-string",大括号里的 i 会被替换成当前值,所以变量名依次是 x0, x1, x2, x3, x4。造完之后 x[0] 就是 x0 这个变量,x[1] 就是 x1,以此类推。
x 是一个装了 5 个 LpVariable 的 Python 列表,x[i] 就是"是否装第 i 件宝物"这个 0/1 变量。
第 10 行:目标函数
prob += lpSum(values[i]*x[i] for i in range(n))
目标是总价值最大。总价值 = 每件宝物的价值 × 是否装它,加起来。
lpSum(...) 是 PuLP 的求和函数,括号里那段 values[i]*x[i] for i in range(n) 会依次算出:values[0]*x[0]、values[1]*x[1]、...、values[4]*x[4],然后 lpSum 把它们加起来。
展开写就是:
prob += 3*x[0] + 4*x[1] + 5*x[2] + 8*x[3] + 9*x[4]
通俗理解: lpSum 和 Python 内置的 sum 效果一样,但 PuLP 会对 lpSum 做优化,大规模问题快得多——所以写 PuLP 时永远用 lpSum,不用 sum。
第 11 行:约束(背包容量)
prob += lpSum(weights[i]*x[i] for i in range(n)) <= 10
约束是总重量不超过 10。总重量 = 每件宝物的重量 × 是否装它,加起来 ≤ 10。展开就是 2*x[0] + 3*x[1] + 4*x[2] + 5*x[3] + 6*x[4] ≤ 10。
第 13 行:prob.solve()
求解。运行完之后每个 x[i].varValue 就是 0 或 1 了。
第 14–15 行:循环打印结果
for 循环遍历 5 件宝物,判断 x[i].varValue 是不是 1——是就打'装',否则打'不装'。这是 Python 的三元表达式:值1 if 条件 else 值2。
运行输出
物品0:不装 物品1:装 物品2:不装 物品3:装 物品4:不装 总价值 = 12.0
装了物品 1 (重 3、值 4) 和物品 3 (重 5、值 8),总重 8 ≤ 10,总价值 12。求解器验证过这是最优组合。
例子 3:指派问题(3×3 二维匹配)
题目回顾
3 个员工做 3 件任务,效率矩阵如下(行=员工,列=任务):
任务0 任务1 任务2 员工 0 9 2 7 员工 1 6 4 3 员工 2 5 8 1
每人只能做 1 件、每件只能派 1 人,问怎么派总效率最高?
完整代码
# 效率矩阵:行=员工,列=任务 eff = [[9, 2, 7], [6, 4, 3], [5, 8, 1]] prob = LpProblem("指派", LpMaximize) # x[i][j] = 1 表示员工 i 做任务 j x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(3)] for i in range(3)] # 目标:总效率最大 prob += lpSum(eff[i][j]*x[i][j] for i in range(3) for j in range(3)) # 约束 1:每人只做 1 件 for i in range(3): prob += lpSum(x[i][j] for j in range(3)) == 1 # 约束 2:每件只 1 人做 for j in range(3): prob += lpSum(x[i][j] for i in range(3)) == 1 prob.solve() for i in range(3): for j in range(3): if x[i][j].varValue == 1: print(f"员工{i} → 任务{j}(效率{eff[i][j]})")
逐行讲解
第 2–4 行:效率矩阵 eff
eff 是一个"二维列表",可以理解成 3 行 3 列的表格。eff[i][j] 就是员工 i 做任务 j 的效率。比如 eff[0][0] = 9(员工 0 做任务 0 效率 9),eff[2][1] = 8(员工 2 做任务 1 效率 8)。"
第 6 行:建问题
和前两个例子一样,新建最大化问题。"
第 9–10 行:二维决策变量
x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(3)] for i in range(3)]
这行是双层列表推导式,一次性造出 9 个 0-1 变量:x_0_0、x_0_1、x_0_2、x_1_0、...、x_2_2。"
★ 拆开看等价于:
x = [] for i in range(3): row = [] for j in range(3): row.append(LpVariable(f"x_{i}_{j}", cat="Binary")) x.append(row)
造完之后,x 是一个 3×3 的二维列表。x[i][j] 就是"员工 i 是否做任务 j"这个 0/1 变量。
第 13 行:目标函数(双 for 求和)
prob += lpSum(eff[i][j]*x[i][j] for i in range(3) for j in range(3))
总效率 = 所有'效率 × 是否指派'加起来。lpSum 里出现了两个 for——for i in range(3) for j in range(3),这是"双重循环",会遍历所有 (i, j) 组合,共 9 项。
展开就是:
prob += 9*x[0][0] + 2*x[0][1] + 7*x[0][2] + 6*x[1][0] + 4*x[1][1] + 3*x[1][2] + 5*x[2][0] + 8*x[2][1] + 1*x[2][2]
第 16–17 行:约束 1 —— 每人只做 1 件
for i in range(3): prob += lpSum(x[i][j] for j in range(3)) == 1
外层 for i 循环 3 次,每次给 prob 加一条约束。内层 lpSum(x[i][j] for j in range(3)) 是"对固定的员工 i,把他做 3 个任务的 0/1 变量加起来"。这个和 = 1,意味着"这个员工恰好做 1 件事"(不能做 0 件、不能做 2 件)。
展开就是 3 条约束:
x[0][0] + x[0][1] + x[0][2] == 1 ← 员工 0 恰好做 1 件 x[1][0] + x[1][1] + x[1][2] == 1 ← 员工 1 恰好做 1 件 x[2][0] + x[2][1] + x[2][2] == 1 ← 员工 2 恰好做 1 件
第 20–21 行:约束 2 —— 每件只 1 人做
for j in range(3): prob += lpSum(x[i][j] for i in range(3)) == 1
和约束 1 反过来:外层固定任务 j,内层把 3 个员工做这件任务的 0/1 变量加起来 = 1,意味着"这件任务恰好由 1 人做"。
展开就是另外 3 条约束:
x[0][0] + x[1][0] + x[2][0] == 1 ← 任务 0 恰好 1 人做 x[0][1] + x[1][1] + x[2][1] == 1 ← 任务 1 恰好 1 人做 x[0][2] + x[1][2] + x[2][2] == 1 ← 任务 2 恰好 1 人做
通俗理解: 两组约束加在一起就构成了"一一匹配":每人做一件、每件一人做。这就是指派问题的核心结构,记住这两个 for 循环的写法。
第 23 行:求解
照旧调用 solve。
第 24–27 行:打印指派结果
用双重 for 遍历所有 (i, j) 组合,如果 x[i][j] = 1,就说明"员工 i 被派去做任务 j",打印出来。只有 3 个位置会是 1(因为 9 个变量里最终只有 3 个被选中),所以只打印 3 行。
运行输出
员工0 → 任务0(效率9) 员工1 → 任务2(效率3) 员工2 → 任务1(效率8) 总效率 = 9 + 3 + 8 = 20
结果:员工 0 干任务 0、员工 1 干任务 2、员工 2 干任务 1,总效率 20。这就是数模里'指派问题'的原型——只要涉及'一一匹配'的场景都能套。比如员工-任务、船-泊位、广告-时段、志愿者-赛道,把 3×3 换成 n×n 即可。
三段代码的共同点
步骤 例 1(LP) 例 2(0-1 背包) 例 3(指派) ① 建问题 LpProblem(..Max..) 一样 一样 ② 定变量 lowBound=0(连续) cat="Binary"(0/1) cat="Binary"(0/1) 单变量 x1, x2 一维列表 x[i] 二维列表 x[i][j] ③ 写目标 6*x1 + 5*x2 lpSum(v[i]*x[i]..) lpSum(eff[i][j]*x[i][j]..) ④ 加约束 两条不等式 一条容量约束 两组 for 循环各 3 条 ⑤ 求解读取 prob.solve() 一样 一样 x1.varValue x[i].varValue x[i][j].varValue
优化题写法:
全连续变量 → LP → LpVariable(lowBound=0)
0/1 选择变量 → 0-1 规划 → cat="Binary"
二维匹配 → 双下标 x[i][j] + 两组 for 循环约束