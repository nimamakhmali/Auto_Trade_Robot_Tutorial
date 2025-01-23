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
   for(int i = OrdersTotal() - 1; i >= 0; i--)
     {
      if(OrderSelect(i, SELECT_BY_POS, MODE_TRADES))  // 
        {
         ulong ticket = OrderGetTicket(i);  // 
         MqlTradeRequest request;
         MqlTradeResult result;

         request.action = TRADE_ACTION_DEAL;
         request.symbol = OrderGetString(ORDER_SYMBOL);
         request.volume = OrderGetDouble(ORDER_VOLUME);
         request.price = SymbolInfoDouble(Symbol(), SYMBOL_BID);  // sell fee
         request.type = ORDER_TYPE_SELL;  // sell
         request.position = ticket;

         if(OrderSend(request, result))
            Print("Closed trade: Ticket ", ticket);
         else
            Print("Failed to close trade: ", GetLastError());
        }
     }
  }
