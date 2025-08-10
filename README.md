# Crypto Alert Tool

Tool này phân tích dữ liệu crypto từ Binance, tính toán vùng giá vào tối ưu và thời điểm vào lệnh, gửi tín hiệu Long/Short về Telegram mỗi 5 phút.

## 🚀 Features

- **Phân tích kỹ thuật nâng cao**: RSI, MACD, Bollinger Bands, Support/Resistance
- **Tính toán vùng giá vào**: Entry zone với giá vào tối ưu dựa trên volatility và momentum
- **Đánh giá thời điểm vào**: Độ mạnh tín hiệu (0-12 điểm) và mức độ khẩn cấp
- **Chất lượng setup**: Đánh giá XUẤT SẮC/TỐT/KHẤP KHẨM/RỦI RO
- **Risk/Reward ratio**: Tự động tính TP/SL và tỷ lệ lời/lỗ
- **Multi-coin analysis**: 4 coin cố định + 10 coin mới + 20 coin trending
- **Chiến lược vào lệnh**: Market Order/Limit Order với giá cụ thể

## 🔧 Cách chạy code local

1. **Cài Python >= 3.8**
2. **Cài các thư viện:**
   ```powershell
   pip install requests schedule matplotlib numpy talib
   ```
3. **Cấu hình:**
   - Mở file `config.py`
   - Điền `TELEGRAM_TOKEN` và `TELEGRAM_CHAT_ID`
4. **Chạy script:**
   ```powershell
   python main.py
   ```

## 🐳 Deploy bằng Docker (Local)

### Lần đầu tiên:

1. **Cài Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Build image:**
   ```powershell
   docker build -t crypto-alert .
   ```
3. **Chạy container:**
   ```powershell
   docker run -d --name crypto-alert --restart unless-stopped crypto-alert
   ```
4. **Kiểm tra logs:**
   ```powershell
   docker logs -f crypto-alert
   ```

### Update source code:

1. **Build lại image:**
   ```powershell
   docker build -t crypto-alert .
   ```
2. **Dừng và xóa container cũ:**
   ```powershell
   docker stop crypto-alert
   docker rm crypto-alert
   ```
3. **Chạy container mới:**
   ```powershell
   docker run -d --name crypto-alert --restart unless-stopped crypto-alert
   ```

## ☁️ Deploy trên Google Cloud

### 🎯 Phương pháp 1: Google Cloud Run (Khuyến nghị)

#### Setup lần đầu:

1. **Truy cập Cloud Run:**
   ```
   https://console.cloud.google.com/run?project=YOUR_PROJECT_ID
   ```
2. **Click "CREATE SERVICE"**
3. **Deploy from source repository:**
   - Repository: `thanhnhan20298/crypto-alert`
   - Branch: `main`
   - Build type: `Dockerfile`
4. **Configuration:**
   - Memory: 1 GiB
   - CPU: 1
   - Timeout: 3600 seconds
   - Concurrency: 1
   - Max instances: 1
   - Environment: `TZ=Asia/Ho_Chi_Minh`

#### Update code:

1. **Commit và push code mới lên GitHub**
2. **Trong Cloud Run Console:**
   - Click "EDIT & DEPLOY NEW REVISION"
   - Chọn "Deploy from source repository"
   - Giữ nguyên settings và click "DEPLOY"

### 🖥️ Phương pháp 2: Google Cloud VM (Compute Engine)

#### Setup lần đầu:

1. **Tạo VM instance trong Compute Engine**
2. **SSH vào VM và clone repo:**
   ```bash
   git clone https://github.com/thanhnhan20298/crypto-alert.git
   cd crypto-alert
   ```
3. **Cài Docker:**
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```
4. **Logout và login lại SSH, sau đó:**
   ```bash
   docker build -t crypto-alert .
   docker run -d --name crypto-alert --restart unless-stopped crypto-alert
   ```

#### Update code trên VM:

1. **SSH vào VM:**
2. **Pull code mới:**
   ```bash
   cd ~/crypto-alert
   git pull origin main
   ```
3. **Stop và remove container cũ:**
   ```bash
   sudo docker stop crypto-alert 2>/dev/null || true
   sudo docker rm crypto-alert 2>/dev/null || true
   ```
4. **Build và chạy container mới:**
   ```bash
   sudo docker build -t crypto-alert .
   sudo docker run -d --name crypto-alert --restart unless-stopped crypto-alert
   ```
5. **Kiểm tra logs:**
   ```bash
   sudo docker logs -f crypto-alert
   ```

### 🔄 GitHub Actions (Tự động deploy)

Sử dụng file `.github/workflows/deploy.yml` để tự động deploy khi push code:

1. **Setup GitHub Secrets:**

   - `GCP_SA_KEY`: Service Account JSON key
   - `GCP_PROJECT_ID`: Google Cloud Project ID

2. **Sau đó chỉ cần:**
   ```bash
   git add .
   git commit -m "Update crypto bot"
   git push origin main
   ```

## 📊 Thông tin Alert

### Mỗi tín hiệu sẽ bao gồm:

- 🚀 **Tên coin** và **lệnh** (LONG/SHORT + leverage)
- 💰 **Giá hiện tại** và **vùng giá vào** (entry zone)
- ⭐ **Giá vào tối ưu** dựa trên phân tích kỹ thuật
- 📏 **Khoảng cách** từ giá hiện tại đến vùng vào
- 🎯 **Take Profit** và 🛡️ **Stop Loss**
- 📈 **Risk/Reward Ratio** (1:X)
- 🔥 **Độ mạnh tín hiệu** (0-12 điểm)
- 🏅 **Chất lượng setup** (XUẤT SẮC/TỐT/KHẤP KHẨM/RỦI RO)
- ⏰ **Thời điểm vào** và 💡 **chiến lược** (Market/Limit Order)
- 📊 **Support/Resistance, RSI, MACD, Bollinger Bands**

### Ví dụ alert:

```
🚀 Tên coin: BTCUSDT
📊 Lệnh: LONG 10x
💰 Giá hiện tại: 45,250.0000
🎯 Vùng vào: 44,800.0000 - 45,100.0000
⭐ Giá vào tối ưu: 44,920.0000
📏 Khoảng cách: 0.73%
🎯 TP: 46,500.0000 | 🛡️ SL: 44,200.0000
📈 R/R Ratio: 1:2.20
🔥 Độ mạnh tín hiệu: 8/12
🏅 Chất lượng setup: ⭐ TỐT
⏰ Thời điểm vào: ⚡ VÀO NGAY - Tín hiệu rất mạnh
💡 Chiến lược: Limit Order tại giá hiện tại
```

## 🛠️ Troubleshooting

### Lỗi thường gặp:

1. **Docker permission denied:**

   ```bash
   sudo usermod -aG docker $USER
   # Logout và login lại
   ```

2. **Container không start:**

   ```bash
   sudo docker logs crypto-alert
   ```

3. **Không nhận được Telegram alerts:**

   - Kiểm tra `TELEGRAM_TOKEN` và `TELEGRAM_CHAT_ID` trong `config.py`
   - Test bot: `/start` trong chat với bot

4. **API rate limit:**
   - Bot tự động retry với exponential backoff
   - Giảm số lượng coin trong `config.py` nếu cần

### Commands hữu ích:

```bash
# Xem logs realtime
sudo docker logs -f crypto-alert

# Restart bot
sudo docker restart crypto-alert

# Xem container status
sudo docker ps

# Xem resource usage
sudo docker stats crypto-alert
```

## 🔧 Tuỳ chỉnh

### Trong file `config.py`:

- **FIXED_SYMBOLS**: Thêm/bớt coin cố định
- **Timeframe**: Thay đổi khung thời gian phân tích
- **Alert frequency**: Điều chỉnh tần suất gửi alert

### Trong file `main.py`:

- **Threshold values**: Điều chỉnh ngưỡng RSI, MACD
- **Risk management**: Tùy chỉnh TP/SL ratio
- **Signal strength**: Thay đổi cách tính điểm tín hiệu

---

## � Support

- **Issues**: https://github.com/thanhnhan20298/crypto-alert/issues
- **Telegram**: @thanhnhan20298

**⚠️ Lưu ý**: Tool này chỉ hỗ trợ phân tích kỹ thuật, không phải lời khuyên đầu tư. Luôn DYOR trước khi trade!
