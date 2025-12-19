import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面标题
st.title('企业数字化转型指数查询系统')

# 读取数据
@st.cache_data

def load_data():
    file_path = 'c:\\Users\\ASUS\\Desktop\\全部\\合并后的数字化转型指数表.xlsx'
    df = pd.read_excel(file_path)
    return df

df = load_data()

# 显示数据概览
st.subheader('数据概览')
st.write(f"共包含 {len(df)} 条记录")
st.write(f"涵盖年份: {df['年份'].min()} - {df['年份'].max()}")
st.write(f"涵盖企业数量: {df['企业名称'].nunique()}")

# 股票代码输入
stock_code = st.text_input('请输入股票代码:', placeholder='例如: 600000')

# 查询按钮
if st.button('查询'):
    if stock_code:
        # 过滤数据
        filtered_df = df[df['股票代码'].astype(str) == stock_code]
        
        if not filtered_df.empty:
            # 获取企业名称
            company_name = filtered_df['企业名称'].iloc[0]
            st.subheader(f'{company_name} ({stock_code}) 数字化转型指数')
            
            # 显示数据表格
            st.dataframe(filtered_df[['年份', '数字化转型指数']].sort_values('年份'), width='stretch')
            
            # 绘制折线图
            st.subheader(f'{company_name} ({stock_code}) 历年数字化转型指数趋势')
            fig = px.line(filtered_df, x='年份', y='数字化转型指数', 
                         title=f'{company_name} 数字化转型指数 (2000-2023)',
                         markers=True, 
                         line_shape='linear')
            fig.update_layout(
                xaxis_title='年份',
                yaxis_title='数字化转型指数',
                xaxis=dict(tickmode='linear', tick0=filtered_df['年份'].min(), dtick=1),
                hovermode='x unified'
            )
            st.plotly_chart(fig, width='stretch')
            
            # 显示统计信息
            st.subheader('统计信息')
            st.write(f"最高指数: {filtered_df['数字化转型指数'].max()}")
            st.write(f"最低指数: {filtered_df['数字化转型指数'].min()}")
            st.write(f"平均指数: {filtered_df['数字化转型指数'].mean():.2f}")
            st.write(f"指数增长率: {(filtered_df['数字化转型指数'].max() - filtered_df['数字化转型指数'].min()) / max(1, filtered_df['数字化转型指数'].min()) * 100:.2f}%")
        else:
            st.error(f"未找到股票代码为 {stock_code} 的企业数据")
    else:
        st.warning('请输入股票代码')

# 侧边栏：显示企业列表
st.sidebar.title('企业列表')
company_list = df[['股票代码', '企业名称']].drop_duplicates().sort_values('股票代码')
st.sidebar.dataframe(company_list, width='stretch')

# 侧边栏：数据筛选示例
st.sidebar.title('数据筛选示例')
year_range = st.sidebar.slider('选择年份范围', df['年份'].min(), df['年份'].max(), (df['年份'].min(), df['年份'].max()))
filtered_by_year = df[(df['年份'] >= year_range[0]) & (df['年份'] <= year_range[1])]
st.sidebar.write(f"该年份范围内共有 {len(filtered_by_year)} 条记录")

# 侧边栏：指数分布
st.sidebar.title('指数分布')
index_range = st.sidebar.slider('选择指数范围', int(df['数字化转型指数'].min()), int(df['数字化转型指数'].max()), (0, 100))
filtered_by_index = df[(df['数字化转型指数'] >= index_range[0]) & (df['数字化转型指数'] <= index_range[1])]
st.sidebar.write(f"该指数范围内共有 {len(filtered_by_index)} 条记录")
