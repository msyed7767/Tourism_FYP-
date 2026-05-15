import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Pakistan Tourism Intelligence",
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
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1120 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255, 215, 0, 0.15);
    }
    
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255, 215, 0, 0.12) !important;
        border-color: #FFD700 !important;
        transform: translateX(4px);
    }
    
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin-bottom: 25px;
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
    .kpi-label { font-size: 0.65rem; color: rgba(255, 255, 255, 0.65); letter-spacing: 1px; }
    
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
    
    .insight-text { color: #FFD700; font-weight: 500; }
    
    .sidebar-metric {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 10px;
        margin: 8px 0;
        border-left: 2px solid #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    """Load Pakistan Tourism Dataset"""
    paths = [
        'data/raw/pakistan_tourism_dataset.csv',
        '../data/raw/pakistan_tourism_dataset.csv',
    ]
    
    df = None
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    
    if df is None:
        st.error("Dataset not found!")
        return None
    
    # Calculate derived columns
    df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
    df['Total_Tourists_M'] = df['Total_Tourists'] / 1000000
    df['Domestic_Tourists_M'] = df['Domestic_Tourists'] / 1000000
    df['International_Tourists_M'] = df['International_Tourists'] / 1000000
    
    return df

with st.spinner("🔄 Loading Pakistan Tourism Dataset..."):
    df = load_data()

if df is None:
    st.stop()

# Get unique values for filters
provinces = ['All'] + sorted(df['Province'].unique().tolist())
destination_types = ['All'] + sorted(df['Destination_Type'].unique().tolist())
years = sorted(df['Year'].unique())

min_year = min(years)
max_year = max(years)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <i class="fas fa-mountain" style="font-size: 2.5rem; color: #FFD700;"></i>
        <div style="font-size: 1.1rem; font-weight: 700; margin-top: 8px;">TOURISM ANALYTICS</div>
        <div style="font-size: 0.6rem; color: #FFD700; letter-spacing: 2px;">PAKISTAN</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    st.markdown('<i class="fas fa-compass"></i> NAVIGATION', unsafe_allow_html=True)
    pages = ["🏠 Dashboard", "🤖 Forecast", "🗺️ Provincial", "📊 Trends", "📋 Data", "ℹ️ About"]
    selected_page = st.radio("", pages, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Smart Filters
    st.markdown('<i class="fas fa-sliders-h"></i> FILTERS', unsafe_allow_html=True)
    
    # Year Range
    year_range = st.slider("Year Range", min_year, max_year, (min_year, max_year))
    
    # Province Filter
    selected_province = st.selectbox("Province", provinces)
    
    # Destination Type
    selected_dest_type = st.selectbox("Destination Type", destination_types)
    
    st.markdown("---")
    
    # Live KPIs
    st.markdown('<i class="fas fa-chart-line"></i> LIVE KPIs', unsafe_allow_html=True)
    
    total_tourists = df['Total_Tourists'].sum() / 1000000
    avg_cost = df['Average_Cost_USD'].mean()
    avg_safety = df['Safety_Rating'].mean()
    
    st.markdown(f"""
    <div class="sidebar-metric">
        <div><i class="fas fa-users"></i> Total Tourists</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{total_tourists:.1f}M</div>
    </div>
    <div class="sidebar-metric">
        <div><i class="fas fa-dollar-sign"></i> Avg Cost</div>
        <div style="font-size: 1.2rem; font-weight: bold;">${avg_cost:.0f}</div>
    </div>
    <div class="sidebar-metric">
        <div><i class="fas fa-shield-alt"></i> Safety Rating</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{avg_safety:.1f}/5</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown('<i class="fas fa-microchip"></i> SYSTEM', unsafe_allow_html=True)
    st.markdown("""
    <div><span class="status-dot status-green"></span> Data Engine</div>
    <div><span class="status-dot status-green"></span> ML Models</div>
    <div><span class="status-dot status-blue"></span> Forecast Ready</div>
    """, unsafe_allow_html=True)

# Filter data based on sidebar selections
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

if selected_province != 'All':
    filtered_df = filtered_df[filtered_df['Province'] == selected_province]

if selected_dest_type != 'All':
    filtered_df = filtered_df[filtered_df['Destination_Type'] == selected_dest_type]

# Aggregate by year for time series
yearly_df = filtered_df.groupby('Year').agg({
    'Domestic_Tourists': 'sum',
    'International_Tourists': 'sum',
    'Total_Tourists': 'sum',
    'Average_Cost_USD': 'mean',
    'Safety_Rating': 'mean',
    'Popularity_Score': 'mean'
}).reset_index()

yearly_df['Total_Tourists_M'] = yearly_df['Total_Tourists'] / 1000000
yearly_df['Domestic_Tourists_M'] = yearly_df['Domestic_Tourists'] / 1000000
yearly_df['International_Tourists_M'] = yearly_df['International_Tourists'] / 1000000
yearly_df['YoY_Growth'] = yearly_df['Total_Tourists_M'].pct_change() * 100

# ==================== DASHBOARD PAGE ====================
if selected_page == "🏠 Dashboard":
    st.markdown('<div class="main-title">Pakistan Tourism Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-chart-line"></i> Real-time Analytics & Business Intelligence</div>', unsafe_allow_html=True)
    
    # Executive Summary
    if len(yearly_df) > 1:
        latest_tourists = yearly_df['Total_Tourists_M'].iloc[-1]
        prev_tourists = yearly_df['Total_Tourists_M'].iloc[-2]
        growth = ((latest_tourists - prev_tourists) / prev_tourists) * 100
        best_year = yearly_df.loc[yearly_df['Total_Tourists_M'].idxmax(), 'Year']
        
        st.markdown(f"""
        <div class="executive-card">
            <i class="fas fa-chart-line" style="color: #FFD700;"></i> 
            <strong>Executive Summary:</strong> Tourism grew by <span class="insight-text">{growth:.1f}%</span> to <span class="insight-text">{latest_tourists:.1f}M</span> visitors. 
            Best year was <span class="insight-text">{int(best_year)}</span> with {yearly_df[yearly_df['Year']==best_year]['Total_Tourists_M'].values[0]:.1f}M tourists.
            Northern areas show highest international interest.
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current = yearly_df['Total_Tourists_M'].iloc[-1] if not yearly_df.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-users"></i></div>
            <div class="kpi-value">{current:.1f}M</div>
            <div class="kpi-label">TOTAL TOURISTS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_cost = yearly_df['Average_Cost_USD'].mean() if not yearly_df.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-dollar-sign"></i></div>
            <div class="kpi-value">${avg_cost:.0f}</div>
            <div class="kpi-label">AVG TRIP COST</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if len(yearly_df) > 1:
            growth_rate = yearly_df['YoY_Growth'].iloc[-1]
        else:
            growth_rate = 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-chart-line"></i></div>
            <div class="kpi-value">{growth_rate:+.1f}%</div>
            <div class="kpi-label">YoY GROWTH</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        safety = yearly_df['Safety_Rating'].mean() if not yearly_df.empty else 0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon"><i class="fas fa-shield-alt"></i></div>
            <div class="kpi-value">{safety:.1f}/5</div>
            <div class="kpi-label">SAFETY RATING</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Tourism Growth Trend</div>', unsafe_allow_html=True)
        fig = px.line(yearly_df, x='Year', y='Total_Tourists_M', markers=True, template='plotly_dark')
        fig.update_traces(line_color='#FFD700', line_width=3, marker_size=8)
        fig.update_layout(xaxis_title="Year", yaxis_title="Tourists (Millions)", height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> Domestic vs International</div>', unsafe_allow_html=True)
        fig = px.line(yearly_df, x='Year', y=['Domestic_Tourists_M', 'International_Tourists_M'], 
                      template='plotly_dark', markers=True,
                      labels={'value': 'Tourists (Millions)', 'variable': 'Type'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-bar"></i> Popularity Score by Year</div>', unsafe_allow_html=True)
        pop_yearly = filtered_df.groupby('Year')['Popularity_Score'].mean().reset_index()
        fig = px.bar(pop_yearly, x='Year', y='Popularity_Score', template='plotly_dark', color='Popularity_Score', color_continuous_scale='Viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title"><i class="fas fa-chart-line"></i> YoY Growth Rate</div>', unsafe_allow_html=True)
        growth_df = yearly_df[['Year', 'YoY_Growth']].dropna()
        fig = px.bar(growth_df, x='Year', y='YoY_Growth', template='plotly_dark', 
                     color='YoY_Growth', color_continuous_scale='RdYlGn')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FORECAST PAGE ====================
elif selected_page == "🤖 Forecast":
    st.markdown('<div class="main-title">AI-Powered Forecast 2025-2030</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-brain"></i> Machine Learning Predictions</div>', unsafe_allow_html=True)
    
    if len(yearly_df) >= 3:
        X = yearly_df[['Year']].values
        y = yearly_df['Total_Tourists_M'].values
        
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
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_df['Year'], y=yearly_df['Total_Tourists_M'],
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
        
        # Forecast Table
        forecast_df = pd.DataFrame({
            'Year': future_years.flatten(),
            'Predicted Tourists (M)': predictions.round(1),
            'Lower Bound': (predictions * 0.9).round(1),
            'Upper Bound': (predictions * 1.1).round(1)
        })
        st.dataframe(forecast_df, use_container_width=True)
        
        total_growth = ((predictions[-1] - predictions[0]) / predictions[0]) * 100
        st.success(f"📈 **Forecast Insight:** Tourism is projected to grow by {total_growth:.1f}% from 2025 to 2030.")
    else:
        st.warning("Not enough data for forecasting. Need at least 3 years of data.")

# ==================== PROVINCIAL PAGE ====================
elif selected_page == "🗺️ Provincial":
    st.markdown('<div class="main-title">Provincial Tourism Analytics</div>', unsafe_allow_html=True)
    
    provincial_df = filtered_df.groupby('Province').agg({
        'Total_Tourists': 'sum',
        'Average_Cost_USD': 'mean',
        'Safety_Rating': 'mean',
        'Popularity_Score': 'mean'
    }).reset_index()
    
    provincial_df['Total_Tourists_M'] = provincial_df['Total_Tourists'] / 1000000
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(provincial_df, x='Province', y='Total_Tourists_M', 
                     title="Tourists by Province (Millions)",
                     template='plotly_dark', color='Total_Tourists_M',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(provincial_df, x='Safety_Rating', y='Popularity_Score', 
                         size='Total_Tourists_M', text='Province',
                         title="Safety vs Popularity by Province",
                         template='plotly_dark', color='Province')
        st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(provincial_df[['Province', 'Total_Tourists_M', 'Average_Cost_USD', 'Safety_Rating', 'Popularity_Score']], 
                 use_container_width=True)

# ==================== TRENDS PAGE ====================
elif selected_page == "📊 Trends":
    st.markdown('<div class="main-title">Destination Analytics</div>', unsafe_allow_html=True)
    
    # Top destinations
    top_destinations = filtered_df.groupby('City').agg({
        'Total_Tourists': 'sum',
        'Popularity_Score': 'mean',
        'Safety_Rating': 'mean'
    }).reset_index().nlargest(10, 'Total_Tourists')
    
    top_destinations['Total_Tourists_M'] = top_destinations['Total_Tourists'] / 1000000
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(top_destinations, x='City', y='Total_Tourists_M', 
                     title="Top 10 Destinations by Tourists",
                     template='plotly_dark', color='Popularity_Score',
                     color_continuous_scale='Hot')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(filtered_df, x='Average_Cost_USD', y='Popularity_Score',
                         size='Total_Tourists', color='Province', hover_name='City',
                         title="Cost vs Popularity Analysis",
                         template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

# ==================== DATA PAGE ====================
elif selected_page == "📋 Data":
    st.markdown('<div class="main-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode()
    st.download_button("📥 Download Filtered Data (CSV)", csv, "pakistan_tourism_data.csv", "text/csv")

# ==================== ABOUT PAGE ====================
elif selected_page == "ℹ️ About":
    st.markdown('<div class="main-title">About Project</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chart-card">
        <h3><i class="fas fa-graduation-cap"></i> Final Year Project 2025</h3>
        <p><strong>Project Title:</strong> Pakistan Tourism Analytics & Forecasting Platform</p>
        <p><strong>Tech Stack:</strong> Python, Streamlit, Pandas, Scikit-learn, Plotly</p>
        <p><strong>ML Model:</strong> Linear Regression for Time Series Forecasting</p>
    </div>
    
    <div class="chart-card">
        <h3><i class="fas fa-database"></i> Data Sources</h3>
        <ul>
            <li>Pakistan Tourism Development Corporation (PTDC)</li>
            <li>Provincial Tourism Departments</li>
            <li>World Bank Tourism Database</li>
        </ul>
        <p><strong>Dataset Features:</strong> 14 columns including Domestic/International tourists, Safety ratings, Popularity scores, and destination details</p>
    </div>
    
    <div class="chart-card">
        <h3><i class="fas fa-chart-line"></i> Key Features</h3>
        <ul>
            <li>Real-time Tourism Analytics Dashboard</li>
            <li>AI-Powered Forecasting 2025-2030</li>
            <li>Provincial & Destination Analysis</li>
            <li>Executive Summary with Key Metrics</li>
            <li>Power BI Ready Data Export</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <i class="fas fa-database"></i> Data Source: PTDC | World Bank | Provincial Tourism Depts &nbsp;|&nbsp;
    <i class="fab fa-python"></i> Python & Streamlit &nbsp;|&nbsp;
    <i class="fas fa-brain"></i> ML: Linear Regression &nbsp;|&nbsp;
    Final Year Project 2025
</div>
""", unsafe_allow_html=True)