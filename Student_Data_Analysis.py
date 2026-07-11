import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.header(":red[Student Performance Dashboard] 🎓")

    selected = option_menu(
        menu_title="Page / Section Options",
        options=[
            "Overview / Home",
            "Academic Performance",
            "Demographics",
            "Family Background",
            "Lifestyle & Social Habits",
            "Correlation Explorer",
            "Myth vs Reality",
            "Raw Data Explorer",
        ],
        menu_icon="menu-button",
        icons=[
            "house",
            "clipboard-data",
            "graph-up",
            "people",
            "heart",
            "diagram-3",
            "question-circle",
            "table",
        ],
        default_index=0,
    )

# -------------------------------
# Load Dataset
# -------------------------------
DATA_PATH = "student_data.csv"


@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)

    # Create pass/fail column once
    df["pass_fail"] = df["G3"].apply(lambda x: "Pass" if x >= 10 else "Fail")

    return df


df = load_data()

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("🎓 Student Performance Analytics Dashboard")

st.markdown(
    """
An interactive exploration of **academic**, **demographic**,
**family**, and **lifestyle** factors behind student performance.
"""
)

st.divider()

# ============================================================
# Overview
# ============================================================
if selected == "Overview / Home":

    st.header(":violet[Overview / Home]")

    total_students = len(df)
    avg_g3 = df["G3"].mean()
    pass_rate = (df["pass_fail"] == "Pass").mean() * 100
    avg_absences = df["absences"].mean()
    higher_ed_pct = (df["higher"] == "yes").mean() * 100

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Students", total_students)
    col2.metric("Avg Final Grade", f"{avg_g3:.1f}/20")
    col3.metric("Pass Rate", f"{pass_rate:.1f}%")
    col4.metric("Avg Absences", f"{avg_absences:.1f}")
    col5.metric("Higher Education", f"{higher_ed_pct:.1f}%")

# ============================================================
# Academic Performance
# ============================================================
elif selected == "Academic Performance":

    st.header(":red[Academic Performance]")

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        st.subheader("Grade Distribution")

        grade_choice = st.selectbox(
            "Select Grade",
            [
                "G3 (Final)",
                "G2 (Second Period)",
                "G1 (First Period)",
            ],
        )

        grade_col = {
            "G3 (Final)": "G3",
            "G2 (Second Period)": "G2",
            "G1 (First Period)": "G1",
        }[grade_choice]

        fig_hist = px.histogram(
            df,
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
            df,
            names="pass_fail",
            title="Pass / Fail Split",
            hole=0.4,
            color="pass_fail",
            color_discrete_map={
                "Pass": "#55A868",
                "Fail": "#C44E52",
            },
        )

        st.plotly_chart(fig_pass, use_container_width=True)

# ============================================================
# Demographics
# ============================================================
elif selected == "Demographics":

    st.header(":blue[Demographics]")

    st.subheader("Student Composition")

    col1, col2, col3 = st.columns(3)

    with col1:

        fig_school = px.pie(
            df,
            names="school",
            title="School",
            hole=0.4,
        )

        st.plotly_chart(fig_school, use_container_width=True)

    with col2:

        fig_gender = px.pie(
            df,
            names="sex",
            title="Gender",
            hole=0.4,
        )

        st.plotly_chart(fig_gender, use_container_width=True)

    with col3:

        fig_address = px.pie(
            df,
            names="address",
            title="Urban vs Rural",
            hole=0.4,
        )

        st.plotly_chart(fig_address, use_container_width=True)

# ============================================================
# Family Background
# ============================================================
elif selected == "Family Background":

    st.header(":green[Family Background]")

    fcol1, fcol2 = st.columns(2)

    with fcol1:
        st.subheader("Family Size vs Final Grade")
        fig_famsize = px.box(
            df,
            x="famsize",
            y="G3",
            color="famsize",
            title="Family Size (LE3 = ≤3, GT3 = >3) vs Final Grade",
            labels={"famsize": "Family Size", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_famsize, use_container_width=True)

    with fcol2:
        st.subheader("Parents' Cohabitation Status")
        fig_pstatus = px.box(
            df,
            x="Pstatus",
            y="G3",
            color="Pstatus",
            title="Parent Cohabitation (T = Together, A = Apart) vs Final Grade",
            labels={"Pstatus": "Parent Status", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_pstatus, use_container_width=True)

    st.divider()

    st.subheader("Parents' Education vs Final Grade")

    edu_col1, edu_col2 = st.columns(2)

    with edu_col1:
        medu_avg = df.groupby("Medu", as_index=False)["G3"].mean()
        fig_medu = px.bar(
            medu_avg,
            x="Medu",
            y="G3",
            title="Mother's Education Level vs Avg Final Grade",
            labels={"Medu": "Mother's Education (0=none, 4=higher ed.)", "G3": "Avg Final Grade"},
            color="G3",
            color_continuous_scale="Greens",
        )
        st.plotly_chart(fig_medu, use_container_width=True)

    with edu_col2:
        fedu_avg = df.groupby("Fedu", as_index=False)["G3"].mean()
        fig_fedu = px.bar(
            fedu_avg,
            x="Fedu",
            y="G3",
            title="Father's Education Level vs Avg Final Grade",
            labels={"Fedu": "Father's Education (0=none, 4=higher ed.)", "G3": "Avg Final Grade"},
            color="G3",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig_fedu, use_container_width=True)

    st.divider()

    st.subheader("Parents' Occupation")

    job_col1, job_col2 = st.columns(2)

    with job_col1:
        fig_mjob = px.pie(
            df,
            names="Mjob",
            title="Mother's Job",
            hole=0.4,
        )
        st.plotly_chart(fig_mjob, use_container_width=True)

    with job_col2:
        fig_fjob = px.pie(
            df,
            names="Fjob",
            title="Father's Job",
            hole=0.4,
        )
        st.plotly_chart(fig_fjob, use_container_width=True)

    st.divider()

    rel_col1, rel_col2 = st.columns(2)

    with rel_col1:
        st.subheader("Family Relationship Quality vs Grade")
        fig_famrel = px.box(
            df,
            x="famrel",
            y="G3",
            color="famrel",
            title="Family Relationship Quality (1=Bad, 5=Excellent) vs Final Grade",
            labels={"famrel": "Family Relationship Quality", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_famrel, use_container_width=True)

    with rel_col2:
        st.subheader("Extra Educational Support from Family")
        famsup_avg = df.groupby("famsup", as_index=False)["G3"].mean()
        fig_famsup = px.bar(
            famsup_avg,
            x="famsup",
            y="G3",
            color="famsup",
            title="Family Educational Support vs Avg Final Grade",
            labels={"famsup": "Family Support", "G3": "Avg Final Grade"},
            color_discrete_map={"yes": "#55A868", "no": "#C44E52"},
        )
        st.plotly_chart(fig_famsup, use_container_width=True)

    st.divider()

    st.subheader("Guardian Type Distribution")
    guardian_counts = df["guardian"].value_counts().reset_index()
    guardian_counts.columns = ["guardian", "count"]
    fig_guardian = px.bar(
        guardian_counts,
        x="guardian",
        y="count",
        title="Primary Guardian",
        labels={"guardian": "Guardian", "count": "Number of Students"},
        color="guardian",
    )
    st.plotly_chart(fig_guardian, use_container_width=True)
# ============================================================
# Lifestyle
# ============================================================
elif selected == "Lifestyle & Social Habits":

    st.header(":orange[Lifestyle & Social Habits]")

    life_col1, life_col2 = st.columns(2)

    with life_col1:
        st.subheader("Weekly Study Time vs Final Grade")
        fig_study = px.box(
            df,
            x="studytime",
            y="G3",
            color="studytime",
            title="Study Time (1=<2h, 2=2-5h, 3=5-10h, 4=>10h) vs Final Grade",
            labels={"studytime": "Weekly Study Time", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_study, use_container_width=True)

    with life_col2:
        st.subheader("Free Time After School vs Final Grade")
        fig_free = px.box(
            df,
            x="freetime",
            y="G3",
            color="freetime",
            title="Free Time (1=Low, 5=High) vs Final Grade",
            labels={"freetime": "Free Time", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_free, use_container_width=True)

    st.divider()

    st.subheader("Going Out with Friends vs Final Grade")
    fig_goout = px.box(
        df,
        x="goout",
        y="G3",
        color="goout",
        title="Going Out Frequency (1=Low, 5=High) vs Final Grade",
        labels={"goout": "Going Out Frequency", "G3": "Final Grade"},
    )
    st.plotly_chart(fig_goout, use_container_width=True)

    st.divider()

    st.subheader("Alcohol Consumption")

    alc_col1, alc_col2 = st.columns(2)

    with alc_col1:
        fig_dalc = px.box(
            df,
            x="Dalc",
            y="G3",
            color="Dalc",
            title="Workday Alcohol Consumption vs Final Grade",
            labels={"Dalc": "Workday Alcohol (1=Low, 5=High)", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_dalc, use_container_width=True)

    with alc_col2:
        fig_walc = px.box(
            df,
            x="Walc",
            y="G3",
            color="Walc",
            title="Weekend Alcohol Consumption vs Final Grade",
            labels={"Walc": "Weekend Alcohol (1=Low, 5=High)", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_walc, use_container_width=True)

    st.divider()

    hcol1, hcol2 = st.columns(2)

    with hcol1:
        st.subheader("Health Status vs Final Grade")
        fig_health = px.box(
            df,
            x="health",
            y="G3",
            color="health",
            title="Health Status (1=Bad, 5=Very Good) vs Final Grade",
            labels={"health": "Health Status", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_health, use_container_width=True)

    with hcol2:
        st.subheader("Internet Access vs Final Grade")
        internet_avg = df.groupby("internet", as_index=False)["G3"].mean()
        fig_internet = px.bar(
            internet_avg,
            x="internet",
            y="G3",
            color="internet",
            title="Internet Access at Home vs Avg Final Grade",
            labels={"internet": "Internet Access", "G3": "Avg Final Grade"},
        )
        st.plotly_chart(fig_internet, use_container_width=True)

    st.divider()

    scol1, scol2 = st.columns(2)

    with scol1:
        st.subheader("Romantic Relationship vs Final Grade")
        fig_romantic = px.box(
            df,
            x="romantic",
            y="G3",
            color="romantic",
            title="In a Romantic Relationship vs Final Grade",
            labels={"romantic": "In Relationship", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_romantic, use_container_width=True)

    with scol2:
        st.subheader("Extracurricular Activities vs Final Grade")
        fig_activities = px.box(
            df,
            x="activities",
            y="G3",
            color="activities",
            title="Participates in Extracurricular Activities vs Final Grade",
            labels={"activities": "Activities", "G3": "Final Grade"},
        )
        st.plotly_chart(fig_activities, use_container_width=True)
# ============================================================
# Correlation Explorer
# ============================================================
elif selected == "Correlation Explorer":

    st.header(":violet[Correlation Explorer]")

    # Select only numeric columns
    numeric_df = df.select_dtypes(include="number")

    st.subheader("Correlation Matrix")

    corr = numeric_df.corr()

    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Correlation Matrix",
    )

    # Increase matrix size
    fig_corr.update_layout(
        width=1200,
        height=900,
        font=dict(size=15),
        title_font=dict(size=22),
        margin=dict(l=20, r=20, t=60, b=20),
    )

    # Increase correlation value text size
    fig_corr.update_traces(
        textfont=dict(size=16)
    )

    st.plotly_chart(fig_corr, use_container_width=True)

# ============================================================
# Myth vs Reality
# ============================================================
elif selected == "Myth vs Reality":

    st.header(":cyan[Myth vs Reality]")

    st.markdown(
        "Pick a common belief about student performance below, and let's "
        "check what the data actually says."
    )

    myth_options = [
        "🍷 Alcohol destroys your grades",
        "💔 Being in a relationship hurts your grades",
        "📚 More study hours guarantee higher grades",
        "🔁 Past failures doom you to fail again",
        "🏙️ Urban students outperform rural students",
        "💰 Paid tutoring significantly boosts your grade",
        "🚪 Skipping school always tanks your grade",
        "🚻 Boys outperform girls academically",
    ]

    selected_myth = st.selectbox("Choose a myth to test:", myth_options)

    st.divider()

    def verdict_box(measure, weak_th, strong_th, higher_is_confirmed_text,
                     partial_text, busted_text):
        """Show a colored verdict card based on effect size."""
        if abs(measure) >= strong_th:
            st.success(f"✅ **CONFIRMED** — {higher_is_confirmed_text}")
        elif abs(measure) >= weak_th:
            st.warning(f"⚠️ **PARTIALLY TRUE** — {partial_text}")
        else:
            st.error(f"❌ **BUSTED** — {busted_text}")

    # ------------------------------------------------------------
    # Myth 1: Alcohol
    # ------------------------------------------------------------
    if selected_myth == myth_options[0]:

        df["alc_avg"] = (df["Dalc"] + df["Walc"]) / 2
        corr = df["alc_avg"].corr(df["G3"])

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.box(
                df, x="Dalc", y="G3", color="Dalc",
                title="Workday Alcohol Use vs Final Grade",
                labels={"Dalc": "Workday Alcohol (1=Low, 5=High)", "G3": "Final Grade"},
            )
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.box(
                df, x="Walc", y="G3", color="Walc",
                title="Weekend Alcohol Use vs Final Grade",
                labels={"Walc": "Weekend Alcohol (1=Low, 5=High)", "G3": "Final Grade"},
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.metric("Correlation: Alcohol Use vs Final Grade", f"{corr:.2f}")
        verdict_box(
            corr, weak_th=0.15, strong_th=0.3,
            higher_is_confirmed_text=f"a real link exists between alcohol use and grades (r = {corr:.2f}).",
            partial_text=f"there's a weak negative link (r = {corr:.2f}) — alcohol matters, but less than the myth suggests.",
            busted_text=f"the correlation is only {corr:.2f} — almost no relationship between alcohol use and final grade in this data.",
        )

    # ------------------------------------------------------------
    # Myth 2: Romantic relationships
    # ------------------------------------------------------------
    elif selected_myth == myth_options[1]:

        means = df.groupby("romantic")["G3"].mean()
        diff = means.get("no", 0) - means.get("yes", 0)

        fig = px.box(
            df, x="romantic", y="G3", color="romantic",
            title="Romantic Relationship vs Final Grade",
            labels={"romantic": "In a Relationship", "G3": "Final Grade"},
            color_discrete_map={"yes": "#C44E52", "no": "#55A868"},
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Avg Grade — Not in Relationship", f"{means.get('no', 0):.1f}")
        c2.metric("Avg Grade — In Relationship", f"{means.get('yes', 0):.1f}", delta=f"{-diff:.1f}")

        verdict_box(
            diff, weak_th=0.5, strong_th=1.5,
            higher_is_confirmed_text=f"students in relationships score {diff:.1f} points lower on average — a meaningful gap.",
            partial_text=f"students in relationships score {diff:.1f} points lower on average — a small but real gap, not a dramatic one.",
            busted_text=f"the gap is only {diff:.1f} points — relationship status barely moves the needle.",
        )

    # ------------------------------------------------------------
    # Myth 3: Study time guarantees grades
    # ------------------------------------------------------------
    elif selected_myth == myth_options[2]:

        corr = df["studytime"].corr(df["G3"])

        fig = px.box(
            df, x="studytime", y="G3", color="studytime",
            title="Weekly Study Time vs Final Grade",
            labels={"studytime": "Study Time (1=<2h, 2=2-5h, 3=5-10h, 4=>10h)", "G3": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Correlation: Study Time vs Final Grade", f"{corr:.2f}")
        verdict_box(
            corr, weak_th=0.15, strong_th=0.3,
            higher_is_confirmed_text=f"more study time reliably tracks with higher grades (r = {corr:.2f}).",
            partial_text=f"study time only weakly predicts grades (r = {corr:.2f}) — it helps, but it's no guarantee.",
            busted_text=f"correlation is just {corr:.2f} — putting in more study hours does not reliably guarantee a higher grade here.",
        )

    # ------------------------------------------------------------
    # Myth 4: Past failures doom future failure
    # ------------------------------------------------------------
    elif selected_myth == myth_options[3]:

        corr = df["failures"].corr(df["G3"])

        fig = px.box(
            df, x="failures", y="G3", color="failures",
            title="Number of Past Class Failures vs Final Grade",
            labels={"failures": "Past Failures", "G3": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Correlation: Past Failures vs Final Grade", f"{corr:.2f}")
        verdict_box(
            corr, weak_th=0.15, strong_th=0.3,
            higher_is_confirmed_text=f"past failures strongly track with lower final grades (r = {corr:.2f}) — the pattern holds up.",
            partial_text=f"past failures show a moderate link to lower grades (r = {corr:.2f}).",
            busted_text=f"correlation is only {corr:.2f} — past failures don't meaningfully predict future performance here.",
        )

    # ------------------------------------------------------------
    # Myth 5: Urban vs rural
    # ------------------------------------------------------------
    elif selected_myth == myth_options[4]:

        means = df.groupby("address")["G3"].mean()
        diff = means.get("U", 0) - means.get("R", 0)

        fig = px.box(
            df, x="address", y="G3", color="address",
            title="Urban (U) vs Rural (R) vs Final Grade",
            labels={"address": "Address Type", "G3": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Avg Grade — Rural", f"{means.get('R', 0):.1f}")
        c2.metric("Avg Grade — Urban", f"{means.get('U', 0):.1f}", delta=f"{diff:.1f}")

        verdict_box(
            diff, weak_th=0.5, strong_th=1.5,
            higher_is_confirmed_text=f"urban students score {diff:.1f} points higher on average — a meaningful gap.",
            partial_text=f"urban students score {diff:.1f} points higher on average — a modest, but real, edge.",
            busted_text=f"the gap is only {diff:.1f} points — location barely matters here.",
        )

    # ------------------------------------------------------------
    # Myth 6: Paid tutoring
    # ------------------------------------------------------------
    elif selected_myth == myth_options[5]:

        means = df.groupby("paid")["G3"].mean()
        diff = means.get("yes", 0) - means.get("no", 0)

        fig = px.box(
            df, x="paid", y="G3", color="paid",
            title="Paid Extra Classes vs Final Grade",
            labels={"paid": "Paid Extra Classes", "G3": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Avg Grade — No Paid Classes", f"{means.get('no', 0):.1f}")
        c2.metric("Avg Grade — Paid Classes", f"{means.get('yes', 0):.1f}", delta=f"{diff:.1f}")

        verdict_box(
            diff, weak_th=0.5, strong_th=1.5,
            higher_is_confirmed_text=f"paid classes correspond to a {diff:.1f}-point boost — a real, noticeable effect.",
            partial_text=f"paid classes correspond to a {diff:.1f}-point boost — a small edge, not a game-changer.",
            busted_text=f"the difference is only {diff:.1f} points — paying for extra classes shows little benefit here.",
        )

    # ------------------------------------------------------------
    # Myth 7: Absences always tank grades
    # ------------------------------------------------------------
    elif selected_myth == myth_options[6]:

        corr = df["absences"].corr(df["G3"])

        fig = px.scatter(
            df, x="absences", y="G3", color="pass_fail",
            title="Absences vs Final Grade",
            labels={"absences": "Number of Absences", "G3": "Final Grade"},
            color_discrete_map={"Pass": "#55A868", "Fail": "#C44E52"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Correlation: Absences vs Final Grade", f"{corr:.2f}")
        verdict_box(
            corr, weak_th=0.15, strong_th=0.3,
            higher_is_confirmed_text=f"absences reliably track with lower grades (r = {corr:.2f}).",
            partial_text=f"absences show only a weak link to grades (r = {corr:.2f}).",
            busted_text=f"correlation is just {corr:.2f} — skipping school shows almost no relationship with final grade in this data.",
        )

    # ------------------------------------------------------------
    # Myth 8: Boys outperform girls
    # ------------------------------------------------------------
    elif selected_myth == myth_options[7]:

        means = df.groupby("sex")["G3"].mean()
        diff = means.get("M", 0) - means.get("F", 0)

        fig = px.box(
            df, x="sex", y="G3", color="sex",
            title="Gender vs Final Grade",
            labels={"sex": "Gender", "G3": "Final Grade"},
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        c1.metric("Avg Grade — Female", f"{means.get('F', 0):.1f}")
        c2.metric("Avg Grade — Male", f"{means.get('M', 0):.1f}", delta=f"{diff:.1f}")

        verdict_box(
            diff, weak_th=0.5, strong_th=1.5,
            higher_is_confirmed_text=f"boys score {diff:.1f} points higher on average — a meaningful gap.",
            partial_text=f"boys score {diff:.1f} points higher on average — a modest gap, worth noting but not dramatic.",
            busted_text=f"the gap is only {diff:.1f} points — gender barely predicts final grade here.",
        )
# ============================================================
# Raw Data Explorer
# ============================================================
elif selected == "Raw Data Explorer":

    st.header(":yellow[Raw Data Explorer]")

    st.subheader("Dataset Snapshot")

    st.caption(
        f"Shape: {df.shape[0]} rows × {df.shape[1]} columns"
    )

    st.dataframe(df.head(10), use_container_width=True)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(df, use_container_width=True)

