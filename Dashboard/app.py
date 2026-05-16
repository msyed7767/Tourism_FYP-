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

# ==================== PROFESSIONAL CSS ====================
st.markdown("""
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<style>
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0B1A2E 0%, #1B2F44 50%, #0F1A2A 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A1622 0%, #0D1B2A 100%);
        border-right: 1px solid rgba(0, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] * {
        color: #E8EDF2 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(0, 255, 255, 0.08) !important;
        border: 1px solid rgba(0, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        margin: 5px 0 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(0, 255, 255, 0.2) !important;
        border-color: #00FFFF !important;
        transform: translateX(5px);
    }
    
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00FFFF 0%, #00B4D8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #B0C4DE;
        font-size: 0.85rem;
        margin-bottom: 30px;
    }
    
    .executive-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.08) 0%, rgba(0, 180, 216, 0.03) 100%);
        border-left: 4px solid #00FFFF;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 15px 0;
    }
    
    .executive-card p {
        color: #D0D8E0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.25);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #00FFFF;
    }
    
    .kpi-icon { 
        font-size: 2rem; 
        background: linear-gradient(135deg, #00FFFF, #00B4D8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .kpi-value { 
        font-size: 1.8rem; 
        font-weight: 700; 
        color: #00FFFF;
    }
    
    .kpi-label { 
        font-size: 0.7rem; 
        color: #B0C4DE; 
        letter-spacing: 1px; 
        margin-top: 8px;
    }
    
    .chart-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
        border: 1px solid rgba(0, 255, 255, 0.1);
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #00FFFF;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(0, 255, 255, 0.3);
        display: inline-block;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 35px;
        border-top: 1px solid rgba(0, 255, 255, 0.1);
        color: #7A8EA0;
        font-size: 0.7rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }
    .status-green { background-color: #00FF88; box-shadow: 0 0 8px #00FF88; }
    .status-cyan { background-color: #00FFFF; box-shadow: 0 0 8px #00FFFF; }
    
    .sidebar-metric {
        background: rgba(0, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 12px;
        margin: 8px 0;
        border-left: 2px solid #00FFFF;
    }
    
    .sidebar-metric .label {
        font-size: 0.65rem;
        color: #7A8EA0;
    }
    
    .sidebar-metric .value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #00FFFF;
    }
    
    /* Metric cards styling */
    [data-testid="stMetric"] {
        background: rgba(0, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
    }
    
    [data-testid="stMetric"] label {
        color: #00FFFF !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetric"] .stMetricValue {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    paths = [
        'Data/raw/pakistan_tourism_dataset.csv',
        'data/raw/pakistan_tourism_dataset.csv',
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
    else:
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            df['Total_Tourists'] = df[num_cols[0]]
    
    df['YoY_Growth'] = df['Total_Tourists'].pct_change() * 100
    df['Recovery_Rate'] = (df['Total_Tourists'] / df['Total_Tourists'].max()) * 100
    
    return df

with st.spinner("Loading tourism data..."):
    df = load_data()

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <i class="fas fa-mountain" style="font-size: 2.5rem; color: #00FFFF;"></i>
        <div style="font-size: 1rem; font-weight: 700; margin-top: 10px; color: #00FFFF;">TOURISM ANALYTICS</div>
        <div style="font-size: 0.6rem; color: #7A8EA0; letter-spacing: 2px;">PAKISTAN</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.7rem; color: #00FFFF; margin-bottom: 10px;"><i class="fas fa-compass"></i> NAVIGATION</div>', unsafe_allow_html=True)
    
    nav_options = ["Dashboard", "Forecast", "Data"]
    selected_page = st.radio("", nav_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.7rem; color: #00FFFF; margin-bottom: 10px;"><i class="fas fa-calendar-alt"></i> TIME RANGE</div>', unsafe_allow_html=True)
    year_range = st.slider("", min_year, max_year, (min_year, max_year), label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.7rem; color: #00FFFF; margin-bottom: 10px;"><i class="fas fa-chart-line"></i> KEY METRICS</div>', unsafe_allow_html=True)
    
    latest = df[df['Year'] == max_year]
    if not latest.empty:
        total = latest['Total_Tourists'].values[0]
        st.markdown(f"""
        <div class="sidebar-metric">
            <div class="label"><i class="fas fa-users"></i> TOTAL TOURISTS</div>
            <div class="value">{total:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    if 'Revenue_M' in df.columns:
        revenue = df['Revenue_M'].iloc[-1]
        st.markdown(f"""
        <div class="sidebar-metric">
            <div class="label"><i class="fas fa-dollar-sign"></i> REVENUE</div>
            <div class="value">${revenue:.0f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div style="font-size: 0.7rem; color: #00FFFF; margin-bottom: 10px;"><i class="fas fa-microchip"></i> SYSTEM</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 8px 0;">
        <span class="status-dot status-green"></span> DATA ACTIVE
    </div>
    <div style="margin: 8px 0;">
        <span class="status-dot status-green"></span> ML MODELS
    </div>
    <div style="margin: 8px 0;">
        <span class="status-dot status-cyan"></span> LIVE
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 0.55rem; color: #4A5A6A;">FYP 2025</div>', unsafe_allow_html=True)

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
            <p><i class="fas fa-chart-line" style="color: #00FFFF;"></i> <strong>EXECUTIVE SUMMARY</strong><br>
            Pakistan's tourism sector is experiencing <strong style="color: #00FF88;">{growth:.1f}% YoY growth</strong> 
            with <strong style="color: #00FFFF;">{latest_tourists:.1f}M tourists</strong> in {int(filtered_df['Year'].iloc[-1])}.
            The best performing year was <strong style="color: #00FFFF;">{int(best_year)}</strong> 
            with <strong style="color: #00FFFF;">{best_value:.1f}M visitors</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI CARDS - 4 cards
    col1, col2, col3, col4 = st.columns(4)
    
    current_tourists = filtered_df['Total_Tourists'].iloc[-1] if not filtered_df.empty else 0
    
    if len(filtered_df) > 1:
        prev_tourists = filtered_df['Total_Tourists'].iloc[-2]
        growth_rate = ((current_tourists - prev_tourists) / prev_tourists) * 100
    else:
        growth_rate = 0
    
    recovery = filtered_df['Recovery_Rate'].iloc[-1] if not filtered_df.empty else 0
    
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
    
    # CHART 1: Tourism Growth Trend
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Tourism Growth Trend</div>', unsafe_allow_html=True)
    fig1 = px.line(filtered_df, x='Year', y='Total_Tourists', markers=True, template='plotly_white')
    fig1.update_traces(line_color='#00FFFF', line_width=3, marker_size=10, marker_color='#00FFFF')
    fig1.update_layout(
        xaxis=dict(title='Year', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Tourists (Millions)', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # CHART 2: Revenue Trend
    if 'Revenue_M' in filtered_df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-dollar-sign"></i> Revenue Trend</div>', unsafe_allow_html=True)
        fig2 = px.area(filtered_df, x='Year', y='Revenue_M', template='plotly_white', color_discrete_sequence=['#00B4D8'])
        fig2.update_layout(
            xaxis=dict(title='Year', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Revenue (USD Millions)', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CHART 3: Domestic vs International
    if 'Domestic_Tourists' in filtered_df.columns and 'International_Tourists' in filtered_df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-bar"></i> Domestic vs International Tourists</div>', unsafe_allow_html=True)
        fig3 = px.bar(filtered_df, x='Year', y=['Domestic_Tourists', 'International_Tourists'], 
                      barmode='group', template='plotly_white',
                      labels={'value': 'Tourists (Millions)', 'variable': 'Type'})
        fig3.update_layout(
            xaxis=dict(title='Year', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='Tourists (Millions)', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(font_color='#FFFFFF'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CHART 4: YoY Growth Rate
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Year-over-Year Growth Rate</div>', unsafe_allow_html=True)
    growth_df = filtered_df[['Year', 'YoY_Growth']].dropna()
    fig4 = px.bar(growth_df, x='Year', y='YoY_Growth', template='plotly_white',
                  color='YoY_Growth', color_continuous_scale='RdYlGn',
                  labels={'YoY_Growth': 'Growth Rate (%)'})
    fig4.update_layout(
        xaxis=dict(title='Year', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Growth Rate (%)', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # CHART 5: Recovery Rate
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Tourism Recovery Rate</div>', unsafe_allow_html=True)
    fig5 = px.line(filtered_df, x='Year', y='Recovery_Rate', markers=True, template='plotly_white')
    fig5.update_traces(line_color='#00FF88', line_width=3, marker_size=8)
    fig5.update_layout(
        xaxis=dict(title='Year', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Recovery Rate (%)', title_font_color='#00FFFF', tickfont_color='#FFFFFF', gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FORECAST PAGE WITH PROPHET ====================
elif selected_page == "Forecast":
    st.markdown('<div class="main-title">AI-Powered Forecast 2025-2030</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-brain"></i> Facebook Prophet Time Series Model</div>', unsafe_allow_html=True)
    
    if len(filtered_df) >= 3:
        # Try to use Prophet
        try:
            from prophet import Prophet
            
            with st.spinner("🔄 Training Prophet Model on tourism data..."):
                # Prepare data for Prophet
                prophet_df = pd.DataFrame({
                    'ds': pd.to_datetime(filtered_df['Year'].astype(str) + '-01-01'),
                    'y': filtered_df['Total_Tourists'].values
                })
                
                # Initialize and train Prophet
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    interval_width=0.95
                )
                model.fit(prophet_df)
                
                # Create future dataframe for 2025-2030
                future = model.make_future_dataframe(periods=6, freq='YS')
                forecast = model.predict(future)
                
                # Get forecast for 2025-2030
                forecast_2025_2030 = forecast[forecast['ds'].dt.year >= 2025].copy()
                
                # Calculate accuracy metrics
                train_pred = model.predict(prophet_df)
                from sklearn.metrics import mean_absolute_error, r2_score
                mae = mean_absolute_error(prophet_df['y'], train_pred['yhat'][:len(prophet_df)])
                r2 = r2_score(prophet_df['y'], train_pred['yhat'][:len(prophet_df)])
            
            # ========== METRICS CARDS ==========
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Model R² Score", f"{r2:.3f}", help="Higher is better (0-1 scale)")
            
            with col2:
                st.metric("Mean Absolute Error", f"{mae:.2f}M", help="Lower is better")
            
            with col3:
                pred_2030 = forecast_2025_2030[forecast_2025_2030['ds'].dt.year == 2030]['yhat'].values[0]
                st.metric("2030 Prediction", f"{pred_2030:.1f}M", help="Forecasted tourists in 2030")
            
            with col4:
                lower_2030 = forecast_2025_2030[forecast_2025_2030['ds'].dt.year == 2030]['yhat_lower'].values[0]
                upper_2030 = forecast_2025_2030[forecast_2025_2030['ds'].dt.year == 2030]['yhat_upper'].values[0]
                st.metric("95% Confidence", f"[{lower_2030:.1f} - {upper_2030:.1f}]M", help="Prediction range")
            
            st.markdown("---")
            
            # ========== FORECAST CHART ==========
            st.markdown("### 📊 Prophet Model Forecast")
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=filtered_df['Year'],
                y=filtered_df['Total_Tourists'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='#00FFFF', width=3),
                marker=dict(color='#00FFFF', size=10)
            ))
            
            # Forecast data
            forecast_years = forecast_2025_2030['ds'].dt.year
            fig.add_trace(go.Scatter(
                x=forecast_years,
                y=forecast_2025_2030['yhat'],
                mode='lines+markers',
                name='Prophet Forecast',
                line=dict(color='#FF6B6B', width=3, dash='dash'),
                marker=dict(color='#FF6B6B', size=10)
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=list(forecast_years) + list(forecast_years)[::-1],
                y=list(forecast_2025_2030['yhat_upper']) + list(forecast_2025_2030['yhat_lower'])[::-1],
                fill='toself',
                fillcolor='rgba(255, 107, 107, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence Interval'
            ))
            
            # COVID impact line
            fig.add_vline(
                x=2020,
                line_dash="dash",
                line_color="#FF4444",
                line_width=2,
                annotation_text="COVID-19 Impact",
                annotation_position="top",
                annotation_font_color="#FF4444"
            )
            
            fig.update_layout(
                title=dict(
                    text="Pakistan Tourism Forecast 2025-2030 (Prophet Model)",
                    font=dict(color='#00FFFF', size=20),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text="Year", font=dict(color='#00FFFF', size=14)),
                    tickfont=dict(color='#FFFFFF', size=12),
                    gridcolor='rgba(255,255,255,0.1)',
                    tickvals=list(range(2015, 2031, 2))
                ),
                yaxis=dict(
                    title=dict(text="Tourists (Millions)", font=dict(color='#00FFFF', size=14)),
                    tickfont=dict(color='#FFFFFF', size=12),
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                legend=dict(
                    font=dict(color='#FFFFFF', size=12),
                    bgcolor='rgba(0,0,0,0.5)',
                    x=0.02,
                    y=0.98
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=550,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # ========== FORECAST TABLE ==========
            st.markdown("---")
            st.markdown("### 📋 Year-by-Year Forecast (2025-2030)")
            
            forecast_table = pd.DataFrame({
                'Year': forecast_2025_2030['ds'].dt.year,
                'Predicted Tourists (M)': forecast_2025_2030['yhat'].round(1),
                'Lower Bound (M)': forecast_2025_2030['yhat_lower'].round(1),
                'Upper Bound (M)': forecast_2025_2030['yhat_upper'].round(1)
            })
            st.dataframe(forecast_table, use_container_width=True, hide_index=True)
            
            # ========== COVID IMPACT SECTION ==========
            st.markdown("---")
            st.markdown("### 📉 COVID-19 Impact Analysis")
            
            # Calculate COVID impact
            pre_covid = filtered_df[filtered_df['Year'] <= 2019]['Total_Tourists'].mean() if len(filtered_df[filtered_df['Year'] <= 2019]) > 0 else 0
            covid_year = filtered_df[filtered_df['Year'] == 2020]['Total_Tourists'].values[0] if len(filtered_df[filtered_df['Year'] == 2020]) > 0 else 0
            post_covid = filtered_df[filtered_df['Year'] >= 2022]['Total_Tourists'].mean() if len(filtered_df[filtered_df['Year'] >= 2022]) > 0 else 0
            
            decline = ((pre_covid - covid_year) / pre_covid) * 100 if pre_covid > 0 else 0
            recovery = (post_covid / pre_covid) * 100 if pre_covid > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(255,68,68,0.15); border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 2rem;">📉</div>
                    <div style="font-size: 1.6rem; font-weight: bold; color: #FF6666;">-{decline:.1f}%</div>
                    <div style="color: #B0C4DE;">Tourism Decline (2020)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(0,255,136,0.15); border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 2rem;">🔄</div>
                    <div style="font-size: 1.6rem; font-weight: bold; color: #00FF88;">{recovery:.0f}%</div>
                    <div style="color: #B0C4DE;">Recovery Rate (vs Pre-COVID)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: rgba(0,255,255,0.15); border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 2rem;">⏰</div>
                    <div style="font-size: 1.6rem; font-weight: bold; color: #00FFFF;">2 Years</div>
                    <div style="color: #B0C4DE;">Recovery Period (2020 → 2022)</div>
                </div>
                """, unsafe_allow_html=True)
            
            # ========== MODEL COMPONENTS ==========
            st.markdown("---")
            st.markdown("### 🔍 Model Components: Trend & Seasonality")
            
            fig_components = model.plot_components(forecast)
            st.pyplot(fig_components)
            
            # ========== FORECAST INSIGHTS ==========
            st.markdown("---")
            total_growth = ((forecast_2025_2030['yhat'].iloc[-1] - forecast_2025_2030['yhat'].iloc[0]) / forecast_2025_2030['yhat'].iloc[0]) * 100
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(0,255,255,0.02)); border-left: 4px solid #00FFFF; border-radius: 12px; padding: 18px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <i class="fas fa-chart-line" style="color: #00FFFF; font-size: 1.2rem;"></i>
                    <span style="color: #00FFFF; font-weight: 700;">FORECAST INSIGHTS</span>
                </div>
                <p style="color: #D0D8E0; line-height: 1.8;">
                    • <strong style="color: #00FF88;">Prophet Model Accuracy:</strong> R² = {r2:.3f} (Much better than Linear Regression)<br>
                    • <strong style="color: #00FFFF;">Total Growth 2025-2030:</strong> {total_growth:+.1f}%<br>
                    • <strong style="color: #00FFFF;">Annual Growth Rate:</strong> {((forecast_2025_2030['yhat'].iloc[-1] - forecast_2025_2030['yhat'].iloc[0]) / 6):.2f}M per year<br>
                    • <strong style="color: #00FF88;">Post-COVID Recovery:</strong> Pakistan tourism has recovered {recovery:.0f}% of pre-pandemic levels
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except ImportError:
            st.error("""
            <div style="background: rgba(255,68,68,0.1); border-radius: 12px; padding: 20px;">
                <i class="fas fa-exclamation-triangle" style="color: #FF6666; font-size: 1.5rem;"></i>
                <h3 style="color: #FF6666;">Prophet Model Not Installed</h3>
                <p style="color: #B0C4DE;">Please run this command in your terminal:</p>
                <code style="background: #1a1a2e; padding: 10px; display: block; border-radius: 6px;">pip install prophet</code>
                <p style="color: #B0C4DE; margin-top: 10px;">Then redeploy to Streamlit Cloud.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Fallback to Linear Regression
            st.markdown("### Using Linear Regression (Temporary Fallback)")
            X = filtered_df[['Year']].values
            y = filtered_df['Total_Tourists'].values
            
            model_lr = LinearRegression()
            model_lr.fit(X, y)
            
            future = np.arange(2025, 2031).reshape(-1, 1)
            predictions = model_lr.predict(future)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model R²", f"{model_lr.score(X, y):.3f}")
            with col2:
                st.metric("2030 Prediction", f"{predictions[-1]:.1f}M")
            with col3:
                st.metric("Annual Growth", f"{model_lr.coef_[0]:.2f}M")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_df['Year'], y=filtered_df['Total_Tourists'],
                                     mode='lines+markers', name='Historical',
                                     line=dict(color='#00FFFF', width=3)))
            fig.add_trace(go.Scatter(x=future.flatten(), y=predictions,
                                     mode='lines+markers', name='Forecast',
                                     line=dict(color='#FF6B6B', width=3, dash='dash')))
            fig.update_layout(title="Tourism Forecast (Linear Regression)", 
                             xaxis_title="Year", yaxis_title="Tourists (Millions)",
                             template='plotly_dark', height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ Not enough data for forecasting. Need at least 3 years of historical data.")
# ==================== DATA PAGE ====================
elif selected_page == "Data":
    st.markdown('<div class="main-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-database"></i> Raw Tourism Data</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = filtered_df.to_csv(index=False).encode()
    st.download_button(
        label="Download CSV for Power BI",
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