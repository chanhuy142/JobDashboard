import streamlit as st
import pandas as pd

st.title('Tìm kiếm công việc theo nhu cầu')

df = pd.read_csv('data/cleaned_dataset.csv')

# Define all your categories and columns
categorical_columns = ['Khu vực tuyển', 'Yêu cầu giới tính', 'Cấp bậc', 'Hình thức làm việc', 'Yêu cầu bằng cấp', 'Yêu cầu kinh nghiệm', 'Loại công ty', 'Nhóm tuổi']
numerical_columns = ['Lương trung bình']
job_columns = ['Công việc chính', 'Công việc liên quan 1', 'Công việc liên quan 2']
all_columns = categorical_columns + numerical_columns + job_columns

# Check if all necessary columns exist in the DataFrame
for col in all_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' not found in DataFrame.")
        st.stop()



# Filtering logic as previously implemented
selections = {}
split_index = len(categorical_columns) // 2
categorical_row1 = categorical_columns[:split_index]
categorical_row2 = categorical_columns[split_index:]

row1_cols = st.columns(len(categorical_row1))
for idx, col_name in enumerate(categorical_row1):
    with row1_cols[idx]:
        options = ['Toàn bộ'] + df[col_name].unique().tolist()
        selections[col_name] = st.selectbox(f'{col_name}', options)

row2_cols = st.columns(len(categorical_row2))

# Generate options for job fields
job_options = set()
for col in job_columns:
    job_options.update(df[col].dropna().unique())

job_options = sorted(job_options)

for idx, col_name in enumerate(categorical_row2):
    with row2_cols[idx]:
        options = ['Toàn bộ'] + df[col_name].unique().tolist()
        selections[col_name] = st.selectbox(f'{col_name}', options)

selections['Ngành nghề'] = st.selectbox('Ngành nghề', ['Toàn bộ'] + job_options)


# Initial range values
overall_min = df[numerical_columns[0]].min()
overall_max = df[numerical_columns[0]].max()

# Inputs for custom salary range
st.subheader('Customize Salary Range')
col1, col2 = st.columns(2)
with col1:
    range_start = st.number_input('Start of Range', min_value=float(overall_min), max_value=float(overall_max), value=float(overall_min), step=1.0)
with col2:
    range_end = st.number_input('End of Range', min_value=float(overall_min), max_value=float(overall_max), value=float(overall_max), step=1.0)

# Adjust range if inputs are out of bounds
range_start = max(range_start, overall_min)
range_end = min(range_end, overall_max)

# Ensure start is not greater than end
if range_start > range_end:
    range_start, range_end = range_end, range_start

# Update slider with the adjusted range
selections[numerical_columns[0]] = st.slider('Lương trung bình', overall_min, overall_max, (range_start, range_end))

filtered_df = df.copy()
for feature, selected_value in selections.items():
    if selected_value != 'Toàn bộ':
        if feature == 'Ngành nghề':
            filtered_df = filtered_df[df[job_columns].apply(lambda x: selected_value in x.values, axis=1)]
        elif feature in categorical_columns:
            filtered_df = filtered_df[filtered_df[feature] == selected_value]
        elif feature in numerical_columns:
            filtered_df = filtered_df[(filtered_df[feature] >= selected_value[0]) & (filtered_df[feature] <= selected_value[1])]

total_job = filtered_df['Số lượng tuyển'].count()
st.markdown(f'Số lượng công việc phù hợp với yêu cầu của bạn: **{total_job}**')

# User selects which columns to display in the DataFrame using checkboxes, divided into four columns
st.text('Chọn các trường để hiển thị:')
selected_columns = []
checkbox_cols = st.columns(4)
col_index = 0
for col in filtered_df.columns:
    with checkbox_cols[col_index]:
        if st.checkbox(col, True):
            selected_columns.append(col)
    col_index = (col_index + 1) % 4

st.write('Các công việc phù hợp với yêu cầu của bạn:')
st.dataframe(filtered_df[selected_columns])
