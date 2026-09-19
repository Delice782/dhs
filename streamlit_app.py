import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Rwanda DHS 2025 Health Gains", layout="wide", page_icon="📊")

custom_style = """
<style>
    .main {
        background-color: #f7f9fb;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b3d63;
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }
    div[data-baseweb="radio"] label {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] button {
        background-color: transparent;
        border: 1px solid rgba(255,255,255,0.3);
        color: #ffffff;
        text-align: left;
    }
    section[data-testid="stSidebar"] button:hover {
        border: 1px solid #e07a1f;
        color: #e07a1f;
    }
    .headline-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .headline-number {
        font-size: 34px;
        font-weight: 700;
        color: #0b3d63;
    }
    .headline-label {
        font-size: 13px;
        color: #555555;
    }
</style>
"""

st.markdown(custom_style, unsafe_allow_html=True)

survey_years = [2020, 2025]

total_fertility_rate_values = [4.1, 3.7]
maternal_mortality_ratio_values = [203, 149]
under_five_mortality_values = [45, 36]
stunting_prevalence_values = [33, 27]
antenatal_care_four_visits_values = [47, 78]

indicator_names = [
    "Total Fertility Rate (children per woman)",
    "Maternal Mortality Ratio (deaths per 100,000 live births)",
    "Under Five Mortality (deaths per 1,000 live births)",
    "Stunting Prevalence (percent of children under five)",
    "Antenatal Care, Four or More Visits (percent of women)",
]

indicator_short_labels = [
    "Fertility Rate",
    "Maternal Mortality",
    "Under Five Mortality",
    "Stunting",
    "ANC 4+ Visits",
]

indicator_values_lookup = {
    indicator_names[0]: total_fertility_rate_values,
    indicator_names[1]: maternal_mortality_ratio_values,
    indicator_names[2]: under_five_mortality_values,
    indicator_names[3]: stunting_prevalence_values,
    indicator_names[4]: antenatal_care_four_visits_values,
}

province_names = ["Kigali", "National Average", "East Province"]
province_fertility_values = [3.1, 3.7, 4.0]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dynamic Dashboard"

if "last_view_mode_value" not in st.session_state:
    st.session_state.last_view_mode_value = "Dynamic Dashboard"

view_mode_options = ["Dynamic Dashboard", "Static Poster"]
view_mode_default_index = view_mode_options.index(st.session_state.last_view_mode_value)

st.sidebar.markdown("## 📊 Rwanda DHS 2025")

st.sidebar.markdown("### View Mode")
view_mode_selection = st.sidebar.radio(
    "View Mode",
    view_mode_options,
    index=view_mode_default_index,
    label_visibility="collapsed",
)

if view_mode_selection != st.session_state.last_view_mode_value:
    st.session_state.last_view_mode_value = view_mode_selection
    st.session_state.current_page = view_mode_selection

st.sidebar.markdown("---")

if st.sidebar.button("About This Data", use_container_width=True):
    st.session_state.current_page = "About This Data"

if st.sidebar.button("How to Use", use_container_width=True):
    st.session_state.current_page = "How to Use"

st.sidebar.markdown("---")

if st.sidebar.button("About the Team", use_container_width=True):
    st.session_state.current_page = "About the Team"

selected_section = st.session_state.current_page

if selected_section == "Dynamic Dashboard":

    st.title("Rwanda's Maternal and Child Health Progress, 2020 to 2025")
    st.caption("Source: Rwanda Demographic and Health Survey 2025, National Institute of Statistics of Rwanda")

    st.markdown("#### Headline Indicators at a Glance")

    metric_columns = st.columns(5)

    for column_index in range(len(indicator_names)):
        indicator_name = indicator_names[column_index]
        indicator_values = indicator_values_lookup[indicator_name]
        ending_value = indicator_values[1]
        with metric_columns[column_index]:
            st.markdown(
                f"""<div class="headline-card">
                    <div class="headline-number">{ending_value}</div>
                    <div class="headline-label">{indicator_short_labels[column_index]}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("")
    st.markdown("#### Explore a Trend")

    selected_indicator = st.selectbox("Choose an indicator to view", indicator_names)

    selected_values = indicator_values_lookup[selected_indicator]

    value_2020 = selected_values[0]
    value_2025 = selected_values[1]

    if value_2020 != 0:
        percent_change = ((value_2025 - value_2020) / value_2020) * 100
    else:
        percent_change = 0

    trend_figure = go.Figure()
    trend_figure.add_trace(
        go.Scatter(
            x=survey_years,
            y=selected_values,
            mode="lines+markers+text",
            text=selected_values,
            textposition="top center",
            line=dict(width=4, color="#0b3d63"),
            marker=dict(size=12, color="#e07a1f"),
        )
    )
    trend_figure.update_layout(
        title=selected_indicator,
        xaxis_title="Survey Year",
        yaxis_title="Value",
        xaxis=dict(tickmode="array", tickvals=survey_years),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(trend_figure, use_container_width=True)

    if percent_change < 0:
        st.success(f"{selected_indicator} fell by {abs(percent_change):.1f} percent between 2020 and 2025.")
    elif percent_change > 0:
        st.info(f"{selected_indicator} rose by {abs(percent_change):.1f} percent between 2020 and 2025.")
    else:
        st.write(f"{selected_indicator} did not change between 2020 and 2025.")

    st.markdown("---")
    st.markdown("#### Total Fertility Rate by Province, 2025")

    province_figure = go.Figure()
    province_figure.add_trace(
        go.Bar(
            x=province_names,
            y=province_fertility_values,
            text=province_fertility_values,
            textposition="outside",
            marker_color="#e07a1f",
        )
    )
    province_figure.update_layout(
        title="Total Fertility Rate by Province, 2025",
        yaxis_title="Children per Woman",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(province_figure, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Summary of All Five Indicators")

    summary_rows = []
    for indicator_name in indicator_names:
        indicator_values = indicator_values_lookup[indicator_name]
        starting_value = indicator_values[0]
        ending_value = indicator_values[1]
        summary_rows.append(
            {
                "Indicator": indicator_name,
                "2020 Value": starting_value,
                "2025 Value": ending_value,
            }
        )

    st.table(summary_rows)

elif selected_section == "Static Poster":

    st.title("Static Poster Preview")
    st.caption("This is the fixed, print style version of the data story. Download it below as a PNG for submission.")

    poster_figure, poster_axes = plt.subplots(3, 2, figsize=(10, 12))
    poster_figure.patch.set_facecolor("#f7f9fb")
    poster_figure.suptitle("Rwanda's Maternal and Child Health Progress, 2020 to 2025", fontsize=16, fontweight="bold", color="#0b3d63")

    axis_list = [
        poster_axes[0, 0],
        poster_axes[0, 1],
        poster_axes[1, 0],
        poster_axes[1, 1],
        poster_axes[2, 0],
    ]

    for panel_index in range(len(indicator_names)):
        indicator_name = indicator_names[panel_index]
        indicator_values = indicator_values_lookup[indicator_name]
        current_axis = axis_list[panel_index]
        current_axis.set_facecolor("#ffffff")
        current_axis.plot(survey_years, indicator_values, marker="o", linewidth=3, color="#0b3d63", markerfacecolor="#e07a1f", markersize=9)
        current_axis.set_title(indicator_short_labels[panel_index], fontsize=10, fontweight="bold")
        current_axis.set_xticks(survey_years)
        for year_index in range(len(survey_years)):
            current_axis.annotate(
                str(indicator_values[year_index]),
                (survey_years[year_index], indicator_values[year_index]),
                textcoords="offset points",
                xytext=(0, 8),
                fontsize=9,
                ha="center",
            )

    poster_axes[2, 1].set_facecolor("#ffffff")
    poster_axes[2, 1].bar(province_names, province_fertility_values, color="#e07a1f")
    poster_axes[2, 1].set_title("Fertility Rate by Province, 2025", fontsize=10, fontweight="bold")
    for province_index in range(len(province_names)):
        poster_axes[2, 1].annotate(
            str(province_fertility_values[province_index]),
            (province_index, province_fertility_values[province_index]),
            textcoords="offset points",
            xytext=(0, 5),
            fontsize=9,
            ha="center",
        )

    poster_figure.text(0.5, 0.01, "Source: Rwanda Demographic and Health Survey 2025, National Institute of Statistics of Rwanda", ha="center", fontsize=8, color="#555555")
    poster_figure.tight_layout(rect=[0, 0.03, 1, 0.96])

    st.pyplot(poster_figure)

    image_buffer = io.BytesIO()
    poster_figure.savefig(image_buffer, format="png", dpi=300, facecolor=poster_figure.get_facecolor())
    image_buffer.seek(0)

    st.download_button(
        label="Download static poster as PNG",
        data=image_buffer,
        file_name="rwanda_dhs_2025_static_poster.png",
        mime="image/png",
    )

elif selected_section == "About This Data":

    st.title("About This Data")
    st.write("Source: Rwanda Demographic and Health Survey 2025 (RDHS7), National Institute of Statistics of Rwanda")
    st.write("Fieldwork period: June to November 2025")
    st.write("Implemented by NISR in collaboration with the Ministry of Health")

elif selected_section == "How to Use":

    st.title("How to Use This Dashboard")
    st.write("Use View Mode in the sidebar to switch between the interactive dashboard and the static poster.")
    st.write("In the Dynamic Dashboard, use the dropdown to explore each health indicator and see how it changed between 2020 and 2025.")
    st.write("In the Static Poster section, click the download button to save a PNG version of the fixed data story for submission.")

else:

    st.title("About the Team")

    team_member_one_name = "Delice Ishimwe"
    team_member_one_role = "Software Engineer"
    team_member_one_school = "Carnegie Mellon University - Africa"
    team_member_one_photo_path = "images/member_one.jpg"

    team_member_two_name = "Full Name Here"
    team_member_two_role = "Data Scientist"
    team_member_two_school = "African Leadership University"
    team_member_two_photo_path = "images/member_two.jpg"

    photo_style = """
    <style>
        .team-photo img {
            border-radius: 50%;
            border: 3px solid #e07a1f;
            width: 160px;
            height: 160px;
            object-fit: cover;
        }
    </style>
    """
    st.markdown(photo_style, unsafe_allow_html=True)

    team_columns = st.columns(2)

    with team_columns[0]:
        st.markdown('<div class="team-photo">', unsafe_allow_html=True)
        st.image(team_member_one_photo_path, width=160)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"**{team_member_one_name}**")
        st.write(team_member_one_role)
        st.write(team_member_one_school)

    with team_columns[1]:
        st.markdown('<div class="team-photo">', unsafe_allow_html=True)
        st.image(team_member_two_photo_path, width=160)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"**{team_member_two_name}**")
        st.write(team_member_two_role)
        st.write(team_member_two_school)

    st.caption("Submitted for the NISR 2026 Infographic Competition")
