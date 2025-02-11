import MetaTrader5 as mt5

if not mt5.initialize():
    print("ّFailed to connect to MetaTrader")
    mt5.shutdown()
    exit()
else:
    print("Successfully") 

account_info = mt5.account_info()
if account_info is not None:
    print(f"Account ID: {account_info.login}")
    print(f"Balance: {account_info.balance}")
    print(f"Equity: {account_info.equity}")
    
symbol = "EURUSD"
symbol_info = mt5.symbol_info(symbol)

if symbol_info is None:
    print(f"Symbol {symbol} not found")  
    mt5.shutdown()
    exit()
      
rates = mt5.copy_rates_from_pos(symbol, mt5. TIMEFRAME_M5, 0, 10)

if rates is None:      
    print("Failed to get historical data")
else:  
    print("Last 10 candles:")
    for rate in rates:
        print(rate) 
        
positions = mt5.positions_get()
if positions:
    print(f"Open Positions: {len(positions)}")
    for pos in positions:
        print(f"Ticket: {pos.ticket}, symbol: {pos.symbol}, Type: {pos.type}, Volume: {pos.volume}")
else:
    print("Not open Positions")
    
mt5.shutdown()                     