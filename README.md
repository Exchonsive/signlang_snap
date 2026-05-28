# signlang_snapshot

## Deskripsi

`signlang_snapshot` adalah aplikasi penerjemah bahasa isyarat yang menggunakan kamera untuk menangkap snapshot tangan dan mendeteksi huruf bahasa isyarat dari gambar tersebut. Aplikasi ini dirancang untuk memproses satu frame snapshot dari kamera, bukan streaming video langsung.

## Fitur

- Deteksi bahasa isyarat dari snapshot kamera
- Visualisasi titik sendi tangan menggunakan MediaPipe
- Pengenalan huruf bahasa isyarat A-Y
- Tampilkan huruf prediksi dan tingkat kepercayaan
- Mudah dijalankan lewat Streamlit

## Struktur Proyek

- `app.py`: kode utama aplikasi Streamlit
- `requirements.txt`: daftar paket Python yang dibutuhkan

## Persyaratan

- Python 3.10+ (direkomendasikan)
- Kamera web aktif dan dapat diakses oleh aplikasi
- Koneksi internet untuk mengunduh model dari Hugging Face pada pertama kali dijalankan

## Instalasi

1. Buat virtual environment, lalu aktifkan:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Pasang dependensi:

```bash
pip install -r requirements.txt
```

## Cara Menjalankan

```bash
streamlit run app.py
```

Buka URL yang ditampilkan di terminal (biasanya `http://localhost:8501`).

## Penggunaan

1. Buka aplikasi di browser.
2. Centang kotak `Mulai / Matikan Kamera`.
3. Tunjukkan tangan Anda ke kamera dan tunggu snapshot diproses.
4. Aplikasi akan mendeteksi huruf bahasa isyarat dari snapshot tersebut dan menampilkan hasil prediksi beserta confidence score.

## Catatan

- Model saat ini mendukung huruf A sampai Y.
- Jika kamera tidak terdeteksi, pastikan izin kamera diberikan dan perangkat kamera terhubung.
- Snapshot kamera dapat diproses satu per satu, bukan streaming video penuh.
- Model diunduh dari Hugging Face: `Exchonsive/cv_sl_maeru`.

## Lisensi

Proyek ini dibuat sebagai portofolio dan dapat dikembangkan lebih lanjut untuk mendukung lebih banyak gesture atau terjemahan frase.
