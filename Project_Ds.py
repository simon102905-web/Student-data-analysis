import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout='wide', initial_sidebar_state='collapsed')

with st.sidebar:
    st.header(":red[Student Performance Dashboard] 🎓")
    selected = option_menu(menu_title="Page/Section Options", options=['Overview / Home', 'Academic Performance', 'Demographics', 'Family Background', 
                                                                       'Lifestyle & Social Habits', 'Correlation Explorer', 'Myth vs Reality', 'Raw Data Explorer'],
                                                                        menu_icon='📃',
                           icons=['house','clipboard-data','graph-up', 'person-lines-fill', 'shield', 'pin-map', 'square-half', 'pin-map-fill'], default_index=2)

DATA_PATH = "student_data.csv"
@st.cache_data
def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

df = load_data()


st.title("🎓 Student Performance Analytics Dashboard")
st.markdown(
    "An interactive exploration of academic, demographic, family, and "
    "lifestyle factors behind student performance."
)
st.divider()


if selected == "Overview / Home":
    st.header(":violet[Overview / Home]")
    total_students = len(df)
    avg_g3 = df["G3"].mean()
    pass_rate = (df["pass_fail"] == "Pass").mean() * 100
    avg_absences = df["absences"].mean()
    higher_ed_pct = (df["higher"] == "yes").mean() * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Students", f"{total_students}")
    col2.metric("Avg Final Grade (G3)", f"{avg_g3:.1f} / 20", border=True)
    col3.metric("Pass Rate", f"{pass_rate:.1f}%", border=True)
    col4.metric("Avg Absences", f"{avg_absences:.1f}", border=True)
    col5.metric("Want Higher Education", f"{higher_ed_pct:.1f}%", border=True)


    
    button = st.form_submit_button("Submit")
    if button:
        #st.write(col1, col2, col3, col4, col5)
        #if col1 == "" or col2 == "" or col3 == "" or col4 == "" or col5 == "":
        #         st.error("Error")
        #         st.warning("Warning")
            #     st.info("Information")
            # else :
            #     st.success("Success")

if selected == "Academic Performance":
    st.header(":red[Academic Performance]")

    academic_df = df.copy()
    academic_df["pass_fail"] = academic_df["G3"].apply(
        lambda g: "Pass" if g >= 10 else "Fail"
    )

    fig_pass = px.pie(
        academic_df,
        names="pass_fail",
        title="Pass / Fail Split (G3 ≥ 10 = Pass)",
        color="pass_fail",
        color_discrete_map={"Pass": "#55A868", "Fail": "#C44E52"},
        hole=0.4,
    )

    st.plotly_chart(fig_pass, use_container_width=True)

if selected == "Academic Performance":
    st.header(":red[Academic Performance]")
    academic_df = df.copy()
    academic_df["pass_fail"] = academic_df["G3"].apply(
        lambda g: "Pass" if g >= 10 else "Fail"
    )
    # with st.form(key='Academic Performance'):
    st.caption("Academic Performance")
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Grade Distribution")
        grade_choice = st.selectbox(
            "Select grade period", ["G3 (Final)", "G2 (2nd period)", "G1 (1st period)"])
        grade_col = {"G3 (Final)": "G3", "G2 (2nd period)": "G2", "G1 (1st period)": "G1"}[grade_choice]
        fig_hist = px.histogram(
            academic_df,
            x=grade_col,
            nbins=20,
            color_discrete_sequence=["#4C72B0"],
            title=f"Distribution of {grade_choice}",
        )
        fig_hist.update_layout(bargap=0.05)
        st.plotly_chart(fig_hist, use_container_width=True)

    with row1_col2:
        st.subheader("Pass vs Fail")
        fig_pass = px.pie(
            academic_df,
            names="pass_fail",
            title="Pass / Fail Split (G3 ≥ 10 = Pass)",
            color="pass_fail",
            color_discrete_map={"Pass": "#55A868", "Fail": "#C44E52"},
            hole=0.4,
        )
        st.plotly_chart(fig_pass, use_container_width=True)
        # button = st.form_submit_button("Submit")
        # if button:
        #     st.write(row1_col1, row1_col2)
        #     if row1_col1 == "" or row1_col2 == "" : 
        #         st.error("Error")
        #         st.warning("Warning")
        #         st.info("Information")
        #     else :
        #         st.success("Success")

if selected == "Demographics":
    st.header(":blue[Demographics]")
    with st.form(key='Demographics'):

        st.subheader("Student Composition")
        row2_col1, row2_col2, row2_col3 = st.columns(3)

        with row2_col1:
            fig_school = px.pie(df, names="school", title="By School", hole=0.4)
            st.plotly_chart(fig_school, use_container_width=True)

        with row2_col2:
            fig_sex = px.pie(df, names="sex", title="By Gender", hole=0.4)
            st.plotly_chart(fig_sex, use_container_width=True)

        with row2_col3:
            fig_addr = px.pie(df, names="address", title="By Address (Urban/Rural)", hole=0.4)
            st.plotly_chart(fig_addr, use_container_width=True)
            button = st.form_submit_button("Submit")
            if button:
                st.write(row2_col1, row2_col2, row2_col3)
            if row2_col1 == "" or row2_col2 == "" or row2_col3 == "" : 
                st.error("Error")
                st.warning("Warning")
                st.info("Information")
            else :
                st.success("Success")

if selected == "Raw Data Explorer":
    st.header(":yellow[Raw Data Explorer]")
    with st.form(key='Raw Data Explorer'):
        st.subheader("Dataset Snapshot")
st.caption(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
st.dataframe(df.head(10), use_container_width=True)



