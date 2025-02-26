import MetaTrader5 as mt5

class RiskManagement:
    
    def connect_to_mt5(self):
        """Connect to MetaTrader 5"""
        if not mt5.initialize():
            print("Failed to initialize MetaTrader 5")
            return None
        else:
            print("MetaTrader 5 Initialized successfully")
            return True

    def __init__(self, symbol="EURUSD", risk_percentage=0.01, stop_loss_pips=50):
        self.symbol = symbol
        self.risk_percentage = risk_percentage
        self.stop_loss_pips = stop_loss_pips
        self.account_balance = self.get_account_balance()
        self.tick_size = self.get_tick_size()

    def get_account_balance(self):
        """Retrieve account balance"""
        account_info = mt5.account_info()
        if account_info is None:
            print("Unable to get account information. Please check your MetaTrader 5 connection.")
            return 0  # Return 0 to avoid division by zero if account info is not fetched
        return account_info.balance

    def get_tick_size(self):
        """Retrieve tick size"""
        symbol_info = mt5.symbol_info(self.symbol)
        if symbol_info is None:
            print(f"Unable to get information for symbol {self.symbol}. Please check if the symbol is available in MetaTrader 5.")
            return 0  # Return 0 to avoid division by zero if symbol info is not fetched
        return symbol_info.point

    def calculate_position_size(self):
        """Calculate position size based on risk management settings"""
        stop_loss_value = self.get_stop_loss_value()  # Example of calculating stop loss
        if stop_loss_value == 0:
            print("Stop loss value is zero. Cannot calculate position size.")
            return 0  # Prevent division by zero

        account_balance = self.get_account_balance()
        position_size = (account_balance * self.risk_percentage) / stop_loss_value
        return position_size

    def set_stop_loss_take_profit(self, entry_price, is_buy=True):
        """محاسبه حد ضرر و حد سود"""
        stop_loss = entry_price - self.stop_loss_pips * self.tick_size if is_buy else entry_price + self.stop_loss_pips * self.tick_size
        take_profit = entry_price + self.stop_loss_pips * self.tick_size * 2 if is_buy else entry_price - self.stop_loss_pips * self.tick_size * 2
        return stop_loss, take_profit

    def get_trade_parameters(self, signal, entry_price):
        """محاسبه پارامترهای تجارت (حجم پوزیشن، حد ضرر، حد سود)"""
        position_size = self.calculate_position_size()
        stop_loss, take_profit = self.set_stop_loss_take_profit(entry_price, is_buy=(signal == 1))

        return {
            "symbol": self.symbol,
            "volume": position_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

# **مثال استفاده**
if __name__ == "__main__":
    # ایجاد شیء مدیریت ریسک
    risk_manager = RiskManagement(symbol="EURUSD", risk_percentage=0.01, stop_loss_pips=50)
    
    # فرض کنید که سیگنال خرید است و قیمت ورود 1.1200 است
    signal = 1  # سیگنال خرید
    entry_price = 1.1200  # قیمت ورود
    
    # دریافت پارامترهای تجارت
    trade_params = risk_manager.get_trade_parameters(signal, entry_price)
    
    print("Trade Parameters:")
    print(trade_params)
