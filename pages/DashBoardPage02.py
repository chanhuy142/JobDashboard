import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

# Set page configuration
st.set_page_config(
    page_title="Tình hình việc làm ở Việt Nam",
    page_icon="📊",
    layout="wide",
)


df = pd.read_csv('data/cleaned_dataset.csv')

# Explode and clean the 'Khu vực tuyển' column
df_exploded = df.assign(**{
    'Khu vực tuyển': df['Khu vực tuyển'].str.split(',')
}).explode('Khu vực tuyển')
df_exploded['Khu vực tuyển'] = df_exploded['Khu vực tuyển'].str.strip()

# Các ngành nghề
job_titles = set(df['Công việc chính'].unique()).union(
    set(df['Công việc liên quan 1'].unique())).union(
    set(df['Công việc liên quan 2'].unique()))

job_titles = ['Tất cả'] + sorted([title for title in job_titles if pd.notna(title)])

# Sidebar
with st.sidebar:
    st.title('Tình hình việc làm ở Việt Nam')

    # Filter by area
    area_list = ['Tất cả'] + list(df_exploded['Khu vực tuyển'].unique())
    area = st.selectbox('Chọn khu vực tuyển', area_list)
    if area != 'Tất cả':
        df_filter = df_exploded[df_exploded['Khu vực tuyển'] == area]
    else:
        df_filter = df

    # Filter by job title
    job_title = st.selectbox('Chọn ngành nghề', job_titles)
    if job_title != 'Tất cả':
        df_filter = df_filter[
            (df_filter['Công việc chính'] == job_title) |
            (df_filter['Công việc liên quan 1'] == job_title) |
            (df_filter['Công việc liên quan 2'] == job_title)
        ]

    # Filter by age group
    age_list = ['Tất cả'] + list(df['Nhóm tuổi'].unique())
    age = st.selectbox('Chọn nhóm tuổi', age_list)
    if age != 'Tất cả':
        df_filter = df_filter[df_filter['Nhóm tuổi'] == age]

    # Filter by gender
    gender_list = ['Tất cả'] + list(df['Yêu cầu giới tính'].unique())
    gender = st.selectbox('Chọn yêu cầu giới tính', gender_list)
    if gender != 'Tất cả':
        df_filter = df_filter[df_filter['Yêu cầu giới tính'].str.contains(gender)]

    # Filter by job level
    level_list = ['Tất cả'] + list(df['Cấp bậc'].unique())
    level = st.selectbox('Chọn cấp bậc', level_list)
    if level != 'Tất cả':
        df_filter = df_filter[df_filter['Cấp bậc'] == level]

    #  job type
    job_type_list = ['Tất cả'] + list(df['Hình thức làm việc'].unique())
    job_type = st.selectbox('Chọn hình thức làm việc', job_type_list)
    if job_type != 'Tất cả':
        df_filter = df_filter[df_filter['Hình thức làm việc'] == job_type]

    # education
    education_list = ['Tất cả'] + list(df['Yêu cầu bằng cấp'].unique())
    education = st.selectbox('Chọn yêu cầu bằng cấp', education_list)
    if education != 'Tất cả':
        df_filter = df_filter[df_filter['Yêu cầu bằng cấp'] == education]

    # experience
    experience_list = ['Tất cả'] + list(df['Yêu cầu kinh nghiệm'].unique())
    experience = st.selectbox('Chọn yêu cầu kinh nghiệm', experience_list)
    if experience != 'Tất cả':
        df_filter = df_filter[df_filter['Yêu cầu kinh nghiệm'] == experience]

st.title("Phân tích chi tiết mức lương")

col1, col2, col3 = st.columns([2, 3, 2])
col4, col5, col6 = st.columns(3)

with col1:
    st.subheader("Phân bố mức lương trung bình theo giới tính")
    # Biểu đồ histogram cho mức lương trung bình, phân biệt theo giới tính
    fig = px.histogram(df_filter, x='Lương trung bình', nbins=30, color_discrete_sequence=['skyblue'])
    fig.update_traces(opacity=0.75)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Box plot mức lương trung bình theo giới tính")
    #  box plot cho mức lương trung bình theo giới tính
    fig = px.box(df_filter, x='Yêu cầu giới tính', y='Lương trung bình', color='Yêu cầu giới tính', 
                 color_discrete_map={'Nam': 'skyblue', 'Nữ': 'salmon', 'Không yêu cầu': 'lightgreen'})
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("Số lượng công việc theo cấp bậc")
    # Bar Chart
    df_job_level = df_filter['Cấp bậc'].value_counts().reset_index()
    df_job_level.columns = ['Cấp bậc', 'Số lượng công việc']
    fig = px.bar(df_job_level, x='Cấp bậc', y='Số lượng công việc', color='Cấp bậc')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Hình thức làm việc")
    # Biểu đồ pie
    df_job_type = df_filter['Hình thức làm việc'].value_counts().reset_index()
    df_job_type.columns = ['Hình thức làm việc', 'Số lượng công việc']
    fig = px.pie(df_job_type, values='Số lượng công việc', names='Hình thức làm việc', color='Hình thức làm việc')
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("Biểu đồ Yêu cầu bằng cấp")
    # Biểu đồ bar
    df_degree = df_filter['Yêu cầu bằng cấp'].value_counts().reset_index()
    df_degree.columns = ['Yêu cầu bằng cấp', 'Số lượng công việc']
    fig = px.bar(df_degree, x='Số lượng công việc', y='Yêu cầu bằng cấp', orientation='h', color='Yêu cầu bằng cấp')
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Biểu đồ Yêu cầu kinh nghiệm")
    # Biểu đồ donut
    df_experience = df_filter['Yêu cầu kinh nghiệm'].value_counts().reset_index()
    df_experience.columns = ['Yêu cầu kinh nghiệm', 'Số lượng công việc']
    fig = px.pie(df_experience, values='Số lượng công việc', names='Yêu cầu kinh nghiệm', hole=0.3)
    st.plotly_chart(fig, use_container_width=True)
