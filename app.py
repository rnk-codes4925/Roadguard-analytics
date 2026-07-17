import streamlit as st
import pandas as pd
import numpy as np
import os
from streamlit_option_menu import option_menu
import plotly.express as px
import textwrap

# Import our custom modules
from utils import load_and_preprocess_data, get_filter_options, filter_dataframe
from style import get_custom_css
from charts import (
    create_monthly_trend_chart,
    create_road_type_horizontal_bar,
    create_donut_charts,
    create_district_treemap,
    create_speed_limit_chart,
    create_geographical_map
)

# Page Configuration
st.set_page_config(
    page_title="RoadGuard Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper to render clean HTML without markdown code block interpretation
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# Load CSS Design System
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Load Data Engine
@st.cache_data
def get_cached_data():
    return load_and_preprocess_data()

try:
    df_raw = get_cached_data()
except Exception as e:
    st.error(f"Error loading safety database: {e}")
    st.stop()

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #FFFFFF; font-weight:800; letter-spacing:0.05em; margin-bottom: 0;'>🛡️ ROADGUARD</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A5C1; font-size:0.85rem; margin-top:2px; margin-bottom: 10px;'>UK Safety Intelligence</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255, 0, 127, 0.2); margin-top: 5px; margin-bottom: 15px;'/>", unsafe_allow_html=True)
    
    # Custom Sidebar Navigation Menu
    selected_page = option_menu(
        menu_title=None,
        options=["Executive Overview", "Deep Dive Analytics", "Spatial Mapping", "Insights & Export"],
        icons=["speedometer2", "graph-up", "map", "download"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#A0A5C1", "font-size": "0.95rem"}, 
            "nav-link": {
                "font-size": "0.85rem",
                "text-align": "left",
                "margin": "3px 0px",
                "color": "#FFFFFF",
                "background-color": "transparent",
                "padding": "8px 12px"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, rgba(255, 0, 127, 0.25) 0%, rgba(0, 200, 255, 0.25) 100%)",
                "border": "1px solid rgba(255, 0, 127, 0.4)",
                "font-weight": "600"
            }
        }
    )
    
    # Dynamic Database Source Uploader Section
    st.markdown("<br><h4 style='color: #FF007F; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;'>DATABASE SOURCE</h4>", unsafe_allow_html=True)
    db_source = st.radio("Choose Data Source", ["🛡️ Pre-loaded Database", "📁 Upload Custom CSV"], index=0, label_visibility="collapsed")
    
    custom_df = None
    if db_source == "📁 Upload Custom CSV":
        uploaded_file = st.file_uploader("Upload Accident CSV File", type=["csv"], help="Upload any accident dataset CSV. It must contain a 'Date' or 'Year' column.")
        if uploaded_file is not None:
            try:
                custom_df = pd.read_csv(uploaded_file)
                # Normalize column names for schema flexibility
                col_mapping = {}
                for col in custom_df.columns:
                    col_lower = col.lower()
                    if col_lower == 'date' and col != 'Date':
                        col_mapping[col] = 'Date'
                    elif col_lower == 'casualties' and col != 'Casualties':
                        col_mapping[col] = 'Casualties'
                    elif col_lower == 'severity' and col != 'Severity':
                        col_mapping[col] = 'Severity'
                    elif col_lower in ['urban_or_rural_area', 'urban_or_rural', 'urban/rural'] and col != 'Urban_or_Rural_Area':
                        col_mapping[col] = 'Urban_or_Rural_Area'
                    elif col_lower in ['light_conditions', 'light_condition', 'light'] and col != 'Light_Conditions':
                        col_mapping[col] = 'Light_Conditions'
                    elif col_lower in ['weather_conditions', 'weather_condition', 'weather'] and col != 'Weather_Conditions':
                        col_mapping[col] = 'Weather_Conditions'
                    elif col_lower in ['road_surface_conditions', 'road_surface_condition', 'road_surface'] and col != 'Road_Surface_Conditions':
                        col_mapping[col] = 'Road_Surface_Conditions'
                    elif col_lower in ['road_type', 'roadtype'] and col != 'Road_Type':
                        col_mapping[col] = 'Road_Type'
                    elif col_lower in ['vehicle_type', 'vehicletype', 'vehicle'] and col != 'Vehicle_Type':
                        col_mapping[col] = 'Vehicle_Type'
                    elif col_lower in ['district', 'area', 'location_district'] and col != 'District':
                        col_mapping[col] = 'District'
                    elif col_lower in ['latitude', 'lat'] and col != 'Latitude':
                        col_mapping[col] = 'Latitude'
                    elif col_lower in ['longitude', 'lon', 'lng'] and col != 'Longitude':
                        col_mapping[col] = 'Longitude'
                    elif col_lower in ['accident_index', 'index', 'id'] and col != 'Accident_Index':
                        col_mapping[col] = 'Accident_Index'
                    elif col_lower in ['speed_limit', 'speedlimit', 'speed'] and col != 'Speed_Limit':
                        col_mapping[col] = 'Speed_Limit'
                
                if col_mapping:
                    custom_df = custom_df.rename(columns=col_mapping)
                
                if 'Date' not in custom_df.columns:
                    st.sidebar.error("❌ CSV must contain a 'Date' column.")
                    custom_df = None
                else:
                    custom_df['Date'] = pd.to_datetime(custom_df['Date'], errors='coerce')
                    custom_df = custom_df.dropna(subset=['Date'])
                    custom_df['Year'] = custom_df['Date'].dt.year
                    custom_df['Month'] = custom_df['Date'].dt.month
                    custom_df['Month_Name'] = custom_df['Date'].dt.strftime('%b')
                    
                    # Ensure optional columns are populated with standard fallback defaults
                    default_cols = {
                        'Casualties': 1,
                        'Severity': 'Slight',
                        'Urban_or_Rural_Area': 'Urban',
                        'Light_Conditions': 'Day',
                        'Weather_Conditions': 'Fine no high winds',
                        'Road_Surface_Conditions': 'Dry',
                        'Road_Type': 'Single carriageway',
                        'Vehicle_Type': 'Car',
                        'District': 'Unknown',
                        'Latitude': 54.0,
                        'Longitude': -2.0,
                        'Accident_Index': 'ACC_CUSTOM',
                        'Speed_Limit': 30
                    }
                    for col_name, val in default_cols.items():
                        if col_name not in custom_df.columns:
                            custom_df[col_name] = val
                    
                    st.sidebar.success("✅ Custom Database Loaded!")
            except Exception as e:
                st.sidebar.error(f"❌ Load failed: {e}")
                custom_df = None

    if custom_df is not None:
        df_raw = custom_df

    st.markdown("<br><h4 style='color: #00C8FF; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;'>GLOBAL FILTER SUITE</h4>", unsafe_allow_html=True)
    filter_opts = get_filter_options(df_raw)
    
    # Global Sidebar Filter Widgets
    road_surface_filter = st.selectbox("Road Surface Condition", filter_opts['road_surface'])
    weather_filter = st.selectbox("Weather Condition", filter_opts['weather'])
    severity_filter = st.selectbox("Accident Severity", filter_opts['severity'])
    urban_rural_filter = st.selectbox("Urban or Rural Area", filter_opts['urban_rural'])
    district_filter = st.selectbox("Filter by District", filter_opts['district'])

    # Dynamic Year Comparison Selection (highly flexible for 2023, 2024, or custom uploads)
    available_years = sorted(df_raw['Year'].dropna().unique().astype(int).tolist(), reverse=True) if not df_raw.empty else []
    
    st.markdown("<br><h4 style='color: #00C8FF; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;'>COMPARE YEARS</h4>", unsafe_allow_html=True)
    if len(available_years) >= 2:
        cy_year = st.selectbox("Current Year (CY)", available_years, index=0)
        py_options = [y for y in available_years if y != cy_year]
        if not py_options:
            py_options = available_years
        py_year = st.selectbox("Prior Year (PY)", py_options, index=min(0, len(py_options)-1))
    elif len(available_years) == 1:
        cy_year = st.selectbox("Current Year (CY)", available_years, index=0)
        py_year = cy_year
    else:
        cy_year = 2022
        py_year = 2021

# Apply filter pipeline
df_filtered = filter_dataframe(
    df_raw,
    road_surface=road_surface_filter,
    weather=weather_filter,
    severity=severity_filter,
    urban_rural=urban_rural_filter,
    district=district_filter
)

# Extract CY Current Year data dynamically
df_cy = df_filtered[df_filtered['Year'] == cy_year] if not df_filtered.empty else pd.DataFrame()

# Helper function to display empty state
def render_empty_state(message="No safety incident records match the active filter criteria."):
    st.markdown(f"""
    <div class="empty-state" style="margin-top: 40px;">
        <div class="empty-state-icon">🔍</div>
        <h3 style="color: #FFFFFF; font-weight:700; margin-top:0;">No Data Found</h3>
        <p class="empty-state-text">{message}</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- ROUTING LOGIC: MULTI-PAGE DASHBOARD -----------------

if df_filtered.empty:
    st.markdown(f'<div class="title-banner"><h1>{selected_page}</h1></div>', unsafe_allow_html=True)
    render_empty_state()

else:
    # ----------------- PAGE 1: EXECUTIVE OVERVIEW -----------------
    if selected_page == "Executive Overview":
        st.markdown('<div class="title-banner"><h1>Road Accident Analysis</h1></div>', unsafe_allow_html=True)
        
        # Metric Computations (CY vs PY)
        df_py = df_filtered[df_filtered['Year'] == py_year]
        
        def compute_metric_and_delta(column, is_count=False):
            if is_count:
                cy_val = len(df_cy)
                py_val = len(df_py)
            else:
                cy_val = df_cy[column].sum() if not df_cy.empty else 0
                py_val = df_py[column].sum() if not df_py.empty else 0
                
            delta_pct = 0.0
            if py_val > 0:
                delta_pct = ((cy_val - py_val) / py_val) * 100
                
            return cy_val, delta_pct
            
        cy_casualties, d_casualties = compute_metric_and_delta('Casualties')
        cy_accidents, d_accidents = compute_metric_and_delta(None, is_count=True)
        
        # Severity breakdowns for casualties
        def get_severity_casualties(df, severity_level):
            sub = df[df['Severity'] == severity_level]
            return sub['Casualties'].sum() if not sub.empty else 0
            
        cy_fatal = get_severity_casualties(df_cy, 'Fatal')
        py_fatal = get_severity_casualties(df_py, 'Fatal')
        d_fatal = ((cy_fatal - py_fatal) / py_fatal * 100) if py_fatal > 0 else 0.0
        
        cy_serious = get_severity_casualties(df_cy, 'Serious')
        py_serious = get_severity_casualties(df_py, 'Serious')
        d_serious = ((cy_serious - py_serious) / py_serious * 100) if py_serious > 0 else 0.0
        
        cy_slight = get_severity_casualties(df_cy, 'Slight')
        py_slight = get_severity_casualties(df_py, 'Slight')
        d_slight = ((cy_slight - py_slight) / py_slight * 100) if py_slight > 0 else 0.0

        def fmt_val(val):
            if val >= 1000:
                return f"{val / 1000:.1f}K"
            return f"{val:,}"

        # KPI Metric Grid Row (Dynamically reflecting the selected years)
        kpi_cols = st.columns(5)
        kpi_titles = [f"Total {cy_year} Casualties", f"Total {cy_year} Accidents", f"{cy_year} Fatal Casualties", f"{cy_year} Serious Casualties", f"{cy_year} Slight Casualties"]
        kpi_vals = [cy_casualties, cy_accidents, cy_fatal, cy_serious, cy_slight]
        kpi_deltas = [d_casualties, d_accidents, d_fatal, d_serious, d_slight]
        
        for idx, col in enumerate(kpi_cols):
            with col:
                metric_html = f"""
                <div data-testid="stMetric" style="margin-bottom:20px;">
                    <div data-testid="stMetricLabel">{kpi_titles[idx]}</div>
                    <div data-testid="stMetricValue">{fmt_val(kpi_vals[idx])}</div>
                    <div class="delta-down">{kpi_deltas[idx]:+.1f}% vs {py_year}</div>
                </div>
                """
                render_html(metric_html)
                
        # Main Layout Grid for Charts & Widgets
        body_cols = st.columns([1, 2.2, 1.2])
        
        # LEFT COLUMN: Casualties by Vehicle Type (Tall Scrolling List)
        with body_cols[0]:
            vehicle_data = df_cy.groupby('Vehicle_Type').agg({'Casualties': 'sum'}).reset_index()
            vehicle_data = vehicle_data.sort_values(by='Casualties', ascending=False)
            
            vehicle_html = '<div class="vehicle-list-container"><div class="vehicle-title">Vehicle Types</div>'
            for _, row in vehicle_data.iterrows():
                vehicle_html += f'<div class="vehicle-item"><div class="vehicle-item-label">{row["Vehicle_Type"]}</div><div class="vehicle-item-val">{row["Casualties"]:,}</div></div>'
            vehicle_html += '</div>'
            
            render_html(vehicle_html)
            
        # MIDDLE COLUMN: Line chart
        with body_cols[1]:
            # Monthly Trend (Height set to 540 to match the left column height perfectly)
            with st.container(border=True):
                trend_fig = create_monthly_trend_chart(df_filtered, height=540)
                if trend_fig:
                    st.plotly_chart(trend_fig, use_container_width=True)
                
        # RIGHT COLUMN: Treemap
        with body_cols[2]:
            # Geographical Hotspots (Height set to 540 to match the left column height perfectly)
            with st.container(border=True):
                treemap_fig = create_district_treemap(df_cy, height=540)
                if treemap_fig:
                    st.plotly_chart(treemap_fig, use_container_width=True)

        # Full-width center section for Casualties Distribution by Road Type
        with st.container(border=True):
            bar_fig = create_road_type_horizontal_bar(df_cy, height=450)
            if bar_fig:
                st.plotly_chart(bar_fig, use_container_width=True)

        # Full-width bottom section for Donut Charts
        # Donut Chart 1: Urban vs Rural Areas
        with st.container(border=True):
            donut1 = create_donut_charts(df_cy, 'Urban_or_Rural_Area')
            if donut1:
                st.plotly_chart(donut1, use_container_width=True)
        
        # Donut Chart 2: Light Conditions
        with st.container(border=True):
            donut2 = create_donut_charts(df_cy, 'Light_Conditions')
            if donut2:
                st.plotly_chart(donut2, use_container_width=True)

    # ----------------- PAGE 2: DEEP DIVE ANALYTICS -----------------
    elif selected_page == "Deep Dive Analytics":
        st.markdown('<div class="title-banner"><h1>Deep Dive Analytics</h1></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='color: #00C8FF; font-weight:700; margin-top:0;'>⚡ Speed Limit Distribution</h3>", unsafe_allow_html=True)
                speed_fig = create_speed_limit_chart(df_filtered)
                if speed_fig:
                    st.plotly_chart(speed_fig, use_container_width=True)
            
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='color: #FF007F; font-weight:700; margin-top:0;'>📊 Incident Severity Cross Tabulation</h3>", unsafe_allow_html=True)
                crosstab = pd.crosstab(df_filtered['Weather_Conditions'], df_filtered['Severity'])
                st.dataframe(crosstab.style.background_gradient(cmap='Purples'), use_container_width=True)

        with st.container(border=True):
            st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>🔍 Interactive Safety Records Explorer</h3>", unsafe_allow_html=True)
            st.write("Browse, search, and filter through the active database segment:")
            st.dataframe(
                df_filtered[['Accident_Index', 'Date', 'Speed_Limit', 'Road_Type', 'Severity', 'District', 'Weather_Conditions', 'Road_Surface_Conditions']],
                use_container_width=True,
                hide_index=True,
                height=350
            )

    # ----------------- PAGE 3: SPATIAL MAPPING -----------------
    elif selected_page == "Spatial Mapping":
        st.markdown('<div class="title-banner"><h1>Geographical Distribution</h1></div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>📍 Coordinate Hotspots Spread</h3>", unsafe_allow_html=True)
            st.write("Spatial incident coordinates plotting. Brighter markers indicate high density/clustering zones.")
            map_fig = create_geographical_map(df_filtered)
            if map_fig:
                st.plotly_chart(map_fig, use_container_width=True)

    # ----------------- PAGE 4: INSIGHTS & EXPORT -----------------
    elif selected_page == "Insights & Export":
        st.markdown('<div class="title-banner"><h1>Insights & Export Suite</h1></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            with st.container(border=True):
                st.markdown("<h3 style='color: #00C8FF; font-weight:700; margin-top:0;'>🔮 Automated Safety Insights</h3>", unsafe_allow_html=True)
                
                tot_incidents = len(df_filtered)
                fatal_count = len(df_filtered[df_filtered['Severity'] == 'Fatal'])
                wet_count = len(df_filtered[df_filtered['Road_Surface_Conditions'] == 'Wet or damp'])
                urban_pct = (len(df_filtered[df_filtered['Urban_or_Rural_Area'] == 'Urban']) / tot_incidents) * 100 if tot_incidents > 0 else 0
                
                insights_md = f"""
                - **Total Active Database Incidents:** A total of **{tot_incidents:,}** road safety logs are loaded under current active filters.
                - **Severity Focus:** **{fatal_count:,} ({fatal_count/tot_incidents*100:.1f}%)** incidents are categorized under the fatal threshold. Immediate safety intervention recommended.
                - **Wet Weather Risk Index:** Approximately **{wet_count:,} ({wet_count/tot_incidents*100:.1f}%)** incidents occurred during wet/damp conditions, showing strong slippery-road safety hazards.
                - **Urban Density Bottlenecks:** Densely structured Urban environments accounted for **{urban_pct:.1f}%** of the current dataset records.
                """
                st.markdown(textwrap.dedent(insights_md).strip())
                
            with st.container(border=True):
                st.markdown("<h3 style='color: #FF007F; font-weight:700; margin-top:0;'>📥 Database Extraction</h3>", unsafe_allow_html=True)
                st.write("Export the current filtered view in CSV format for offline reporting.")
                
                csv_data = df_filtered.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="💾 Download Current View as CSV",
                    data=csv_data,
                    file_name="road_guard_filtered_data.csv",
                    mime="text/csv"
                )
                
        with col2:
            with st.container(border=True):
                st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>📊 Activity Summary Stream</h3>", unsafe_allow_html=True)
                st.dataframe(
                    df_filtered[['Accident_Index', 'Date', 'Speed_Limit', 'Road_Type', 'Severity', 'District']],
                    use_container_width=True,
                    hide_index=True,
                    height=300
                )



# import streamlit as st
# import pandas as pd
# import numpy as np
# import os
# from streamlit_option_menu import option_menu
# import plotly.express as px
# import textwrap

# # Import our custom modules
# from utils import load_and_preprocess_data, get_filter_options, filter_dataframe
# from style import get_custom_css
# from charts import (
#     create_monthly_trend_chart,
#     create_road_type_horizontal_bar,
#     create_donut_charts,
#     create_district_treemap,
#     create_speed_limit_chart,
#     create_geographical_map
# )

# # Page Configuration
# st.set_page_config(
#     page_title="RoadGuard Analytics",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Helper to render clean HTML without markdown code block interpretation
# def render_html(html_str):
#     st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# # Load CSS Design System
# st.markdown(get_custom_css(), unsafe_allow_html=True)

# # Load Data Engine
# @st.cache_data
# def get_cached_data():
#     return load_and_preprocess_data()

# try:
#     df_raw = get_cached_data()
# except Exception as e:
#     st.error(f"Error loading safety database: {e}")
#     st.stop()

# # Sidebar Navigation
# with st.sidebar:
#     st.markdown("<h2 style='text-align: center; color: #FFFFFF; font-weight:800; letter-spacing:0.05em; margin-bottom: 0;'>🛡️ ROADGUARD</h2>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #A0A5C1; font-size:0.85rem; margin-top:2px; margin-bottom: 10px;'>UK Safety Intelligence</p>", unsafe_allow_html=True)
#     st.markdown("<hr style='border-color: rgba(255, 0, 127, 0.2); margin-top: 5px; margin-bottom: 15px;'/>", unsafe_allow_html=True)
    
#     # Custom Sidebar Navigation Menu
#     selected_page = option_menu(
#         menu_title=None,
#         options=["Executive Overview", "Deep Dive Analytics", "Spatial Mapping", "Insights & Export"],
#         icons=["speedometer2", "graph-up", "map", "download"],
#         menu_icon="cast",
#         default_index=0,
#         styles={
#             "container": {"padding": "0!important", "background-color": "transparent"},
#             "icon": {"color": "#A0A5C1", "font-size": "0.95rem"}, 
#             "nav-link": {
#                 "font-size": "0.85rem",
#                 "text-align": "left",
#                 "margin": "3px 0px",
#                 "color": "#FFFFFF",
#                 "background-color": "transparent",
#                 "padding": "8px 12px"
#             },
#             "nav-link-selected": {
#                 "background": "linear-gradient(135deg, rgba(255, 0, 127, 0.25) 0%, rgba(0, 200, 255, 0.25) 100%)",
#                 "border": "1px solid rgba(255, 0, 127, 0.4)",
#                 "font-weight": "600"
#             }
#         }
#     )
    
#     st.markdown("<br><h4 style='color: #00C8FF; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;'>GLOBAL FILTER SUITE</h4>", unsafe_allow_html=True)
#     filter_opts = get_filter_options(df_raw)
    
#     # Global Sidebar Filter Widgets
#     road_surface_filter = st.selectbox("Road Surface Condition", filter_opts['road_surface'])
#     weather_filter = st.selectbox("Weather Condition", filter_opts['weather'])
#     severity_filter = st.selectbox("Accident Severity", filter_opts['severity'])
#     urban_rural_filter = st.selectbox("Urban or Rural Area", filter_opts['urban_rural'])
#     district_filter = st.selectbox("Filter by District", filter_opts['district'])

# # Apply filter pipeline
# df_filtered = filter_dataframe(
#     df_raw,
#     road_surface=road_surface_filter,
#     weather=weather_filter,
#     severity=severity_filter,
#     urban_rural=urban_rural_filter,
#     district=district_filter
# )

# # Extract CY Current Year data (2022)
# df_cy = df_filtered[df_filtered['Year'] == 2022] if not df_filtered.empty else pd.DataFrame()

# # Helper function to display empty state
# def render_empty_state(message="No safety incident records match the active filter criteria."):
#     st.markdown(f"""
#     <div class="empty-state" style="margin-top: 40px;">
#         <div class="empty-state-icon">🔍</div>
#         <h3 style="color: #FFFFFF; font-weight:700; margin-top:0;">No Data Found</h3>
#         <p class="empty-state-text">{message}</p>
#     </div>
#     """, unsafe_allow_html=True)

# # ----------------- ROUTING LOGIC: MULTI-PAGE DASHBOARD -----------------

# if df_filtered.empty:
#     st.markdown(f'<div class="title-banner"><h1>{selected_page}</h1></div>', unsafe_allow_html=True)
#     render_empty_state()

# else:
#     # ----------------- PAGE 1: EXECUTIVE OVERVIEW -----------------
#     if selected_page == "Executive Overview":
#         st.markdown('<div class="title-banner"><h1>Road Accident Analysis</h1></div>', unsafe_allow_html=True)
        
#         # Metric Computations (CY vs PY)
#         df_py = df_filtered[df_filtered['Year'] == 2021]
        
#         def compute_metric_and_delta(column, is_count=False):
#             if is_count:
#                 cy_val = len(df_cy)
#                 py_val = len(df_py)
#             else:
#                 cy_val = df_cy[column].sum() if not df_cy.empty else 0
#                 py_val = df_py[column].sum() if not df_py.empty else 0
                
#             delta_pct = 0.0
#             if py_val > 0:
#                 delta_pct = ((cy_val - py_val) / py_val) * 100
                
#             return cy_val, delta_pct
            
#         cy_casualties, d_casualties = compute_metric_and_delta('Casualties')
#         cy_accidents, d_accidents = compute_metric_and_delta(None, is_count=True)
        
#         # Severity breakdowns for casualties
#         def get_severity_casualties(df, severity_level):
#             sub = df[df['Severity'] == severity_level]
#             return sub['Casualties'].sum() if not sub.empty else 0
            
#         cy_fatal = get_severity_casualties(df_cy, 'Fatal')
#         py_fatal = get_severity_casualties(df_py, 'Fatal')
#         d_fatal = ((cy_fatal - py_fatal) / py_fatal * 100) if py_fatal > 0 else 0.0
        
#         cy_serious = get_severity_casualties(df_cy, 'Serious')
#         py_serious = get_severity_casualties(df_py, 'Serious')
#         d_serious = ((cy_serious - py_serious) / py_serious * 100) if py_serious > 0 else 0.0
        
#         cy_slight = get_severity_casualties(df_cy, 'Slight')
#         py_slight = get_severity_casualties(df_py, 'Slight')
#         d_slight = ((cy_slight - py_slight) / py_slight * 100) if py_slight > 0 else 0.0

#         def fmt_val(val):
#             if val >= 1000:
#                 return f"{val / 1000:.1f}K"
#             return f"{val:,}"

#         # KPI Metric Grid Row
#         kpi_cols = st.columns(5)
#         kpi_titles = ["Total CY Casualties", "Total CY Accidents", "CY Fatal Casualties", "CY Serious Casualties", "CY Slight Casualties"]
#         kpi_vals = [cy_casualties, cy_accidents, cy_fatal, cy_serious, cy_slight]
#         kpi_deltas = [d_casualties, d_accidents, d_fatal, d_serious, d_slight]
        
#         for idx, col in enumerate(kpi_cols):
#             with col:
#                 metric_html = f"""
#                 <div data-testid="stMetric" style="margin-bottom:20px;">
#                     <div data-testid="stMetricLabel">{kpi_titles[idx]}</div>
#                     <div data-testid="stMetricValue">{fmt_val(kpi_vals[idx])}</div>
#                     <div class="delta-down">{kpi_deltas[idx]:.1f}% vs PY</div>
#                 </div>
#                 """
#                 render_html(metric_html)
                
#         # Main Layout Grid for Charts & Widgets
#         body_cols = st.columns([1, 2.2, 1.2])
        
#         # LEFT COLUMN: Casualties by Vehicle Type (Tall Scrolling List)
#         with body_cols[0]:
#             vehicle_data = df_cy.groupby('Vehicle_Type').agg({'Casualties': 'sum'}).reset_index()
#             vehicle_data = vehicle_data.sort_values(by='Casualties', ascending=False)
            
#             vehicle_html = '<div class="vehicle-list-container"><div class="vehicle-title">Vehicle Types</div>'
#             for _, row in vehicle_data.iterrows():
#                 vehicle_html += f'<div class="vehicle-item"><div class="vehicle-item-label">{row["Vehicle_Type"]}</div><div class="vehicle-item-val">{row["Casualties"]:,}</div></div>'
#             vehicle_html += '</div>'
            
#             render_html(vehicle_html)
            
#         # MIDDLE COLUMN: Line chart
#         with body_cols[1]:
#             # Monthly Trend (Height set to 540 to match the left column height perfectly)
#             with st.container(border=True):
#                 trend_fig = create_monthly_trend_chart(df_filtered, height=540)
#                 if trend_fig:
#                     st.plotly_chart(trend_fig, use_container_width=True)
                
#         # RIGHT COLUMN: Treemap
#         with body_cols[2]:
#             # Geographical Hotspots (Height set to 540 to match the left column height perfectly)
#             with st.container(border=True):
#                 treemap_fig = create_district_treemap(df_cy, height=540)
#                 if treemap_fig:
#                     st.plotly_chart(treemap_fig, use_container_width=True)

#         # Full-width center section for Casualties Distribution by Road Type
#         with st.container(border=True):
#             bar_fig = create_road_type_horizontal_bar(df_cy, height=450)
#             if bar_fig:
#                 st.plotly_chart(bar_fig, use_container_width=True)

#         # Full-width bottom section for Donut Charts
#         # Donut Chart 1: Urban vs Rural Areas
#         with st.container(border=True):
#             donut1 = create_donut_charts(df_cy, 'Urban_or_Rural_Area')
#             if donut1:
#                 st.plotly_chart(donut1, use_container_width=True)
        
#         # Donut Chart 2: Light Conditions
#         with st.container(border=True):
#             donut2 = create_donut_charts(df_cy, 'Light_Conditions')
#             if donut2:
#                 st.plotly_chart(donut2, use_container_width=True)

#     # ----------------- PAGE 2: DEEP DIVE ANALYTICS -----------------
#     elif selected_page == "Deep Dive Analytics":
#         st.markdown('<div class="title-banner"><h1>Deep Dive Analytics</h1></div>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns([1.5, 1])
        
#         with col1:
#             with st.container(border=True):
#                 st.markdown("<h3 style='color: #00C8FF; font-weight:700; margin-top:0;'>⚡ Speed Limit Distribution</h3>", unsafe_allow_html=True)
#                 speed_fig = create_speed_limit_chart(df_filtered)
#                 if speed_fig:
#                     st.plotly_chart(speed_fig, use_container_width=True)
            
#         with col2:
#             with st.container(border=True):
#                 st.markdown("<h3 style='color: #FF007F; font-weight:700; margin-top:0;'>📊 Incident Severity Cross Tabulation</h3>", unsafe_allow_html=True)
#                 crosstab = pd.crosstab(df_filtered['Weather_Conditions'], df_filtered['Severity'])
#                 st.dataframe(crosstab.style.background_gradient(cmap='Purples'), use_container_width=True)

#         with st.container(border=True):
#             st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>🔍 Interactive Safety Records Explorer</h3>", unsafe_allow_html=True)
#             st.write("Browse, search, and filter through the active database segment:")
#             st.dataframe(
#                 df_filtered[['Accident_Index', 'Date', 'Speed_Limit', 'Road_Type', 'Severity', 'District', 'Weather_Conditions', 'Road_Surface_Conditions']],
#                 use_container_width=True,
#                 hide_index=True,
#                 height=350
#             )

#     # ----------------- PAGE 3: SPATIAL MAPPING -----------------
#     elif selected_page == "Spatial Mapping":
#         st.markdown('<div class="title-banner"><h1>Geographical Distribution</h1></div>', unsafe_allow_html=True)
        
#         with st.container(border=True):
#             st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>📍 Coordinate Hotspots Spread</h3>", unsafe_allow_html=True)
#             st.write("Spatial incident coordinates plotting. Brighter markers indicate high density/clustering zones.")
#             map_fig = create_geographical_map(df_filtered)
#             if map_fig:
#                 st.plotly_chart(map_fig, use_container_width=True)

#     # ----------------- PAGE 4: INSIGHTS & EXPORT -----------------
#     elif selected_page == "Insights & Export":
#         st.markdown('<div class="title-banner"><h1>Insights & Export Suite</h1></div>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns([1.5, 1])
        
#         with col1:
#             with st.container(border=True):
#                 st.markdown("<h3 style='color: #00C8FF; font-weight:700; margin-top:0;'>🔮 Automated Safety Insights</h3>", unsafe_allow_html=True)
                
#                 tot_incidents = len(df_filtered)
#                 fatal_count = len(df_filtered[df_filtered['Severity'] == 'Fatal'])
#                 wet_count = len(df_filtered[df_filtered['Road_Surface_Conditions'] == 'Wet or damp'])
#                 urban_pct = (len(df_filtered[df_filtered['Urban_or_Rural_Area'] == 'Urban']) / tot_incidents) * 100 if tot_incidents > 0 else 0
                
#                 insights_md = f"""
#                 - **Total Active Database Incidents:** A total of **{tot_incidents:,}** road safety logs are loaded under current active filters.
#                 - **Severity Focus:** **{fatal_count:,} ({fatal_count/tot_incidents*100:.1f}%)** incidents are categorized under the fatal threshold. Immediate safety intervention recommended.
#                 - **Wet Weather Risk Index:** Approximately **{wet_count:,} ({wet_count/tot_incidents*100:.1f}%)** incidents occurred during wet/damp conditions, showing strong slippery-road safety hazards.
#                 - **Urban Density Bottlenecks:** Densely structured Urban environments accounted for **{urban_pct:.1f}%** of the current dataset records.
#                 """
#                 st.markdown(textwrap.dedent(insights_md).strip())
                
#             with st.container(border=True):
#                 st.markdown("<h3 style='color: #FF007F; font-weight:700; margin-top:0;'>📥 Database Extraction</h3>", unsafe_allow_html=True)
#                 st.write("Export the current filtered view in CSV format for offline reporting.")
                
#                 csv_data = df_filtered.to_csv(index=False).encode('utf-8')
                
#                 st.download_button(
#                     label="💾 Download Current View as CSV",
#                     data=csv_data,
#                     file_name="road_guard_filtered_data.csv",
#                     mime="text/csv"
#                 )
                
#         with col2:
#             with st.container(border=True):
#                 st.markdown("<h3 style='color: #FFFFFF; font-weight:700; margin-top:0;'>📊 Activity Summary Stream</h3>", unsafe_allow_html=True)
#                 st.dataframe(
#                     df_filtered[['Accident_Index', 'Date', 'Speed_Limit', 'Road_Type', 'Severity', 'District']],
#                     use_container_width=True,
#                     hide_index=True,
#                     height=300
#                 )
