//+------------------------------------------------------------------+
//| 1-Minute Moving Average Crossover Strategy                      |
//+------------------------------------------------------------------+
#include <Trade/Trade.mqh>
CTrade trade; // Trading object

// Strategy Parameters
input int fastPeriod = 5;   // Fast MA Period
input int slowPeriod = 20;  // Slow MA Period
input double lotSize = 0.1; // Lot Size
input double stopLoss = 10; // Stop Loss in pips
input double takeProfit = 20; // Take Profit in pips
input string tradeSymbol = "EURUSD"; // Symbol to trade
input ENUM_TIMEFRAMES timeFrame = PERIOD_M1; // 1-Minute Timeframe

//+------------------------------------------------------------------+
//| OnTick Function (Runs on Every New Tick)                        |
//+------------------------------------------------------------------+
void OnTick()
{
   if(_Symbol != tradeSymbol) return; // Only trade on selected symbol

   // Get MA values
   double maFast = iMA(_Symbol, timeFrame, fastPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
   double maSlow = iMA(_Symbol, timeFrame, slowPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
   double maFastPrev = iMA(_Symbol, timeFrame, fastPeriod, 0, MODE_SMA, PRICE_CLOSE, 1);
   double maSlowPrev = iMA(_Symbol, timeFrame, slowPeriod, 0, MODE_SMA, PRICE_CLOSE, 1);
   
   // Check if trade already open
   if(PositionSelect(_Symbol))
       return; // Don't open new trade if already in a position
   
   // Define Stop Loss & Take Profit
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double slPips = stopLoss * point;
   double tpPips = takeProfit * point;
   
   // Buy Condition: Fast MA crosses above Slow MA
   if(maFast > maSlow && maFastPrev <= maSlowPrev)
   {
      double buyPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      double stopLossLevel = buyPrice - slPips;
      double takeProfitLevel = buyPrice + tpPips;

      trade.Buy(lotSize, _Symbol, buyPrice, stopLossLevel, takeProfitLevel, "MA Crossover Buy");
   }

   // Sell Condition: Fast MA crosses below Slow MA
   if(maFast < maSlow && maFastPrev >= maSlowPrev)
   {
      double sellPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      double stopLossLevel = sellPrice + slPips;
      double takeProfitLevel = sellPrice - tpPips;

      trade.Sell(lotSize, _Symbol, sellPrice, stopLossLevel, takeProfitLevel, "MA Crossover Sell");
   }
}
