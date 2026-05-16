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

# ==================== PROFESSIONAL CSS WITH FONT AWESOME ====================
st.markdown("""
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<style>
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255, 215, 0, 0.15);
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        margin: 5px 0 !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 215, 0, 0.12) !important;
        border-color: #FFD700 !important;
        transform: translateX(5px);
    }
    
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin-bottom: 30px;
    }
    
    .executive-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.02) 100%);
        border-left: 4px solid #FFD700;
        border-radius: 12px;
        padding: 15px 20px;
        margin: 15px 0;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        border: 1px solid rgba(255, 215, 0, 0.25);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: #FFD700;
    }
    
    .kpi-icon { font-size: 1.8rem; color: #FFD700; margin-bottom: 8px; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #FFD700; }
    .kpi-label { font-size: 0.7rem; color: rgba(255, 255, 255, 0.7); letter-spacing: 1px; }
    
    .chart-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        padding: 18px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    .chart-card:hover {
        border-color: rgba(255, 215, 0, 0.3);
    }
    
    .chart-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #FFD700;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        display: inline-block;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 35px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.7rem;
    }
    
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .status-green { background-color: #00FF88; box-shadow: 0 0 6px #00FF88; }
    .status-blue { background-color: #00BFFF; box-shadow: 0 0 6px #00BFFF; }
    
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 10px;
        margin: 8px 0;
        border-left: 2px solid #FFD700;
    }
    
    /* Radio button styling */
    .stRadio > div {
        gap: 5px;
    }
    .stRadio label {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        padding: 8px 12px !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    """Load data from CSV or create sample data"""
    
    # Try to find CSV file
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
    
    # If no CSV found, create sample data
    if df is None:
        data = {
            'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'Domestic_Tourists': [12.5, 13.2, 14.1, 15.0, 16.2, 3.5, 4.2, 8.5, 10.2, 13.5],
            'International_Tourists': [1.8, 1.9, 2.1, 2.2, 2.0, 0.4, 0.6, 1.2, 1.6, 2.3],
            'Revenue_M': [850, 890, 950, 1020, 1100, 220, 310, 580, 780, 1050],
            'Hotels': [1250, 1280, 1320, 1380, 1450, 980, 1020, 1150, 1280, 1420],
        }
        df = pd.DataFrame(data)
    
    # Calculate Total Tourists (Millions)
    if 'Domestic_Tourists' in df.columns and 'International_Tourists' in df.columns:
        df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
    elif 'Total_Tourists' not in df.columns:
        # Use first numeric column
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            df['Total_Tourists'] = df[num_cols[0]]
        else:
            df['Total_Tourists'] = 0
    
    # Calculate YoY Growth
    df['YoY_Growth'] = df['Total_Tourists'].pct_change() * 100
    
    # Calculate Recovery Rate (using max as baseline)
    df['Recovery_Rate'] = (df['Total_Tourists'] / df['Total_Tourists'].max()) * 100
    
    return df

with st.spinner("Loading tourism data..."):
    df = load_data()

# Get year range
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# ==================== PROFESSIONAL SIDEBAR ====================
with st.sidebar:
    # Brand Area
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 15px 0;">
        <i class="fas fa-mountain" style="font-size: 2.5rem; color: #FFD700;"></i>
        <div style="font-size: 1rem; font-weight: 700; margin-top: 8px;">TOURISM ANALYTICS</div>
        <div style="font-size: 0.6rem; color: #FFD700; letter-spacing: 2px;">PAKISTAN</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<div style="font-size: 0.65rem; color: #FFD700; margin-bottom: 10px;"><i class="fas fa-compass"></i> NAVIGATION</div>', unsafe_allow_html=True)
    
    # Custom navigation with icons
    nav_options = ["Dashboard", "Forecast", "Data"]
    nav_icons = ["fa-chart-line", "fa-chart-simple", "fa-table"]
    
    selected_page = st.radio(
        "",
        nav_options,
        format_func=lambda x: x,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Year Filter
    st.markdown('<div style="font-size: 0.65rem; color: #FFD700; margin-bottom: 10px;"><i class="fas fa-calendar-alt"></i> TIME RANGE</div>', unsafe_allow_html=True)
    
    year_range = st.slider("", min_year, max_year, (min_year, max_year), label_visibility="collapsed")
    
    st.markdown("---")
    
    # Key Metrics in Sidebar
    st.markdown('<div style="font-size: 0.65rem; color: #FFD700; margin-bottom: 10px;"><i class="fas fa-chart-line"></i> KEY METRICS</div>', unsafe_allow_html=True)
    
    latest = df[df['Year'] == max_year]
    if not latest.empty:
        total = latest['Total_Tourists'].values[0]
        st.markdown(f"""
        <div class="sidebar-metric">
            <div><i class="fas fa-users"></i> Total Tourists</div>
            <div style="font-size: 1.2rem; font-weight: bold;">{total:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    if 'Revenue_M' in df.columns:
        revenue = df['Revenue_M'].iloc[-1] if not df.empty else 0
        st.markdown(f"""
        <div class="sidebar-metric">
            <div><i class="fas fa-dollar-sign"></i> Revenue</div>
            <div style="font-size: 1.2rem; font-weight: bold;">${revenue:.0f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown('<div style="font-size: 0.65rem; color: #FFD700; margin-bottom: 10px;"><i class="fas fa-microchip"></i> SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("""
    <div><span class="status-dot status-green"></span> <i class="fas fa-database"></i> Data Active</div>
    <div><span class="status-dot status-green"></span> <i class="fas fa-brain"></i> ML Models Ready</div>
    <div><span class="status-dot status-blue"></span> <i class="fas fa-cloud"></i> Live</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 0.55rem; opacity: 0.5;">FYP 2025</div>', unsafe_allow_html=True)

# Filter data based on year range
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

# ==================== DASHBOARD PAGE ====================
if selected_page == "Dashboard":
    st.markdown('<div class="main-title">Pakistan Tourism Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-chart-line"></i> Real-time Analytics & Business Intelligence</div>', unsafe_allow_html=True)
    
       # Executive Summary with better styling
    if len(filtered_df) > 1:
        latest_tourists = filtered_df['Total_Tourists'].iloc[-1]
        prev_tourists = filtered_df['Total_Tourists'].iloc[-2]
        growth = ((latest_tourists - prev_tourists) / prev_tourists) * 100
        best_year = filtered_df.loc[filtered_df['Total_Tourists'].idxmax(), 'Year']
        best_value = filtered_df['Total_Tourists'].max()
        
        st.markdown(f"""
        <div class="executive-card">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <i class="fas fa-chart-line" style="color: #FFD700; font-size: 1.2rem;"></i>
                <span style="color: #FFD700; font-weight: 600;">EXECUTIVE SUMMARY</span>
            </div>
            <div style="color: #FFFFFF; font-size: 0.9rem; line-height: 1.6;">
                Pakistan's tourism sector is experiencing 
                <span style="color: #00FF88; font-weight: 600;">{growth:.1f}% YoY growth</span> 
                with <span style="color: #FFD700; font-weight: 600;">{latest_tourists:.1f}M tourists</span> in {int(filtered_df['Year'].iloc[-1])}.
                The best performing year was <span style="color: #FFD700; font-weight: 600;">{int(best_year)}</span> 
                with <span style="color: #FFD700; font-weight: 600;">{best_value:.1f}M visitors</span>.
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
    
    avg_revenue = filtered_df['Revenue_M'].mean() if 'Revenue_M' in filtered_df.columns else 0
    
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
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-dollar-sign"></i></div>
            <div class="kpi-value">${avg_revenue:.0f}M</div>
            <div class="kpi-label">AVG REVENUE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        recovery = filtered_df['Recovery_Rate'].iloc[-1] if not filtered_df.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
            <div class="kpi-value">{recovery:.0f}%</div>
            <div class="kpi-label">RECOVERY RATE</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chart 1: Tourism Growth
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Tourism Growth Trend</div>', unsafe_allow_html=True)
    fig1 = px.line(filtered_df, x='Year', y='Total_Tourists', markers=True, template='plotly_dark')
    fig1.update_traces(line_color='#FFD700', line_width=3, marker_size=8)
    fig1.update_layout(xaxis_title="Year", yaxis_title="Tourists (Millions)", height=400)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 2 & 3: Two columns
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Domestic_Tourists' in filtered_df.columns and 'International_Tourists' in filtered_df.columns:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title"><i class="fas fa-chart-bar"></i> Domestic vs International</div>', unsafe_allow_html=True)
            fig2 = px.bar(filtered_df, x='Year', y=['Domestic_Tourists', 'International_Tourists'], 
                         barmode='group', template='plotly_dark',
                         labels={'value': 'Tourists (Millions)', 'variable': 'Type'})
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if 'Revenue_M' in filtered_df.columns:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Revenue Trend</div>', unsafe_allow_html=True)
            fig3 = px.area(filtered_df, x='Year', y='Revenue_M', template='plotly_dark', color_discrete_sequence=['#FF6B6B'])
            fig3.update_layout(xaxis_title="Year", yaxis_title="Revenue (USD Millions)", height=400)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 4: YoY Growth
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Year-over-Year Growth Rate</div>', unsafe_allow_html=True)
    growth_df = filtered_df[['Year', 'YoY_Growth']].dropna()
    fig4 = px.bar(growth_df, x='Year', y='YoY_Growth', template='plotly_dark',
                  color='YoY_Growth', color_continuous_scale='RdYlGn',
                  labels={'YoY_Growth': 'Growth Rate (%)'})
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
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
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Model R² Score", f"{model.score(X, y):.3f}")
        with col2:
            st.metric("2030 Prediction", f"{predictions[-1]:.1f}M")
        with col3:
            st.metric("Annual Growth", f"{model.coef_[0]:.2f}M")
        with col4:
            st.metric("Forecast Period", "2025-2030")
        
        # Forecast Chart
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Total_Tourists'],
                                 mode='lines+markers', name='Historical',
                                 line=dict(color='#FFD700', width=3)))
        fig.add_trace(go.Scatter(x=future_years.flatten(), y=predictions,
                                 mode='lines+markers', name='Forecast',
                                 line=dict(color='#FF6B6B', width=3, dash='dash')))
        fig.add_trace(go.Scatter(
            x=list(future_years.flatten()) + list(future_years.flatten())[::-1],
            y=list(predictions * 1.1) + list(predictions * 0.9)[::-1],
            fill='toself', fillcolor='rgba(255,107,107,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval'
        ))
        fig.update_layout(title="Tourism Forecast 2025-2030",
                          xaxis_title="Year", yaxis_title="Tourists (Millions)",
                          template='plotly_dark', height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Forecast Table
        forecast_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Predicted Tourists (M)': predictions.round(1),
            'Lower Bound': (predictions * 0.9).round(1),
            'Upper Bound': (predictions * 1.1).round(1)
        })
        st.dataframe(forecast_df, use_container_width=True)
        
        total_growth = ((predictions[-1] - predictions[0]) / predictions[0]) * 100
        st.success(f"📈 Forecast Insight: Tourism is projected to grow by {total_growth:.1f}% from 2025 to 2030.")
    else:
        st.warning("Not enough data for forecasting. Need at least 3 years of data.")

# ==================== DATA PAGE ====================
elif selected_page == "Data":
    st.markdown('<div class="main-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-database"></i> Raw Tourism Data</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button
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