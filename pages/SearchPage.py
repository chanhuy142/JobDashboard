import streamlit as st
import pandas as pd

df = pd.read_csv('cleaned_dataset.csv')

categorical_columns = ['Khu vực tuyển', 'Yêu cầu giới tính', 'Cấp bậc', 'Hình thức làm việc', 'Yêu cầu bằng cấp', 'Yêu cầu kinh nghiệm', 'Loại công ty', 'Nhóm tuổi']
numerical_columns = ['Lương trung bình']
job_columns = ['Công việc chính', 'Công việc liên quan 1', 'Công việc liên quan 2']

for col in categorical_columns + numerical_columns + job_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' not found in DataFrame.")
        st.stop()

job_options = set()
for col in job_columns:
    job_options.update(df[col].dropna().unique())

job_options = sorted(job_options)

selections = {}

st.title('Tìm kiếm công việc')

split_index = len(categorical_columns) // 2
categorical_row1 = categorical_columns[:split_index]
categorical_row2 = categorical_columns[split_index:]

row1_cols = st.columns(len(categorical_row1))
for idx, col_name in enumerate(categorical_row1):
    with row1_cols[idx]:
        options = ['Toàn bộ'] + df[col_name].unique().tolist()
        selections[col_name] = st.selectbox(f'{col_name}', options)

row2_cols = st.columns(len(categorical_row2))
for idx, col_name in enumerate(categorical_row2):
    with row2_cols[idx]:
        options = ['Toàn bộ'] + df[col_name].unique().tolist()
        selections[col_name] = st.selectbox(f'{col_name}', options)

selections['Ngành nghề'] = st.selectbox('Ngành nghề', ['Toàn bộ'] + job_options)

for feature in numerical_columns:
    min_value = df[feature].min()
    max_value = df[feature].max()
    selections[feature] = st.slider(f'{feature}', min_value, max_value, (min_value, max_value))

filtered_df = df.copy()
for feature, selected_value in selections.items():
    if selected_value != 'Toàn bộ':
        if feature == 'Ngành nghề':
            filtered_df = filtered_df[df[job_columns].apply(lambda x: selected_value in x.values, axis=1)]
        elif feature in categorical_columns:
            filtered_df = filtered_df[filtered_df[feature] == selected_value]
        elif feature in numerical_columns:
            filtered_df = filtered_df[(filtered_df[feature] >= selected_value[0]) & (filtered_df[feature] <= selected_value[1])]

total_job = filtered_df['Số lượng tuyển'].sum()
total_job = int(total_job)

st.markdown(f'Số lượng công việc phù hợp với yêu cầu của bạn: **{total_job}**')

st.write('Công việc phù hợp với yêu cầu của bạn:')
st.dataframe(filtered_df.drop(columns=['Ngày cập nhật', 'Lượt xem']))
