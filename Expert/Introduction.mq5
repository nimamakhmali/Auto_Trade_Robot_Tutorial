//+------------------------------------------------------------------+
//|                                                      SimpleEA.mq5|
//|                   Copyright 2025, Your Name                      |
//+------------------------------------------------------------------+
#property copyright "Your Name"
#property version   "1.00"
#property description "A simple expert advisor example"

//+------------------------------------------------------------------+
/                                            |
//+------------------------------------------------------------------+
int OnInit()
  {
   Print("Expert initialized!");
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//|                                                       |
//+------------------------------------------------------------------+
void OnTick()
  {
   double lot = 0.1;
   double price = SymbolInfoDouble(Symbol(), SYMBOL_ASK);  // قیمت خرید
   double sl = price - 50 * Point;  // 
   double tp = price + 50 * Point;  // 

   MqlTradeRequest request;
   MqlTradeResult result;

   request.action = TRADE_ACTION_DEAL;
   request.symbol = Symbol();
   request.volume = lot;
   request.price = price;
   request.sl = sl;
   request.tp = tp;
   request.type = ORDER_TYPE_BUY;
   request.deviation = 10;

   if(OrderSend(request, result))
      Print("Trade opened successfully!");
   else
      Print("Trade failed: ", GetLastError());
  }

//+------------------------------------------------------------------+
//|                                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   Print("Expert deinitialized!");
  }
