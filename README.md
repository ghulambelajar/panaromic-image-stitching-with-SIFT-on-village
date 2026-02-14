# Image Stitching Panorama using SIFT & RANSAC

Proyek Final Project Visi Komputer ini mengimplementasikan algoritma **SIFT (Scale-Invariant Feature Transform)** untuk menggabungkan dua citra lingkungan desa menjadi satu **Panorama** utuh yang mulus (*seamless*).


---

## 📸 Preview Hasil
Berikut adalah visualisasi dari proses deteksi fitur, pencocokan (*matching*), hingga penyatuan gambar (*stitching*).

![Hasil Panorama](results/result.png)

---

## 🚀 Fitur Utama
* **Deteksi Fitur Robust:** Menggunakan SIFT untuk mengenali objek meskipun ada perubahan skala (*zoom*) dan rotasi.
* **Pencocokan Akurat:** Menggunakan *Brute-Force Matcher* dengan filter *Lowe's Ratio Test* (0.75) untuk membuang kecocokan palsu.
* **Koreksi Geometri:** Menggunakan algoritma **RANSAC** untuk estimasi matriks Homografi yang presisi.
* **Smart Stitching:** Teknik *Warp Perspective* dengan perluasan kanvas otomatis agar gambar tidak terpotong.

---

## 🛠️ Cara Menjalankan

1.  **Persiapan Library**
    Pastikan Python sudah terinstall, lalu install *dependency* berikut:
    ```bash
    pip install -r requirements.txt
    ```
  

2.  **Siapkan Gambar**
    Masukkan dua gambar yang ingin digabung ke dalam folder `images/`.
    * `images/desa-1.jpeg`
    * `images/desa-2.jpeg`

3.  **Jalankan Program**
    Buka terminal dan jalankan perintah:
    ```bash
    python panaromic.py
    ```

4.  **Cek Hasil**
    Gambar hasil panorama akan otomatis tersimpan di folder `results/` dengan nama `result.png`.

---

## 📂 Struktur Direktori
```text
.
├── images/             # Folder input citra (desa-1, desa-2)
├── results/            # Folder output hasil panorama
├── panaromic.py        # Source code utama (Main Script)
├── requirements.txt    # Daftar library yang dibutuhkan
└── report.pdf          # Laporan lengkap Final Project
