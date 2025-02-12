import MetaTrader5 as mt5
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect to MetaTrader 5!")
        print(mt5.last_error())
        return False
    else:   
        print("✅ Connected to MetaTrader 5!")
        return True

# Get account information
def get_account_info():
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ Failed to get account information!")
        return
    print(f"Account ID: {account_info.login}")
    print(f"Balance: {account_info.balance}")
    print(f"Equity: {account_info.equity}")
    print(f"Margin Free: {account_info.margin_free}")

# Run
if __name__ == "__main__":
    if connect_mt5():
        get_account_info()
        mt5.shutdown()
