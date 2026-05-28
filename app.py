import cv2
import numpy as np
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model
from huggingface_hub import hf_hub_download

# Konfigurasi Halaman
st.set_page_config(page_title="Penerjemah Isyarat Tangan", layout="centered")

# --- TRIK CSS UNTUK KOTAK HIJAU & MIRROR KAMERA ---
st.markdown("""
<style>
[data-testid="stCameraInput"] {
    position: relative;
}

/* 1. Efek Mirror (Invert) untuk video live dan hasil jepretan di browser */
[data-testid="stCameraInput"] video,
[data-testid="stCameraInput"] img {
    transform: scaleX(-1);
}

/* 2. Memperbesar Kotak Panduan Hijau */
[data-testid="stCameraInput"]::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 350px;  /* <-- Ukuran kotak diperbesar */
    height: 350px; /* <-- Ukuran kotak diperbesar */
    border: 4px dashed #00FF00;
    pointer-events: none;
    z-index: 99;
    box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.4);
}
</style>
""", unsafe_allow_html=True)
# -------------------------------------------------

st.title("Penerjemah Bahasa Isyarat (A-Y)")
st.write("Aplikasi ini menggunakan model CNN untuk menebak bahasa isyarat tanganmu!")

# Memuat Model dengan Cache agar cepat
@st.cache_resource
def load_hf_model():
    # PENTING: Jangan lupa ubah ini dengan username Hugging Face kamu
    repo_id = "Exchonsive/cv_sl_maeru" 
    filename = "cv_maeru_sl.h5"
    model_path = hf_hub_download(repo_id=repo_id, filename=filename)
    return load_model(model_path)

model = load_hf_model()

# Instruksi Penggunaan
st.markdown("### 📸 Cara Penggunaan:")
st.info("**Posisikan tanganmu tepat di dalam kotak hijau**, lalu tekan tombol 'Take Photo'. Kamera sudah dibuat seperti cermin agar lebih mudah!")

# Widget Kamera Bawaan Streamlit
camera_image = st.camera_input("Ambil Foto Isyarat Tangan")

if camera_image is not None:
    # Membaca gambar dari widget Streamlit
    image = Image.open(camera_image)
    frame = np.array(image)
    
    # Membalik gambar (mirror) di sisi Python agar sesuai dengan yang dilihat user
    frame = cv2.flip(frame, 1)
    
    # Menghitung koordinat untuk memotong area TEPAT DI TENGAH (Square)
    h, w, c = frame.shape
    # Menyesuaikan rasio potongan dengan kotak CSS yang diperbesar
    box_size = min(h, w) - 40 
    start_x = w // 2 - box_size // 2
    start_y = h // 2 - box_size // 2
    
    # Memotong (Crop) bagian tengah yang berisi tangan
    hand_crop = frame[start_y:start_y+box_size, start_x:start_x+box_size]
    
    # Menggambar kotak hijau tebal di hasil foto sebagai visualisasi area potong
    cv2.rectangle(frame, (start_x, start_y), (start_x+box_size, start_y+box_size), (0, 255, 0), 3)
    
    # Menampilkan gambar yang sudah diproses agar user tahu area mana yang dibaca model
    st.image(frame, caption="Area kotak hijau yang dianalisis oleh Model", use_container_width=True)

    # Pra-pemrosesan
    gray_crop = cv2.cvtColor(hand_crop, cv2.COLOR_RGB2GRAY)
    resized_crop = cv2.resize(gray_crop, (28, 28))
    normalized_crop = resized_crop / 255.0
    
    # Menambahkan dimensi batch
    input_data = np.expand_dims(normalized_crop, axis=[0, -1])
    
    # Inferensi (Prediksi)
    predictions = model.predict(input_data, verbose=0)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions) * 100
    
    # Konversi Index ke Huruf A-Y
    predicted_letter = chr(predicted_class + 65 + (1 if predicted_class >= 9 else 0))
    
    # Menampilkan Hasil
    st.markdown("---")
    st.success(f"## Tebakan Model: Huruf **{predicted_letter}**")
    st.metric(label="Tingkat Keyakinan (Confidence)", value=f"{confidence:.2f}%")