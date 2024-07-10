#đếm sô luọng job theo từng loại bằng cấp
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
from wordcloud import WordCloud
import base64
from io import BytesIO

st.set_page_config(
    page_title="Tình hình việc làm ở Việt Nam",
    page_icon="📊",
    layout="wide",
    )
alt.themes.enable("dark")

df_reshaped = pd.read_csv('cleaned_dataset.csv')

with st.sidebar:
    st.title('Tình hình việc làm ở Việt Nam')
    # Split and explode the 'Khu vực tuyển' column
    df_exploded = df_reshaped.assign(**{
        'Khu vực tuyển': df_reshaped['Khu vực tuyển'].str.split(',')
    }).explode('Khu vực tuyển')

    # Strip any leading/trailing whitespace from the 'Khu vực tuyển' column
    df_exploded['Khu vực tuyển'] = df_exploded['Khu vực tuyển'].str.strip()
    
    #tạo list tỉnh thành, có 1 loại là Tất cả
    area_list = ['Tất cả'] + list(df_exploded['Khu vực tuyển'].unique())
    #tạo selectbox để chọn tỉnh thành
    area = st.selectbox('Chọn khu vực tuyển', area_list)
    #tạo df_area để lọc theo khu vực tuyển
    if area != 'Tất cả':
        df_filter = df_exploded[df_exploded['Khu vực tuyển'] == area]
    else:
        df_filter = df_reshaped
    #Chọn nhóm tuổi
    age_list = ['Tất cả'] + list(df_filter['Nhóm tuổi'].unique())
    age = st.selectbox('Chọn nhóm tuổi', age_list)
    #lọc theo nhóm tuổi
    if age != 'Tất cả':
        df_filter = df_filter[df_filter['Nhóm tuổi'] == age]
    else:
        df_filter = df_filter
    
    #Chọn bằng cấp
    degree_list = ['Tất cả'] + list(df_filter['Yêu cầu bằng cấp'].unique())
    degree = st.selectbox('Chọn bằng cấp', degree_list)
    #lọc theo bằng cấp
    if degree != 'Tất cả':
        df_filter = df_filter[df_filter['Yêu cầu bằng cấp'] == degree]
    else:
        df_filter = df_filter


col = st.columns((1,1), gap='small')
with col[0]:


# Giả sử bạn đã có dữ liệu df_highsalary
# df_highsalary là một DataFrame chứa các cột: 'Ngành nghề', 'Tỉ lệ công việc lương cao', 'Tổng số lượng tuyển'

# Tổng số lượng tuyển dụng trong các ngành
    
    upper_quartile = df_reshaped['Mức lương trung bình'].quantile(0.75)
    df_highsalary = df_reshaped[df_reshaped['Mức lương trung bình'] >= upper_quartile]
    df_exp = df_reshaped.copy()
    df_exp['Ngành nghề'] = df_exp['Ngành nghề'].str.split('/')
    df_exp = df_exp.explode('Ngành nghề')
    df_exp.reset_index(inplace=True)
    df_exp.drop(columns=['index'], inplace=True)
    df_copy_grouped = df_exp.groupby('Ngành nghề')['Số lượng tuyển'].sum()
    df_copy_grouped = pd.DataFrame(df_copy_grouped)

    df_exp = df_reshaped.copy()
    df_exp['Công việc chính'] = df_exp['Công việc chính']
    df_exp = df_exp('Công việc chính')
    df_exp.reset_index(inplace=True)
    df_exp.drop(columns=['index'], inplace=True)
    df_copy_grouped = df_exp.groupby('Công việc chính')['Số lượng tuyển'].sum()
    df_copy_grouped = pd.DataFrame(df_copy_grouped)
    df_copy_grouped.head()

    df_highsalary.loc[:, 'Ngành nghề'] = df_highsalary['Ngành nghề'].str.split('/')
    df_highsalary = df_highsalary.explode('Ngành nghề')
    df_highsalary.reset_index(inplace=True)
    df_highsalary.drop(columns=['index'], inplace=True)
    df_highsalary_grouped = df_highsalary.groupby('Ngành nghề')['Số lượng tuyển'].sum()
    df_highsalary_grouped = pd.DataFrame(df_highsalary_grouped)
    df_highsalary_grouped.head(10)


    # Tạo subplot với một trục y bên trái và một trục y bên phải
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Thêm biểu đồ bar vào subplot
    fig.add_trace(
        go.Bar(
            x=df_highsalary['Ngành nghề'].head(10),
            y=df_highsalary['Tỉ lệ công việc lương cao'].head(10),
            name='Tỉ lệ công việc lương cao'
        ),
        secondary_y=False,
    )

    # Thêm biểu đồ line vào subplot
    fig.add_trace(
        go.Scatter(
            x=df_highsalary['Ngành nghề'].head(10),
            y=df_highsalary['Tổng số lượng tuyển'].head(10),
            name='Tổng số lượng tuyển',
            line=dict(color='red')
        ),
        secondary_y=True,
    )

    # Cập nhật layout
    fig.update_layout(
        title_text='Top 10 ngành nghề có tỉ lệ công việc lương cao',
        xaxis_tickangle=-90
    )

    # Cập nhật tiêu đề cho các trục y
    fig.update_yaxes(title_text="Tỉ lệ công việc lương cao", secondary_y=False)
    fig.update_yaxes(title_text="Tổng số lượng tuyển", secondary_y=True)

    fig.show()



    # Split các giá trị trong cột 'Từ khoá' và vẽ word cloud
    df_reshaped['Từ khóa'] = df_reshaped['Từ khóa'].str.split('; ')
    df_keywords = df_reshaped.explode('Từ khóa')
    df_keywords = df_keywords['Từ khóa'].value_counts().reset_index()
    df_keywords.columns = ['Từ khóa', 'Số lượng']
    df_keywords = df_keywords.sort_values(by='Số lượng', ascending=False)
    #Vẽ word cloud
    wordcloud = WordCloud(width=800, height=400, background_color ='#0f1116').generate(df_keywords['Từ khóa'].to_string(index=False))
    st.image(wordcloud.to_image(), caption='Từ khóa phổ biến', use_column_width=True)

# with col[1]:


