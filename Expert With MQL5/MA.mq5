//+------------------------------------------------------------------+
//| 1-Minute Moving Average Crossover Strategy                      |
//+------------------------------------------------------------------+
#include <Trade/Trade.mqh>
CTrade trade; 

// Inputs
input int fastPeriod = 5;   
input int slowPeriod = 20;  
input double lotSize = 0.1; 
input double stopLoss = 10; 
input double takeProfit = 20; 
input string tradeSymbol = "EURUSD"; 
input ENUM_TIMEFRAMES timeFrame = PERIOD_M1; 

//+------------------------------------------------------------------+
//| OnTick Function (Runs Every Tick)                                |
//+------------------------------------------------------------------+
void OnTick()
{
   if(_Symbol != tradeSymbol) return; 

   // Get MA Handles
   int fastMAHandle = iMA(_Symbol, timeFrame, fastPeriod, 0, MODE_SMA, PRICE_CLOSE);
   int slowMAHandle = iMA(_Symbol, timeFrame, slowPeriod, 0, MODE_SMA, PRICE_CLOSE);

   // Array to store indicator values
   double fastMA[], slowMA[];
   
   // Copy indicator values
   if(CopyBuffer(fastMAHandle, 0, 0, 2, fastMA) < 0) return;
   if(CopyBuffer(slowMAHandle, 0, 0, 2, slowMA) < 0) return;
   
   double maFast = fastMA[0];  
   double maSlow = slowMA[0];  
   double maFastPrev = fastMA[1];  
   double maSlowPrev = slowMA[1];

   // Check if trade already open
   if(PositionSelect(_Symbol)) return; 
   
   // Define Stop Loss & Take Profit
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double slPips = stopLoss * point;
   double tpPips = takeProfit * point;
   
   // Buy Condition
   if(maFast > maSlow && maFastPrev <= maSlowPrev)
   {
      double buyPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      trade.Buy(lotSize, _Symbol, buyPrice, buyPrice - slPips, buyPrice + tpPips, "Buy Signal");
   }

   // Sell Condition
   if(maFast < maSlow && maFastPrev >= maSlowPrev)
   {
      double sellPrice = SymbolInfoDouble(_Symbol, SYMBOL_BID);
      trade.Sell(lotSize, _Symbol, sellPrice, sellPrice + slPips, sellPrice - tpPips, "Sell Signal");
   }
}
