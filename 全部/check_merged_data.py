import pandas as pd

# 读取合并后的文件
merged_file = r'c:\Users\ASUS\Desktop\全部\合并后的数字化转型指数表.xlsx'

# 读取前10行数据
df = pd.read_excel(merged_file, nrows=10)

# 显示数据
print("合并后的数据前10行：")
print(df)
print("\n数据列：")
print(df.columns.tolist())
print("\n数据类型：")
print(df.dtypes)
