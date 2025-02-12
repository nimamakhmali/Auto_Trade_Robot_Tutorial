// ذخیره داده‌های بازار در یک فایل CSV
void OnStart()
{
   // مسیر فایل در پوشه مشترک متاتریدر 5
   string filePath = "market_data.csv";
   
   // دریافت اطلاعات قیمت‌های فعلی
   double bid = SymbolInfoDouble(Symbol(), SYMBOL_BID);
   double ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK);
   datetime timestamp = TimeCurrent();
   
   // باز کردن فایل برای نوشتن (FILE_COMMON یعنی در پوشه‌ی مشترک ذخیره می‌شود)
   int fileHandle = FileOpen(filePath, FILE_CSV | FILE_WRITE | FILE_COMMON);
   
   if (fileHandle != INVALID_HANDLE)
   {
      // نوشتن اطلاعات در فایل
      FileWrite(fileHandle, TimeToString(timestamp, TIME_SECONDS), bid, ask);
      
      // بستن فایل
      FileClose(fileHandle);
      
      Print("✅ Data saved successfully in: ", filePath);
   }
   else
   {
      Print("❌ Failed to open file for writing!");
   }
}
