import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv('cleaned_dataset.csv')

# Ensure column names match those in the DataFrame
categorical_columns = ['Khu vực tuyển', 'Yêu cầu giới tính', 'Cấp bậc', 'Hình thức làm việc', 'Yêu cầu bằng cấp', 'Yêu cầu kinh nghiệm', 'Loại công ty', 'Nhóm tuổi', 'Công việc chính']
numerical_columns = ['Lương trung bình']

# Check if all columns exist in the DataFrame
for col in categorical_columns + numerical_columns:
    if col not in df.columns:
        st.error(f"Column '{col}' not found in DataFrame.")
        st.stop()

# Create a dictionary to store the selected values
selections = {}

st.title('Tìm kiếm công việc')

# Split categorical columns into two rows
split_idx = len(categorical_columns) // 2
cat_columns_row1 = categorical_columns[:split_idx]
cat_columns_row2 = categorical_columns[split_idx:]

# Create columns for the first row of categorical filters
cat_cols_row1 = st.columns(len(cat_columns_row1))

# Loop through each categorical feature in the first row and create a selectbox for it
for idx, feature in enumerate(cat_columns_row1):
    if feature == 'Khu vực tuyển':
        options = ['Toàn bộ'] + list(set(', '.join(df[feature].dropna().unique()).split(', ')))
    else:
        options = ['Toàn bộ'] + df[feature].unique().tolist()  # Add 'Toàn bộ' option to the unique options list
    
    with cat_cols_row1[idx]:
        selections[feature] = st.selectbox(f'{feature}', options)

# Create columns for the second row of categorical filters
cat_cols_row2 = st.columns(len(cat_columns_row2))

# Loop through each categorical feature in the second row and create a selectbox for it
for idx, feature in enumerate(cat_columns_row2):
    # For 'Từ khóa', split values by ';' and get unique options
    if feature == 'Khu vực tuyển':
        options = ['Toàn bộ'] + list(set(', '.join(df[feature].dropna().unique()).split(', ')))
    else:
        options = ['Toàn bộ'] + df[feature].unique().tolist()  # Add 'Toàn bộ' option to the unique options list
    
    with cat_cols_row2[idx]:
        selections[feature] = st.selectbox(f'{feature}', options)

# Create sliders for numerical columns
for feature in numerical_columns:
    min_value = df[feature].min()
    max_value = df[feature].max()
    selections[feature] = st.slider(f'{feature}', min_value, max_value, (min_value, max_value))

# Filter the DataFrame based on selections
filtered_df = df.copy()
for feature, selected_value in selections.items():
    if feature in categorical_columns and selected_value != 'Toàn bộ':
        if feature == 'Từ khóa':
            filtered_df = filtered_df[filtered_df[feature].apply(lambda x: selected_value in x.split('; '))]
        else:
            filtered_df = filtered_df[filtered_df[feature] == selected_value]
    elif feature in numerical_columns:
        filtered_df = filtered_df[(filtered_df[feature] >= selected_value[0]) & (filtered_df[feature] <= selected_value[1])]

# Display the filtered DataFrame
st.write('Công việc phù hợp với yêu cầu của bạn:')
st.dataframe(filtered_df)
