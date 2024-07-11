import streamlit as st
import joblib
import pandas as pd

# Cấu hình giao diện người dùng
st.title("Mức Lương và Mức độ cạnh tranh của công việc mà bạn đang quan tâm ")
st.write("Hãy cho chúng tôi thông tin về công việc của bạn để dự đoán")

# Định nghĩa các tên cột và tiêu đề tương ứng
label_encoded_columns = [
    'Recruitment_Area', 'Gender_Requirement', 'Level', 'Working_Form',
    'Degree_Requirement', 'Experience_Requirement', 'Company_Type',
    'Age_Group', 'Main_Job', 'Related_Job1', 'Related_Job2'
]

column_translations = {
    'Recruitment_Area': "Khu vực bạn muốn làm việc là?",
    'Gender_Requirement': "Yêu cầu giới tính của bạn là?",
    'Level': "Cấp bậc của bạn là?",
    'Working_Form': "Hình thức làm việc của bạn là?",
    'Degree_Requirement': "Yêu cầu bằng cấp của bạn là?",
    'Experience_Requirement': "Yêu cầu kinh nghiệm của bạn là?",
    'Company_Type': "Loại hình công ty bạn muốn làm việc?",
    'Age_Group': "Nhóm tuổi của bạn?",
    'Main_Job': "Công việc chính của bạn là?",
    'Related_Job1': "Công việc có thể liên quan 1 của bạn là?",
    'Related_Job2': "Công việc có thể liên quan 2 của bạn là?"
}

# Tải mô hình dự đoán lương
salary_model = joblib.load("./models/Salary_Model/KNN.pkl")

# Tải mô hình dự đoán số người quan tâm
interest_model = joblib.load("./models/Views_Model/KNN.pkl")

# Tải Label Encoders
label_encoders = {
    col: joblib.load(f"./models/Label_Encoders/{col}.pkl")
    for col in label_encoded_columns
}

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    h1 {
        color: #333;
    }
    .highlight {
        font-size: 24px;
        font-weight: bold;
        color: #ff6347;
    }
    .column-label {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tạo các input cho người dùng nhập liệu
user_input = {}
for col in label_encoded_columns:
    if col not in ['Main_Job', 'Related_Job1', 'Related_Job2']:
        options = label_encoders[col].classes_
        user_input[col] = st.selectbox(column_translations[col], options)

# Đảm bảo các trường Main_Job, Related_Job1, và Related_Job2 không trùng nhau
main_job = st.selectbox(column_translations['Main_Job'], label_encoders['Main_Job'].classes_)
related_job1 = st.selectbox(column_translations['Related_Job1'], label_encoders['Related_Job1'].classes_)
if related_job1 == "Không yêu cầu thêm":
    related_job2 = "Không yêu cầu thêm"
else:
    related_job2 = st.selectbox(column_translations['Related_Job2'], label_encoders['Related_Job2'].classes_)

if main_job == related_job1 or main_job == related_job2 or (related_job1 != "Không yêu cầu thêm" and related_job1 == related_job2):
    st.warning("Các công việc không được chọn trùng nhau.")
else:
    user_input['Main_Job'] = main_job
    user_input['Related_Job1'] = related_job1
    user_input['Related_Job2'] = related_job2

    # Khi nhấn nút "Dự đoán"
    if st.button("Dự đoán"):
        input_data = pd.DataFrame([user_input])

        # Áp dụng Label Encoding cho các cột phân loại
        for col in label_encoded_columns:
            input_data[col] = label_encoders[col].transform(input_data[col])

        # Dự đoán mức lương và số người quan tâm
        salary_prediction = salary_model.predict(input_data)
        interest_prediction = interest_model.predict(input_data)

        # Hiển thị kết quả
        st.markdown(f"<div class='highlight'>Mức lương chúng tôi dự đoán cho bạn là: {salary_prediction[0]:,.2f} triệu</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='highlight'>Có {interest_prediction[0]:,.0f} người đang quan tâm đến công việc này giống bạn</div>", unsafe_allow_html=True)
