@ECHO OFF

ECHO 設定網頁首頁的對應本機的位置
cd C:\Users\?\Desktop\python作品

ECHO 若有 ngrok 每次重開務必先進行驗證'('驗證TOKEN與轉換的網址每次相異')'
ECHO 指令如下 見文件內容
::ngrok authtoken <YOUR_AUTH_TOKEN>

ECHO 至網站(如下)用 google 帳戶登入，取得驗證 AUTH_TOKEN
ECHO 網址如下 見文件內容
::https://dashboard.ngrok.com/auth/your-authtoken

ECHO 記得先開啟 ngrok 。指令 ngrok http 8000
ECHO 啟動伺服器，試用連結 localhost:8000
ECHO Ctrl + C 即可關閉
python -m http.server 8000 --bind 127.0.0.1

PAUSE

ECHO finish
