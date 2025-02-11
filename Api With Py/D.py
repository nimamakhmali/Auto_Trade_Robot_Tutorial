import MetaTrader5 as mt5
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    return True

# Get open positions
def get_open_positions():
    positions = mt5.positions_get()
    if positions is None:
        print("❌ No open positions found!")
        return
    
    print("📌 Open Positions:")
    for pos in positions:
        print(f"Order: {pos.ticket}, Symbol: {pos.symbol}, Type: {'Buy' if pos.type == 0 else 'Sell'}, Volume: {pos.volume}, Price: {pos.price_open}")

# Run
if __name__ == "__main__":
    if connect_mt5():
        get_open_positions()
        mt5.shutdown()
