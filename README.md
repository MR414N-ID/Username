<div align="center">

<img src="assets/banner.svg" alt="Username Finder by MR414N-ID" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Termux-Ready-000000?style=for-the-badge&logo=android&logoColor=3DDC84)
![Linux](https://img.shields.io/badge/Linux-Supported-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Sites](https://img.shields.io/badge/Situs-200%2B-ff79c6?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-50fa7b?style=for-the-badge)

**Cari satu username di 200+ situs dan media sosial sekaligus, langsung dari terminal.**

</div>

---

## ✨ Fitur

- 🔎 Mengecek **200+ situs** (media sosial, developer, game, musik, marketplace, dll.)
- ⚡ Cepat, memakai **30 thread** paralel
- 🎯 Hasil jelas: `[sukses]` + link profil, atau `[gagal]`
- 🛡️ Anti hasil palsu: dites ulang dengan username acak untuk membuang situs yang selalu membalas "ada"
- 💾 Link yang ditemukan otomatis tersimpan ke `hasil_<username>.txt`
- 🎨 Tampilan terminal berwarna dengan banner Tux ala Linux
- 📱 Ramah **Termux** (layar sempit otomatis menyesuaikan)

## 🖼️ Tampilan

<div align="center">
  <img src="assets/preview.svg" alt="Contoh tampilan" width="700"/>
  <br/>
  <sub>Contoh tampilan (data hanya ilustrasi)</sub>
</div>

## 📦 Instalasi

### Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/USERNAME_KAMU/NAMA_REPO.git
cd NAMA_REPO
pip install -r requirements.txt
```

### Linux / macOS / Windows

```bash
git clone https://github.com/USERNAME_KAMU/NAMA_REPO.git
cd NAMA_REPO
pip install -r requirements.txt
```

> Ganti `USERNAME_KAMU` dan `NAMA_REPO` dengan akun dan nama repo GitHub kamu.

## 🚀 Cara Pakai

```bash
python username.py
```

Lalu ketik username yang ingin dicari:

```
[?] Masukkan username >> mayor_tedy
```

Atau langsung lewat argumen:

```bash
python username.py mayor_tedy
```

Contoh hasil:

```
[sukses] tiktok: https://www.tiktok.com/@mayor_tedy
[gagal] github
[sukses] instagram: https://www.instagram.com/mayor_tedy/

Selesai: 2 ditemukan dari 202 situs.
Link tersimpan di hasil_mayor_tedy.txt
```

## ➕ Menambah Situs

Buka `username.py`, lalu tambahkan satu baris di dalam `SITES_TEXT` dengan format:

```
namasitus https://contoh.com/{u}
```

`{u}` akan diganti otomatis dengan username yang dicari.

## ⚠️ Catatan

- Situs yang memuat halaman lewat JavaScript atau memblokir bot (misalnya Instagram, Facebook, LinkedIn) bisa memberi hasil kurang akurat.
- Pola URL situs bisa berubah sewaktu-waktu. Kalau ada yang meleset, silakan buat *issue* atau *pull request*.

## ⚖️ Disclaimer

Tools ini dibuat untuk keperluan **OSINT yang sah dan edukasi**, misalnya mengecek jejak username milik sendiri atau riset keamanan yang diizinkan. Penulis tidak bertanggung jawab atas penyalahgunaan, termasuk pelacakan, pelecehan, atau penguntitan. Gunakan dengan bijak dan patuhi hukum serta aturan setiap situs.

## 👤 Author

<div align="center">

**BY. MR414N-ID**

⭐ Kalau berguna, kasih bintang di repo ini ya!

</div>
