#đếm sô luọng job theo từng loại bằng cấp
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd
st.set_page_config(
    page_title="Tình hình việc làm ở Việt Nam",
    
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
    

        
    

    
    


    



col = st.columns((0.7,1,1.7), gap='small')

with col[0]:
    #đếm số luọng công việc bằng tổng số lượn tuyển
    total_job = df_filter['Số lượng tuyển'].sum()
    #ép về int
    total_job = int(total_job)
    st.markdown('#### Tổng quan')
    # tạo 1 box có witdh height và background color để hiển thị số lượng công việc
    st.markdown(f'<div style="witdh:100;background-color:#262730;color:white;font-size:20px;border-radius:2px;text-align:center;padding:25px; padding-right:10px; padding-left:10px"> <div style="font-size: 30px; font-weight: bold">{total_job}</div><div>Công việc</div> </div>', 
                unsafe_allow_html=True)
    #make a little gap only space between the box and the next box
    st.markdown(f'<div style="height: 20px;"></div>', unsafe_allow_html=True)
    

    total_job_title = df_filter['Công việc chính'].nunique()
    total_job_title = int(total_job_title)
    st.markdown(f'<div style="witdh:100;background-color:#262730;color:white;font-size:20px;border-radius:2px;text-align:center;padding:25px; padding-right:10px; padding-left:10px; "> <div style="font-size: 30px; font-weight: bold">{total_job_title}</div><div>Công việc chính</div> </div>',
    unsafe_allow_html=True)
    st.markdown(f'<div style="height: 50px;"></div>', unsafe_allow_html=True)
    with st.container(height=360):
        #đếm số lượng ngành nghề băng cách đếm số lượng giá trị khác nhau trong cột ngành nghề
        #total_job_category = df_reshaped['Ngành nghề'].nunique()
        #đếm số công việc theo giới tính
        job_man = df_filter[df_filter['Yêu cầu giới tính'] == 'Nam']['Số lượng tuyển'].sum()
        job_woman = df_filter[df_filter['Yêu cầu giới tính'] == 'Nữ']['Số lượng tuyển'].sum()   
        #tạo dataframe mới để hiển thị số lượng công việc theo giới tính
        df_job = pd.DataFrame({'Giới tính': ['Nam', 'Nữ'], 'Số lượng công việc': [job_man,job_woman]})
        #pie chart, kéo gần cái label vào được hong
        fig = px.pie(df_job, values='Số lượng công việc', names='Giới tính', color='Giới tính', color_discrete_map={'Nam':'pink', 'Nữ':'blue'})
        fig.update_traces(textposition='outside')
        fig.update_layout(title={
            'text': "Số lượng công việc theo giới tính",
            },uniformtext_minsize=12, uniformtext_mode='hide',autosize=False, width=350, height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    
    
with col[1]:
    with st.container(height=350):
        #lấy ra các loại bằng cấp, đếm công việc theo từng loại, tạo dataframe mới rồi ve bar chart
        df_degree = df_filter['Yêu cầu bằng cấp'].value_counts().reset_index()
        df_degree.columns = ['Yêu cầu bằng cấp', 'Số lượng công việc']
        fig=px.pie(df_degree, values='Số lượng công việc', names='Yêu cầu bằng cấp', color='Yêu cầu bằng cấp')
        
        fig.update_traces(textposition='inside')
        fig.update_layout(title={
            'text': "Số lượng công việc theo bằng cấp",
            },uniformtext_minsize=7, uniformtext_mode='hide'
        )
        st.plotly_chart(fig, use_container_width=False)
    st.markdown(f'<div style="height: 20px;"></div>', unsafe_allow_html=True)
    with st.container(height=350):
        #lấy ra các loại Nhóm tuổi, đếm công việc theo từng loại, tạo dataframe mới rồi ve pie chart
        df_age = df_filter['Nhóm tuổi'].value_counts().reset_index()
        df_age.columns = ['Nhóm tuổi', 'Số lượng công việc']
        fig=px.pie(df_age, values='Số lượng công việc', names='Nhóm tuổi', color='Nhóm tuổi')
        fig.update_traces(textposition='inside')
        fig.update_layout(title={
            'text': "Số lượng công việc theo nhóm tuổi",
            },uniformtext_minsize=7, uniformtext_mode='hide'
        )
        st.plotly_chart(fig, use_container_width=False)

with col[2]:
    with st.container(height=350):
        #ve hbar chart top 10 ngành nghề có số lượng công việc lớn nhất
        df_job_category = df_filter.groupby('Công việc chính')['Số lượng tuyển'].sum().reset_index()
        df_job_category = df_job_category.sort_values('Số lượng tuyển', ascending=False).head(10)
        fig = px.bar(df_job_category, x='Số lượng tuyển', y='Công việc chính', orientation='h')
        fig.update_layout(title={
            'text': "Top 10 công việc có số lượng tuyển lớn nhất",
            },uniformtext_minsize=7, uniformtext_mode='hide'
        )
        st.plotly_chart(fig, use_container_width=False)
        
    #create world map

    st.markdown(f'<div style="height: 20px;"></div>', unsafe_allow_html=True)
    area_df = pd.Series(df_reshaped['Khu vực tuyển']).str.split(',').explode().str.strip()
    area_df = pd.DataFrame(area_df.value_counts())
    area_df.reset_index(inplace=True)
    area_df.columns = ['Khu vực', 'Số lượng']
    
        # Đọc bản đồ
    vietnam_map = gpd.read_file('vietnam.geojson')

    # Chuẩn hóa tên tỉnh thành
    vietnam_map = vietnam_map.replace({"Hồ Chí Minh city": "TP.HCM"})
    vietnam_map = vietnam_map.replace({"Thừa Thiên - Huế": "Thừa Thiên Huế"})
    print(list(vietnam_map['name']))

    # Merge dữ liệu
    merged = vietnam_map.set_index('name').join(area_df.set_index('Khu vực'))

    # Prepare data for Plotly
    merged = merged.reset_index()
    custom_colorscale = [
    [0.0, "rgb(255, 255, 204)"],
    [0.01, "rgb(255, 237, 160)"],
    [0.015, "rgb(254, 200, 118)"],
    [0.03, "rgb(254, 178, 76)"],

    [0.1, "rgb(189, 0, 38)"],
    [1.0, "rgb(128, 0, 38)"]
]
    
    with st.container(height=350):
        fig = px.choropleth(merged,
                        geojson=merged.geometry,
                        locations=merged.index,
                        color="Số lượng",
                        hover_name="name",
                        hover_data=["Số lượng"],
                        color_continuous_scale=custom_colorscale,
                        labels={'Số lượng':'Số lượng công việc'},
                        projection="mercator",
                       

                        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_text='Số lượng công việc tuyển theo khu vực', title_x=0.5, geo=dict(bgcolor= 'rgba(0,0,0,0)'),)
        st.plotly_chart(fig, use_container_width=True)
        






        

    
    
