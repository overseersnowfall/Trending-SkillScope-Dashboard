import sys, os
import streamlit as st
import plotly.express as px
import re
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard.data import (
    ROLES, get_top_skills, get_salary_summary,
    get_total_jobs, get_top_locations, get_seniority_breakdown
)

st.set_page_config(
    page_title="SkillScope Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Trending SkillScope Dashboard")
st.markdown("Real-time UK job market insights — discover which skills employers want most.")
st.divider()

with st.sidebar:
    st.header("Filters")
    selected_role = st.selectbox(
        "Select a role",
        options=ROLES,
        format_func=lambda x: x.title()
    )
    st.caption("Data sourced from Reed.co.uk")

# ── SECTION 1: Summary metrics ─────────────────────
st.subheader(f"📌 {selected_role.title()} — Market Snapshot")
total_jobs   = get_total_jobs(selected_role)
salary_df    = get_salary_summary(selected_role)
top_skill_df, _ = get_top_skills(selected_role, limit=1)
top_skill        = top_skill_df["skill"][0] if not top_skill_df.empty else "N/A"
avg_min = salary_df["avg_min"][0] if not salary_df.empty else 0
avg_max = salary_df["avg_max"][0] if not salary_df.empty else 0
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs Found",   total_jobs)
col2.metric("Top Skill",          top_skill.title())
col3.metric("Avg Min Salary",     f"£{avg_min:,.0f}")
col4.metric("Avg Max Salary",     f"£{avg_max:,.0f}")
st.divider()

# ── SECTION 2: Top skills chart ────────────────────
st.subheader(f"🛠️ Top Skills for {selected_role.title()}")
skills_df, _ = get_top_skills(selected_role)
if skills_df.empty:
    st.info("No skill data found for this role yet.")
else:
    fig = px.bar(
        skills_df.sort_values("percentage"),
        x="percentage",
        y="skill",
        orientation="h",
        text="percentage",
        color="percentage",
        color_continuous_scale="Blues",
        labels={"percentage": "% of job postings", "skill": "Skill"}
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    fig.update_xaxes(range=[0, 110])
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# ── SECTION 3: Seniority breakdown ──────────────────
st.subheader(f"🎓 Entry Level vs Senior — {selected_role.title()}")
st.caption("Based on job title keywords across all postings in the database")

sen_result = get_seniority_breakdown(selected_role)

if isinstance(sen_result, pd.DataFrame) and sen_result.empty:
    st.info("No seniority data available for this role.")
else:
    sen_df, sen_total = sen_result

    # Metric summary above the chart
    junior_row = sen_df[sen_df["seniority"] == "Junior / Graduate"]
    mid_row    = sen_df[sen_df["seniority"] == "Mid-level"]
    senior_row = sen_df[sen_df["seniority"] == "Senior / Lead"]

    junior_pct = float(junior_row["percentage"].values[0]) \
                 if not junior_row.empty else 0
    mid_pct    = float(mid_row["percentage"].values[0]) \
                 if not mid_row.empty else 0
    senior_pct = float(senior_row["percentage"].values[0]) \
                 if not senior_row.empty else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Junior / Graduate", f"{junior_pct}%")
    c2.metric("Mid-level",         f"{mid_pct}%")
    c3.metric("Senior / Lead",     f"{senior_pct}%")

    # Bar chart
    fig_sen = px.bar(
        sen_df,
        x="seniority",
        y="percentage",
        text="percentage",
        color="seniority",
        color_discrete_map={
            "Junior / Graduate": "#1D9E75",
            "Mid-level"        : "#378ADD",
            "Senior / Lead"    : "#534AB7",
            "Manager"          : "#BA7517"
        },
        labels={
            "percentage": "% of job postings",
            "seniority" : "Seniority level"
        }
    )
    fig_sen.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        showlegend=False
    )
    fig_sen.update_layout(showlegend=False)
    fig_sen.update_yaxes(range=[0, 110])
    st.plotly_chart(fig_sen, use_container_width=True)

    # Plain-English takeaway for the student
    if junior_pct < 10:
        st.warning(
            f"⚠️ Only {junior_pct}% of {selected_role.title()} postings are "
            f"junior or graduate level. This is a competitive entry point — "
            f"internships, personal projects, and bootcamps will help you "
            f"stand out."
        )
    elif junior_pct < 25:
        st.info(
            f"ℹ️ {junior_pct}% of postings are junior or graduate level. "
            f"Entry-level roles exist but are limited — strong portfolio "
            f"projects are important."
        )
    else:
        st.success(
            f"✅ {junior_pct}% of postings are junior or graduate level — "
            f"a healthy number of entry opportunities for this role."
        )

st.divider()

# ── SECTION 4: Hot locations ────────────────────────
st.subheader(f"📍 Where Are {selected_role.title()} Jobs?")

loc_df = get_top_locations(selected_role)

def is_real_city(location):
    """Return True if location looks like a real city name, not a postcode."""
    if not location:
        return False
    generic = {"united kingdom", "england", "scotland", "wales",
               "uk", "remote", "home based", "nationwide"}
    if location.lower().strip() in generic:
        return False
    postcode = r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2}$'
    if re.match(postcode, location.upper().strip()):
        return False
    return True

loc_df = loc_df[loc_df["location"].apply(is_real_city)]

if loc_df.empty:
    st.info("No location data available for this role.")
else:
    fig3 = px.bar(
        loc_df,
        x="location",
        y="job_count",
        text="job_count",
        color="job_count",
        color_continuous_scale="Greens",
        labels={"job_count": "Jobs", "location": "City"}
    )
    fig3.update_layout(showlegend=False, coloraxis_showscale=False)
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)
st.divider()

st.caption("Data sourced from Reed.co.uk · Refreshed daily · Built with Streamlit + Plotly")