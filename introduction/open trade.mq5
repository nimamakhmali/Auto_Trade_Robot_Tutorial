
//+------------------------------------------------------------------+
//|                                                      MyExpert.mq5|
//|                   Copyright 2025, Your Name                      |
//|                   https://yourwebsite.com                        |
//+------------------------------------------------------------------+
#property copyright "Your Name, 2025"
#property version   "1.00"
#property description "This is a simple trading expert advisor"



void OnStart()
  {
   double lot = 0.1;  // حجم معامله
   double price = SymbolInfoDouble(Symbol(), SYMBOL_ASK);  // قیمت خرید
   double sl = price - 50 * Point;  // حد ضرر (Stop Loss)
   double tp = price + 50 * Point;  // حد سود (Take Profit)

   MqlTradeRequest request;       // درخواست معامله
   MqlTradeResult result;         // نتیجه معامله

   request.action = TRADE_ACTION_DEAL;  // نوع معامله (مستقیم)
   request.symbol = Symbol();          // نماد معاملاتی فعلی
   request.volume = lot;               // حجم معامله
   request.price = price;              // قیمت معامله
   request.sl = sl;                    //
   request.tp = tp;                    // 
   request.type = ORDER_TYPE_BUY;      // order
   request.deviation = 10;             // pip

   if(OrderSend(request, result))      // ارسال معامله
      Print("Trade opened successfully: Ticket ", result.order);
   else
      Print("Failed to open trade: ", GetLastError());
  }
