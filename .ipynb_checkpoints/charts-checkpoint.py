import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Standard styling config for all Plotly charts
def apply_neon_theme(fig, height=350, margin=None):
    if margin is None:
        margin = dict(l=40, r=40, t=80, b=40)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF',
        font_family='Inter',
        height=height,
        margin=margin,
        title=dict(
            font=dict(size=18, family='Inter', color='#FFFFFF', weight='bold'),
            x=0.5, y=0.95,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            linecolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            title=dict(font=dict(size=13, family='Inter', color='#A0A5C1'))
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            linecolor='rgba(255, 255, 255, 0.1)',
            zeroline=False,
            title=dict(font=dict(size=13, family='Inter', color='#A0A5C1'))
        )
    )
    return fig

def create_monthly_trend_chart(df, height=540):
    if df.empty:
        return None

    # Group by Year and Month
    trend = df.groupby(['Year', 'Month', 'Month_Name']).agg({'Casualties': 'sum'}).reset_index()
    # Sort months correctly
    trend = trend.sort_values(by=['Year', 'Month'])
    
    # Pivot to get years side-by-side
    pivot_df = trend.pivot(index='Month_Name', columns='Year', values='Casualties')
    
    # Reorder index to follow standard calendar
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_df = pivot_df.reindex(month_order)
    pivot_df = pivot_df.dropna(how='all') # Drop months with no data
    
    fig = go.Figure()
    
    # Prior Year (2021) - Muted silver-purple line
    if 2021 in pivot_df.columns:
        fig.add_trace(go.Scatter(
            x=pivot_df.index,
            y=pivot_df[2021],
            name='2021 (Prior Year)',
            mode='lines',
            line=dict(color='rgba(160, 165, 193, 0.5)', width=3, dash='dot'),
            hoverinfo='x+y'
        ))
        
    # Current Year (2022) - Cyber Cyan glowing filled area
    if 2022 in pivot_df.columns:
        fig.add_trace(go.Scatter(
            x=pivot_df.index,
            y=pivot_df[2022],
            name='2022 (Current Year)',
            mode='lines',
            line=dict(color='#00C8FF', width=4),
            fill='tozeroy',
            fillcolor='rgba(0, 200, 255, 0.12)',
            hoverinfo='x+y'
        ))
        
    fig.update_layout(
        title=dict(
            text="CY vs PY Casualties – Monthly Trend Analysis"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#FFFFFF')
        ),
        hovermode="x unified"
    )
    
    return apply_neon_theme(fig, height=height)

def create_road_type_horizontal_bar(df, height=450):
    if df.empty:
        return None
        
    road_data = df.groupby('Road_Type').agg({'Casualties': 'sum'}).reset_index()
    road_data = road_data.sort_values(by='Casualties', ascending=True)
    
    fig = px.bar(
        road_data,
        x='Casualties',
        y='Road_Type',
        orientation='h',
        color_discrete_sequence=['#FF007F'] # Neon Pink bars
    )
    
    fig.update_traces(
        marker_color='#FF007F',
        marker_line_color='rgba(255, 0, 127, 0.6)',
        marker_line_width=1,
        opacity=0.85
    )
    
    fig.update_layout(
        title=dict(
            text="Casualties Distribution by Road Type"
        ),
        xaxis_title="Casualties Count",
        yaxis_title="",
        bargap=0.35
    )
    
    return apply_neon_theme(fig, height=height, margin=dict(l=160, r=20, t=60, b=40))

def create_donut_charts(df, column):
    if df.empty or column not in df.columns:
        return None
        
    donut_data = df.groupby(column).size().reset_index(name='Count')
    
    # Set labels based on column
    title_text = "CY Casualties: Urban vs Rural Areas" if "Urban" in column else "Casualties by Light Conditions"
    
    # Custom color mappings: Cyan for first category, Pink for second
    color_map = {
        'Urban': '#00C8FF',
        'Rural': '#FF007F',
        'Day': '#FF007F',
        'Dark': '#00C8FF'
    }
    
    colors = [color_map.get(str(x), '#A0A5C1') for x in donut_data[column]]
    
    fig = go.Figure(data=[go.Pie(
        labels=donut_data[column],
        values=donut_data['Count'],
        hole=.6,
        marker=dict(colors=colors, line=dict(color='#0B0D1B', width=3)),
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        textposition='outside',
        textfont=dict(size=13, color='#FFFFFF'),
        domain=dict(y=[0.05, 0.85])
    )])
    
    fig.update_layout(
        title=dict(
            text=title_text
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#FFFFFF')
        )
    )
    
    return apply_neon_theme(fig, height=450, margin=dict(l=50, r=50, t=80, b=60))

def create_district_treemap(df, height=540):
    if df.empty:
        return None
        
    # Get top 10 districts by casualities
    district_data = df.groupby('District').agg({'Casualties': 'sum'}).reset_index()
    district_data = district_data.sort_values(by='Casualties', ascending=False).head(10)
    
    # Mosaic purple/magenta block colors (Vercel-meets-Synthwave)
    colors = [
        '#2D0B2E', '#4A0D4A', '#651163', '#80157A', 
        '#9B1C90', '#B523A4', '#CD2BB5', '#E336C3', 
        '#F644CD', '#FF55D6'
    ]
    
    fig = px.treemap(
        district_data,
        path=[px.Constant("Top 10 Districts"), 'District'],
        values='Casualties',
        color='Casualties',
        color_continuous_scale=colors
    )
    
    fig.update_layout(
        title=dict(
            text="Geographical Hotspots – Top 10 Districts"
        ),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    fig.update_traces(
        textinfo="label+value",
        textposition="middle center",
        texttemplate="<b>%{label}</b><br>%{value} Casualties",
        textfont=dict(size=14, color='#FFFFFF')
    )
    
    return apply_neon_theme(fig, height=height)

def create_speed_limit_chart(df):
    if df.empty:
        return None
    speed_data = df.groupby('Speed_Limit').size().reset_index(name='Accident Count')
    fig = px.bar(
        speed_data,
        x='Speed_Limit',
        y='Accident Count',
        labels={'Speed_Limit': 'Speed Limit (mph)', 'Accident Count': 'Incident Count'},
        color_discrete_sequence=['#00C8FF']
    )
    fig.update_traces(
        marker_color='#00C8FF',
        marker_line_color='rgba(0, 200, 255, 0.6)',
        marker_line_width=1,
        opacity=0.85
    )
    fig.update_layout(
        title=dict(
            text="Incident Distribution by Speed Limit"
        ),
        xaxis_title="Speed Limit (mph)",
        yaxis_title="Incident Count",
        bargap=0.35
    )
    return apply_neon_theme(fig)

def create_geographical_map(df):
    if df.empty:
        return None
    
    fig = px.scatter(
        df,
        x='Longitude',
        y='Latitude',
        color='Severity',
        size='Casualties',
        hover_name='District',
        hover_data=['Date', 'Speed_Limit', 'Road_Type'],
        color_discrete_map={'Fatal': '#FF007F', 'Serious': '#FFB300', 'Slight': '#00C8FF'},
        opacity=0.75
    )
    
    fig.update_layout(
        title=dict(
            text="Geographical Incident Hotspots Mapping"
        ),
        xaxis=dict(showgrid=False, zeroline=False, title="Longitude"),
        yaxis=dict(showgrid=False, zeroline=False, title="Latitude"),
        plot_bgcolor='rgba(26, 21, 44, 0.4)'
    )
    return apply_neon_theme(fig, height=450)
