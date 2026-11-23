# Generator UTS Bisnis Intelegent: 7 dataset (CSV + Excel + SQL) kotor, soal per paket, kunci dosen.
# Jalankan: python gen_uts.py   (deterministik, seed tetap per paket)
import random, csv, re, json, sqlite3, os, datetime, zipfile, shutil
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
FN = ["Budi", "Siti", "Andi", "Dewi", "Rizki", "Putri", "Agus", "Rina", "Fajar", "Wulan", "Hendra", "Maya", "Dimas", "Lestari", "Yoga", "Intan", "Eko", "Ratna", "Bayu", "Nadia", "Tono", "Sari", "Arif", "Citra", "Joko", "Anisa", "Gilang", "Mega", "Rudi", "Tika"]
LN = ["Santoso", "Wijaya", "Pratama", "Lestari", "Hidayat", "Saputra", "Nugroho", "Kusuma", "Rahayu", "Wibowo", "Susanto", "Permata", "Setiawan", "Maharani", "Firmansyah", "Anggraini", "Gunawan", "Utami", "Kurniawan", "Syahputra"]
KOTA = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar", "Denpasar", "Semarang", "Yogyakarta"]
KALIAS = {"Jakarta": ["DKI Jakarta", "Jkt"], "Surabaya": ["Sby"], "Bandung": ["Bdg"]}
MET = ["Transfer Bank", "Tunai", "E-Wallet", "Kartu Kredit"]
MVAR = {"Transfer Bank": ["transfer", "TRANSFER BANK", "Transfer  Bank", "Transfer bank "], "Tunai": ["tunai", "Cash", "TUNAI "], "E-Wallet": ["ewallet", "E Wallet", "e-wallet", "Gopay", "OVO"], "Kartu Kredit": ["kartu kredit", "CC", "KARTU KREDIT"]}
STAT = ["Selesai", "Selesai", "Selesai", "Diproses", "Batal"]
SUP = ["CV Sumber Jaya", "PT Nusa Mitra", "UD Berkah Abadi", "PT Karya Mandiri", "CV Maju Bersama"]


def rp(n): return "Rp " + f"{int(round(n)):,}".replace(",", ".")


# ---------------------------------------------------------------- KONFIGURASI 7 PAKET
def D(no, slug, bisnis, cerita, d1, it, cb, fact, start, end, seg, cats, seed):
    return dict(no=no, slug=slug, bisnis=bisnis, cerita=cerita, d1=d1, it=it, cb=cb, fact=fact, start=start, end=end, seg=seg, cats=cats, seed=seed)

PAKET = [
 D(1, "kopikita", "KopiKita", "KopiKita adalah jaringan kedai kopi dengan 5 outlet. Manajemen ingin tahu menu dan outlet mana yang paling menyumbang penjualan, serta bagaimana perilaku belanja member.",
   dict(tbl="member", id="ID_Member", pref="MBR", label="Member"), dict(label="Menu", pref="MNU", kode="Kode_Menu", nama="Nama_Menu", sheet="Menu"),
   dict(label="Outlet", pref="OTL", kode="Kode_Outlet", nama="Nama_Outlet", sheet="Outlet", names=["KopiKita Dago", "KopiKita Braga", "KopiKita Kemang", "KopiKita Tunjungan", "KopiKita Kuta"], tipe=["Mall", "Ruko", "Kampus"]),
   "penjualan", (2025, 1, 1), (2025, 6, 30), ["Reguler", "Gold", "Baru"],
   {"Kopi": [("Espresso", "gelas", 18000), ("Americano", "gelas", 22000), ("Cafe Latte", "gelas", 28000), ("Cappuccino", "gelas", 28000), ("Kopi Susu Gula Aren", "gelas", 24000)],
    "Non-Kopi": [("Matcha Latte", "gelas", 30000), ("Cokelat Panas", "gelas", 26000), ("Teh Lemon", "gelas", 16000), ("Red Velvet Latte", "gelas", 29000), ("Es Jeruk", "gelas", 15000)],
    "Makanan": [("Nasi Goreng Kampung", "porsi", 32000), ("Mie Goreng Spesial", "porsi", 30000), ("Roti Bakar Cokelat", "porsi", 22000), ("Sandwich Ayam", "porsi", 28000), ("Kentang Goreng", "porsi", 20000)],
    "Camilan": [("Pisang Goreng", "porsi", 18000), ("Croissant", "pcs", 21000), ("Brownies", "pcs", 19000), ("Donat Gula", "pcs", 12000), ("Cookies Oat", "pcs", 14000)]}, 1101),
 D(2, "apotek-sehat", "Apotek Sehat Sentosa", "Apotek Sehat Sentosa memiliki 5 cabang. Pemilik ingin mengetahui kategori produk dan cabang yang paling menguntungkan serta pola pembelian pasien.",
   dict(tbl="pasien", id="ID_Pasien", pref="PSN", label="Pasien"), dict(label="Obat", pref="OBT", kode="Kode_Obat", nama="Nama_Obat", sheet="Obat"),
   dict(label="Apotek", pref="APT", kode="Kode_Apotek", nama="Nama_Apotek", sheet="Apotek", names=["Sehat Sentosa Pusat", "Sehat Sentosa Dago", "Sehat Sentosa Kemang", "Sehat Sentosa Darmo", "Sehat Sentosa Sanur"], tipe=["Pusat", "Cabang", "Klinik"]),
   "penjualan", (2025, 2, 1), (2025, 7, 31), ["Umum", "Langganan", "Baru"],
   {"Vitamin": [("Vitamin C 500mg", "strip", 24000), ("Vitamin D3 1000IU", "botol", 68000), ("Multivitamin Dewasa", "botol", 85000), ("Zinc 20mg", "strip", 32000), ("Kalsium Tulang", "botol", 54000)],
    "Obat Bebas": [("Parasetamol 500mg", "strip", 6500), ("Antasida Sirup", "botol", 18000), ("Obat Batuk Herbal", "botol", 21000), ("Salep Luka", "tube", 17500), ("Tetes Mata", "botol", 23000)],
    "Alat Kesehatan": [("Masker Medis 50s", "box", 35000), ("Termometer Digital", "pcs", 45000), ("Tensimeter Digital", "pcs", 320000), ("Hand Sanitizer 100ml", "botol", 15000), ("Plester Luka 10s", "box", 8500)],
    "Perawatan": [("Sabun Antiseptik", "botol", 22000), ("Sunscreen SPF 50", "tube", 76000), ("Pelembap Wajah", "tube", 58000), ("Sampo Anti Ketombe", "botol", 31000), ("Minyak Kayu Putih", "botol", 19000)]}, 2202),
 D(3, "eduplus", "EduPlus Academy", "EduPlus Academy menjual kursus daring lewat 5 kampus mitra. Manajemen ingin mengetahui kursus dan kampus mitra yang paling laku serta tren pendaftaran per bulan.",
   dict(tbl="peserta", id="ID_Peserta", pref="PST", label="Peserta"), dict(label="Kursus", pref="KRS", kode="Kode_Kursus", nama="Nama_Kursus", sheet="Kursus"),
   dict(label="Kampus Mitra", pref="KMP", kode="Kode_Kampus", nama="Nama_Kampus", sheet="Kampus", names=["Politeknik Nusantara", "Universitas Cendekia", "Institut Teknologi Mandala", "Akademi Digital Utama", "Universitas Bina Insani"], tipe=["Negeri", "Swasta", "Politeknik"]),
   "pendaftaran", (2025, 7, 1), (2025, 12, 31), ["Mahasiswa", "Profesional", "Baru"],
   {"Data": [("Dasar Excel untuk Bisnis", "kursi", 350000), ("SQL untuk Pemula", "kursi", 450000), ("Power BI Mahir", "kursi", 750000), ("Python untuk Analisis Data", "kursi", 850000), ("Statistik Bisnis", "kursi", 500000)],
    "Desain": [("Desain Grafis Dasar", "kursi", 400000), ("UI/UX Fundamental", "kursi", 900000), ("Editing Video", "kursi", 650000), ("Fotografi Produk", "kursi", 550000), ("Ilustrasi Digital", "kursi", 700000)],
    "Bisnis": [("Digital Marketing", "kursi", 800000), ("Manajemen Proyek", "kursi", 950000), ("Dasar Akuntansi UMKM", "kursi", 450000), ("Public Speaking", "kursi", 300000), ("Strategi Penjualan", "kursi", 600000)],
    "Bahasa": [("Bahasa Inggris Bisnis", "kursi", 500000), ("Persiapan IELTS", "kursi", 1200000), ("Bahasa Jepang N5", "kursi", 850000), ("Bahasa Mandarin Dasar", "kursi", 750000), ("Menulis Profesional", "kursi", 350000)]}, 3303),
 D(4, "hotelnusa", "Hotel Nusa Group", "Hotel Nusa Group mengelola 5 hotel. Direktur operasional ingin tahu jenis layanan dan hotel yang paling menyumbang pendapatan serta pola reservasi per bulan.",
   dict(tbl="tamu", id="ID_Tamu", pref="TMU", label="Tamu"), dict(label="Layanan", pref="LYN", kode="Kode_Layanan", nama="Nama_Layanan", sheet="Layanan"),
   dict(label="Hotel", pref="HTL", kode="Kode_Hotel", nama="Nama_Hotel", sheet="Hotel", names=["Nusa Bandung", "Nusa Jakarta", "Nusa Yogyakarta", "Nusa Bali", "Nusa Surabaya"], tipe=["Bintang 3", "Bintang 4", "Bintang 5"]),
   "reservasi", (2025, 1, 1), (2025, 6, 30), ["Reguler", "Corporate", "Baru"],
   {"Kamar": [("Kamar Standar", "malam", 450000), ("Kamar Superior", "malam", 600000), ("Kamar Deluxe", "malam", 800000), ("Suite Junior", "malam", 1300000), ("Suite Eksekutif", "malam", 2100000)],
    "Makan": [("Sarapan Prasmanan", "pax", 90000), ("Makan Malam Set", "pax", 175000), ("Paket Afternoon Tea", "pax", 120000), ("Room Service Hemat", "porsi", 85000), ("Paket Barbeque", "pax", 220000)],
    "Spa": [("Pijat Tradisional 60'", "sesi", 250000), ("Aromaterapi 90'", "sesi", 380000), ("Lulur dan Mandi Susu", "sesi", 420000), ("Refleksi Kaki 45'", "sesi", 150000), ("Paket Pasangan", "sesi", 750000)],
    "Ruang Rapat": [("Ruang Rapat Kecil", "hari", 1500000), ("Ruang Rapat Sedang", "hari", 2800000), ("Ballroom Setengah Hari", "hari", 6500000), ("Paket Coffee Break", "pax", 65000), ("Sewa Proyektor", "hari", 350000)]}, 4404),
 D(5, "fashionku", "FashionKu", "FashionKu adalah toko fashion daring dengan 5 gudang. Tim merchandising ingin mengetahui kategori produk dan gudang pemenuhan pesanan yang paling berkontribusi pada penjualan.",
   dict(tbl="pembeli", id="ID_Pembeli", pref="PMB", label="Pembeli"), dict(label="Produk", pref="SKU", kode="Kode_SKU", nama="Nama_Produk", sheet="Produk"),
   dict(label="Gudang", pref="GDG", kode="Kode_Gudang", nama="Nama_Gudang", sheet="Gudang", names=["Gudang Jakarta Pusat", "Gudang Bandung Timur", "Gudang Surabaya Barat", "Gudang Medan Kota", "Gudang Makassar"], tipe=["Pusat", "Regional", "Mitra"]),
   "pesanan", (2025, 3, 1), (2025, 8, 31), ["Reguler", "VIP", "Baru"],
   {"Atasan": [("Kaos Polos Katun", "pcs", 65000), ("Kemeja Flanel", "pcs", 145000), ("Blouse Satin", "pcs", 125000), ("Hoodie Fleece", "pcs", 185000), ("Kemeja Batik Modern", "pcs", 160000)],
    "Bawahan": [("Celana Jeans Slim", "pcs", 210000), ("Celana Chino", "pcs", 175000), ("Rok Plisket", "pcs", 115000), ("Celana Kulot", "pcs", 130000), ("Celana Training", "pcs", 95000)],
    "Sepatu": [("Sneakers Putih", "pasang", 325000), ("Sandal Jepit Premium", "pasang", 89000), ("Sepatu Lari Ringan", "pasang", 395000), ("Flatshoes Wanita", "pasang", 155000), ("Sepatu Kulit Formal", "pasang", 450000)],
    "Aksesori": [("Topi Baseball", "pcs", 55000), ("Tas Selempang", "pcs", 135000), ("Ikat Pinggang Kulit", "pcs", 85000), ("Kacamata Hitam", "pcs", 99000), ("Dompet Lipat", "pcs", 75000)]}, 5505),
 D(6, "kirimcepat", "KirimCepat Express", "KirimCepat Express adalah perusahaan logistik dengan 5 hub pemilahan. Manajer operasional ingin tahu layanan dan hub yang paling banyak menghasilkan pendapatan pengiriman.",
   dict(tbl="pengirim", id="ID_Pengirim", pref="PGR", label="Pengirim"), dict(label="Layanan", pref="LYN", kode="Kode_Layanan", nama="Nama_Layanan", sheet="Layanan"),
   dict(label="Hub", pref="HUB", kode="Kode_Hub", nama="Nama_Hub", sheet="Hub", names=["Hub Jakarta Timur", "Hub Bandung Kota", "Hub Surabaya Utara", "Hub Medan Barat", "Hub Makassar"], tipe=["Utama", "Satelit", "Transit"]),
   "pengiriman", (2025, 4, 1), (2025, 9, 30), ["Reguler", "Bisnis", "Baru"],
   {"Reguler": [("Reguler Dalam Kota", "paket", 9000), ("Reguler Antar Kota", "paket", 14000), ("Reguler Antar Pulau", "paket", 28000), ("Reguler Hemat", "paket", 8000), ("Reguler Sehari Tiba", "paket", 16000)],
    "Ekspres": [("Ekspres Same Day", "paket", 35000), ("Ekspres Next Day", "paket", 22000), ("Ekspres Pagi", "paket", 30000), ("Ekspres Antar Pulau", "paket", 48000), ("Ekspres Dokumen", "paket", 18000)],
    "Kargo": [("Kargo Darat per 10kg", "koli", 45000), ("Kargo Udara per 10kg", "koli", 125000), ("Kargo Laut per 10kg", "koli", 32000), ("Kargo Pindahan Rumah", "koli", 350000), ("Kargo Barang Besar", "koli", 220000)],
    "Instan": [("Kurir Instan 3 Jam", "paket", 26000), ("Kurir Motor Kota", "paket", 20000), ("Kurir Mobil Box", "paket", 75000), ("Kurir Makanan Beku", "paket", 38000), ("Kurir Malam Hari", "paket", 32000)]}, 6606),
 D(7, "cinekita", "CineKita Cinema", "CineKita Cinema mengoperasikan 5 bioskop. Manajemen ingin mengetahui jenis produk dan bioskop yang paling menyumbang pendapatan, termasuk penjualan tiket dibanding makanan dan minuman.",
   dict(tbl="anggota", id="ID_Anggota", pref="ANG", label="Anggota"), dict(label="Produk", pref="PRD", kode="Kode_Produk", nama="Nama_Produk", sheet="Produk"),
   dict(label="Bioskop", pref="BSK", kode="Kode_Bioskop", nama="Nama_Bioskop", sheet="Bioskop", names=["CineKita Grand Indonesia", "CineKita Paris Van Java", "CineKita Tunjungan Plaza", "CineKita Sun Plaza", "CineKita Beachwalk"], tipe=["Reguler", "Premier", "Mini"]),
   "penjualan_tiket", (2025, 5, 1), (2025, 10, 31), ["Reguler", "Platinum", "Baru"],
   {"Tiket": [("Tiket Reguler Weekday", "lembar", 40000), ("Tiket Reguler Weekend", "lembar", 55000), ("Tiket Premier", "lembar", 90000), ("Tiket Anak", "lembar", 30000), ("Tiket Sweetbox", "lembar", 130000)],
    "Popcorn": [("Popcorn Asin Kecil", "pcs", 35000), ("Popcorn Asin Besar", "pcs", 52000), ("Popcorn Karamel Kecil", "pcs", 40000), ("Popcorn Karamel Besar", "pcs", 58000), ("Popcorn Mix Jumbo", "pcs", 68000)],
    "Minuman": [("Cola Medium", "gelas", 24000), ("Cola Large", "gelas", 30000), ("Air Mineral", "botol", 12000), ("Teh Dingin", "gelas", 20000), ("Kopi Dingin", "gelas", 28000)],
    "Paket Combo": [("Combo Berdua", "paket", 110000), ("Combo Keluarga", "paket", 195000), ("Combo Hemat Solo", "paket", 65000), ("Combo Premier", "paket", 150000), ("Combo Anak", "paket", 75000)]}, 7707),
]


# ---------------------------------------------------------------- UTIL
def d_iso(d): return d.isoformat()
def d_slash(d): return d.strftime("%d/%m/%Y")
def d_dash(d): return d.strftime("%d-%m-%Y")
def d_id(d): return f"{d.day} {BULAN[d.month-1]} {d.year}"


def q(v):
    if v is None: return "NULL"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def nid(s, w):
    m = re.match(r"^([A-Za-z]{3})-?(\d+)$", s.strip())
    return f"{m.group(1).upper()}-{int(m.group(2)):0{w}d}"


def build(P):
    R = random.Random(P["seed"])
    K = {}
    def cnt(k, n=1): K[k] = K.get(k, 0) + n
    def rdate(a, b): return a + datetime.timedelta(days=R.randint(0, (b - a).days))
    d1, it, cb = P["d1"], P["it"], P["cb"]
    start, end = datetime.date(*P["start"]), datetime.date(*P["end"])
    no = f"{P['no']:02d}"
    name = f"dataset-{no}-{P['slug']}"
    out = os.path.join(ROOT, "dataset", name)
    kunci = os.path.join(ROOT, "kunci-dosen", name)
    os.makedirs(out, exist_ok=True); os.makedirs(kunci, exist_ok=True)
    f_d1 = f"{d1['tbl']}_{P['slug'].replace('-', '_')}.csv"
    f_xl = f"{it['sheet'].lower()}_{cb['sheet'].lower()}_{P['slug'].replace('-', '_')}.xlsx"
    f_sql = f"{P['fact']}_{P['slug'].replace('-', '_')}.sql"
    f_csv = f"{P['fact']}_{P['slug'].replace('-', '_')}_cadangan.csv"
    db = P["slug"].replace("-", "_")

    # ---- Dimensi 1 (CSV)
    N1 = 100
    cust, used = [], set()
    for i in range(1, N1 + 1):
        while True:
            n = f"{R.choice(FN)} {R.choice(LN)}"
            if n not in used: used.add(n); break
        em = n.lower().replace(" ", ".") + "@" + R.choice(["gmail.com", "yahoo.com", "outlook.com"])
        hp = "08" + R.choice(["12", "13", "21", "52", "57", "78", "81", "95"]) + "".join(R.choice("0123456789") for _ in range(8))
        cust.append(dict(ID=f"{d1['pref']}-{i:04d}", Nama=n, Kota=R.choice(KOTA), Email=em, HP=hp, Tgl=rdate(datetime.date(2024, 1, 1), start - datetime.timedelta(days=1)), Seg=R.choice(P["seg"])))

    def fmt_hp(hp):
        r = R.random()
        if r < .10: return f"{hp[:4]}-{hp[4:8]}-{hp[8:]}", "hp_format"
        if r < .20: return f"+62 {hp[1:4]} {hp[4:8]} {hp[8:]}", "hp_format"
        if r < .28: return "62" + hp[1:], "hp_format"
        if r < .34: return hp[1:], "hp_format"
        if r < .37: return "", "hp_kosong"
        return hp, None

    def dirty_cust(c):
        nama = c["Nama"]; r = R.random()
        if r < .15: nama = nama.upper(); cnt("d1_nama_huruf")
        elif r < .27: nama = nama.lower(); cnt("d1_nama_huruf")
        if R.random() < .12: nama = R.choice([" ", "  "]) + nama + R.choice([" ", "  "]); cnt("d1_nama_spasi")
        kota = c["Kota"]; r = R.random()
        if r < .08: kota = kota.lower(); cnt("d1_kota_variasi")
        elif r < .14: kota = kota.upper(); cnt("d1_kota_variasi")
        elif r < .22: kota = kota + " "; cnt("d1_kota_variasi")
        elif r < .27 and kota in KALIAS: kota = R.choice(KALIAS[kota]); cnt("d1_kota_alias")
        em = c["Email"]; r = R.random()
        if r < .08: em = em.upper(); cnt("d1_email_huruf")
        elif r < .13: em = ""; cnt("d1_email_kosong")
        elif r < .17: em = em.replace("@", ""); cnt("d1_email_tanpa_at")
        elif r < .23: em = " " + em + " "; cnt("d1_email_spasi")
        hp, tag = fmt_hp(c["HP"])
        if tag: cnt("d1_" + tag)
        d = c["Tgl"]; r = R.random()
        if r < .50: tg = d_iso(d)
        elif r < .75: tg = d_slash(d); cnt("d1_tgl_slash")
        elif r < .90: tg = d_id(d); cnt("d1_tgl_teks")
        else: tg = d_dash(d); cnt("d1_tgl_strip")
        seg = c["Seg"]; r = R.random()
        if r < .08: seg = ""; cnt("d1_segmen_kosong")
        elif r < .18: seg = seg.lower() if R.random() < .5 else seg.upper(); cnt("d1_segmen_huruf")
        return [c["ID"], nama, kota, em, hp, tg, seg]

    rows = [dirty_cust(c) for c in cust]
    for i in sorted(R.sample(range(len(rows)), 5), reverse=True): rows.insert(i + 1, list(rows[i]))
    cnt("d1_duplikat", 5)
    with open(os.path.join(out, f_d1), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([d1["id"], "Nama", "Kota", "Email", "No_HP", "Tanggal_Daftar", "Segmen"]); w.writerows(rows)
    K["d1_baris_file"] = len(rows); K["d1_baris_bersih"] = N1

    # ---- Item (Excel sheet 1) + Cabang (sheet 2)
    items = []
    for kat, lst in P["cats"].items():
        for n, s, h in lst: items.append(dict(Nama=n, Kat=kat, Sat=s, Harga=h))
    for i, p in enumerate(items, 1):
        p["Kode"] = f"{it['pref']}-{i:03d}"; p["Sup"] = R.choice(SUP); p["Stok"] = R.randint(8, 400); p["Aktif"] = R.random() < .88
    blank_idx = set(R.sample(range(len(items)), 2))
    irows = []
    for i, p in enumerate(items):
        kode = p["Kode"]; r = R.random()
        if r < .10: kode = kode.lower(); cnt("it_kode_huruf")
        elif r < .18: kode = " " + kode + " "; cnt("it_kode_spasi")
        nama = p["Nama"]
        if R.random() < .10: nama = nama.upper(); cnt("it_nama_huruf")
        kat = p["Kat"]; r = R.random()
        if r < .12: kat = kat.lower(); cnt("it_kat_variasi")
        elif r < .20: kat = kat.upper() + " "; cnt("it_kat_variasi")
        elif r < .26: kat = " " + kat; cnt("it_kat_variasi")
        harga = p["Harga"]
        if i in blank_idx: harga = None; cnt("it_harga_kosong")
        elif R.random() < .30: harga = "Rp " + f"{p['Harga']:,}".replace(",", "."); cnt("it_harga_teks")
        stok = p["Stok"]; r = R.random()
        if r < .08: stok = -R.randint(1, 5); cnt("it_stok_negatif")
        elif r < .14: stok = None; cnt("it_stok_kosong")
        elif r < .18: stok = "habis"; cnt("it_stok_teks")
        ak = "Ya" if p["Aktif"] else "Tidak"
        if R.random() < .45:
            ak = {"Ya": R.choice(["Y", "ya", "TRUE", "Aktif"]), "Tidak": R.choice(["N", "tidak", "FALSE", "Nonaktif"])}[ak]; cnt("it_aktif_variasi")
        irows.append([kode, nama, kat, harga, p["Sat"], p["Sup"], stok, ak])
    for i in sorted(R.sample(range(len(irows)), 2), reverse=True): irows.insert(i + 1, list(irows[i]))
    cnt("it_duplikat", 2)

    cabs = []
    cities = R.sample(KOTA, len(cb["names"]))
    for i, (n, c) in enumerate(zip(cb["names"], cities), 1):
        cabs.append(dict(Kode=f"{cb['pref']}-{i:02d}", Nama=n, Kota=c, Mgr=f"{R.choice(FN)} {R.choice(LN)}", Tipe=R.choice(cb["tipe"])))
    crows = []
    for c in cabs:
        kode = c["Kode"]; r = R.random()
        if r < .20: kode = kode.lower(); cnt("cb_kode_huruf")
        elif r < .40: kode = " " + kode + " "; cnt("cb_kode_spasi")
        kota = c["Kota"]; r = R.random()
        if r < .25: kota = kota.upper(); cnt("cb_kota_variasi")
        elif r < .45: kota = kota.lower() + " "; cnt("cb_kota_variasi")
        crows.append([kode, c["Nama"], kota, c["Mgr"], c["Tipe"]])
    crows.insert(2, list(crows[1])); cnt("cb_duplikat", 1)

    wb = Workbook(); ws = wb.active; ws.title = it["sheet"]
    ws["A1"] = f"DAFTAR {it['label'].upper()} {P['bisnis'].upper()}"; ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = "Diperbarui: akhir periode oleh bagian pusat"; ws.append([])
    ws.append([it["kode"], it["nama"], "Kategori", "Harga", "Satuan", "Pemasok", "Stok", "Aktif"])
    for c in ws[4]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0B5A7A")
    for r in irows: ws.append(r)
    ws.append([]); ws.append([f"Total: {len(irows)} baris"])
    for col, wd in zip("ABCDEFGH", [14, 30, 14, 14, 9, 20, 8, 10]): ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet(cb["sheet"])
    ws2.append([cb["kode"], cb["nama"], "Kota", "Manajer", "Tipe"])
    for c in ws2[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0B5A7A")
    for r in crows: ws2.append(r)
    for col, wd in zip("ABCDE", [14, 30, 14, 22, 12]): ws2.column_dimensions[col].width = wd
    ws3 = wb.create_sheet("Catatan")
    ws3["A1"] = "Catatan admin. Bukan data master."; ws3["A2"] = "Harga kosong berarti belum diisi pemasok."
    try:
        wb.save(os.path.join(out, f_xl))
    except PermissionError:
        print('PERINGATAN: Excel terkunci, dilewati (isi sama karena seed tetap):', f_xl)
    K["it_baris_file"] = len(irows); K["it_baris_bersih"] = len(items); K["cb_baris_file"] = len(crows); K["cb_baris_bersih"] = len(cabs)

    # ---- Fakta (SQL)
    price = {p["Kode"]: p["Harga"] for p in items}
    blank_codes = {items[i]["Kode"] for i in blank_idx}
    N = 400
    oc = set(R.sample(range(N), 8)); oi = set(R.sample([i for i in range(N) if i not in oc], 5))
    trx = []
    for i in range(N):
        pid = f"{d1['pref']}-{R.randint(1, N1):04d}"; kode = items[R.randrange(len(items))]["Kode"]
        if i in oc: pid = f"{d1['pref']}-{R.randint(N1 + 1, N1 + 10):04d}"
        if i in oi: kode = f"{it['pref']}-{R.randint(len(items) + 1, len(items) + 5):03d}"
        qty = R.choices(range(1, 11), weights=[18, 18, 14, 12, 10, 8, 6, 5, 5, 4])[0]
        trx.append(dict(Tgl=rdate(start, end), PID=pid, Kode=kode, Cab=R.choice(cabs)["Kode"], Qty=qty, Harga=price.get(kode, R.choice([9000, 12500, 25000, 40000])),
                        Disc=R.choice([0, 0, 0, 5, 10, 15]), Met=R.choice(MET), Stat=R.choice(STAT)))
    trx.sort(key=lambda t: t["Tgl"])
    for i, t in enumerate(trx, 1): t["ID"] = f"TRX-{i:05d}"
    cnt("f_orphan_d1", len(oc)); cnt("f_orphan_item", len(oi))

    def dirty_id(s):
        r = R.random()
        if r < .12: return s.lower(), "huruf"
        if r < .22: return " " + s + " ", "spasi"
        if r < .28: return s.replace("-", ""), "tanpa_strip"
        return s, None

    frows = []
    for t in trx:
        pid, g1 = dirty_id(t["PID"]); kode, g2 = dirty_id(t["Kode"]); cab, g3 = dirty_id(t["Cab"])
        if g1: cnt("f_d1_" + g1)
        if g2: cnt("f_item_" + g2)
        if g3: cnt("f_cb_" + g3)
        r = R.random(); d = t["Tgl"]
        if r < .60: tg = d_iso(d)
        elif r < .85: tg = d_slash(d); cnt("f_tgl_slash")
        else: tg = d_dash(d); cnt("f_tgl_strip")
        qty = t["Qty"]; r = R.random(); fl = None
        if r < .04: qty = None; fl = "kosong"
        elif r < .06: qty = -qty; fl = "tidak_wajar"
        elif r < .07: qty = 0; fl = "tidak_wajar"
        elif r < .085: qty = qty * 100; fl = "tidak_wajar"
        if fl: cnt("f_qty_" + fl)
        harga = t["Harga"]
        if R.random() < .06 and t["Kode"] in price and t["Kode"] not in blank_codes: harga = None; cnt("f_harga_null")
        disc = t["Disc"]; r = R.random()
        if r < .45: ds = R.choice([f"{disc}%", f"{disc} %", f"{disc}"]); cnt("f_diskon_format")
        elif r < .50: ds = ""; cnt("f_diskon_kosong"); disc = 0
        else: ds = f"{disc}%"
        met = t["Met"]
        if R.random() < .35: met = R.choice(MVAR[met]); cnt("f_metode_variasi")
        st = t["Stat"]; r = R.random()
        if r < .10: st = st.lower(); cnt("f_status_variasi")
        elif r < .16: st = st.upper() + " "; cnt("f_status_variasi")
        elif r < .19: st = None; cnt("f_status_null")
        frows.append(dict(ID=t["ID"], Tgl=tg, PID=pid, Kode=kode, Cab=cab, Qty=qty, Harga=harga, Disc=ds, Met=met, Stat=st))
    for i in sorted(R.sample(range(len(frows)), 10), reverse=True): frows.insert(i + 1, dict(frows[i]))
    cnt("f_duplikat", 10)
    K["f_baris_file"] = len(frows); K["f_baris_bersih"] = N

    cols = ["ID_Transaksi", "Tanggal_Transaksi", d1["id"], it["kode"], cb["kode"], "Qty", "Harga_Satuan", "Diskon", "Metode_Bayar", "Status"]
    sql = [f"-- {P['bisnis']} | Tabel {P['fact']} (data mentah, belum dibersihkan)", "-- Dialek MySQL / MariaDB.",
           f"CREATE DATABASE IF NOT EXISTS {db} CHARACTER SET utf8mb4;", f"USE {db};", f"DROP TABLE IF EXISTS {P['fact']};",
           f"CREATE TABLE {P['fact']} (\n  ID_Transaksi      VARCHAR(12),\n  Tanggal_Transaksi VARCHAR(20),\n  {d1['id']:<17} VARCHAR(14),\n  {it['kode']:<17} VARCHAR(14),\n  {cb['kode']:<17} VARCHAR(14),\n  Qty               INT NULL,\n  Harga_Satuan      DECIMAL(14,2) NULL,\n  Diskon            VARCHAR(8),\n  Metode_Bayar      VARCHAR(30),\n  Status            VARCHAR(15) NULL\n);", ""]
    vals = [f"({q(r['ID'])},{q(r['Tgl'])},{q(r['PID'])},{q(r['Kode'])},{q(r['Cab'])},{q(r['Qty'])},{q(None if r['Harga'] is None else float(r['Harga']))},{q(r['Disc'])},{q(r['Met'])},{q(r['Stat'])})" for r in frows]
    sql.append(f"INSERT INTO {P['fact']} VALUES\n" + ",\n".join(vals) + ";")
    sql += ["", f"SELECT COUNT(*) AS jumlah_baris FROM {P['fact']};"]
    txt = "\n".join(sql) + "\n"
    open(os.path.join(out, f_sql), "w", encoding="utf-8").write(txt)
    s2 = re.sub(r"CREATE DATABASE.*?;\n|USE .*?;\n|SELECT COUNT.*", "", txt).replace("CHARACTER SET utf8mb4", "")
    con = sqlite3.connect(":memory:"); con.executescript(s2)
    assert con.execute(f"select count(*) from {P['fact']}").fetchone()[0] == len(frows)
    with open(os.path.join(out, f_csv), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cols)
        for r in frows: w.writerow([r["ID"], r["Tgl"], r["PID"], r["Kode"], r["Cab"], "" if r["Qty"] is None else r["Qty"], "" if r["Harga"] is None else r["Harga"], r["Disc"], r["Met"], "" if r["Stat"] is None else r["Stat"]])

    # ---- Verifikasi: bersihkan dengan aturan baku
    seen, uniq = set(), []
    for r in frows:
        if r["ID"] in seen: continue
        seen.add(r["ID"]); uniq.append(r)
    K["f_baris_setelah_dedup"] = len(uniq)
    valid_c = {c["ID"] for c in cust}; valid_i = set(price); valid_b = {c["Kode"] for c in cabs}
    K["f_orphan_d1_akhir"] = sum(1 for r in uniq if nid(r["PID"], 4) not in valid_c)
    K["f_orphan_item_akhir"] = sum(1 for r in uniq if nid(r["Kode"], 3) not in valid_i)
    kat_of = {p["Kode"]: p["Kat"] for p in items}; nm_of = {p["Kode"]: p["Nama"] for p in items}; cb_nm = {c["Kode"]: c["Nama"] for c in cabs}
    tot, used_rows = 0, 0
    per_kat, per_cb, per_bln, per_item, buyers = {}, {}, {}, {}, set()
    excl = {"qty": 0, "batal": 0}; clean = []
    for r in uniq:
        kode = nid(r["Kode"], 3); pid = nid(r["PID"], 4); cab = nid(r["Cab"], 2)
        stt = (r["Stat"] or "Tidak Diketahui").strip().title()
        dd_s = r["Disc"].replace("%", "").strip(); dd = int(dd_s) if dd_s else 0
        h = r["Harga"] if r["Harga"] is not None else price[kode]
        tg = r["Tgl"]
        if "-" in tg and tg[4] == "-": dt = datetime.date.fromisoformat(tg)
        else: dt = datetime.datetime.strptime(tg.replace("-", "/"), "%d/%m/%Y").date()
        ok = not (r["Qty"] is None or r["Qty"] <= 0 or r["Qty"] > 50)
        net = (r["Qty"] * float(h) * (1 - dd / 100)) if ok else None
        met = next(m for m in MET if r["Met"] and (r["Met"] in MVAR[m] or r["Met"] == m)) if True else None
        clean.append([r["ID"], dt.isoformat(), pid if pid in valid_c else "UNK", kode if kode in valid_i else "UNK", cab, r["Qty"] if r["Qty"] is not None else "", h, dd, met, stt, "OK" if ok else "Qty Tidak Valid", round(net) if net is not None else ""])
        if not ok: excl["qty"] += 1; continue
        if stt == "Batal": excl["batal"] += 1; continue
        tot += net; used_rows += 1
        kat = kat_of.get(kode, "Tidak Terdaftar"); per_kat[kat] = per_kat.get(kat, 0) + net
        per_cb[cb_nm[cab]] = per_cb.get(cb_nm[cab], 0) + net
        per_bln[dt.strftime("%Y-%m")] = per_bln.get(dt.strftime("%Y-%m"), 0) + net
        nm = nm_of.get(kode, "Tidak Terdaftar"); per_item[nm] = per_item.get(nm, 0) + net
        buyers.add(pid)
    K["total_bersih"] = round(tot); K["baris_dihitung"] = used_rows; K["dikecualikan"] = excl
    K["rata2_nilai"] = round(tot / used_rows)
    K["per_kategori"] = {k: round(v) for k, v in sorted(per_kat.items(), key=lambda x: -x[1])}
    K["per_cabang"] = {k: round(v) for k, v in sorted(per_cb.items(), key=lambda x: -x[1])}
    K["per_bulan"] = {k: round(v) for k, v in sorted(per_bln.items())}
    ranked = sorted((kv for kv in per_item.items() if kv[0] != "Tidak Terdaftar"), key=lambda x: -x[1])
    K["top5_item"] = [(k, round(v)) for k, v in ranked[:5]]
    K["pelanggan_pembeli_unik"] = len([b for b in buyers if b != "UNK"])
    K["blank_codes"] = sorted(blank_codes)
    K["tanggal_min"] = d_iso(start); K["tanggal_max"] = d_iso(end); K["hari_kalender"] = (end - start).days + 1
    K["tgl_data_min"] = min(c[1] for c in clean); K["tgl_data_max"] = max(c[1] for c in clean)
    K["tgl_data_hari"] = (datetime.date.fromisoformat(K["tgl_data_max"]) - datetime.date.fromisoformat(K["tgl_data_min"])).days + 1

    # ---- Berkas kunci (bersih)
    with open(os.path.join(kunci, "fact_bersih.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["ID_Transaksi", "Tanggal", d1["id"], it["kode"], cb["kode"], "Qty", "Harga_Satuan", "Diskon_Persen", "Metode_Bayar", "Status", "Status_Kualitas", "Nilai_Bersih"]); w.writerows(clean)
    for fn, hdr, data in [
        (f"dim_{d1['tbl']}_bersih.csv", [d1["id"], "Nama", "Kota", "Email", "No_HP", "Tanggal_Daftar", "Segmen"], [[c["ID"], c["Nama"], c["Kota"], c["Email"], c["HP"], c["Tgl"].isoformat(), c["Seg"]] for c in cust]),
        (f"dim_{it['sheet'].lower()}_bersih.csv", [it["kode"], it["nama"], "Kategori", "Harga", "Satuan", "Pemasok", "Aktif"], [[p["Kode"], p["Nama"], p["Kat"], "" if p["Kode"] in blank_codes else p["Harga"], p["Sat"], p["Sup"], "Ya" if p["Aktif"] else "Tidak"] for p in items]),
        (f"dim_{cb['sheet'].lower()}_bersih.csv", [cb["kode"], cb["nama"], "Kota", "Manajer", "Tipe"], [[c["Kode"], c["Nama"], c["Kota"], c["Mgr"], c["Tipe"]] for c in cabs])]:
        with open(os.path.join(kunci, fn), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(hdr); w.writerows(data)
    K["_file"] = dict(d1=f_d1, xl=f_xl, sql=f_sql, csv=f_csv, db=db)
    K["_inv"] = dict(
        d1_hp_kota=sum(1 for c in cust if c["Kota"] in KALIAS), n_items=len(items), n_cat=len(P["cats"]))
    return K, name, out


# ---------------------------------------------------------------- SOAL
def soal(P, K):
    d1, it, cb, fact = P["d1"], P["it"], P["cb"], P["fact"]
    F = K["_file"]; no = f"{P['no']:02d}"
    mulai = f"{BULAN[P['start'][1]-1]} {P['start'][0]}"; selesai = f"{BULAN[P['end'][1]-1]} {P['end'][0]}"
    dim_d1, dim_it, dim_cb = f"Dim_{d1['label']}", f"Dim_{it['label']}", f"Dim_{cb['label'].replace(' ', '')}"
    fct = f"Fact_{fact.title().replace('_', '')}"
    return f"""# UJIAN TENGAH SEMESTER: BISNIS INTELEGENT

**Paket {no}: {P['bisnis']}**

| | |
|---|---|
| Mata kuliah | Bisnis Intelegent (materi Pertemuan 1 sampai 7) |
| Waktu | 120 menit |
| Sifat | Praktik, kerja berpasangan, buka catatan |
| Perangkat | Power BI Desktop, MySQL/MariaDB (atau berkas CSV cadangan), draw.io atau alat gambar lain |
| Anggota | Mahasiswa 1 (Varian A): ............................ NIM: ............ <br> Mahasiswa 2 (Varian B): ............................ NIM: ............ |

Setiap pasangan mendapat **dataset yang berbeda** dari pasangan lain. Angka hasil Anda tidak akan sama dengan pasangan lain, jadi jangan menyalin. Bagian A, B, C dikerjakan berdua. Bagian D dijawab perorangan sesuai varian masing-masing. Seluruh jawaban, termasuk Bagian D kedua mahasiswa, dikumpulkan dalam **satu laporan PDF per pasangan**.

---

## Skenario

{P['cerita']}

Data mentah datang dari tiga sumber yang berbeda dan belum bersih. Tugas Anda: **mengekstrak, mentransformasi, dan memuat** data tersebut, lalu **merancang dan membangun star schema** yang siap dipakai untuk analisis. Periode data: **{mulai} sampai {selesai}**.

## Berkas yang diberikan

| Berkas | Sumber | Isi |
|---|---|---|
| `{F['d1']}` | CSV | Master {d1['label'].lower()} (kolom `{d1['id']}`, Nama, Kota, Email, No_HP, Tanggal_Daftar, Segmen) |
| `{F['xl']}` | Excel | Sheet `{it['sheet']}` (master {it['label'].lower()}, judul dan header tidak di baris 1), sheet `{cb['sheet']}` (master {cb['label'].lower()}), sheet `Catatan` (bukan data) |
| `{F['sql']}` | Database MySQL | Tabel `{fact}` pada database `{F['db']}`: tabel transaksi. Kolom: ID_Transaksi, Tanggal_Transaksi, {d1['id']}, {it['kode']}, {cb['kode']}, Qty, Harga_Satuan, Diskon, Metode_Bayar, Status |
| `{F['csv']}` | CSV | Salinan isi tabel `{fact}`, **hanya dipakai bila MySQL tidak bisa dijalankan** (nilai Extract dikurangi, lihat A1) |

Hubungan antar data: `{fact}.{d1['id']}` ke master {d1['label'].lower()}, `{fact}.{it['kode']}` ke master {it['label'].lower()}, `{fact}.{cb['kode']}` ke master {cb['label'].lower()}. Kunci di tabel transaksi sengaja kotor sehingga relasi gagal sebelum dibersihkan.

---

## BAGIAN A. ETL (35 poin)

### A1. Extract (8 poin)
1. Muat ketiga sumber ke Power BI Desktop: CSV, sheet Excel `{it['sheet']}` dan `{cb['sheet']}`, serta tabel `{fact}` dari MySQL (jalankan `{F['sql']}` lebih dulu). Sheet `Catatan` tidak dimuat.
2. Catat jumlah baris **sesuai sumber** sebelum dibersihkan pada tabel berikut.

| Tabel | Baris di sumber | Catatan |
|---|---|---|
| {d1['label']} | | |
| {it['label']} (data saja, tanpa judul/total) | | |
| {cb['label']} | | |
| {fact} | | harus sama dengan `SELECT COUNT(*)` |

Jika memakai berkas CSV cadangan, nilai A1 poin 1 dikurangi 2 poin dan tuliskan alasannya.

### A2. Transform (20 poin)
Terapkan **semua aturan baku** berikut di Power Query. Setiap langkah harus tercatat di Applied Steps dan diberi nama yang jelas. Aturan ini sama untuk seluruh paket supaya hasil bisa dinilai adil.

**Tabel {d1['label']}**
- T1. Hapus duplikat persis; hapus spasi di tepi dan spasi ganda di dalam teks.
- T2. `Nama`: Capitalize Each Word. `Kota`: rapikan huruf dan spasi, alias `Jkt` dan `DKI Jakarta` menjadi `Jakarta`, `Sby` menjadi `Surabaya`, `Bdg` menjadi `Bandung`.
- T3. `Email`: huruf kecil. Email tanpa tanda `@` dianggap tidak valid, ganti menjadi null.
- T4. `No_HP`: seragamkan menjadi 12 digit berawalan `08` tanpa tanda baca (`+62`, `62`, atau tanpa angka 0 di depan diperbaiki). Kosong dibiarkan null.
- T5. `Tanggal_Daftar`: ubah ke tipe Date. Ada format `yyyy-MM-dd`, `dd/MM/yyyy`, `dd-MM-yyyy`, dan teks Indonesia seperti `21 Juni 2024`. Hati-hati dengan locale.
- T6. `Segmen`: rapikan huruf; kosong diisi `Tidak Diketahui`.

**Tabel {it['label']} dan {cb['label']}**
- T7. {it['label']}: buang baris judul, baris kosong, dan baris `Total`; naikkan header. Kode: hapus spasi dan huruf besar. Kategori dan nama: rapikan huruf dan spasi. Harga bertuliskan `Rp 12.500` diubah menjadi angka; harga yang kosong dibiarkan null. Stok negatif, kosong, atau bertuliskan `habis` diganti null. `Aktif`: seragamkan menjadi `Ya` atau `Tidak` (Y, ya, TRUE, Aktif sama dengan Ya; N, tidak, FALSE, Nonaktif sama dengan Tidak). Hapus duplikat.
- T8. {cb['label']}: kode huruf besar tanpa spasi tepi, kota dirapikan, duplikat dihapus.

**Tabel {fact}**
- T9. Hapus baris dengan `ID_Transaksi` yang sama (duplikat persis).
- T10. Seragamkan semua kunci (`{d1['id']}`, `{it['kode']}`, `{cb['kode']}`): hapus spasi tepi, huruf besar, dan kembalikan tanda hubung bila hilang (contoh `{d1['pref'].lower()}0045` menjadi `{d1['pref']}-0045`).
- T11. `Tanggal_Transaksi` menjadi tipe Date (tiga format campur).
- T12. `Qty` kosong, nol, negatif, atau lebih dari 50 dianggap tidak valid: **baris tetap disimpan**, tetapi beri kolom `Status_Kualitas` bernilai `OK` atau `Qty Tidak Valid`.
- T13. `Harga_Satuan` yang null diisi dari harga {it['label'].lower()} pada master (setelah dibersihkan).
- T14. `Diskon` (`10%`, `10 %`, `10`, kosong) menjadi angka persen; kosong dihitung 0.
- T15. `Metode_Bayar` diseragamkan menjadi 4 nilai: `Transfer Bank`, `Tunai`, `E-Wallet`, `Kartu Kredit`.
- T16. `Status`: rapikan huruf (Selesai, Diproses, Batal); null menjadi `Tidak Diketahui`.
- T17. Tambah kolom `Nilai_Bersih = Qty x Harga_Satuan x (1 - Diskon)`.
- T18. Kunci pada transaksi yang **tidak punya pasangan** di master ({d1['label'].lower()} dan {it['label'].lower()} tidak terdaftar) **tidak boleh dihapus**. Tambahkan baris `Tidak Terdaftar` dengan kunci `UNK` pada dimensi terkait dan arahkan kuncinya ke sana.

Selain membersihkan data, buat **Tabel A2 (tabel temuan masalah)** di laporan. Catat minimal 10 masalah kualitas data yang berbeda, dengan kolom: jenis masalah, kolom yang terdampak, jumlah baris terdampak, dan langkah perbaikan yang Anda lakukan.

### A3. Load (7 poin)
1. Muat hasil akhir ke model: tabel dimensi bersih dan satu tabel fakta bersih. Tabel mentah/staging **tidak dimuat** ke model (nonaktifkan *Enable load*).
2. Lengkapi **tabel rekonsiliasi** berikut dan jelaskan selisihnya.

| Tabel | Baris sumber (A1) | Baris setelah bersih | Selisih dan penyebab |
|---|---|---|---|
| {d1['label']} | | | |
| {it['label']} | | | |
| {cb['label']} | | | |
| {fact} | | | |

---

## BAGIAN B. STAR SCHEMA (30 poin)

### B1. Rancangan di atas kertas (10 poin)
Sebelum membangun model di Power BI, rancang dulu di laporan Anda. Ada tiga bagian.

**1. Proses bisnis dan grain (3 poin).** Jawab dengan dua kalimat pendek:
- *Proses bisnis*: kejadian apa yang dicatat oleh tabel fakta `{fct}`?
- *Grain*: satu baris di tabel fakta mewakili apa? (Contoh bentuk jawaban: "satu baris = satu ...")

**2. Klasifikasi kolom (5 poin).** Buat tabel berisi **semua kolom** dari tabel transaksi, ditambah kolom `Nilai_Bersih` yang Anda hitung sendiri. Golongkan tiap kolom ke salah satu jenis berikut:
- **Kunci**: pengenal yang menghubungkan fakta dengan dimensi.
- **Ukuran (measure)**: angka yang bisa dijumlahkan atau dirata-ratakan.
- **Atribut dimensi**: keterangan untuk mengelompokkan atau memfilter, seperti kota, kategori, nama bulan.

Tulis juga tabel asalnya: `{fct}` atau salah satu dimensi. Contoh baris yang sudah terisi (lengkapi sisanya):

| Kolom | Jenis | Tabel asal |
|---|---|---|
| `ID_Transaksi` | Kunci | `{fct}` |
| `{d1['id']}` | Kunci | `{fct}` dan `{dim_d1}` |
| `Qty` | Ukuran | `{fct}` |
| `Nilai_Bersih` | Ukuran (hasil hitung: Qty x Harga_Satuan x (1 - Diskon)) | `{fct}` |
| `Kota` | Atribut dimensi | `{dim_d1}` |
| ... | ... | ... |

**3. Dimensi dan kunci utamanya (2 poin).** Tulis keempat tabel dimensi yang akan Anda bangun, dan untuk masing-masing sebutkan **kolom kunci utamanya** (kolom yang nilainya unik dan tidak ada yang sama). Isi tabel berikut:

| Tabel dimensi | Kunci utama |
|---|---|
| `{dim_d1}` | ... |
| `{dim_it}` | ... |
| `{dim_cb}` | ... |
| `Dim_Tanggal` | ... |

### B2. Implementasi (12 poin)
1. Bangun star schema di Model view dengan satu fakta `{fct}` dan empat dimensi: `{dim_d1}`, `{dim_it}`, `{dim_cb}`, dan **`Dim_Tanggal` buatan Anda sendiri**.
2. `Dim_Tanggal` harus menutup seluruh rentang tanggal transaksi tanpa celah, memuat minimal kolom: Tanggal, Tahun, Nomor Bulan, Nama Bulan, Kuartal, Hari dalam Minggu. Urutkan Nama Bulan berdasarkan Nomor Bulan.
3. Atur relasi **One-to-Many** dari tiap dimensi ke fakta, arah filter tunggal, hanya satu relasi aktif per pasangan tabel. Semua kunci dimensi harus unik.
4. Buktikan model bekerja: tabel visual lintas tabel (Kategori, Nama Bulan, Total Nilai Bersih) dan jumlahnya cocok dengan total tanpa filter.

### B3. Dokumentasi dan analisis (8 poin)
1. Gambarkan diagram star schema (tabel, kolom kunci, kardinalitas) di draw.io atau tangkapan layar Model view yang rapi.
2. Jelaskan dalam 3 sampai 5 kalimat: mengapa bentuk bintang dipilih dibanding satu tabel datar (flat) atau snowflake untuk data ini.
3. Jelaskan bagaimana Anda memperlakukan kunci yatim (baris `UNK`) dan apa dampaknya bila baris itu dihapus.

---

## BAGIAN C. VALIDASI DAN LAPORAN (20 poin)

### C1. Measure (8 poin)
Buat measure berikut pada tabel khusus `_Measures` (atau di fakta) dengan format yang benar, dan hanya menghitung baris `Status_Kualitas = OK` dengan `Status` bukan `Batal`:
1. `Total Penjualan Bersih`
2. `Jumlah Transaksi`
3. `Rata-rata Nilai Transaksi` (gunakan `DIVIDE`)
4. `Kontribusi Kategori %` (nilai kategori terhadap total, tetap benar saat difilter)

### C2. Halaman laporan (8 poin)
Buat satu halaman laporan berisi: 4 kartu (3 measure di atas dan jumlah {d1['label'].lower()} yang bertransaksi), minimal 3 visual yang tepat (tren per bulan, perbandingan per {cb['label'].lower()}, 5 {it['label'].lower()} teratas), dan slicer Kategori. Judul visual harus berupa pesan, bukan nama field.

### C3. Angka validasi (4 poin)
Tuliskan hasil akhir Anda:

| Pertanyaan | Jawaban Anda |
|---|---|
| Total Penjualan Bersih (Rp) | |
| Jumlah transaksi yang dihitung | |
| Rata-rata nilai transaksi (Rp) | |
| Jumlah baris fakta setelah bersih | |
| {cb['label']} dengan penjualan tertinggi | |
| Bulan dengan penjualan tertinggi | |
| Jumlah hari pada `Dim_Tanggal` | |

---

## BAGIAN D. PERTANYAAN KONSEP, PERORANGAN DALAM SATU LAPORAN (15 poin)

Jawab singkat (3 sampai 6 kalimat per soal) memakai contoh dari dataset Anda. Tulis jawaban di bagian akhir laporan PDF yang sama, dengan sub-judul nama masing-masing mahasiswa. Mahasiswa 1 menjawab **Varian A**, Mahasiswa 2 menjawab **Varian B**.

**Varian A**
1. (5) Mengapa analisis sebaiknya tidak dijalankan langsung pada database transaksi (OLTP), dan apa peran ETL di antaranya?
2. (5) Mengapa kunci yang tidak seragam (huruf, spasi, tanda hubung) menggagalkan relasi? Tunjukkan contoh dari data Anda.
3. (5) Jelaskan perbedaan *measure* dan *calculated column* dan pilih mana untuk `Nilai_Bersih` dan `Total Penjualan Bersih`. Berikan alasan.

**Varian B**
1. (5) Apa beda tabel fakta dan tabel dimensi? Klasifikasikan 3 kolom dari dataset Anda dan beri alasan.
2. (5) Apa yang terjadi pada hasil jumlah jika relasi dimensi ke fakta bersifat Many-to-Many atau dimensi memiliki kunci duplikat? Berikan contoh.
3. (5) Sebutkan dua risiko menghapus baris dengan Qty tidak valid dibanding menandainya lewat `Status_Kualitas`.

---

## Yang dikumpulkan
1. Berkas `.pbix` (nama: `UTS_Paket{no}_NIM1_NIM2.pbix`).
2. Laporan `.pdf` berisi: Tabel A1, Tabel A2 (temuan masalah), Tabel A3, jawaban B1 dan B3, diagram star schema, tangkapan layar halaman laporan, tabel angka validasi C3, dan jawaban Bagian D kedua mahasiswa (Varian A dan Varian B, masing-masing diberi nama penjawabnya).

## Rubrik ringkas

| Bagian | Poin | Penilaian utama |
|---|---|---|
| A. ETL | 35 | Extract tiga sumber, kelengkapan dan kebenaran 18 aturan, rekonsiliasi baris |
| B. Star schema | 30 | Grain dan klasifikasi, relasi dan kardinalitas benar, Dim_Tanggal lengkap, diagram dan alasan |
| C. Validasi | 20 | Measure, halaman laporan, kecocokan angka dengan kunci |
| D. Konsep | 15 | Ketepatan konsep dan contoh dari dataset sendiri |
| **Total** | **100** | |
"""


def kunci_md(allP):
    L = ["# Kunci Dosen: UTS Bisnis Intelegent (7 Paket)", "", "Dokumen ini khusus dosen. Jangan dibagikan ke mahasiswa.", "",
         "## Ringkasan paket", "", "| Paket | Bisnis | Berkas mahasiswa |", "|---|---|---|"]
    for P, K, name in allP:
        L.append(f"| {P['no']:02d} | {P['bisnis']} | `publik/paket-mahasiswa/{name}.zip` |")
    L += ["", "Setiap zip berisi: soal (`soal-uts.html`), CSV master, Excel (item + cabang), SQL transaksi, dan CSV cadangan transaksi. Berkas bersih per paket ada di `kunci-dosen/dataset-XX-.../` (fact_bersih.csv dan tiga dimensi bersih).", "",
          "## Aturan hitung (sama untuk semua paket)", "",
          "- Hapus duplikat berdasarkan `ID_Transaksi`; seragamkan kunci; tanggal ke Date.",
          "- `Qty` kosong, nol, negatif atau lebih dari 50 diberi `Status_Kualitas = Qty Tidak Valid` (baris tetap di fakta, tidak dihitung). Qty tidak valid dicek lebih dulu, baru `Batal`, jadi dua kelompok itu tidak tumpang tindih.",
          "- `Harga_Satuan` null diisi dari harga master. Diskon kosong = 0. `Nilai_Bersih = Qty x Harga x (1 - Diskon)`.",
          "- Dihitung bila `Status_Kualitas = OK` dan Status bukan `Batal`. Status null menjadi `Tidak Diketahui` dan **tetap dihitung**.",
          "- Kunci yatim tidak dihapus; dipetakan ke baris `UNK` (Tidak Terdaftar).",
          "- Dua harga master dikosongkan sengaja; transaksi untuk keduanya tidak pernah bernilai null, jadi tidak memengaruhi total.", "",
          "## Rancangan star schema acuan (semua paket)", "",
          "Grain: satu baris transaksi (`ID_Transaksi`). Fakta: tanggal, kunci tiga dimensi, Qty, Harga_Satuan, Diskon, Metode_Bayar, Status, Status_Kualitas, Nilai_Bersih. Metode_Bayar dan Status boleh tetap di fakta sebagai degenerate attribute atau dipindah ke dimensi kecil (keduanya diterima).",
          "", "| Tabel | Kunci | Relasi |", "|---|---|---|",
          "| Fact | `ID_Transaksi` | fakta, sisi Many |", "| Dim pelanggan | ID unik | 1 ke Many |", "| Dim item (Kode, Nama, Kategori, Harga, Satuan, Pemasok, Aktif) | Kode unik | 1 ke Many |", "| Dim cabang | Kode unik | 1 ke Many |", "| Dim_Tanggal | Tanggal | 1 ke Many |",
          "", "Kesalahan umum: kategori dipisah menjadi tabel sendiri (snowflake) tanpa alasan, relasi Many-to-Many, Dim_Tanggal diambil dari tanggal transaksi saja (berlubang), kunci belum seragam sehingga relasi kosong, menghapus kunci yatim.", "",
          "Penilaian Dim_Tanggal: bila mahasiswa membuat dari tanggal pertama sampai terakhir **di data transaksi** (bukan kalender penuh periode), jumlah harinya mengikuti angka (hari antara tanggal transaksi pertama dan terakhir) pada tiap paket; keduanya diterima asal tanpa celah.", ""]
    for P, K, name in allP:
        d1, it, cb = P["d1"], P["it"], P["cb"]
        L += ["---", "", f"## Paket {P['no']:02d}: {P['bisnis']}", "",
              f"Database `{K['_file']['db']}`, tabel `{P['fact']}`. Periode {K['tanggal_min']} sampai {K['tanggal_max']} (kalender penuh {K['hari_kalender']} hari; hari antara tanggal transaksi pertama dan terakhir: {K['tgl_data_hari']}).", "",
              "### Jumlah baris (A1, A3)", "", "| Tabel | Baris di file | Duplikat | Baris bersih |", "|---|---|---|---|",
              f"| {d1['label']} (CSV) | {K['d1_baris_file']} | {K.get('d1_duplikat',0)} | {K['d1_baris_bersih']} |",
              f"| {it['label']} (Excel, data saja) | {K['it_baris_file']} | {K.get('it_duplikat',0)} | {K['it_baris_bersih']} |",
              f"| {cb['label']} (Excel) | {K['cb_baris_file']} | {K.get('cb_duplikat',0)} | {K['cb_baris_bersih']} |",
              f"| {P['fact']} (SQL) | {K['f_baris_file']} | {K.get('f_duplikat',0)} | {K['f_baris_setelah_dedup']} |", "",
              f"Kunci yatim setelah dibersihkan: {d1['label'].lower()} tak terdaftar **{K['f_orphan_d1_akhir']}** baris, {it['label'].lower()} tak terdaftar **{K['f_orphan_item_akhir']}** baris. Harga kosong di master: `{', '.join(K['blank_codes'])}`.", "",
              "### Angka validasi (C3)", "", "| Ukuran | Nilai |", "|---|---|",
              f"| **Total Penjualan Bersih** | **{rp(K['total_bersih'])}** |", f"| Jumlah transaksi dihitung | {K['baris_dihitung']} |", f"| Rata-rata nilai transaksi | {rp(K['rata2_nilai'])} |",
              f"| Baris fakta setelah bersih | {K['f_baris_setelah_dedup']} |", f"| Dikecualikan karena Qty tidak valid | {K['dikecualikan']['qty']} |", f"| Dikecualikan karena Batal | {K['dikecualikan']['batal']} |",
              f"| {d1['label']} unik yang bertransaksi | {K['pelanggan_pembeli_unik']} |",
              f"| {cb['label']} tertinggi | {next(iter(K['per_cabang']))} ({rp(next(iter(K['per_cabang'].values())))}) |",
              f"| Bulan tertinggi | {max(K['per_bulan'], key=K['per_bulan'].get)} ({rp(max(K['per_bulan'].values()))}) |", "",
              "Per kategori:", "", "| Kategori | Total |", "|---|---|"] + [f"| {k} | {rp(v)} |" for k, v in K["per_kategori"].items()] + [
              "", f"Per {cb['label'].lower()}:", "", f"| {cb['label']} | Total |", "|---|---|"] + [f"| {k} | {rp(v)} |" for k, v in K["per_cabang"].items()] + [
              "", "Per bulan:", "", "| Bulan | Total |", "|---|---|"] + [f"| {k} | {rp(v)} |" for k, v in K["per_bulan"].items()] + [
              "", "5 teratas:", "", "| Nama | Total |", "|---|---|"] + [f"| {k} | {rp(v)} |" for k, v in K["top5_item"]] + [
              "", "### Masalah yang ditanam", "", "| Kode | Jumlah |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in sorted(K.items()) if re.match(r"^(d1|it|cb|f)_(?!baris)", k) and isinstance(v, int) and k not in ("f_orphan_d1_akhir", "f_orphan_item_akhir")] + [""]
    L += ["---", "", "## Kunci Bagian D (ringkas)", "",
          "**Varian A.** (1) OLTP dioptimalkan untuk transaksi harian; query analitik berat menurunkan kinerja dan struktur ter-normalisasi menyulitkan analisis. ETL menarik, membersihkan, dan memuat data ke wadah analitik terpisah. (2) Relasi mencocokkan nilai persis; `mbr0045`, ` MBR-0045 `, dan `MBR-0045` dianggap kunci berbeda sehingga baris fakta tidak menemukan pasangan. (3) Calculated column dihitung per baris saat refresh dan disimpan (cocok untuk `Nilai_Bersih`, atau dihitung di Power Query); measure dihitung saat query sesuai konteks filter (wajib untuk `Total Penjualan Bersih`, agar dinamis terhadap slicer).",
          "",
          "**Varian B.** (1) Fakta berisi peristiwa terukur (Qty, Nilai_Bersih); dimensi berisi konteks (Kategori, Kota, Nama Bulan). (2) Nilai terhitung ganda karena satu kunci cocok ke banyak baris dimensi, sehingga total membesar dan filter ambigu. (3) Menghapus kehilangan jejak audit dan mengubah jumlah transaksi/rata-rata tanpa kontrol; baris yang dihapus tidak dapat dipulihkan atau ditelusuri; menandai memungkinkan analisis kualitas data dan aturan bisa diubah.", ""]
    return "\n".join(L)


from md2html import md2html

def main():
    allP = []
    pk = os.path.join(ROOT, "publik", "paket-mahasiswa")
    os.makedirs(pk, exist_ok=True)
    for P in PAKET:
        K, name, out = build(P)
        open(os.path.join(out, "soal-uts.html"), "w", encoding="utf-8").write(md2html(soal(P, K), f"UTS Bisnis Intelegent - Paket {P['no']:02d} {P['bisnis']}"))
        zp = os.path.join(pk, name + ".zip")
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for fn in sorted(f for f in os.listdir(out) if not f.startswith('~$')): z.write(os.path.join(out, fn), f"{name}/{fn}")
        allP.append((P, K, name))
    open(os.path.join(ROOT, "kunci-dosen", "kunci-jawaban-uts.md"), "w", encoding="utf-8").write(kunci_md(allP))
    json.dump({n: {k: v for k, v in K.items() if not k.startswith("_")} for P, K, n in allP}, open(os.path.join(HERE, "key_uts.json"), "w"), indent=1, ensure_ascii=False)
    for P, K, n in allP:
        print(n, "| trx", K["f_baris_file"], "->", K["f_baris_setelah_dedup"], "| total", rp(K["total_bersih"]), "| dihitung", K["baris_dihitung"], K["dikecualikan"], "| yatim", K["f_orphan_d1_akhir"], K["f_orphan_item_akhir"])


if __name__ == "__main__":
    main()
