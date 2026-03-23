# NSE Portfolio Tracker 📈

A real-time stock portfolio tracker for the Indian market (NSE), built in Python. Tracks live prices, calculates P&L, visualizes sector allocation, and runs price alerts — available as both a terminal dashboard and a Streamlit web app.

---

## Features

- **Live Prices** — fetches real-time NSE stock prices via `yfinance`
- **P&L Tracking** — calculates profit/loss per stock and across the full portfolio
- **Sector Allocation** — donut chart showing portfolio distribution by sector
- **Price Alerts** — configurable profit/loss threshold alerts for every holding
- **Stock Search** — quick lookup of any stock in your portfolio
- **Add / Delete Stocks** — manage your holdings directly from the web UI
- **Two Interfaces** — terminal dashboard (via `rich`) and a web app (via `streamlit`)

---

## Screenshots

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/f721586f-9011-4fd4-b695-e209c47cf93a" />


---

## Tech Stack

| Tool | Purpose |
|------|---------|
| `yfinance` | Live NSE stock price data |
| `streamlit` | Web dashboard UI |
| `plotly` | Interactive charts |
| `rich` | Terminal dashboard |

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Ibraaaaaaaaaa/nse-portfolio-tracker.git
cd nse-portfolio-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the web app
```bash
streamlit run app.py
```

### 4. Or run the terminal version
```bash
python "finance project.py"
```

---

## Requirements

```
yfinance
streamlit
plotly
rich
```

---

## Project Structure

```
nse-portfolio-tracker/
├── app.py                  # Streamlit web dashboard
├── finance project.py      # Terminal version with rich dashboard
├── requirements.txt
└── README.md
```

---

## Future Plans

- Save/load portfolio data via JSON
- Historical performance charts
- Support for multiple portfolios
