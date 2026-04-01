import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

#Page config
st.set_page_config(
    page_title="NSE Portfolio Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Custom CSS

st.markdown("""
<style>
section[data-testid="stSidebar"] { display: block !important; }
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --accent: #00e5a0;
    --accent2: #7c6aff;
    --red: #ff4d6d;
    --green: #00e5a0;
    --text: #e8e8f0;
    --muted: #6b6b8a;
}
[data-testid="stSidebar"] {
    transform: none !important;
    min-width: 300px !important;
}
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 320px !important;
    width: 320px !important;
}

[data-testid="stSidebar"] * {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* Hide default streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent);
}
.metric-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
}
.metric-value.green { color: var(--green); }
.metric-value.red { color: var(--red); }

/* Table */
.stock-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}
.stock-table th {
    text-align: left;
    padding: 12px 16px;
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    font-family: 'Syne', sans-serif;
}
.stock-table td {
    padding: 14px 16px;
    border-bottom: 1px solid #1a1a24;
    color: var(--text);
}
.stock-table tr:hover td { background: var(--surface2); }
.pill-green {
    background: rgba(0,229,160,0.12);
    color: var(--green);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.pill-red {
    background: rgba(255,77,109,0.12);
    color: var(--red);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.pill-neutral {
    background: rgba(124,106,255,0.12);
    color: var(--accent2);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
}

/* Section headers */
.section-header {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Alert boxes */
.alert-green {
    background: rgba(0,229,160,0.08);
    border: 1px solid rgba(0,229,160,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    color: var(--green);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin: 4px 0;
}
.alert-red {
    background: rgba(255,77,109,0.08);
    border: 1px solid rgba(255,77,109,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    color: var(--red);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin: 4px 0;
}
.alert-safe {
    background: rgba(124,106,255,0.08);
    border: 1px solid rgba(124,106,255,0.3);
    border-radius: 8px;
    padding: 10px 16px;
    color: var(--accent2);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin: 4px 0;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons */
.stButton button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 8px 20px !important;
}
.stButton button:hover {
    background: #00c985 !important;
}

/* Page title */
.page-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: var(--text);
    line-height: 1;
}
.page-title span { color: var(--accent); }
.page-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 2px;
    margin-top: 6px;
}

div[data-testid="stPlotlyChart"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)

#Portfolio Data
if "portfolio" not in st.session_state:
    st.session_state.portfolio = [
        {"symbol": "RELIANCE",   "quantity": 10, "buy_price_avg": 2400.00, "sector": "Energy"},
        {"symbol": "TCS",        "quantity": 5,  "buy_price_avg": 3500.00, "sector": "IT"},
        {"symbol": "HDFCBANK",   "quantity": 15, "buy_price_avg": 1600.00, "sector": "Banking"},
        {"symbol": "INFY",       "quantity": 20, "buy_price_avg": 1450.00, "sector": "IT"},
        {"symbol": "WIPRO",      "quantity": 25, "buy_price_avg": 420.00,  "sector": "IT"},
        {"symbol": "ICICIBANK",  "quantity": 12, "buy_price_avg": 950.00,  "sector": "Banking"},
        {"symbol": "ADANIENT",   "quantity": 8,  "buy_price_avg": 2800.00, "sector": "Conglomerate"},
        {"symbol": "BAJFINANCE", "quantity": 6,  "buy_price_avg": 6800.00, "sector": "Finance"},
        {"symbol": "ASIANPAINT", "quantity": 10, "buy_price_avg": 3200.00, "sector": "Consumer"},
        {"symbol": "MARUTI",     "quantity": 4,  "buy_price_avg": 9500.00, "sector": "Automobile"},
        {"symbol": "SUNPHARMA",  "quantity": 18, "buy_price_avg": 1100.00, "sector": "Pharma"},
        {"symbol": "HINDUNILVR", "quantity": 8,  "buy_price_avg": 2500.00, "sector": "Consumer"},
        {"symbol": "ITC",        "quantity": 40, "buy_price_avg": 430.00,  "sector": "Consumer"},
    ]

portfolio = st.session_state.portfolio

#Logic Functions
def fetch_live_price():
    for i in portfolio:
        x = i["symbol"] + ".NS"
        ticker = yf.Ticker(x)
        price1 = round(ticker.fast_info['last_price'], 1)
        i["price"] = price1

def add_stock(user_add, quantity1, cp, bp_new, sector="Other"):
    new_stock = {
        "symbol": user_add,
        "quantity": quantity1,
        "buy_price_avg": bp_new,
        "price": cp,
        "sector": sector
    }
    portfolio.append(new_stock)
    return f"Stock {user_add} added successfully!"

def stock_del(stock):
    for i in portfolio:
        if i["symbol"] == stock:
            portfolio.remove(i)
            return True
    return False

def p_or_l(stck):
    for i in portfolio:
        if i["symbol"] == stck:
            return (i["price"] - i["buy_price_avg"]) * i["quantity"]

def performance():
    lst = []
    for i in portfolio:
        profit_or_loss = (i["price"] - i["buy_price_avg"]) * i["quantity"]
        lst.append((i["symbol"], profit_or_loss))
    best = max(lst, key=lambda x: x[1])
    worst = min(lst, key=lambda x: x[1])
    return best, worst

def total_value():
    sum1 = 0
    for i in portfolio:
        sum1 += i["price"] * i["quantity"]
    return sum1

def price_alert(p_alert, l_alert):
    alerts = []
    for i in portfolio:
        profit_loss_percent = ((i["price"] - i["buy_price_avg"]) / i["buy_price_avg"]) * 100
        if profit_loss_percent > p_alert:
            alerts.append(("green", f"🟢 PROFIT ALERT — {i['symbol']} (+{profit_loss_percent:.1f}%), Consider Selling!"))
        elif profit_loss_percent < -l_alert:
            alerts.append(("red", f"🔴 LOSS ALERT — {i['symbol']} ({profit_loss_percent:.1f}%), Danger Zone!"))
        else:
            alerts.append(("safe", f"✅ {i['symbol']} is Safe ({profit_loss_percent:+.1f}%)"))
    return alerts

def sector_allocation():
    dict1 = {}
    for i in portfolio:
        val = i["quantity"] * i["price"]
        dict1[i["sector"]] = dict1.get(i["sector"], 0) + val
    return dict1

#Fetch prices on load
if "prices_loaded" not in st.session_state:
    with st.spinner("Fetching live prices from NSE..."):
        fetch_live_price()
    st.session_state.prices_loaded = True

#Header
col_title, col_refresh = st.columns([5, 1])
with col_title:
    st.markdown("""
    <div class="page-title">Portfolio<span>.</span></div>
    <div class="page-subtitle">NSE LIVE TRACKER — INDIA</div>
    """, unsafe_allow_html=True)
with col_refresh:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⟳ Refresh"):
        with st.spinner("Fetching live prices..."):
            fetch_live_price()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

#Top Metrics
tv = total_value()
total_invested = sum(i["buy_price_avg"] * i["quantity"] for i in portfolio)
total_pl = tv - total_invested
total_pl_pct = (total_pl / total_invested) * 100
best, worst = performance()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Value</div>
        <div class="metric-value">₹{tv:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    pl_class = "green" if total_pl >= 0 else "red"
    pl_sign = "+" if total_pl >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total P&L</div>
        <div class="metric-value {pl_class}">{pl_sign}₹{total_pl:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Best Performer</div>
        <div class="metric-value green">{best[0]}<br><span style="font-size:16px">+₹{best[1]:,.0f}</span></div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Worst Performer</div>
        <div class="metric-value red">{worst[0]}<br><span style="font-size:16px">₹{worst[1]:,.0f}</span></div>
    </div>""", unsafe_allow_html=True)

#Portfolio Table
st.markdown('<div class="section-header">Holdings</div>', unsafe_allow_html=True)

rows = ""
for i in portfolio:
    pl = (i["price"] - i["buy_price_avg"]) * i["quantity"]
    pl_pct = ((i["price"] - i["buy_price_avg"]) / i["buy_price_avg"]) * 100
    pl_sign = "+" if pl >= 0 else ""
    pill_class = "pill-green" if pl >= 0 else "pill-red"
    rows += f"""
    <tr>
        <td><strong>{i['symbol']}</strong></td>
        <td><span class="pill-neutral">{i.get('sector','—')}</span></td>
        <td>{i['quantity']}</td>
        <td>₹{i['buy_price_avg']:,.1f}</td>
        <td>₹{i.get('price', 0):,.1f}</td>
        <td><span class="{pill_class}">{pl_sign}₹{pl:,.0f} ({pl_sign}{pl_pct:.1f}%)</span></td>
    </tr>"""

st.markdown(f"""
<div style="background:#111118; border:1px solid #2a2a3a; border-radius:12px; overflow:hidden; margin-bottom:24px;">
<table class="stock-table">
    <thead>
        <tr>
            <th>Symbol</th><th>Sector</th><th>Qty</th>
            <th>Avg Buy</th><th>Live Price</th><th>P&L</th>
        </tr>
    </thead>
    <tbody>{rows}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

#Charts
st.markdown('<div class="section-header">Analytics</div>', unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    symbols = [i["symbol"] for i in portfolio]
    pl_values = [(i["price"] - i["buy_price_avg"]) * i["quantity"] for i in portfolio]
    fig_bar = go.Figure(go.Bar(
        x=symbols, y=pl_values,
        marker=dict(
            color=pl_values,
            colorscale=[[0, "#ff4d6d"], [0.5, "#2a2a3a"], [1, "#00e5a0"]],
            line=dict(width=0)
        )
    ))
    fig_bar.update_layout(
        title=dict(text="P&L per Stock", font=dict(family="Syne", size=14, color="#e8e8f0")),
        paper_bgcolor="#111118", plot_bgcolor="#111118",
        font=dict(family="JetBrains Mono", color="#6b6b8a"),
        xaxis=dict(gridcolor="#1a1a24", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#1a1a24", tickprefix="₹"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    sector_data = sector_allocation()
    fig_pie = go.Figure(go.Pie(
        labels=list(sector_data.keys()),
        values=list(sector_data.values()),
        hole=0.55,
        marker=dict(colors=["#00e5a0","#7c6aff","#ff4d6d","#ffd166","#06d6a0","#118ab2","#ef476f"]),
        textfont=dict(family="JetBrains Mono", size=11),
    ))
    fig_pie.update_layout(
        title=dict(text="Sector Allocation", font=dict(family="Syne", size=14, color="#e8e8f0")),
        paper_bgcolor="#111118", plot_bgcolor="#111118",
        font=dict(family="JetBrains Mono", color="#6b6b8a"),
        legend=dict(font=dict(size=10, color="#6b6b8a"), bgcolor="#111118"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    st.plotly_chart(fig_pie, use_container_width=True)

#Sidebar
with st.sidebar:
    st.markdown("""
    <div style="font-size:18px; font-weight:800; letter-spacing:-0.5px; margin-bottom:4px;">Controls</div>
    <div style="font-size:10px; letter-spacing:2px; color:#6b6b8a; font-family:'JetBrains Mono',monospace; margin-bottom:24px;">MANAGE PORTFOLIO</div>
    """, unsafe_allow_html=True)

    #Add Stock
    if st.checkbox("Add Stock"):
        sym = st.text_input("Symbol (e.g. TATAMOTORS)", key="add_sym").upper()
        qty = st.number_input("Quantity", min_value=1, value=1, key="add_qty")
        bp  = st.number_input("Buy Price (₹)", min_value=0.0, value=100.0, key="add_bp")
        cp  = st.number_input("Current Price (₹)", min_value=0.0, value=100.0, key="add_cp")
        sec = st.selectbox("Sector", ["IT","Banking","Energy","Finance","Consumer","Pharma","Automobile","Conglomerate","Other"], key="add_sec")
        if st.button("Add Stock"):
            if sym:
                msg = add_stock(sym, qty, cp, bp, sec)
                st.success(msg)
                st.rerun()

    #Delete Stock
    if st.checkbox("Delete Stock"):
        symbols_list = [i["symbol"] for i in portfolio]
        del_sym = st.selectbox("Select stock to delete", symbols_list, key="del_sym")
        if st.button("Delete Stock"):
            if stock_del(del_sym):
                st.success(f"{del_sym} removed.")
                st.rerun()

    #Price Alert
    if st.checkbox("Price Alerts"):
        p_thresh = st.slider("Profit Alert (%)", 1, 100, 15)
        l_thresh = st.slider("Loss Alert (%)", 1, 100, 10)
        if st.button("Run Alerts"):
            alerts = price_alert(p_thresh, l_thresh)
            for kind, msg in alerts:
                if kind == "green":
                    st.markdown(f'<div class="alert-green">{msg}</div>', unsafe_allow_html=True)
                elif kind == "red":
                    st.markdown(f'<div class="alert-red">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-safe">{msg}</div>', unsafe_allow_html=True)

    #Stock Search
    if st.checkbox("Search Stock"):
        search_sym = st.selectbox("Select stock", [i["symbol"] for i in portfolio], key="search_sym")
        if st.button("Search"):
            for i in portfolio:
                if i["symbol"] == search_sym:
                    pl = (i["price"] - i["buy_price_avg"]) * i["quantity"]
                    st.markdown(f"""
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; line-height:2;">
                    <b>{i['symbol']}</b><br>
                    Qty: {i['quantity']}<br>
                    Buy Avg: ₹{i['buy_price_avg']}<br>
                    Live: ₹{i['price']}<br>
                    P&L: {'🟢' if pl>=0 else '🔴'} ₹{pl:,.0f}
                    </div>""", unsafe_allow_html=True)
