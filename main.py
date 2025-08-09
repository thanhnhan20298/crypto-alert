# --- ATR Calculation ---
def calculate_atr(ohlc, period=14):
    if len(ohlc) < period:
        return None
    trs = []
    for i in range(1, len(ohlc)):
        high = ohlc[i][2]
        low = ohlc[i][3]
        prev_close = ohlc[i-1][4]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    atr = sum(trs[-period:]) / period
    return atr
import time

import schedule
import requests
import threading
import matplotlib.pyplot as plt
import io
import base64

TELEGRAM_TOKEN = '8258155089:AAEsuHGa6HWp4GZfsQb4X6F3igTzvpA315w'
TELEGRAM_CHAT_ID = '7047923199'

def send_telegram(text, image=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    r = requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': text})
    print(f"Telegram response: {r.text}")
    if image:
        url_photo = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto'
        files = {'photo': image}
        r_photo = requests.post(url_photo, data={'chat_id': TELEGRAM_CHAT_ID}, files=files)
        print(f"Telegram photo response: {r_photo.text}")
# --- MACD Calculation ---
def calculate_bollinger(closes, period=20, num_std=2):
    if len(closes) < period:
        return None, None, None
    ma = sum(closes[-period:]) / period
    std = (sum([(x - ma) ** 2 for x in closes[-period:]]) / period) ** 0.5
    upper = ma + num_std * std
    lower = ma - num_std * std
    return ma, upper, lower

def calculate_stochastic(ohlc, k_period=14, d_period=3):
    if len(ohlc) < k_period:
        return None, None
    closes = [item[4] for item in ohlc]
    stoch_k = []
    for i in range(k_period, len(closes)):
        high = max([ohlc[j][2] for j in range(i - k_period, i)])
        low = min([ohlc[j][3] for j in range(i - k_period, i)])
        k = 100 * (closes[i] - low) / (high - low) if high != low else 0
        stoch_k.append(k)
    stoch_d = [sum(stoch_k[max(0, i - d_period + 1):i + 1]) / d_period for i in range(len(stoch_k))]
    return stoch_k[-1], stoch_d[-1] if stoch_d else None



# --- RSI Calculation ---
def calculate_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    deltas = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
    gains = [d for d in deltas if d > 0]
    losses = [-d for d in deltas if d < 0]
    avg_gain = sum(gains)/period if gains else 0
    avg_loss = sum(losses)/period if losses else 0
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# --- MACD Calculation ---
def calculate_macd(closes, fast_period=12, slow_period=26, signal_period=9):
    if len(closes) < slow_period + signal_period:
        return None, None
    def ema(data, period):
        ema_values = []
        k = 2 / (period + 1)
        ema_prev = sum(data[:period]) / period
        ema_values.append(ema_prev)
        for price in data[period:]:
            ema_new = price * k + ema_prev * (1 - k)
            ema_values.append(ema_new)
            ema_prev = ema_new
        return ema_values
    fast_ema = ema(closes, fast_period)
    slow_ema = ema(closes, slow_period)
    macd_line = [f - s for f, s in zip(fast_ema[-len(slow_ema):], slow_ema)]
    signal_line = ema(macd_line, signal_period)
    macd_value = macd_line[-1]
    signal_value = signal_line[-1]
    return macd_value, signal_value

# --- Analysis Logic ---
def get_cg_id(symbol):
    mapping = {
        'BTCUSDT': 'bitcoin',
        'ETHUSDT': 'ethereum',
        'BNBUSDT': 'binancecoin',
        'SOLUSDT': 'solana',
    }
    return mapping.get(symbol, symbol)
def get_trending_coins():
    url = 'https://api.coingecko.com/api/v3/search/trending'
    resp = requests.get(url)
    trending = []
    if resp.status_code == 200:
        data = resp.json()
        trending = [item['item']['id'] for item in data['coins']]
    return trending

def get_cg_ohlc(coin_id, days=1):
    # Lấy dữ liệu OHLC 5 phút từ CoinGecko
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days={days}'
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        closes = [float(item[4]) for item in data]  # item: [timestamp, open, high, low, close]
        return closes
    return []

def analyze_and_alert():
    coins = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']
    signals_main = []
    signals_others = []
    state = {}
    results = {}

    def analyze_symbol(symbol):
        coin_id = get_cg_id(symbol)
        try:
            url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days=1'
            resp = requests.get(url)
            if resp.status_code != 200:
                return
            ohlc = resp.json()
            closes = [float(item[4]) for item in ohlc]
            window = closes[-50:]
            rsi = calculate_rsi(window)
            macd, macd_signal = calculate_macd(window)
            atr = calculate_atr(ohlc[-50:], period=14)
            support = min(window)
            resistance = max(window)
            price = window[-1]
            ma, bb_upper, bb_lower = calculate_bollinger(window)
            stoch_k, stoch_d = calculate_stochastic(ohlc[-50:])
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            signal = None
            # Tối ưu: nới rộng ngưỡng RSI, chỉ cần 1 điều kiện đúng
            if (
                rsi is not None and rsi < 40
                or (macd is not None and macd > macd_signal)
                or price > resistance
                or (bb_upper is not None and price > bb_upper)
                or (stoch_k is not None and stoch_k < 20)
            ):
                signal = 'LONG'
            elif (
                rsi is not None and rsi > 60
                or (macd is not None and macd < macd_signal)
                or price < support
                or (bb_lower is not None and price < bb_lower)
                or (stoch_k is not None and stoch_k > 80)
            ):
                signal = 'SHORT'
            prev = state.get(symbol, {'side': None})
            # Tự động hóa leverage
            macd_strength = abs(macd - macd_signal) if macd is not None and macd_signal is not None else 0
            price_strength = 0
            if signal == 'LONG' and resistance > 0:
                price_strength = (price - resistance) / resistance
            elif signal == 'SHORT' and support > 0:
                price_strength = (support - price) / support
            if (rsi is not None and (rsi < 25 or rsi > 75)) or macd_strength > 2 or price_strength > 0.02:
                leverage = 125
            elif (rsi is not None and (rsi < 35 or rsi > 65)) or macd_strength > 1 or price_strength > 0.01:
                leverage = 50
            else:
                leverage = 20
            tp_ratio = 2
            sl_ratio = 1
            max_hold_minutes = 60
            chart_image = None
            def make_chart():
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(window, label='Close')
                if ma:
                    ax.plot([ma]*len(window), label='MA')
                if bb_upper and bb_lower:
                    ax.plot([bb_upper]*len(window), label='BB Upper')
                    ax.plot([bb_lower]*len(window), label='BB Lower')
                ax.set_title(f'{symbol} {now}')
                ax.legend()
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                plt.close(fig)
                return buf
            if signal and signal != prev['side']:
                tp = price + tp_ratio * atr if signal == 'LONG' else price - tp_ratio * atr
                sl = price - sl_ratio * atr if signal == 'LONG' else price + sl_ratio * atr
                entry_msg = (
                    f"Tên coin: {symbol}\n"
                    f"Lệnh: {signal} {leverage}x\n"
                    f"Thời điểm vào: {now}\n"
                    f"TP: {tp:,.2f} | SL: {sl:,.2f}\n"
                    f"Vùng hỗ trợ: {support:,.2f} | Vùng kháng cự: {resistance:,.2f}\n"
                    f"Bollinger: MA={ma:,.2f} Upper={bb_upper:,.2f} Lower={bb_lower:,.2f}\n"
                    f"Stochastic: K={stoch_k:.2f} D={stoch_d:.2f}\n"
                    f"Thời điểm ra: ..."
                )
                chart_image = make_chart()
                if symbol in coins:
                    signals_main.append((entry_msg, chart_image))
                else:
                    signals_others.append((entry_msg, chart_image))
                print(entry_msg)
                state[symbol] = {'side': signal, 'entry': price, 'entry_time': now, 'tp': tp, 'sl': sl}
            elif prev['side']:
                exit_reason = None
                if (prev['side'] == 'LONG' and price >= prev['tp']) or (prev['side'] == 'SHORT' and price <= prev['tp']):
                    exit_reason = 'TP hit'
                elif (prev['side'] == 'LONG' and price <= prev['sl']) or (prev['side'] == 'SHORT' and price >= prev['sl']):
                    exit_reason = 'SL hit'
                else:
                    entry_time_struct = time.strptime(prev['entry_time'], '%Y-%m-%d %H:%M:%S')
                    entry_timestamp = time.mktime(entry_time_struct)
                    now_timestamp = time.mktime(time.strptime(now, '%Y-%m-%d %H:%M:%S'))
                    hold_minutes = (now_timestamp - entry_timestamp) / 60
                    if hold_minutes >= max_hold_minutes:
                        exit_reason = 'Max hold time'
                if not signal and exit_reason is None:
                    exit_reason = 'Signal reversed'
                if exit_reason:
                    exit_msg = (
                        f"Tên coin: {symbol}\n"
                        f"Lệnh: {prev['side']} {leverage}x\n"
                        f"Thời điểm vào: {prev['entry_time']}\n"
                        f"Thời điểm ra: {now}\n"
                        f"Lý do thoát: {exit_reason}"
                    )
                    chart_image = make_chart()
                    if symbol in coins:
                        signals_main.append((exit_msg, chart_image))
                    else:
                        signals_others.append((exit_msg, chart_image))
                    print(exit_msg)
                    state[symbol] = {'side': None, 'entry': None, 'entry_time': None, 'tp': None, 'sl': None}
        except Exception as e:
            print(f"{symbol}: Lỗi khi phân tích: {e}")

    threads = []
    for symbol in coins:
        t = threading.Thread(target=analyze_symbol, args=(symbol,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # Gửi tổng hợp tín hiệu đẹp
    if signals_main or signals_others:
        alert_main = "\n====================\n".join([msg for msg, _ in signals_main])
        alert_others = "\n====================\n".join([msg for msg, _ in signals_others])
        msg = f"🔥 Crypto Signals ({time.strftime('%Y-%m-%d %H:%M:%S')}) 🔥\n\n"
        if alert_main:
            msg += "--- COIN CHÍNH ---\n" + alert_main + "\n\n"
        if alert_others:
            msg += "--- COIN RÁC / TRENDING ---\n" + alert_others
        # Gửi từng ảnh chart cho từng tín hiệu
        for entry in signals_main + signals_others:
            send_telegram(entry[0], image=entry[1])
        send_telegram(msg)
        print(f"Sent {len(signals_main) + len(signals_others)} signals to Telegram.")
    else:
        print("No signals to send.")

# --- Scheduler ---
if __name__ == "__main__":

    schedule.every(5).minutes.do(analyze_and_alert)
    while True:
        schedule.run_pending()
        time.sleep(5)
