import os
import shutil
import zipfile
import gradio as gr
from faster_whisper import WhisperModel

# 初始化 Whisper 模型（在伺服器端載入）
# device="cpu" 確保在 Hugging Face Spaces 免費版硬體上穩定執行
MODEL = WhisperModel("base", device="cpu", compute_type="int8")

def format_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"

def save_srt(segments, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg.start)
            end = format_time(seg.end)
            text = seg.text.strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def process_videos(video_files, selected_lang, progress=gr.Progress()):
    if not video_files:
        return "請至少上傳一個影片或音訊檔案。", None

    # 建立臨時工作目錄
    output_dir = "whisper_outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    srt_files = []
    total_files = len(video_files)

    # 批量處理
    for idx, video_path in enumerate(video_files):
        # 取得原始檔名
        base_name = os.path.basename(video_path)
        name_without_ext = os.path.splitext(base_name)[0]
        srt_path = os.path.join(output_dir, f"{name_without_ext}.srt")

        # 更新網頁進度條 (Gradio 內建功能，會即時顯示在網頁上)
        progress(idx / total_files, desc=f"正在處理 ({idx+1}/{total_files}): {base_name}")

        # Faster-Whisper 直接讀取上傳的影片/音訊檔案
        if selected_lang == "auto":
            segments, _ = MODEL.transcribe(video_path)
        else:
            segments, _ = MODEL.transcribe(video_path, language=selected_lang, task="transcribe")

        save_srt(segments, srt_path)
        srt_files.append(srt_path)

    # 將所有生好的 SRT 打包成 ZIP
    zip_path = "subtitles_output.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for srt in srt_files:
            zipf.write(srt, os.path.basename(srt))

    return f"成功處理完成 {total_files} 個檔案！", zip_path

# 建立 Web UI 介面
with gr.Blocks(title="Whisper 批次字幕工具網頁版") as demo:
    gr.Markdown("# 🎬 Whisper 批次字幕工具網頁版")
    gr.Markdown("上傳影片或純音訊檔，AI 將自動為您抽取並生成 SRT 字幕檔案。")
    
    with gr.Row():
        with gr.Column():
            # 檔案上傳組件 (支援多檔案、拖曳，並限定影片與音訊格式)
            file_input = gr.File(
                label="請上傳影片/音訊 (可多選拖曳)", 
                file_count="multiple", 
                type="filepath",
                file_types=["video", "audio"]
            )
            
            # 語言選擇單選鈕
            lang_input = gr.Radio(
                label="選擇影片語言",
                choices=[
                    ("自動偵測", "auto"),
                    ("中文", "zh"),
                    ("日文", "ja"),
                    ("韓文", "ko"),
                    ("英文", "en"),
                    ("法文", "fr"),
                    ("德文", "de"),
                ],
                value="zh"
            )
            
            start_btn = gr.Button("🚀 開始批次辨識", variant="primary")
            
        with gr.Column():
            status_output = gr.Textbox(label="執行狀態", value="等待上傳檔案...")
            # 下載組件 (處理完會把 ZIP 丟到這裡讓使用者點擊下載)
            download_output = gr.File(label="下載字幕壓縮檔 (ZIP)")

    # 綁定按鈕點擊事件
    start_btn.click(
        fn=process_videos,
        inputs=[file_input, lang_input],
        outputs=[status_output, download_output]
    )

if __name__ == "__main__":
    # server_name="0.0.0.0" 允許雲端外網連入，並將主題載入移至 launch 中
    demo.launch(server_name="0.0.0.0", theme=gr.themes.Soft())
