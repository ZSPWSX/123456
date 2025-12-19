import pandas as pd
import os

# 设置输入文件夹路径
input_folder = r'c:\Users\ASUS\Desktop\全部\新建文件夹'
output_file = r'c:\Users\ASUS\Desktop\全部\合并后的数字化转型指数表.xlsx'

# 获取所有Excel文件
files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx') and '数字化转型指数结果表' in f]

# 初始化一个空的DataFrame来存储合并后的数据
merged_data = pd.DataFrame()

# 遍历每个文件
for file in files:
    # 提取年份
    year = file[:4]
    file_path = os.path.join(input_folder, file)
    
    try:
        # 获取文件的所有工作表名称
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        print(f"文件 {file} 的工作表名称: {sheet_names}")
        
        # 尝试不同的工作表名称（考虑大小写和不同命名）
        target_sheet = None
        for sheet in sheet_names:
            if 'sheet4' in sheet.lower() or '4' in sheet:
                target_sheet = sheet
                break
        
        if target_sheet:
            # 读取目标工作表
            df = pd.read_excel(file_path, sheet_name=target_sheet)
            
            # 检查必要的列是否存在（考虑不同的列名）
            df.columns = df.columns.str.strip()  # 去除列名中的空格
            columns_lower = df.columns.str.lower()
            
            # 映射可能的列名
            stock_code_col = None
            company_name_col = None
            digital_index_col = None
            
            for i, col in enumerate(columns_lower):
                if '股票' in col or 'code' in col or 'stock' in col:
                    stock_code_col = df.columns[i]
                if '企业' in col or '公司' in col or 'name' in col:
                    company_name_col = df.columns[i]
                if '数字化' in col or '转型' in col or '指数' in col or 'index' in col:
                    digital_index_col = df.columns[i]
            
            if stock_code_col and company_name_col and digital_index_col:
                # 提取需要的列
                df_selected = df[[stock_code_col, company_name_col, digital_index_col]].copy()
                # 重命名列
                df_selected.columns = ['股票代码', '企业名称', '数字化转型指数']
                # 添加年份列
                df_selected['年份'] = year
                # 将当前文件的数据添加到合并数据中
                merged_data = pd.concat([merged_data, df_selected], ignore_index=True)
                print(f"成功处理文件: {file}，使用工作表: {target_sheet}")
            else:
                print(f"文件 {file} 缺少必要的列")
                print(f"可用列: {list(df.columns)}")
        else:
            print(f"文件 {file} 中没有找到包含'sheet4'或'4'的工作表")
    except Exception as e:
        print(f"处理文件 {file} 时出错: {str(e)}")

# 保存合并后的数据
try:
    merged_data.to_excel(output_file, index=False)
    print(f"\n合并完成！结果保存到: {output_file}")
    print(f"共处理了 {len(files)} 个文件")
    print(f"合并后的数据行数: {len(merged_data)}")
    if len(merged_data) > 0:
        print(f"数据列: {list(merged_data.columns)}")
except Exception as e:
    print(f"保存文件时出错: {str(e)}")
