#đếm sô luọng job theo từng loại bằng cấp
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd

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
    


col = st.columns((1,1), gap='small')

with col[0]:
    total_pos =df_filter['Số lượng tuyển'].count()
    total_pos = int(total_pos)
    #đếm số luọng công việc bằng tổng số lượn tuyển
    total_job = df_filter['Số lượng tuyển'].sum()
    #ép về int
    total_job = int(total_job)
    
    st.markdown('#### Tổng quan')

    st.markdown(f'<div style="width:50%;background-color:#262730;color:white;font-size:20px;border-radius:2px;text-align:center;padding:5px; padding-right:5px; padding-left:5px"> <div style="font-size: 30px; font-weight: bold">{total_pos}</div><div>Số công việc</div> </div>', 
                unsafe_allow_html=True)
    #make a little gap only space between the box and the next box
    st.markdown(f'<div style="height: 20px;"></div>', unsafe_allow_html=True)
    # tạo 1 box có witdh height và background color để hiển thị số lượng công việc
    st.markdown(f'<div style="width:50%;background-color:#262730;color:white;font-size:20px;border-radius:2px;text-align:center;padding:5px; padding-right:5px; padding-left:5px"> <div style="font-size: 30px; font-weight: bold">{total_job}</div><div>Số lượng tuyển</div> </div>', 
                unsafe_allow_html=True)
    #make a little gap only space between the box and the next box
    st.markdown(f'<div style="height: 20px;"></div>', unsafe_allow_html=True)
    

    total_job_title = df_filter['Công việc chính'].nunique()
    total_job_title = int(total_job_title)
    st.markdown(f'<div style="width:50%;background-color:#262730;color:white;font-size:20px;border-radius:2px;text-align:center;padding:5px; padding-right:5px; padding-left:5px; "> <div style="font-size: 30px; font-weight: bold">{total_job_title}</div><div>Ngành nghề</div> </div>',
    unsafe_allow_html=True)
    st.markdown(f'<div style="height: 50px;"></div>', unsafe_allow_html=True)

    #make histogram chart for Lương trung bình
    st.markdown('#### Lương trung bình')
    # vẽ histogram chart cho lương trung bình bằng plotly
    fig = px.histogram(df_reshaped, x='Lương trung bình', nbins=30)
    fig.update_layout(bargap=0.1, autosize=False, width=450, height=200)
    with st.container(height=200):
        st.plotly_chart(fig, use_container_width=True)

with col[1]:
    
        
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
    [1.0, "rgb(128, 0, 38)"]]
    
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
    fig.update_layout(title_text='Số lượng công việc tuyển theo khu vực', title_x=0.5, geo=dict(bgcolor= 'rgba(0,0,0,0)'), autosize=False, width=450, height=650)
    with st.container(height=650):
        st.plotly_chart(fig, use_container_width=True)
        
        






        

    
    
