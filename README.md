# Handweapon Mini Game (OpenCV-Based)

Proyek ini adalah mini game interaktif berbasis visi komputer yang mensimulasikan mekanisme permainan tebas (seperti Fruit Ninja). Game ini dikembangkan menggunakan Python dengan library OpenCV dan NumPy tanpa menggunakan game engine eksternal.

## Fitur Utama
* **Hand Detection:** Deteksi tangan secara real-time menggunakan teknik *Skin Color Masking* pada ruang warna HSV.
* **Image Morphology:** Pembersihan noise data mask menggunakan operasi manual Opening (Erosi & Dilasi).
* **Gesture Tracking:** Mengikuti posisi telapak tangan (palm) menggunakan *Image Moments*.
* **Score System:** Sistem kalkulasi skor berdasarkan interaksi senjata dengan objek musuh.
