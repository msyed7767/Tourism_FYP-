import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

from PIL import Image

favicon = Image.open("Dashboard/favicon.png")

st.set_page_config(
    page_title="Pakistan Tourism Analytics",
    page_icon=favicon,   # <-- replace the old string
    layout="wide",
    initial_sidebar_state="expanded"

)

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

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: #07111E !important;
        border-right: 1px solid rgba(0,255,255,0.12);
    }
    [data-testid="stSidebar"] * { color: #C8D8E8 !important; }

    .brand-block {
        padding: 28px 0 20px 0;
        text-align: center;
        border-bottom: 1px solid rgba(0,255,255,0.1);
        margin-bottom: 8px;
    }
    .brand-icon {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, #00FFFF22, #00B4D822);
        border: 1px solid rgba(0,255,255,0.35);
        border-radius: 14px;
        display: inline-flex; align-items: center; justify-content: center;
        margin-bottom: 12px;
    }
    .brand-icon i { font-size: 1.4rem; color: #00FFFF; }
    .brand-name {
        font-size: 0.85rem; font-weight: 700; letter-spacing: 2.5px;
        color: #E8F4FF !important; text-transform: uppercase;
    }
    .brand-sub {
        font-size: 0.58rem; letter-spacing: 4px;
        color: #4A6A8A !important; margin-top: 3px; text-transform: uppercase;
    }

    .nav-section {
        padding: 16px 16px 8px 16px;
    }
    .nav-label {
        font-size: 0.58rem; letter-spacing: 2.5px; color: #3A6080 !important;
        text-transform: uppercase; margin-bottom: 8px; padding-left: 4px;
    }

    .sidebar-divider {
        border: none; border-top: 1px solid rgba(0,255,255,0.07);
        margin: 4px 16px;
    }

    .metric-block {
        margin: 0 14px 8px 14px;
        background: rgba(0,255,255,0.04);
        border: 1px solid rgba(0,255,255,0.1);
        border-radius: 10px;
        padding: 12px 14px;
    }
    .metric-block .m-label {
        font-size: 0.6rem; letter-spacing: 2px;
        color: #3A6080 !important; text-transform: uppercase; margin-bottom: 4px;
    }
    .metric-block .m-label i { color: #00FFFF !important; margin-right: 5px; }
    .metric-block .m-value {
        font-size: 1.35rem; font-weight: 700; color: #00FFFF !important; line-height: 1;
    }
    .metric-block .m-sub {
        font-size: 0.62rem; color: #4A7A9A !important; margin-top: 3px;
    }

    .status-row {
        display: flex; align-items: center; gap: 8px;
        padding: 5px 0; font-size: 0.72rem; color: #6A90B0 !important;
    }
    .dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
    .dot-green { background:#00FF88; box-shadow: 0 0 6px #00FF88; }
    .dot-cyan  { background:#00FFFF; box-shadow: 0 0 6px #00FFFF; }
    .dot-blue  { background:#00B4D8; box-shadow: 0 0 6px #00B4D8; }

    /* ── MAIN CONTENT ── */
    .main-title {
        font-size: 2.1rem; font-weight: 800;
        background: linear-gradient(135deg, #00FFFF 0%, #00B4D8 60%, #0090B8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 6px; letter-spacing: -0.5px;
    }
    .main-title i { margin-right: 10px; }
    .subtitle {
        text-align: center; color: #6A90B0;
        font-size: 0.82rem; margin-bottom: 28px; letter-spacing: 0.5px;
    }
    .subtitle i { margin-right: 5px; color: #00FFFF; }

    .exec-card {
        background: linear-gradient(135deg, rgba(0,255,255,0.06), rgba(0,180,216,0.02));
        border-left: 3px solid #00FFFF;
        border-radius: 10px; padding: 16px 20px; margin-bottom: 24px;
    }
    .exec-card p {
        color: #B0C8E0; font-size: 0.88rem; line-height: 1.65; margin: 0;
    }
    .exec-card strong { color: #E8F4FF; }
    .exec-card .highlight-green { color: #00FF88; font-weight: 600; }
    .exec-card .highlight-cyan  { color: #00FFFF; font-weight: 600; }

    /* KPI cards */
    .kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 24px; }
    .kpi-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(0,255,255,0.18);
        border-radius: 14px; padding: 20px 16px; text-align: center;
        transition: transform .25s, border-color .25s;
    }
    .kpi-card:hover { transform: translateY(-4px); border-color: rgba(0,255,255,0.5); }
    .kpi-card .k-icon {
        font-size: 1.4rem; color: #00FFFF;
        background: rgba(0,255,255,0.1); border-radius: 10px;
        width: 44px; height: 44px; display: inline-flex;
        align-items: center; justify-content: center; margin-bottom: 12px;
    }
    .kpi-card .k-value {
        font-size: 1.75rem; font-weight: 700; color: #FFFFFF;
        line-height: 1; margin-bottom: 6px;
    }
    .kpi-card .k-label {
        font-size: 0.65rem; color: #5A8AAA;
        letter-spacing: 1.8px; text-transform: uppercase;
    }

    /* Chart cards */
    .chart-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(0,255,255,0.08);
        border-radius: 14px; padding: 20px; margin-bottom: 16px;
    }
    .chart-header {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 16px; padding-bottom: 12px;
        border-bottom: 1px solid rgba(0,255,255,0.1);
    }
    .chart-icon {
        width: 32px; height: 32px; border-radius: 8px;
        background: rgba(0,255,255,0.1);
        display: inline-flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .chart-icon i { font-size: 0.85rem; color: #00FFFF; }
    .chart-title { font-size: 0.92rem; font-weight: 600; color: #D0E8F8; }
    .chart-sub   { font-size: 0.7rem; color: #4A7A9A; margin-top: 1px; }

    /* Streamlit metric overrides */
    [data-testid="stMetric"] {
        background: rgba(0,255,255,0.06) !important;
        border: 1px solid rgba(0,255,255,0.15) !important;
        border-radius: 12px !important; padding: 18px !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #7AAAC8 !important; font-size: 0.75rem !important;
        font-weight: 500 !important; letter-spacing: 0.5px !important;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important; font-size: 1.7rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] { color: #00FF88 !important; }

    /* Footer */
    .footer {
        text-align: center; padding: 24px 0 16px 0;
        margin-top: 40px; border-top: 1px solid rgba(0,255,255,0.07);
        color: #3A5A7A; font-size: 0.68rem; letter-spacing: 0.5px;
    }
    .footer i { color: #00FFFF; margin-right: 4px; }
    .footer span { margin: 0 10px; }

    /* Streamlit radio fix */
    [data-testid="stRadio"] > div { gap: 4px !important; }
    [data-testid="stRadio"] label {
        border-radius: 8px !important;
        padding: 8px 12px !important;
        transition: background .2s !important;
    }
    [data-testid="stRadio"] label:hover {
        background: rgba(0,255,255,0.07) !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background: rgba(0,255,255,0.05) !important;
        border: 1px solid rgba(0,255,255,0.2) !important;
        border-radius: 8px !important; color: #C8D8E8 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: rgba(0,255,255,0.08) !important;
        border: 1px solid rgba(0,255,255,0.3) !important;
        color: #00FFFF !important; border-radius: 8px !important;
        font-weight: 600 !important; letter-spacing: 0.5px !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: rgba(0,255,255,0.18) !important;
    }
</style>
""", unsafe_allow_html=True)


# ── PLOT DEFAULTS (no title, no height — add per chart) ──────────────────────
def plot_layout(h=400, xtitle='', ytitle=''):
    return dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter'),
        xaxis=dict(title=xtitle, title_font=dict(color='#7AAAC8', size=11),
                   tickfont=dict(color='#8AAAC0', size=10),
                   gridcolor='rgba(255,255,255,0.06)', zeroline=False),
        yaxis=dict(title=ytitle, title_font=dict(color='#7AAAC8', size=11),
                   tickfont=dict(color='#8AAAC0', size=10),
                   gridcolor='rgba(255,255,255,0.06)', zeroline=False),
        legend=dict(font=dict(color='#A0C0D8', size=10),
                    bgcolor='rgba(0,0,0,0)', borderwidth=0),
        margin=dict(l=10, r=10, t=10, b=10),
        height=h,
    )


def chart_card(icon, title, subtitle=''):
    sub_html = f'<div class="chart-sub">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-icon"><i class="fas fa-{icon}"></i></div>
        <div><div class="chart-title">{title}</div>{sub_html}</div>
      </div>
    """, unsafe_allow_html=True)


def end_card():
    st.markdown('</div>', unsafe_allow_html=True)


# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = [
        os.path.join(base_dir, 'Data', 'raw', 'pakistan_tourism_dataset.csv'),
        os.path.join(base_dir, 'data', 'raw', 'pakistan_tourism_dataset.csv'),
        'Data/raw/pakistan_tourism_dataset.csv',
        'data/raw/pakistan_tourism_dataset.csv',
    ]
    df = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break

    if df is None:
        st.warning("CSV not found — showing sample data. Run from TOURISM_FYP root folder.")
        df = pd.DataFrame({
            'Year': [2015,2015,2016,2016,2017,2018,2019,2020,2021,2022,2023,2024],
            'Province': ['Punjab','Sindh','Punjab','Sindh','Balochistan','Gilgit-Baltistan',
                         'Khyber Pakhtunkhwa','Punjab','Sindh','Gilgit-Baltistan',
                         'Khyber Pakhtunkhwa','Punjab'],
            'City': ['Lahore','Karachi','Islamabad','Thatta','Ziarat','Skardu',
                     'Naran','Taxila','Hyderabad','Fairy Meadows','Chitral','Murree'],
            'Destination_Type': ['Historical','Urban','Urban','Historical','Nature','Mountain',
                                  'Nature','Historical','Cultural','Mountain','Nature','Hill Station'],
            'Domestic_Tourists':      [4500000,3800000,2000000,700000,350000,800000,
                                        1100000,500000,650000,450000,550000,2500000],
            'International_Tourists': [350000,420000,500000,25000,12000,120000,
                                        60000,15000,22000,90000,40000,180000],
            'Peak_Season':  ['Winter','Winter','Spring','Winter','Summer','Summer',
                             'Summer','Winter','Winter','Summer','Summer','Summer'],
            'Average_Temperature_C': [18,22,20,24,14,9,12,19,25,7,11,13],
            'Average_Cost_USD':      [300,350,320,180,220,450,300,200,210,500,280,260],
            'Main_Attraction': ['Badshahi Mosque','Clifton Beach','Faisal Mosque',
                                'Makli Necropolis','Ziarat Juniper Forest','Shangrila Lake',
                                'Saif-ul-Malook Lake','Taxila Museum','Pakka Qila',
                                'Nanga Parbat View','Kalash Valley','Mall Road Murree'],
            'Safety_Rating':           [4,3,5,3,3,5,4,4,3,5,4,4],
            'Accommodation_Type':      ['Hotels','Hotels','Hotels','Guest Houses','Guest Houses',
                                         'Lodges','Hotels','Hotels','Guest Houses','Camps',
                                         'Guest Houses','Hotels'],
            'Transport_Accessibility': ['High','High','High','Low','Low','Medium',
                                         'Medium','High','Medium','Low','Low','High'],
            'Popularity_Score':        [85,82,87,70,68,90,86,72,69,92,81,89],
        })

    df['Total_Tourists'] = df['Domestic_Tourists'] + df['International_Tourists']
    df['Revenue_M'] = ((df['Total_Tourists'] * df['Average_Cost_USD']) / 1_000_000).round(1)

    ydf = (df.groupby('Year', as_index=False)
             .agg(Domestic_Tourists=('Domestic_Tourists','sum'),
                  International_Tourists=('International_Tourists','sum'),
                  Total_Tourists=('Total_Tourists','sum'),
                  Revenue_M=('Revenue_M','sum'),
                  Popularity_Score=('Popularity_Score','mean')))
    ydf['Total_Tourists_M']         = (ydf['Total_Tourists'] / 1e6).round(2)
    ydf['Domestic_Tourists_M']      = (ydf['Domestic_Tourists'] / 1e6).round(2)
    ydf['International_Tourists_M'] = (ydf['International_Tourists'] / 1e6).round(2)
    ydf['YoY_Growth']               = ydf['Total_Tourists_M'].pct_change() * 100
    ydf['Recovery_Rate']            = (ydf['Total_Tourists_M'] / ydf['Total_Tourists_M'].max()) * 100
    return df, ydf


with st.spinner("Loading data..."):
    df, year_df = load_data()

min_year = int(year_df['Year'].min())
max_year = int(year_df['Year'].max())


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-icon"><i class="fas fa-mountain"></i></div>
        <div class="brand-name">Tourism Analytics</div>
        <div class="brand-sub">Pakistan</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section"><div class="nav-label">Navigation</div></div>', unsafe_allow_html=True)
    selected_page = st.radio("", ["Dashboard", "Forecast", "Destinations", "Data"], label_visibility="collapsed")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="nav-section"><div class="nav-label">Time Range</div></div>', unsafe_allow_html=True)
    year_range = st.slider("", min_year, max_year, (min_year, max_year), label_visibility="collapsed")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="nav-section"><div class="nav-label">Key Metrics</div></div>', unsafe_allow_html=True)

    latest = year_df[year_df['Year'] == max_year]
    if not latest.empty:
        tm = latest['Total_Tourists_M'].values[0]
        rv = latest['Revenue_M'].values[0]
        st.markdown(f"""
        <div class="metric-block">
            <div class="m-label"><i class="fas fa-users"></i>Total Tourists {max_year}</div>
            <div class="m-value">{tm:.2f}M</div>
            <div class="m-sub">Domestic + International</div>
        </div>
        <div class="metric-block">
            <div class="m-label"><i class="fas fa-dollar-sign"></i>Revenue {max_year}</div>
            <div class="m-value">${rv:.0f}M</div>
            <div class="m-sub">Estimated USD</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="nav-section"><div class="nav-label">System Status</div></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 16px 12px 16px;">
        <div class="status-row"><span class="dot dot-green"></span>Data Pipeline Active</div>
        <div class="status-row"><span class="dot dot-cyan"></span>ML Models Loaded</div>
        <div class="status-row"><span class="dot dot-blue"></span>Live Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;padding:10px 0;font-size:0.58rem;color:#2A4A6A;letter-spacing:1.5px;">TOURISM FYP &nbsp;·&nbsp; 2025</div>', unsafe_allow_html=True)


# ── FILTERED DATA ─────────────────────────────────────────────────────────────
fy  = year_df[(year_df['Year'] >= year_range[0]) & (year_df['Year'] <= year_range[1])].copy()
fdf = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if selected_page == "Dashboard":
    st.markdown('<div class="main-title"><i class="fas fa-mountain"></i>Pakistan Tourism Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-chart-line"></i>Real-time Analytics &amp; Business Intelligence Platform</div>', unsafe_allow_html=True)

    if len(fy) > 1:
        lt = fy['Total_Tourists_M'].iloc[-1]
        pt = fy['Total_Tourists_M'].iloc[-2]
        gr = ((lt - pt) / pt) * 100
        by = int(fy.loc[fy['Total_Tourists_M'].idxmax(), 'Year'])
        bv = fy['Total_Tourists_M'].max()
        cy = int(fy['Year'].iloc[-1])
        st.markdown(f"""
        <div class="exec-card"><p>
            <i class="fas fa-chart-line" style="color:#00FFFF;margin-right:8px;"></i>
            <strong>Executive Summary</strong> &nbsp;—&nbsp;
            Pakistan's tourism is recording a
            <span class="highlight-green">{gr:.1f}% year-on-year growth</span>
            with <span class="highlight-cyan">{lt:.2f}M visitors</span> in {cy}.
            Peak performance was in <span class="highlight-cyan">{by}</span>
            at <span class="highlight-cyan">{bv:.2f}M tourists</span>.
        </p></div>
        """, unsafe_allow_html=True)

    ct = fy['Total_Tourists_M'].iloc[-1]  if not fy.empty else 0
    cr = fy['Revenue_M'].iloc[-1]         if not fy.empty else 0
    cg = fy['YoY_Growth'].iloc[-1]        if len(fy) > 1   else 0
    rr = fy['Recovery_Rate'].iloc[-1]     if not fy.empty else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="k-icon"><i class="fas fa-users"></i></div><div class="k-value">{ct:.2f}M</div><div class="k-label">Total Tourists</div></div>', unsafe_allow_html=True)
    with c2:
        color = "#00FF88" if cg >= 0 else "#FF6B6B"
        st.markdown(f'<div class="kpi-card"><div class="k-icon"><i class="fas fa-arrow-trend-up"></i></div><div class="k-value" style="color:{color};">{cg:+.1f}%</div><div class="k-label">YoY Growth</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="k-icon"><i class="fas fa-dollar-sign"></i></div><div class="k-value">${cr:.0f}M</div><div class="k-label">Revenue (USD)</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card"><div class="k-icon"><i class="fas fa-rotate"></i></div><div class="k-value">{rr:.0f}%</div><div class="k-label">Recovery Rate</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart 1
    chart_card("chart-line", "Tourism Growth Trend", "Total visitors per year (millions)")
    fig = px.line(fy, x='Year', y='Total_Tourists_M', markers=True, template='plotly_dark')
    fig.update_traces(line_color='#00FFFF', line_width=2.5, marker_size=9,
                      marker_color='#FFFFFF', marker_line_color='#00FFFF', marker_line_width=2)
    fig.update_layout(**plot_layout(400, 'Year', 'Tourists (Millions)'))
    st.plotly_chart(fig, use_container_width=True)
    end_card()

    # Chart 2
    chart_card("dollar-sign", "Revenue Trend", "Estimated tourism revenue in USD millions")
    fig2 = px.area(fy, x='Year', y='Revenue_M', template='plotly_dark',
                   color_discrete_sequence=['#00B4D8'])
    fig2.update_traces(fill='tozeroy', fillcolor='rgba(0,180,216,0.15)', line_color='#00B4D8', line_width=2.5)
    fig2.update_layout(**plot_layout(400, 'Year', 'Revenue (USD M)'))
    st.plotly_chart(fig2, use_container_width=True)
    end_card()

    # Chart 3
    chart_card("chart-bar", "Domestic vs International", "Comparison of visitor origins per year")
    fig3 = px.bar(fy, x='Year', y=['Domestic_Tourists_M','International_Tourists_M'],
                  barmode='group', template='plotly_dark',
                  color_discrete_map={'Domestic_Tourists_M':'#00FFFF','International_Tourists_M':'#FF6B6B'},
                  labels={'value':'Tourists (M)','variable':'Type'})
    fig3.update_layout(**plot_layout(400, 'Year', 'Tourists (Millions)'))
    st.plotly_chart(fig3, use_container_width=True)
    end_card()

    # Chart 4
    chart_card("percent", "Year-over-Year Growth Rate", "Positive = growth, Negative = decline")
    gdf = fy[['Year','YoY_Growth']].dropna()
    fig4 = px.bar(gdf, x='Year', y='YoY_Growth', template='plotly_dark',
                  color='YoY_Growth', color_continuous_scale='RdYlGn',
                  labels={'YoY_Growth':'Growth (%)'})
    fig4.update_layout(**plot_layout(400, 'Year', 'Growth Rate (%)'))
    st.plotly_chart(fig4, use_container_width=True)
    end_card()

    # Chart 5
    chart_card("rotate", "Recovery Rate", "Recovery relative to peak performance year")
    fig5 = px.line(fy, x='Year', y='Recovery_Rate', markers=True, template='plotly_dark')
    fig5.update_traces(line_color='#00FF88', line_width=2.5, marker_size=9,
                       marker_color='#FFFFFF', marker_line_color='#00FF88', marker_line_width=2)
    fig5.update_layout(**plot_layout(400, 'Year', 'Recovery Rate (%)'))
    st.plotly_chart(fig5, use_container_width=True)
    end_card()


# ══════════════════════════════════════════════════════════════════════════════
# FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif selected_page == "Forecast":
    st.markdown('<div class="main-title"><i class="fas fa-brain"></i>AI-Powered Forecast 2025–2030</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-microchip"></i>Linear Regression Forecasting Model</div>', unsafe_allow_html=True)

    if len(fy) >= 3:
        X  = fy[['Year']].values
        y  = fy['Total_Tourists_M'].values
        m  = LinearRegression().fit(X, y)
        fy_pred = np.arange(2025, 2031).reshape(-1, 1)
        preds   = m.predict(fy_pred)
        r2      = m.score(X, y)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Model R² Score",  f"{r2:.3f}")
        with c2: st.metric("2030 Prediction", f"{preds[-1]:.2f}M tourists")
        with c3: st.metric("Annual Growth",   f"{m.coef_[0]:.3f}M / year")

        st.markdown("<br>", unsafe_allow_html=True)

        chart_card("chart-line", "Tourism Forecast 2025–2030", "Historical data + linear regression projection")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fy['Year'], y=fy['Total_Tourists_M'],
            mode='lines+markers', name='Historical',
            line=dict(color='#00FFFF', width=2.5),
            marker=dict(size=9, color='#FFFFFF',
                        line=dict(color='#00FFFF', width=2))
        ))
        fig.add_trace(go.Scatter(
            x=fy_pred.flatten(), y=preds,
            mode='lines+markers', name='Forecast',
            line=dict(color='#FF6B6B', width=2.5, dash='dash'),
            marker=dict(size=9, color='#FFFFFF',
                        line=dict(color='#FF6B6B', width=2))
        ))
        fig.add_vline(x=2020, line_dash="dot", line_color="rgba(255,165,0,0.6)",
                      annotation_text="COVID-19",
                      annotation_font=dict(color="rgba(255,165,0,0.9)", size=11))
        fig.update_layout(**plot_layout(500, 'Year', 'Tourists (Millions)'))
        st.plotly_chart(fig, use_container_width=True)
        end_card()

        st.markdown("<br>", unsafe_allow_html=True)
        chart_card("table", "Year-by-Year Forecast Table", "Predicted tourist arrivals and estimated revenue")
        tbl = pd.DataFrame({
            'Year': list(range(2025, 2031)),
            'Predicted Tourists (M)': [round(float(p), 2) for p in preds],
            'Est. Revenue (USD M)':   [round(float(p)*1e6*280/1e6, 0) for p in preds],
        })
        st.dataframe(tbl, use_container_width=True, hide_index=True)
        end_card()
    else:
        st.warning("Not enough data for forecasting — need at least 3 years.")


# ══════════════════════════════════════════════════════════════════════════════
# DESTINATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif selected_page == "Destinations":
    st.markdown('<div class="main-title"><i class="fas fa-map-location-dot"></i>Destination Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-magnifying-glass-chart"></i>Explore tourism by province, city &amp; destination type</div>', unsafe_allow_html=True)

    # Chart 1 — Top Cities
    chart_card("building-columns", "Top Cities by Total Tourists", "Ranked by cumulative visitor count")
    city_df = (fdf.groupby('City', as_index=False)['Total_Tourists'].sum()
                  .sort_values('Total_Tourists', ascending=False).head(10))
    city_df['Total_M'] = (city_df['Total_Tourists'] / 1e6).round(2)
    fc = px.bar(city_df, x='City', y='Total_M', template='plotly_dark',
                color='Total_M', color_continuous_scale='Teal',
                labels={'Total_M':'Tourists (M)'})
    fc.update_layout(**plot_layout(420, 'City', 'Tourists (Millions)'))
    st.plotly_chart(fc, use_container_width=True)
    end_card()

    c1, c2 = st.columns(2)
    with c1:
        chart_card("map", "Tourists by Province", "Share of total visitors per province")
        prov = fdf.groupby('Province', as_index=False)['Total_Tourists'].sum()
        prov['Total_M'] = (prov['Total_Tourists']/1e6).round(2)
        fp = px.pie(prov, values='Total_M', names='Province', template='plotly_dark',
                    color_discrete_sequence=px.colors.sequential.Teal)
        fp.update_traces(textfont_color='#FFFFFF')
        fp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='#FFFFFF', family='Inter'),
                         legend=dict(font=dict(color='#A0C0D8')),
                         margin=dict(l=10,r=10,t=10,b=10), height=380)
        st.plotly_chart(fp, use_container_width=True)
        end_card()

    with c2:
        chart_card("layer-group", "Tourists by Destination Type", "Mountain, nature, urban and more")
        dest = fdf.groupby('Destination_Type', as_index=False)['Total_Tourists'].sum()
        dest['Total_M'] = (dest['Total_Tourists']/1e6).round(2)
        fd = px.pie(dest, values='Total_M', names='Destination_Type', template='plotly_dark',
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        fd.update_traces(textfont_color='#FFFFFF')
        fd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='#FFFFFF', family='Inter'),
                         legend=dict(font=dict(color='#A0C0D8')),
                         margin=dict(l=10,r=10,t=10,b=10), height=380)
        st.plotly_chart(fd, use_container_width=True)
        end_card()

    # Chart — Scatter (fixed: no **PLOT_LAYOUT conflict)
    chart_card("shield-halved", "Safety Rating vs Popularity Score", "Bubble size = total tourists")
    fs = px.scatter(fdf, x='Safety_Rating', y='Popularity_Score',
                    color='Destination_Type', size='Total_Tourists',
                    hover_data=['City','Province','Main_Attraction'],
                    template='plotly_dark',
                    labels={'Safety_Rating':'Safety Rating (1–5)',
                            'Popularity_Score':'Popularity Score'})
    fs.update_layout(**plot_layout(450, 'Safety Rating (1–5)', 'Popularity Score'))
    st.plotly_chart(fs, use_container_width=True)
    end_card()

    # Chart — Avg Cost
    chart_card("money-bill-trend-up", "Average Cost by Destination Type", "Mean visitor spend in USD")
    cost = fdf.groupby('Destination_Type', as_index=False)['Average_Cost_USD'].mean().round(0)
    fco = px.bar(cost, x='Destination_Type', y='Average_Cost_USD', template='plotly_dark',
                 color='Average_Cost_USD', color_continuous_scale='Oranges',
                 labels={'Average_Cost_USD':'Avg Cost (USD)'})
    fco.update_layout(**plot_layout(400, 'Destination Type', 'Average Cost (USD)'))
    st.plotly_chart(fco, use_container_width=True)
    end_card()

    # Chart — Peak Season
    chart_card("sun", "Peak Season Distribution", "Total tourists by preferred travel season")
    sea = fdf.groupby('Peak_Season', as_index=False)['Total_Tourists'].sum()
    sea['Total_M'] = (sea['Total_Tourists']/1e6).round(2)
    fse = px.bar(sea, x='Peak_Season', y='Total_M', template='plotly_dark',
                 color='Peak_Season',
                 color_discrete_sequence=['#00FFFF','#FF6B6B','#00FF88','#FFD700'],
                 labels={'Total_M':'Tourists (M)'})
    fse.update_layout(**plot_layout(400, 'Peak Season', 'Tourists (Millions)'))
    st.plotly_chart(fse, use_container_width=True)
    end_card()


# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
elif selected_page == "Data":
    st.markdown('<div class="main-title"><i class="fas fa-database"></i>Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle"><i class="fas fa-table"></i>Raw Tourism Data — All Columns</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total Records",     len(fdf))
    with c2: st.metric("Cities",            fdf['City'].nunique())
    with c3: st.metric("Provinces",         fdf['Province'].nunique())
    with c4: st.metric("Destination Types", fdf['Destination_Type'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    provinces = ['All'] + sorted(fdf['Province'].unique().tolist())
    sel_prov  = st.selectbox("Filter by Province", provinces)
    disp      = fdf if sel_prov == 'All' else fdf[fdf['Province'] == sel_prov]

    chart_card("table", "Tourism Records", f"Showing {len(disp)} records")
    st.dataframe(disp, use_container_width=True, hide_index=True)
    end_card()

    csv = disp.to_csv(index=False).encode()
    st.download_button("Download CSV for Power BI", csv,
                       "pakistan_tourism.csv", "text/csv",
                       use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("chart-simple", "Quick Statistics", "Descriptive stats for numeric columns")
    st.dataframe(disp.describe().round(2), use_container_width=True)
    end_card()


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span><i class="fas fa-database"></i>Data Source: PTDC &amp; World Bank</span>
    <span><i class="fab fa-python"></i>Python &amp; Streamlit</span>
    <span><i class="fas fa-brain"></i>ML: Linear Regression</span>
    <span><i class="fas fa-graduation-cap"></i>Final Year Project 2025</span>
</div>
""", unsafe_allow_html=True)