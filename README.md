# Crypto Alert Tool

Tool này phân tích dữ liệu crypto, gửi tín hiệu Long/Short và cảnh báo về Telegram mỗi 3-5 phút.

## Features

- Phân tích dữ liệu nhiều coin (CoinGecko)
- Tín hiệu Long/Short, TP/SL, leverage tự động
- Gửi cảnh báo và chart lên Telegram
- Chạy định kỳ mỗi 3 phút

## Cách chạy code local

1. Cài Python >= 3.8
2. Cài các thư viện:
   ```powershell
   pip install requests schedule matplotlib
   ```
3. Mở file `main.py`, điền token Telegram và chat_id.
4. Chạy script:
   ```powershell
   python main.py
   ```

## Deploy bằng Docker (lần đầu)

1. Cài Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Mở PowerShell tại thư mục dự án, build image:
   ```powershell
   docker build -t crypto-alert .
   ```
3. Chạy container:
   ```powershell
   docker run -d --name crypto-alert crypto-alert
   ```
4. Kiểm tra log:
   ```powershell
   docker logs -f crypto-alert
   ```

## Deploy lại khi update source code

1. Build lại image:
   ```powershell
   docker build -t crypto-alert .
   ```
2. Dừng và xóa container cũ:
   ```powershell
   docker stop crypto-alert
   docker rm crypto-alert
   ```
3. Chạy lại container mới:
   ```powershell
   docker run -d --name crypto-alert crypto-alert
   ```

## Tuỳ chỉnh

Bạn có thể chỉnh sửa logic phân tích trong file `main.py` để phù hợp chiến lược cá nhân.
