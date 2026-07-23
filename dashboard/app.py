import sys, os
import streamlit as st
import plotly.express as px
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard.data import (
    ROLES, get_top_skills, get_salary_summary,
    get_total_jobs, get_top_locations, get_comparison_skills
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

# ── SECTION 3: Role comparison ──────────────────────
st.subheader("⚖️ Role Comparison")
compare_role = st.selectbox(
    "Compare with:",
    options=[r for r in ROLES if r != selected_role],
    format_func=lambda x: x.title()
)

comp_df = get_comparison_skills(selected_role, compare_role)
if comp_df.empty:
    st.info("No shared skills found between these two roles.")
else:
    fig2 = px.bar(
        comp_df,
        x="skill",
        y=["role1_count", "role2_count"],
        barmode="group",
        labels={
            "value"     : "Job postings",
            "skill"     : "Skill",
            "variable"  : "Role"
        },
        color_discrete_map={
            "role1_count": "#378ADD",
            "role2_count": "#1D9E75"
        }
    )
    newnames = {
        "role1_count": selected_role.title(),
        "role2_count": compare_role.title()
    }
    fig2.for_each_trace(lambda t: t.update(name=newnames[t.name]))
    st.plotly_chart(fig2, use_container_width=True)
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