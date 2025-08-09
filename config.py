# Chỉ cần điền thông tin Telegram
TELEGRAM_TOKEN = '8258155089:AAEsuHGa6HWp4GZfsQb4X6F3igTzvpA315w'
TELEGRAM_CHAT_ID = '7047923199'

# Các coin cố định
FIXED_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']

# Lấy 10 coin mới nhất và 20 coin thịnh hành nhất từ CoinGecko
def get_dynamic_symbols():
    import requests
    # 10 coin mới nhất
    new_url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'
    new_resp = requests.get(new_url)
    new_coins = []
    if new_resp.status_code == 200:
        coins = new_resp.json()
        new_coins = [coin['id'] for coin in coins[-10:]]
    # 20 coin thịnh hành nhất
    trending_url = 'https://api.coingecko.com/api/v3/search/trending'
    trending_resp = requests.get(trending_url)
    trending_coins = []
    if trending_resp.status_code == 200:
        data = trending_resp.json()
        trending_coins = [item['item']['id'] for item in data['coins']][:20]
    # Chuyển về dạng SYMBOLS (id của CoinGecko)
    return new_coins + trending_coins

SYMBOLS = FIXED_SYMBOLS + get_dynamic_symbols()
