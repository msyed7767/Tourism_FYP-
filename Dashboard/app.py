import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

st.set_page_config(
    page_title="Pakistan Tourism Analytics",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PROFESSIONAL CSS WITH NEW COLOURS ====================
st.markdown("""
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<style>
    * { font-family: 'Inter', sans-serif; }
    
    /* Main Background - Fresh Professional Gradient */
    .stApp {
        background: linear-gradient(135deg, #0B1A2E 0%, #1B2F44 50%, #0F1A2A 100%);
    }
    
    /* Sidebar - Modern Deep Navy */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1622 0%, #0D1B2A 50%, #0A1622 100%);
        border-right: 1px solid rgba(0, 255, 255, 0.12);
    }
    
    [data-testid="stSidebar"] * {
        color: #E8EDF2 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(0, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        margin: 5px 0 !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(0, 255, 255, 0.15) !important;
        border-color: #00FFFF !important;
        transform: translateX(5px);
    }
    
    /* Main Title - Cyan to Gold Gradient */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00FFFF 0%, #00B4D8 30%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(200, 210, 220, 0.7);
        font-size: 0.85rem;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }
    
    /* Executive Card - Glass Effect with Cyan Border */
    .executive-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.08) 0%, rgba(0, 180, 216, 0.03) 100%);
        backdrop-filter: blur(10px);
        border-left: 4px solid #00FFFF;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 15px 0;
    }
    
    /* KPI Cards - Modern Glassmorphism */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #00FFFF;
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.15);
    }
    
    .kpi-icon { 
        font-size: 2rem; 
        background: linear-gradient(135deg, #00FFFF, #00B4D8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .kpi-value { 
        font-size: 1.6rem; 
        font-weight: 700; 
        background: linear-gradient(135deg, #FFFFFF, #00FFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-label { 
        font-size: 0.7rem; 
        color: rgba(200, 210, 220, 0.8); 
        letter-spacing: 1px; 
        margin-top: 8px;
    }
    
    /* Chart Cards */
    .chart-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
        border: 1px solid rgba(0, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .chart-card:hover {
        border-color: rgba(0, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.07);
    }
    
    .chart-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #00FFFF;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(0, 255, 255, 0.3);
        display: inline-block;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 35px;
        border-top: 1px solid rgba(0, 255, 255, 0.08);
        color: rgba(200, 210, 220, 0.4);
        font-size: 0.7rem;
    }
    
    /* Status Indicators */
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-green { background-color: #00FF88; box-shadow: 0 0 8px #00FF88; animation: pulse 2s infinite; }
    .status-cyan { background-color: #00FFFF; box-shadow: 0 0 8px #00FFFF; animation: pulse 2s infinite; }
    
    @keyframes pulse {
        0% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.5; transform: scale(1); }
    }
    
    /* Sidebar Metrics */
    .sidebar-metric {
        background: rgba(0, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 12px;
        margin: 8px 0;
        border-left: 2px solid #00FFFF;
    }
    
    /* Radio Buttons Styling */
    .stRadio > div {
        gap: 5px;
    }
    .stRadio label {
        background: rgba(0, 255, 255, 0.05);
        border-radius: 8px;
        padding: 8px 12px !important;
        width: 100%;
    }
    .stRadio label:hover {
        background: rgba(0, 255, 255, 0.12);
    }
    
    /* Slider Styling */
    [data-testid="stSidebar"] .stSlider {
        padding: 8px 0;
    }
    
    /* Metric Styling */
    [data-testid="stMetric"] {
        background: rgba(0, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px;
    }
    [data-testid="stMetric"] label {
        color: #00FFFF !important;
    }
    [data-testid="stMetric"] .stMetricValue {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    paths = [
        'Data/raw/pakistan_tourism_dataset.csv',
        'data/raw/pakistan_tourism_dataset.csv',
        'pakistan_tourism_dataset.csv',
    ]
    
    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    
    if df is None:
        data = {
            'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Domestic_Tourists': [12.5, 13.2, 14.1, 15.0, 16.2, 3.5, 4.2, 8.5, 10.2, 13.5],
            'International_Tourists': [1.8, 1.9, 2.1, 2.2, 2.0, 0.4, 0.6, 1.2, 1.6, 2.3],
            'Revenue_M': [850, 890, 950, 1020, 1100, 220, 310, 580, 780, 1050],
        }
        df = pd.DataFrame(data)
    
    if 'Domestic_Tourists' in df.columns and 'International_Tourists' in df.columns:
        df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
    elif 'Total_Tourists' not in df.columns:
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            df['Total_Tourists'] = df[num_cols[0]]
        else:
            df['Total_Tourists'] = 0
    
    df['YoY_Growth'] = df['Total_Tourists'].pct_change() * 100
    df['Recovery_Rate'] = (df['Total_Tourists'] / df['Total_Tourists'].max()) * 100
    
    return df

with st.spinner("Loading tourism data..."):
    df = load_data()

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# ==================== SIDEBAR WITH NEW COLOURS ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 25px 0 15px 0;">
        <i class="fas fa-mountain" style="font-size: 2.5rem; background: linear-gradient(135deg, #00FFFF, #00B4D8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"></i>
        <div style="font-size: 1rem; font-weight: 700; margin-top: 10px; background: linear-gradient(135deg, #FFFFFF, #00FFFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TOURISM ANALYTICS</div>
        <div style="font-size: 0.6rem; color: #00FFFF; letter-spacing: 2px; margin-top: 4px;">PAKISTAN</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.65rem; color: #00FFFF; letter-spacing: 1.5px; margin-bottom: 12px;"><i class="fas fa-compass"></i> NAVIGATION</div>', unsafe_allow_html=True)
    
    nav_options = ["Dashboard", "Forecast", "Data"]
    selected_page = st.radio("", nav_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.65rem; color: #00FFFF; letter-spacing: 1.5px; margin-bottom: 12px;"><i class="fas fa-calendar-alt"></i> TIME RANGE</div>', unsafe_allow_html=True)
    year_range = st.slider("", min_year, max_year, (min_year, max_year), label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.65rem; color: #00FFFF; letter-spacing: 1.5px; margin-bottom: 12px;"><i class="fas fa-chart-line"></i> KEY METRICS</div>', unsafe_allow_html=True)
    
    latest = df[df['Year'] == max_year]
    if not latest.empty:
        total = latest['Total_Tourists'].values[0]
        st.markdown(f"""
        <div class="sidebar-metric">
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-users" style="color: #00FFFF;"></i>
                <span style="font-size: 0.7rem; opacity: 0.8;">TOTAL TOURISTS</span>
            </div>
            <div style="font-size: 1.3rem; font-weight: bold; color: #00FFFF;">{total:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    if 'Revenue_M' in df.columns:
        revenue = df['Revenue_M'].iloc[-1] if not df.empty else 0
        st.markdown(f"""
        <div class="sidebar-metric">
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-dollar-sign" style="color: #00FFFF;"></i>
                <span style="font-size: 0.7rem; opacity: 0.8;">REVENUE</span>
            </div>
            <div style="font-size: 1.3rem; font-weight: bold; color: #00FFFF;">${revenue:.0f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.65rem; color: #00FFFF; letter-spacing: 1.5px; margin-bottom: 12px;"><i class="fas fa-microchip"></i> SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 8px 0; display: flex; align-items: center; gap: 8px;">
        <span class="status-dot status-green"></span>
        <span><i class="fas fa-database"></i> Data Active</span>
    </div>
    <div style="margin: 8px 0; display: flex; align-items: center; gap: 8px;">
        <span class="status-dot status-green"></span>
        <span><i class="fas fa-brain"></i> ML Models Ready</span>
    </div>
    <div style="margin: 8px 0; display: flex; align-items: center; gap: 8px;">
        <span class="status-dot status-cyan"></span>
        <span><i class="fas fa-cloud"></i> Live Dashboard</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 0.55rem; opacity: 0.4; letter-spacing: 1px;">FINAL YEAR PROJECT 2025</div>', unsafe_allow_html=True)

# Filter data
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

# ==================== DASHBOARD PAGE ====================
if selected_page == "Dashboard":
    st.markdown('<div class="main-title">Pakistan Tourism Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-chart-line"></i> Real-time Analytics & Business Intelligence</div>', unsafe_allow_html=True)
    
    # Executive Summary
    if len(filtered_df) > 1:
        latest_tourists = filtered_df['Total_Tourists'].iloc[-1]
        prev_tourists = filtered_df['Total_Tourists'].iloc[-2]
        growth = ((latest_tourists - prev_tourists) / prev_tourists) * 100
        best_year = filtered_df.loc[filtered_df['Total_Tourists'].idxmax(), 'Year']
        best_value = filtered_df['Total_Tourists'].max()
        
        st.markdown(f"""
        <div class="executive-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <i class="fas fa-chart-line" style="color: #00FFFF; font-size: 1.2rem;"></i>
                <span style="color: #00FFFF; font-weight: 600; letter-spacing: 1px;">EXECUTIVE SUMMARY</span>
            </div>
            <div style="color: #D0D8E0; font-size: 0.9rem; line-height: 1.6;">
                Pakistan's tourism sector is experiencing 
                <span style="color: #00FF88; font-weight: 600;">{growth:.1f}% YoY growth</span> 
                with <span style="color: #00FFFF; font-weight: 600;">{latest_tourists:.1f}M tourists</span> in <span style="color: #FFFFFF;">{int(filtered_df['Year'].iloc[-1])}</span>.
                The best performing year was <span style="color: #00FFFF; font-weight: 600;">{int(best_year)}</span> 
                with <span style="color: #00FFFF; font-weight: 600;">{best_value:.1f}M visitors</span>.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Cards Row
    col1, col2, col3, col4 = st.columns(4)
    
    current_tourists = filtered_df['Total_Tourists'].iloc[-1] if not filtered_df.empty else 0
    
    if len(filtered_df) > 1:
        prev_tourists = filtered_df['Total_Tourists'].iloc[-2]
        growth_rate = ((current_tourists - prev_tourists) / prev_tourists) * 100
    else:
        growth_rate = 0
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-users"></i></div>
            <div class="kpi-value">{current_tourists:.1f}M</div>
            <div class="kpi-label">TOTAL TOURISTS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
            <div class="kpi-value">{growth_rate:+.1f}%</div>
            <div class="kpi-label">YoY GROWTH</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        recovery = filtered_df['Recovery_Rate'].iloc[-1] if not filtered_df.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
            <div class="kpi-value">{recovery:.0f}%</div>
            <div class="kpi-label">RECOVERY RATE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-calendar"></i></div>
            <div class="kpi-value">{len(filtered_df)}</div>
            <div class="kpi-label">YEARS DATA</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Tourism Growth Trend</div>', unsafe_allow_html=True)
    fig1 = px.line(filtered_df, x='Year', y='Total_Tourists', markers=True, template='plotly_dark')
    fig1.update_traces(line_color='#00FFFF', line_width=3, marker_size=8, marker_color='#00FFFF')
    fig1.update_layout(xaxis_title="Year", yaxis_title="Tourists (Millions)", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Second Chart
    if 'Revenue_M' in filtered_df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Revenue Trend</div>', unsafe_allow_html=True)
        fig2 = px.area(filtered_df, x='Year', y='Revenue_M', template='plotly_dark', color_discrete_sequence=['#00B4D8'])
        fig2.update_layout(xaxis_title="Year", yaxis_title="Revenue (USD Millions)", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FORECAST PAGE ====================
elif selected_page == "Forecast":
    st.markdown('<div class="main-title">AI-Powered Forecast 2025-2030</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-brain"></i> Machine Learning Predictions</div>', unsafe_allow_html=True)
    
    if len(filtered_df) >= 3:
        X = filtered_df[['Year']].values
        y = filtered_df['Total_Tourists'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_years = np.arange(2025, 2031).reshape(-1, 1)
        predictions = model.predict(future_years)
        
        # Better formatting for metric values
        r2_score = model.score(X, y)
        pred_2030 = predictions[-1]
        annual_growth = model.coef_[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model R² Score", f"{r2_score:.3f}")
        with col2:
            st.metric("2030 Prediction", f"{pred_2030:.1f}M")
        with col3:
            st.metric("Annual Growth", f"{annual_growth:.2f}M")
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Historical data line
        fig.add_trace(go.Scatter(
            x=filtered_df['Year'], 
            y=filtered_df['Total_Tourists'],
            mode='lines+markers', 
            name='Historical',
            line=dict(color='#00FFFF', width=3),
            marker=dict(color='#00FFFF', size=8)
        ))
        
        # Forecast line
        fig.add_trace(go.Scatter(
            x=future_years.flatten(), 
            y=predictions,
            mode='lines+markers', 
            name='Forecast',
            line=dict(color='#FF6B6B', width=3, dash='dash'),
            marker=dict(color='#FF6B6B', size=8)
        ))
        
        # Update layout with proper colours
        fig.update_layout(
            title=dict(
                text="Tourism Forecast 2025-2030",
                font=dict(color='#00FFFF', size=20)
            ),
            xaxis=dict(
                title=dict(text="Year", font=dict(color='#00FFFF', size=14)),
                tickfont=dict(color='#FFFFFF', size=12),
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                title=dict(text="Tourists (Millions)", font=dict(color='#00FFFF', size=14)),
                tickfont=dict(color='#FFFFFF', size=12),
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            legend=dict(
                font=dict(color='#FFFFFF', size=12),
                bgcolor='rgba(0,0,0,0.5)'
            ),
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Forecast Table with better formatting
        forecast_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Predicted Tourists (M)': predictions.round(1)
        })
        st.dataframe(forecast_df, use_container_width=True)
        
        # Insight message
        total_growth = ((predictions[-1] - predictions[0]) / predictions[0]) * 100
        st.info(f"📈 **Forecast Insight:** Tourism is projected to {'increase' if total_growth > 0 else 'decrease'} by {abs(total_growth):.1f}% from 2025 to 2030.")
        
    else:
        st.warning("⚠️ Not enough data for forecasting. Need at least 3 years of data.")
# ==================== DATA PAGE ====================
elif selected_page == "Data":
    st.markdown('<div class="main-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-database"></i> Raw Tourism Data</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = filtered_df.to_csv(index=False).encode()
    st.download_button(
        label="📥 Download CSV for Power BI",
        data=csv,
        file_name="pakistan_tourism_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <i class="fas fa-database"></i> Data Source: PTDC | World Bank &nbsp;|&nbsp;
    <i class="fab fa-python"></i> Python & Streamlit &nbsp;|&nbsp;
    <i class="fas fa-brain"></i> ML: Linear Regression &nbsp;|&nbsp;
    Final Year Project 2025
</div>
""", unsafe_allow_html=True)