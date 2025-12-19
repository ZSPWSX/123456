import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面标题
st.title('企业数字化转型指数查询系统')

# 读取数据
@st.cache_data(ttl=3600, show_spinner="正在加载数据...")
def load_data():
    file_path = r'c:\Users\ASUS\Desktop\全部\合并后的数字化转型指数表.xlsx'
    df = pd.read_excel(file_path)
    # 确保股票代码是字符串类型，方便查询
    df['股票代码'] = df['股票代码'].astype(str)
    return df

# 加载数据
df = load_data()

# 显示数据概览
st.subheader('数据概览')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总记录数", f"{len(df):,}")
with col2:
    st.metric("涵盖年份", f"{df['年份'].min()} - {df['年份'].max()}")
with col3:
    st.metric("企业数量", f"{df['企业名称'].nunique()}")

# 显示示例股票代码
st.info("示例股票代码：600000 (浦发银行), 600001 (邯郸钢铁), 600002 (齐鲁石化)")

# 股票代码输入
stock_code = st.text_input(
    '请输入股票代码:', 
    placeholder='例如: 600000',
    help='输入6位数字的股票代码'
)

# 添加自动完成建议
if stock_code:
    # 获取匹配的股票代码和企业名称
    suggestions = df[df['股票代码'].str.startswith(stock_code)][['股票代码', '企业名称']].drop_duplicates()
    if not suggestions.empty:
        st.write("匹配的股票代码:")
        for _, row in suggestions.head(5).iterrows():
            st.write(f"- {row['股票代码']}: {row['企业名称']}")

# 查询按钮
if st.button('查询', type='primary'):
    if stock_code:
        # 确保输入是纯数字
        if stock_code.isdigit():
            # 过滤数据
            filtered_df = df[df['股票代码'] == stock_code]
            
            if not filtered_df.empty:
                # 获取企业名称
                company_name = filtered_df['企业名称'].iloc[0]
                st.success(f"找到 {company_name} ({stock_code}) 的数据")
                
                st.subheader(f'{company_name} ({stock_code}) 数字化转型指数')
                
                # 显示数据表格
                st.dataframe(
                    filtered_df[['年份', '数字化转型指数']].sort_values('年份'), 
                    width='stretch',
                    hide_index=True
                )
                
                # 绘制折线图
                st.subheader(f'{company_name} ({stock_code}) 历年数字化转型指数趋势')
                fig = px.line(
                    filtered_df.sort_values('年份'), 
                    x='年份', 
                    y='数字化转型指数', 
                    title=f'{company_name} 数字化转型指数趋势',
                    markers=True, 
                    line_shape='linear',
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(
                    xaxis_title='年份',
                    yaxis_title='数字化转型指数',
                    xaxis=dict(
                        tickmode='linear', 
                        tick0=filtered_df['年份'].min(), 
                        dtick=1
                    ),
                    hovermode='x unified',
                    template='plotly_white',
                    height=500
                )
                fig.update_traces(hovertemplate='年份: %{x}<br>数字化转型指数: %{y}')
                st.plotly_chart(fig, width='stretch')
                
                # 显示统计信息
                st.subheader('统计信息')
                stats_df = filtered_df.sort_values('年份')
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("最高指数", stats_df['数字化转型指数'].max())
                with col2:
                    st.metric("最低指数", stats_df['数字化转型指数'].min())
                with col3:
                    st.metric("平均指数", f"{stats_df['数字化转型指数'].mean():.2f}")
                with col4:
                    # 计算增长率
                    if len(stats_df) > 1:
                        first_val = stats_df['数字化转型指数'].iloc[0]
                        last_val = stats_df['数字化转型指数'].iloc[-1]
                        if first_val != 0:
                            growth_rate = (last_val - first_val) / first_val * 100
                            st.metric("年均增长率", f"{growth_rate:.2f}%")
                        else:
                            st.metric("年均增长率", "N/A")
                    else:
                        st.metric("年均增长率", "N/A")
            else:
                st.error(f"未找到股票代码为 {stock_code} 的企业数据")
                st.info("请检查股票代码是否正确，或尝试其他股票代码")
        else:
            st.error("请输入有效的数字股票代码")
    else:
        st.warning('请输入股票代码')

# 侧边栏：企业搜索和选择
st.sidebar.title('企业搜索')
# 获取所有企业列表
all_companies = df[['股票代码', '企业名称']].drop_duplicates().sort_values('企业名称')
# 选择企业
selected_company = st.sidebar.selectbox(
    '从列表中选择企业:',
    options=all_companies.apply(lambda x: f"{x['股票代码']}: {x['企业名称']}", axis=1).tolist(),
    index=None,
    placeholder='选择企业'
)

# 如果从侧边栏选择了企业
if selected_company:
    stock_code_from_sidebar = selected_company.split(':')[0]
    # 过滤数据
    filtered_df = df[df['股票代码'] == stock_code_from_sidebar]
    if not filtered_df.empty:
        company_name = filtered_df['企业名称'].iloc[0]
        st.sidebar.subheader(f'{company_name} ({stock_code_from_sidebar})')
        st.sidebar.write(f"数据条数: {len(filtered_df)}")
        st.sidebar.write(f"年份范围: {filtered_df['年份'].min()} - {filtered_df['年份'].max()}")

# 侧边栏：数据筛选
st.sidebar.title('数据筛选')
year_range = st.sidebar.slider(
    '选择年份范围', 
    df['年份'].min(), 
    df['年份'].max(), 
    (df['年份'].min(), df['年份'].max())
)

index_range = st.sidebar.slider(
    '选择指数范围', 
    int(df['数字化转型指数'].min()), 
    int(df['数字化转型指数'].max()), 
    (0, 100)
)

# 应用筛选
filtered_data = df[
    (df['年份'] >= year_range[0]) & 
    (df['年份'] <= year_range[1]) &
    (df['数字化转型指数'] >= index_range[0]) &
    (df['数字化转型指数'] <= index_range[1])
]

st.sidebar.write(f"筛选后记录数: {len(filtered_data):,}")

# 显示数据样本
if st.checkbox('显示数据样本'):
    st.subheader('数据样本')
    st.dataframe(df.head(10), width='stretch', hide_index=True)
