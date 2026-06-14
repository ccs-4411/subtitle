# 🎬 Whisper 批次字幕工具網頁版 (Whisper Subtitle Generator Web)

一個基於 **Gradio** 與 **Faster-Whisper (Aisegment)** 打造的網頁版批次自動字幕抽取工具。專為快速、輕量化、跨平台需求設計，支援多檔案同時拖曳上傳，自動識別或指定語言，並一鍵打包匯出帶有精確時間軸的 `SRT` 字幕壓縮檔。

---

## ✨ 核心特色

- 🗂️ **批次處理**：支援同時拖曳多個影片或純音訊檔案進行排隊辨識。
- 🌐 **多國語言**：內建「自動偵測」，亦可手動指定 中文、日文、韓文、英文 等多國語言。
- 📦 **打包下載**：所有辨識完成的 `.srt` 檔案會自動壓縮為一個 `ZIP` 檔，方便一鍵下載。
- ☁️ **雲端優化**：相容於 Hugging Face Spaces (免費版 CPU 16GB RAM) 與 Render 等雲端平台。
- ⚡ **高速極佳化**：採用 `faster-whisper` 的 CTranslate2 後端與 `int8` 量化，在 CPU 環境下依然能保持極高的推理速度與低記憶體佔用。

---

## 🛠️ 專案目錄結構

```text
├── app.py               # Gradio 網頁主程式
├── requirements.txt     # 雲端依賴套件清單
└── README.md            # 專案說明文件

如果你想在自己的 Windows / Mac 電腦上開網頁來跑
git clone [https://github.com/你的帳號/你的專案名稱.git](https://github.com/你的帳號/你的專案名稱.git)
cd 你的專案名稱

安裝必要套件
pip install -r requirements.txt
啟動網頁服務
python app.py
啟動後，打開瀏覽器輸入控制台顯示的網址（通常為 http://127.0.0.1:7860）即可開始使用。

🚀 雲端部署指南 (Cloud Deployment)
🥇 推薦：Hugging Face Spaces (全免費)
前往 Hugging Face Spaces 建立一個新的 Space。

SDK 務必選擇 Gradio，硬體選擇 CPU Basic (免費規格)。

透過網頁上的 Add file 功能，直接建立：

app.py：貼入本專案的網頁版原始碼。

requirements.txt：填入依賴套件。

儲存後等待 1~2 分鐘建立（Building）完成，狀態變為 Running 即可上線使用。

💡 小撇步：Hugging Face 免費版具備快取功能，首次熱機載入 Whisper 模型後，未來網站重啟/喚醒皆能秒級讀取模型，體驗極佳。
