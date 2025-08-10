# Chỉ cần điền thông tin Telegram
TELEGRAM_TOKEN = '8258155089:AAEsuHGa6HWp4GZfsQb4X6F3igTzvpA315w'
TELEGRAM_CHAT_ID = '7047923199'

# Các coin cố định - format Binance
FIXED_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']

# Lấy top coin từ Binance 24hr ticker
def get_dynamic_symbols():
    import requests
    try:
        # Lấy top volume coins từ Binance
        url = 'https://api.binance.com/api/v3/ticker/24hr'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            tickers = response.json()
            
            # Filter USDT pairs và sort theo volume
            usdt_pairs = [
                ticker for ticker in tickers 
                if ticker['symbol'].endswith('USDT') 
                and ticker['symbol'] not in FIXED_SYMBOLS
                and float(ticker['volume']) > 1000000  # Volume > 1M
            ]
            
            # Sort theo volume và lấy top 20
            usdt_pairs.sort(key=lambda x: float(x['quoteVolume']), reverse=True)
            dynamic_symbols = [ticker['symbol'] for ticker in usdt_pairs[:20]]
            
            print(f"✅ Loaded {len(dynamic_symbols)} dynamic symbols")
            return dynamic_symbols
            
    except Exception as e:
        print(f"❌ Error loading dynamic symbols: {e}")
        
    # Fallback nếu API lỗi
    return [
        'ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'LTCUSDT', 'XRPUSDT',
        'MATICUSDT', 'AVAXUSDT', 'ATOMUSDT', 'NEARUSDT', 'FTMUSDT'
    ]

# Combine fixed và dynamic symbols
def get_all_symbols():
    return FIXED_SYMBOLS + get_dynamic_symbols()

SYMBOLS = get_all_symbols()
