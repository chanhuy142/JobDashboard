import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from wordcloud import WordCloud

st.set_page_config(
    page_title="Tình hình việc làm ở Việt Nam",
    page_icon="📊",
    layout="wide",
)
df_reshaped = pd.read_csv("cleaned_dataset.csv")

with st.sidebar:
    st.title("Tình hình việc làm ở Việt Nam")
    # Split and explode the 'Khu vực tuyển' column
    df_exploded = df_reshaped.assign(
        **{"Khu vực tuyển": df_reshaped["Khu vực tuyển"].str.split(",")}
    ).explode("Khu vực tuyển")

    # Strip any leading/trailing whitespace from the 'Khu vực tuyển' column
    df_exploded["Khu vực tuyển"] = df_exploded["Khu vực tuyển"].str.strip()

    # tạo list tỉnh thành, có 1 loại là Tất cả
    area_list = ["Tất cả"] + list(df_exploded["Khu vực tuyển"].unique())
    # tạo selectbox để chọn tỉnh thành
    area = st.selectbox("Chọn khu vực tuyển", area_list)
    # tạo df_area để lọc theo khu vực tuyển
    if area != "Tất cả":
        df_filter = df_exploded[df_exploded["Khu vực tuyển"] == area]
    else:
        df_filter = df_reshaped
    # Chọn nhóm tuổi
    age_list = ["Tất cả"] + list(df_filter["Nhóm tuổi"].unique())
    age = st.selectbox("Chọn nhóm tuổi", age_list)
    # lọc theo nhóm tuổi
    if age != "Tất cả":
        df_filter = df_filter[df_filter["Nhóm tuổi"] == age]
    else:
        df_filter = df_filter

    # Chọn bằng cấp
    degree_list = ["Tất cả"] + list(df_filter["Yêu cầu bằng cấp"].unique())
    degree = st.selectbox("Chọn bằng cấp", degree_list)
    # lọc theo bằng cấp
    if degree != "Tất cả":
        df_filter = df_filter[df_filter["Yêu cầu bằng cấp"] == degree]
    else:
        df_filter = df_filter

st.title("Phân tích chi tiết về thông tin tuyển dụng")
col1, col2 = st.columns(2, gap="small")
col3, col4 = st.columns(2, gap="small")
with col1:
    # Giả sử bạn đã có dữ liệu df_highsalary
    upper_quartile = df_reshaped["Lương trung bình"].quantile(0.75)
    df_highsalary = df_reshaped[
        df_reshaped["Lương trung bình"] >= upper_quartile
    ]
    df_exp = df_reshaped.copy()
    df_copy_grouped = df_exp.groupby("Công việc chính")["Số lượng tuyển"].sum()
    df_copy_grouped = pd.DataFrame(df_copy_grouped)
    df_highsalary_grouped = df_highsalary.groupby("Công việc chính")[
        "Số lượng tuyển"
    ].sum()
    df_highsalary_grouped = pd.DataFrame(df_highsalary_grouped)
    df_highsalary = pd.merge(
        df_highsalary_grouped, df_copy_grouped, on="Công việc chính"
    )
    df_highsalary.reset_index(inplace=True)
    df_highsalary.columns = [
        "Ngành nghề",
        "Số lượng tuyển lương cao",
        "Tổng số lượng tuyển",
    ]
    df_highsalary["Tỉ lệ công việc lương cao"] = (
        df_highsalary["Số lượng tuyển lương cao"]
        / df_highsalary["Tổng số lượng tuyển"]
        * 100
    )
    df_highsalary.sort_values(
        by="Tỉ lệ công việc lương cao", ascending=False, inplace=True
    )
    df_highsalary.reset_index(inplace=True)
    df_highsalary.drop(
        columns=["index", "Số lượng tuyển lương cao"], inplace=True
    )

    # Tạo subplot với một trục y bên trái và một trục y bên phải
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Thêm biểu đồ line vào subplot cho Tỉ lệ công việc lương cao
    fig.add_trace(
        go.Scatter(
            x=df_highsalary["Ngành nghề"].head(10),
            y=df_highsalary["Tỉ lệ công việc lương cao"].head(10),
            name="Tỉ lệ công việc lương cao",
            line=dict(color="blue"),
        ),
        secondary_y=False,
    )

    # Thêm biểu đồ bar vào subplot cho Tổng số lượng tuyển
    fig.add_trace(
        go.Bar(
            x=df_highsalary["Ngành nghề"].head(10),
            y=df_highsalary["Tổng số lượng tuyển"].head(10),
            name="Tổng số lượng tuyển",
        ),
        secondary_y=True,
    )

    # Cập nhật layout
    fig.update_layout(
        title_text="Top 10 ngành nghề có tỉ lệ công việc lương cao",
        xaxis_tickangle=-45,
        legend=dict(x=1, y=1, xanchor="right", yanchor="top"),
        height=500,
        width=600,
    )

    # Cập nhật tiêu đề cho các trục y
    fig.update_yaxes(title_text="Tỉ lệ công việc lương cao", secondary_y=False)
    fig.update_yaxes(title_text="Tổng số lượng tuyển", secondary_y=True)

    st.plotly_chart(fig)

with col3:

    st.markdown("###### **Từ khóa phổ biến**")

    # Split các giá trị trong cột 'Từ khoá' và vẽ word cloud
    df_reshaped["Từ khóa"] = df_reshaped["Từ khóa"].str.split("; ")
    df_keywords = df_reshaped.explode("Từ khóa")
    df_keywords = df_keywords["Từ khóa"].value_counts().reset_index()
    df_keywords.columns = ["Từ khóa", "Số lượng"]
    df_keywords = df_keywords.sort_values(by="Số lượng", ascending=False)
    # Vẽ word cloud
    wordcloud = WordCloud(
        width=800, height=400, background_color="#0f1116"
    ).generate(df_keywords["Từ khóa"].to_string(index=False))
    st.image(
        wordcloud.to_image(),
        caption="Từ khóa phổ biến",
        use_column_width=True,
    )
    # Thêm tiêu đề cho wordcloud bằng kích thước tiêu đề của các biểu đồ khác


with col4:
    df_grouped = (
        df_reshaped.groupby("Công việc chính")["Lượt xem"].sum().reset_index()
    )

    # Lấy top 10 công việc chính có nhiều lượt xem nhất
    df_top10 = df_grouped.nlargest(10, "Lượt xem")

    # Vẽ Tree Map
    fig = px.treemap(
        df_top10,
        path=["Công việc chính"],
        values="Lượt xem",
        title="Top 10 công việc chính có nhiều lượt xem nhất",
        color="Lượt xem",
        color_continuous_scale=px.colors.sequential.Sunset,
        height=500,
        width=600,
    )

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    st.plotly_chart(fig)

with col2:
    # Hàm để xử lý việc thêm giây nếu thiếu
    def ensure_full_datetime(date_str):
        if pd.isna(date_str):
            return date_str
        if (
            len(date_str) == 16
        ):  # Kiểm tra nếu độ dài chuỗi là 'YYYY-MM-DD HH:MM' hoặc 'DD/MM/YYYY HH:MM'
            return date_str + ":00"
        return date_str

    # Áp dụng hàm để đảm bảo tất cả các giá trị datetime đều có giây
    df_reshaped["Ngày cập nhật"] = df_reshaped["Ngày cập nhật"].apply(
        ensure_full_datetime
    )

    # Chuyển đổi cột 'Ngày cập nhật' thành kiểu datetime, cho phép suy luận định dạng
    df_reshaped["Ngày cập nhật"] = pd.to_datetime(
        df_reshaped["Ngày cập nhật"],
        infer_datetime_format=True,
        dayfirst=True,
        errors="coerce",
    )

    # Loại bỏ các giá trị NaT
    df_reshaped = df_reshaped.dropna(subset=["Ngày cập nhật"])

    # Tạo cột ngày
    df_reshaped["Ngày"] = df_reshaped["Ngày cập nhật"].dt.date

    # Tính tổng số lượng tuyển theo ngày
    df_daily = df_reshaped.groupby("Ngày")["Số lượng tuyển"].sum().reset_index()

    # Vẽ biểu đồ đường
    fig = px.line(
        df_daily, x="Ngày", y="Số lượng tuyển", title="Số bài đăng theo ngày"
    )

    # Cập nhật layout để hiển thị ngày và tháng, và xoay nhãn trục x 45 độ
    fig.update_layout(
        xaxis_title="Ngày",
        yaxis_title="Số lượng tuyển",
        xaxis_tickformat="%d-%m",
        xaxis=dict(tickangle=-45),
        height=500,
        width=600,
    )

    st.plotly_chart(fig)
