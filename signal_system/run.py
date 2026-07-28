import uvicorn
import subprocess
import sys
import time

if __name__ == "__main__":
    print("Arayüz (Streamlit) ayağa kaldırılıyor...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app/dashboard.py"]
    )

    time.sleep(2)
    print("Arka plan (FastAPI) ayağa kaldırılıyor...")
    try:
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n Sistem kapatılıyor. Arayüz de sonlandırılıyor...")
        # Terminalde Ctrl+C yaparsan, arkada açık kalan Streamlit'i de temizce öldürür
        streamlit_process.terminate()
        streamlit_process.wait()
        print("Sistem başarıyla durduruldu.")