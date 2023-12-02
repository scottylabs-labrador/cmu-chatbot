import streamlit as st
import query as qy
import textwrap
#MVPMVPMVPMVPMVPMVPMVPMVPMVP


st.title(":red[_Scotty's :blue[Course] :violet[Recommender]_]")
st.title("_:green[Ask Me Something]_")

with st.sidebar:

    with st.form(key="my_form"):
        user_ugrad_grad = st.sidebar.selectbox("Undergraduate or Graduate", ("","Undergraduate", "Graduate"))
        #user_units = st.sidebar.selectbox("Units", ("", "4.5", "5", "9", "10", "11", "12"));
        user_department = st.sidebar.selectbox("Department", ("", 'Architecture', 'Art', 'Arts & Entertainment Management', 'BXA Intercollege Degree Programs', 'Biological Sciences', 'Biomedical Engineering', 'Business Administration', 'CFA Interdisciplinary', 'CIT Interdisciplinary', 'Carnegie Mellon University-Wide Studies', 'Center for the Arts in Society', 'Chemical Engineering', 'Chemistry', 'Civil & Environmental Engineering', 'Computational Biology', 'Computer Science', 'Design', 'Dietrich College Information Systems', 'Dietrich College Interdisciplinary', 'Drama', 'Economics', 'Electrical & Computer Engineering', 'Engineering & Public Policy', 'English', 'Entertainment Technology Pittsburgh', 'General Dietrich College', 'Heinz College Wide Courses', 'History', 'Human-Computer Interaction', 'Information & Communication Technology', 'Information Networking Institute', 'Information Systems:Sch of IS & Mgt', 'Institute for Politics and Strategy', 'Institute for Software Research', 'Integrated Innovation Institute', 'Language Technologies Institute', 'MCS Interdisciplinary', 'Machine Learning', 'Materials Science & Engineering', 'Mathematical Sciences', 'Mechanical Engineering', 'Medical Management:Sch of Pub Pol & Mgt', 'Modern Languages', 'Music', 'Naval Science - ROTC', 'Philosophy', 'Physical Education', 'Physics', 'Neuroscience Institute', 'Psychology', 'Public Management:Sch of Pub Pol & Mgt', 'Public Policy & Mgt:Sch of Pub Pol & Mgt', 'Robotics', 'SCS Interdisciplinary', 'Social & Decision Sciences', 'Statistics and Data Science', 'StuCo (Student Led Courses)', 'Tepper School of Business'));
        
        query = st.sidebar.text_area(
            label = "What do you want to learn about?",
            max_chars=100,
            key="query"
        )

        submit_button = st.form_submit_button(label='Search')

if query and submit_button:
    response = qy.get_response_from_query(query, user_ugrad_grad.lower(), user_department)
    st.subheader("Answer: ")
    repo = '<p style="font-family:sans-serif; color:Black; font-size: 22px;">' + response + '</p>'
    st.markdown(repo, unsafe_allow_html=True)