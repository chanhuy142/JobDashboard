import streamlit as st
import pandas as pd

st.title('Tìm kiếm công việc theo nhu cầu')

# Load the dataset
df = pd.read_csv('./data/cleaned_dataset.csv')

# Define all categories and columns
categorical_columns = ['Khu vực tuyển', 'Yêu cầu giới tính', 'Cấp bậc', 'Hình thức làm việc', 'Yêu cầu bằng cấp', 'Yêu cầu kinh nghiệm', 'Loại công ty', 'Nhóm tuổi']
numerical_columns = ['Lương trung bình']
job_columns = ['Công việc chính', 'Công việc liên quan 1', 'Công việc liên quan 2']
all_columns = categorical_columns + numerical_columns + job_columns

# Initialize session state for filter visibility and selections if not already set
if 'show_filters' not in st.session_state:
    st.session_state.show_filters = False

def update_filters():
    # This function will be called to update the session state and filtered DataFrame
    st.session_state.filters_updated = True  # Trigger a rerun

# Button to toggle visibility of filters
if st.button('Toggle Filters'):
    st.session_state.show_filters = not st.session_state.show_filters

if st.session_state.show_filters:
    # Generate options for job fields
    job_options = set()
    for col in job_columns:
        job_options.update(df[col].dropna().unique())
    job_options = sorted(job_options)

    # Filtering logic and input controls
    split_index = len(categorical_columns) // 2
    row1_cols = st.columns(len(categorical_columns[:split_index]))
    row2_cols = st.columns(len(categorical_columns[split_index:]))

    for idx, col_name in enumerate(categorical_columns[:split_index]):
        with row1_cols[idx]:
            options = ['Toàn bộ'] + df[col_name].unique().tolist()
            current_selection = st.session_state.filters.get(col_name, 'Toàn bộ')
            st.session_state.filters[col_name] = st.selectbox(f'{col_name}', options, index=options.index(current_selection), on_change=update_filters)

    for idx, col_name in enumerate(categorical_columns[split_index:]):
        with row2_cols[idx]:
            options = ['Toàn bộ'] + df[col_name].unique().tolist()
            current_selection = st.session_state.filters.get(col_name, 'Toàn bộ')
            st.session_state.filters[col_name] = st.selectbox(f'{col_name}', options, index=options.index(current_selection), on_change=update_filters)

    # Select box for job category within the toggle section
    current_selection = st.session_state.filters.get('Ngành nghề', 'Toàn bộ')
    st.session_state.filters['Ngành nghề'] = st.selectbox('Ngành nghề', ['Toàn bộ'] + job_options, index=job_options.index(current_selection) if current_selection in job_options else 0, on_change=update_filters)

    # Custom salary range input controls linked with slider
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.filters['range_start'] = st.number_input('Start of Range', min_value=df[numerical_columns[0]].min(), max_value=df[numerical_columns[0]].max(), value=st.session_state.filters['range_start'], step=1.0, on_change=update_filters)
    with col2:
        st.session_state.filters['range_end'] = st.number_input('End of Range', min_value=df[numerical_columns[0]].min(), max_value=df[numerical_columns[0]].max(), value=st.session_state.filters['range_end'], step=1.0, on_change=update_filters)

    # Slider that updates based on number inputs
    range_start, range_end = st.slider('Lương trung bình', min_value=df[numerical_columns[0]].min(), max_value=df[numerical_columns[0]].max(), value=(st.session_state.filters['range_start'], st.session_state.filters['range_end']), step=1.0, on_change=update_filters)
    st.session_state.filters['range_start'], st.session_state.filters['range_end'] = range_start, range_end

# Apply the filter based on session state selections
filtered_df = df.copy()
for col_name, selected_value in st.session_state.filters.items():
    if selected_value != 'Toàn bộ' and col_name in categorical_columns:
        filtered_df = filtered_df[filtered_df[col_name] == selected_value]
if st.session_state.filters['Ngành nghề'] != 'Toàn bộ':
    filtered_df = filtered_df[df[job_columns].apply(lambda x: st.session_state.filters['Ngành nghề'] in x.values, axis=1)]
filtered_df = filtered_df[(filtered_df[numerical_columns[0]] >= st.session_state.filters['range_start']) & (filtered_df[numerical_columns[0]] <= st.session_state.filters['range_end'])]

# Display the count of jobs that match the selection
total_job = filtered_df['Số lượng tuyển'].count()
st.markdown(f'Số lượng công việc phù hợp với yêu cầu của bạn: **{total_job}**')

# Checkbox columns for selecting displayed DataFrame columns
st.text('Chọn các trường để hiển thị:')
selected_columns = []
checkbox_cols = st.columns(4)
col_index = 0
for col in filtered_df.columns:
    with checkbox_cols[col_index]:
        if st.checkbox(col, True):
            selected_columns.append(col)
    col_index = (col_index + 1) % 4

# Always display the resulting DataFrame
st.write('Các công việc phù hợp với yêu cầu của bạn:')
st.dataframe(filtered_df[selected_columns])
