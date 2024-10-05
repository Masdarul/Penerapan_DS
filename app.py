import streamlit as st 
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")  # wide or centered

# Load the data
df = pd.read_csv("data/data_baru.csv", delimiter=",")
df_0 = df.loc[df['Status'] == 0]
df_1 = df.loc[df['Status'] == 1]
df_2 = df.loc[df['Status'] == 2]

# Category mapping for the 'Course' column
category = {
    33: 'Biofuel Production Technologies',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy',
    9070: 'Communication Design',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Nursing',
    9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management',
    9773: 'Journalism and Communication',
    9853: 'Basic Education',
    9991: 'Management (evening attendance)'
}
df['Course_Label'] = df['Course'].replace(category)

# Title and introduction
st.title(":blue[Jaya Jaya Institute Student Performance]")
st.write("""
        Oleh: Masdarul Rizqi
        """)

# Tabs setup
tab1, tab2, tab3 = st.tabs(["Beranda", "Dashboard", "Prediction"])

# Tab 1 - Beranda
with tab1:
    st.header("Background")
    st.write("""
    **Jaya Jaya Institut** merupakan salah satu institusi pendidikan tinggi yang telah berdiri sejak tahun 2000. 
    Hingga saat ini, institut ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun, 
    terdapat juga sejumlah siswa yang tidak menyelesaikan pendidikannya atau dropout.
    
    Jumlah siswa dropout yang tinggi menjadi salah satu tantangan besar bagi sebuah institusi pendidikan. 
    Oleh karena itu, **Jaya Jaya Institut** ingin mendeteksi secepat mungkin siswa yang mungkin akan melakukan 
    dropout, sehingga mereka dapat diberikan bimbingan dan dukungan khusus.
    
    Sebagai calon data scientist, Anda diminta untuk membantu Jaya Jaya Institut dalam menyelesaikan 
    permasalahan ini dengan menganalisis faktor-faktor yang dapat memprediksi kemungkinan siswa melakukan dropout.
    """)
    st.markdown("### Permasalahan Bisnis")
    st.markdown("""
    * Atribut mana yang paling berhubungan dengan status mahasiswa
    * Seberapa besar dropout rate dan graduation rate secara keseluruhan
    * Bagaimana hubungan penerimaan mahasiswa dengan status mahasiswa
    * Bagaimana nilai masuk memengaruhi status mahasiswa
    * Bagaimana cara mengidentifikasi mahasiswa yang akan melakukan dropout
    """)

# Tab 2 - Dashboard
with tab2:
    st.header("Dashboard")

    # Function for formatting cards
    def add_card(content):
        return f"""
        <div style='height: auto; border: 2px solid #ccc; border-radius: 5px; padding: 10px; margin-bottom: 10px; text-align: center;'>{content}</div>
        """
    
    # Function for creating pie charts
    def create_pie_chart(df, column, title):
        value_counts = df[column].value_counts()
        labels = value_counts.index
        values = value_counts.values
        fig = px.pie(df, values=values, names=labels, title=title)
        st.plotly_chart(fig)

    # Function for creating bar charts
    def create_bar_chart(df, title):
        value_counts = df.value_counts()
        fig = px.bar(value_counts, x=value_counts.index, y=value_counts.values, labels={'x': title, 'y': 'Count'})
        st.plotly_chart(fig)
    
    # Dashboard filters (Status, Course, Time, Gender)
    col1, col2, col3, col4 = st.columns(4)
    
    # Filter 1: Status
    status_dict = {'None': None, 'Dropout': 0, 'Enrolled': 1, 'Graduated': 2}
    selected_status = col1.selectbox('Select status', list(status_dict.keys()))
    if status_dict[selected_status] is not None:
        df = df[df['Status'] == status_dict[selected_status]]
    
    # Filter 2: Course
    course_list = ['None'] + list(df['Course_Label'].unique())
    selected_course = col2.selectbox('Select course', course_list)
    if selected_course != "None":
        df = df[df['Course_Label'] == selected_course]
    
    # Filter 3: Time
    time_dict = {'None': None, 'Daytime': 1, 'Evening': 0}
    selected_time = col3.selectbox('Select attendance time', list(time_dict.keys()))
    if time_dict[selected_time] is not None:
        df = df[df['Daytime_evening_attendance'] == time_dict[selected_time]]
    
    # Filter 4: Gender
    gender_dict = {'None': None, 'Male': 1, 'Female': 0}
    selected_gender = col4.selectbox('Select gender', list(gender_dict.keys()))
    if gender_dict[selected_gender] is not None:
        df = df[df['Gender'] == gender_dict[selected_gender]]
    
    # Display Key Metrics (Dropout, Enrolled, Graduated)
    if len(df) > 0:
        dropout_rate = round((len(df[df['Status'] == 0]) / len(df)) * 100, 2)
        enrolled_rate = round((len(df[df['Status'] == 1]) / len(df)) * 100, 2)
        graduation_rate = round((len(df[df['Status'] == 2]) / len(df)) * 100, 2)
    else:
        dropout_rate = 0
        enrolled_rate = 0
        graduation_rate = 0

    colDr, colSt = st.columns([1, 2])
    with colDr:
        st.markdown(add_card(f"<b>Dropout Rate:</b> {dropout_rate}%"), unsafe_allow_html=True)
    with colSt:
        st.markdown(add_card(f"<b>Total Students:</b> {len(df)}"), unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.markdown(add_card(f"<b>Dropout:</b> {len(df[df['Status'] == 0])}"), unsafe_allow_html=True)
        col2.markdown(add_card(f"<b>Enrolled:</b> {len(df[df['Status'] == 1])}"), unsafe_allow_html=True)
        col3.markdown(add_card(f"<b>Graduated:</b> {len(df[df['Status'] == 2])}"), unsafe_allow_html=True)
    
    # Scholarship by status and Average Grade per Semester
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Scholarship Holder by Status')
        create_pie_chart(df, 'Scholarship_holder', 'Scholarship Holders')
    
    with col2:
        st.subheader('Average Grade per Semester')
        try:
            avg_grade_1st_sem = df.groupby('Status')['Curricular_units_1st_sem_grade'].mean()
            avg_grade_2nd_sem = df.groupby('Status')['Curricular_units_2nd_sem_grade'].mean()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=avg_grade_1st_sem.index, y=avg_grade_1st_sem, name='1st Semester'))
            fig.add_trace(go.Bar(x=avg_grade_2nd_sem.index, y=avg_grade_2nd_sem, name='2nd Semester'))
            st.plotly_chart(fig)
        except:
            st.write("No data available")

    # New visualizations for Gender, Course, and Attendance Time
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('Student Count by Gender')
        df_gender = df['Gender'].replace({1: 'Male', 0: 'Female'})
        create_bar_chart(df_gender, 'Gender Distribution')
    
    with col2:
        st.subheader('Dropout Rate by Course')

        # Calculate dropout rate per course
        total_course = df.groupby('Course_Label')['Status'].apply(lambda x: (x == 0).mean() * 100).sort_values(ascending=False)
        labels = total_course.index.tolist()

        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")  # Set background style
        palette = sns.color_palette("Set2", len(total_course))  # Choose a color palette
        bars = sns.barplot(x=total_course, y=labels, palette=palette)

        # Adding titles and labels
        plt.title('Dropout Rate by Course', fontsize=16, fontweight='bold', color='darkblue')
        plt.xlabel('Dropout Rate (%)', fontsize=14)
        plt.ylabel('Course', fontsize=14)

        # Adding value labels on top of the bars
        for i, rate in enumerate(total_course):
            plt.text(rate + 1, i, f'{rate:.2f}%', ha='center', va='center', fontsize=10, color='black')

        # Customize the background color
        plt.gca().set_facecolor('lightgrey')

        # Display the plot
        plt.tight_layout()
        st.pyplot(plt)

    with col3:
        st.subheader('Student Count by Attendance Time')
        df_attendance = df['Daytime_evening_attendance'].replace({1: 'Daytime', 0: 'Evening'})
        create_bar_chart(df_attendance, 'Attendance Time')

# Tab 3 - Prediction (not implemented here)
with tab3:
    st.header("Prediction")
    st.subheader("Prediction")
    course_list = list(df.Course_Label.unique())[::-1]
    course_list.sort()

    if 'pred_selected' not in st.session_state:
        st.session_state.pred_selected = None

    if st.session_state.pred_selected is None:
        course_selected = st.selectbox('Course', ['None', *course_list])
    else:
        course_selected = st.selectbox('Course', course_list)

    if course_selected == 'None':
        st.error("Please select a valid course.")
    else:
        st.session_state.course_selected = course_selected

    reverse_mapping = {v: k for k, v in category.items()}

    if course_selected != 'None':
        course_selected = reverse_mapping[course_selected]

    # ===============================================================

    if course_selected in [9991, 8014]:
        time_selected=0
    else:
        time_selected=1

    # ===============================================================

    admgrade_selected = st.number_input("Admission grade", value=0.0, step=0.1, min_value=0.0, max_value=200.0)
    admgrade_selected = round(admgrade_selected,1)

    # ===============================================================

    colGender, colAge = st.columns(2)

    with colGender:
        gender_list = ['Male', 'Female']
        gender_selected = st.selectbox('Gender', (gender_list))

        if gender_selected=="Female":
            gender_selected=0
        elif gender_selected=="Male":
            gender_selected=1

    with colAge:
        age_selected = st.number_input("Age at enrollment", step=1, min_value=17, max_value=70)

    # ===============================================================
    bool1, bool2 = st.columns(2)

    with bool1:
        special_list = ['Yes', 'No']
        special_selected = st.radio('Special education needs?', (special_list))

        if (special_selected=="No"):
            special_selected=0
        elif(special_selected=="Yes"):
            special_selected=1
        
    # ===============================================================
    with bool2:
        debtor_list = ['Yes', 'No']
        debtor_selected = st.radio('Debtor?', (debtor_list))

        if (debtor_selected=="No"):
            debtor_selected=0
        elif(debtor_selected=="Yes"):
            debtor_selected=1

    # ===============================================================
    bool3, bool4 = st.columns(2)
    with bool3:
        tuition_list = ['Yes', 'No']
        tuition_selected = st.radio('Tuition up to date?', (tuition_list))

        if (tuition_selected=="No"):
            tuition_selected=0
        elif(tuition_selected=="Yes"):
            tuition_selected=1

    # ===============================================================
    with bool4:
        scholarship_list = ['Yes', 'No']
        scholarship_selected = st.radio('Scholarship holder?', (scholarship_list))

        if (scholarship_selected=="No"):
            scholarship_selected=0
        elif(scholarship_selected=="Yes"):
            scholarship_selected=1

    # ===============================================================
    grade1, grade2 = st.columns(2)

    with grade1:   
        grade1_selected = st.number_input("First semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
        grade1_selected = round(grade1_selected,2)
    
    with grade2:
        grade2_selected = st.number_input("Second semester grade", value=0.0, step=0.1, min_value=0.0, max_value=20.0)
        grade2_selected = round(grade2_selected,2)

    st.markdown('<style>div.stButton > button {margin: 0 auto; display: block; background: white; color: black;}</style>', unsafe_allow_html=True)
    button_predict = st.button("Predict", key='custom_button')
    if button_predict:
        if course_selected=="None":
            st.write("Please select a valid course.")
        else:
            model = joblib.load('random_forest_model.joblib')
            user_data = {
                'Course': [course_selected], 
                'Daytime_evening_attendance': [time_selected], 
                'Admission_grade': [admgrade_selected], 
                'Educational_special_needs': [special_selected], 
                'Debtor': [debtor_selected], 
                'Tuition_fees_up_to_date': [tuition_selected], 
                'Gender': [gender_selected], 
                'Scholarship_holder': [scholarship_selected], 
                'Age_at_enrollment': [age_selected], 
                'Curricular_units_1st_sem_grade': [grade1_selected],
                'Curricular_units_2nd_sem_grade': [grade2_selected]
            }

            X_new = pd.DataFrame(user_data)
            predictions = model.predict(X_new)
            st.subheader("Prediction Result")
            if predictions == 0:
                st.write("Student is likely to dropout.")
            elif predictions == 1:
                st.write("Student is NOT likely to dropout.")
