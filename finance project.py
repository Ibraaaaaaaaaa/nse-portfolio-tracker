#importing required modules
import yfinance as yf
import plotly.express as py
from rich.console import Console
from rich.table import Table

#Pre-Determined set of stocks in a portfolio
portfolio = [

    {"symbol": "RELIANCE", "quantity": 10, "buy_price_avg": 2400.00,"sector": "Energy"},
    {"symbol": "TCS", "quantity": 5, "buy_price_avg": 3500.00,"sector": "IT"},
    {"symbol": "HDFCBANK", "quantity": 15, "buy_price_avg": 1600.00,"sector": "Banking"},
    {"symbol": "INFY", "quantity": 20, "buy_price_avg": 1450.00, "sector": "IT"},
    {"symbol": "WIPRO", "quantity": 25, "buy_price_avg": 420.00, "sector": "IT"},
    {"symbol": "ICICIBANK", "quantity": 12, "buy_price_avg": 950.00, "sector": "Banking"},
    {"symbol": "ADANIENT", "quantity": 8, "buy_price_avg": 2800.00, "sector": "Conglomerate"},
    {"symbol": "BAJFINANCE", "quantity": 6, "buy_price_avg": 6800.00, "sector": "Finance"},
    {"symbol": "ASIANPAINT", "quantity": 10, "buy_price_avg": 3200.00, "sector": "Consumer"},
    {"symbol": "MARUTI", "quantity": 4, "buy_price_avg": 9500.00, "sector": "Automobile"},
    {"symbol": "SUNPHARMA", "quantity": 18, "buy_price_avg": 1100.00, "sector": "Pharma"},
    {"symbol": "HINDUNILVR", "quantity": 8, "buy_price_avg": 2500.00, "sector": "Consumer"},
    {"symbol": "ITC", "quantity": 40, "buy_price_avg": 430.00, "sector": "Consumer"}
]

#Live Price of shares 
def fetch_live_price():
    global price1
    for i in portfolio:
        x = i["symbol"] + ".NS"
        ticker = yf.Ticker(x)
        price1 = round(ticker.fast_info['last_price'], 1)
        i["price"] = price1

#Adding a new stock by user
def add_stock(user_add, quantity1, cp, bp_new, sector):

    new_stock = {
        "symbol": user_add,
        "quantity": quantity1,
        "buy_price_avg": bp_new,
        "price": cp,
        "sector": sector
    }
    portfolio.append(new_stock)


    bp = (i["buy_price_avg"] + bp_new) / 2
    if i["symbol"] == user_add:
        return i["symbol"], i["quantity"], i["buy_price_avg"], i["price"]

    port = f"Your new portfolio is: {portfolio}"
    return  f"Your stock {new_stock} was added successfully", port


#Changing of price by user
def price(stck, n_quantity, quantity, n_bp):

    if n_quantity == "y":
        for stock in portfolio:
            if stock["symbol"] == stck:
                stock["price"] = price1
                stock["quantity"] = quantity
                stock["buy_price_avg"] = n_bp
        return portfolio
    elif n_quantity == "n":
        for stock in portfolio:
            if stock["symbol"] == stck:
                stock["price"] = price1
                stock["buy_price_avg"] = n_bp
        return portfolio

#Calculation of P/L of a stock
def p_or_l(stck):

    for i in portfolio:
        if i["symbol"] == stck:
            profit_or_loss = (i["price"] - i["buy_price_avg"]) * i["quantity"]
            return profit_or_loss

#Deletion of stock
def stock_del(stock):
    for i in portfolio:
        if i["symbol"] == stock:
            portfolio.remove(i)
#Stock search
def stock_search(stock):

    for i in portfolio:
        if i["symbol"] == stock:
            return i["symbol"], i["quantity"], i["buy_price_avg"], i["price"]

#Best and Worst performing stocks
def performance():
    lst = []
    for i in portfolio:
        profit_or_loss = (i["price"] - i["buy_price_avg"]) * i["quantity"]
        lst.append(profit_or_loss)
    return max(lst), min(lst)

#Total Portfolio value
def total_value():

    sum1 = 0
    for i in portfolio:
        sum1 += i["price"] * i["quantity"]
    return sum1

#Price alerts
def price_alert(p_alert, l_alert):
    alerts = []
    p_alert = p_alert/100
    l_alert = l_alert/100
    for i in portfolio:
        profit_loss_percent = ((i["price"] - i["buy_price_avg"]) / i["buy_price_avg"]) * 100
        if p_alert < profit_loss_percent:
           alerts.append(" 🟢 PROFIT ALERT - {i['symbol']}, Consider Selling!!")
        elif l_alert > profit_loss_percent:
            alerts.append(" 🔴 LOSS ALERT - {i['symbol']}, Danger Zone!!")
        else:
            alerts.append("{i['symbol']}, Is Safe!!")
    return alerts

#Graphs of P/L
def show_pl_chart():
    symbols = []
    for i in portfolio:
        symbols.append(i["symbol"])
    pl_values = []
    for i in portfolio:
        pl_values.append((i["price"] - i["buy_price_avg"]) * i["quantity"])
    fig = py.bar(
    x=symbols,
    y=pl_values,
    title="Portfolio P&L",
    labels={"x": "Stock", "y": "Profit / Loss (₹)"},
    color=pl_values,
    color_continuous_scale=["red", "green"])
    fig.show()

#Sector wise arrangement
def sector_allocation():
    global dict1
    dict1 = {}
    for i in portfolio:
        if i["sector"] in dict1:
            dict1[i["sector"]] += i["quantity"] * i["price"]
        elif i["sector"] not in dict1:
            dict1[i["sector"]] = i["quantity"] * i["price"]


#Sector Pie Chart
def show_sector_chart():
    sector_allocation()
    sectors = list(dict1.keys())
    sector_value = list(dict1.values())

    fig = py.pie(names=sectors, values=sector_value)
    fig.show()

#Menu/Dashboard
def show_dashboard():
    p_or_l("MARUTI")

    console = Console()
    table = Table(show_header=True, header_style="bold blue")

    table.add_column("Symbol", justify="center", style="bold blue")
    table.add_column("Quantity", justify="center", style="white")
    table.add_column("Buy Price", justify="center", style="bold blue")
    table.add_column("Current Price", justify="center", style="bold blue")
    table.add_column("P&L", justify="center", style="bold blue")

    for i in portfolio:
        profit_or_loss = round((i["price"] - i["buy_price_avg"]) * i["quantity"], 1)
        table.add_row(i["symbol"], str(i["quantity"]), str(i["buy_price_avg"]), str(i["price"]), str(profit_or_loss))
    console.print(table)




