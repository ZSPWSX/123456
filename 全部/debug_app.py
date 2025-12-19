import pandas as pd

# 读取数据
file_path = r'c:\Users\ASUS\Desktop\全部\合并后的数字化转型指数表.xlsx'
df = pd.read_excel(file_path)

# 检查数据基本信息
print("数据基本信息：")
print(df.info())

# 检查前10条数据
print("\n前10条数据：")
print(df.head(10))

# 检查股票代码的数据类型
print("\n股票代码的数据类型：", df['股票代码'].dtype)

# 检查股票代码的前几个值
print("\n股票代码前10个值：")
print(df['股票代码'].head(10).tolist())

# 尝试不同的查询方式
print("\n尝试查询股票代码 600000：")
# 方式1：直接用整数查询
result1 = df[df['股票代码'] == 600000]
print("用整数查询结果：", len(result1))

# 方式2：用字符串查询
result2 = df[df['股票代码'].astype(str) == '600000']
print("用字符串查询结果：", len(result2))

# 方式3：去除空格后查询
result3 = df[df['股票代码'].astype(str).str.strip() == '600000']
print("去除空格后查询结果：", len(result3))

# 检查数据中是否真的有600000
print("\n检查数据中是否包含600000：")
print(600000 in df['股票代码'].values)
