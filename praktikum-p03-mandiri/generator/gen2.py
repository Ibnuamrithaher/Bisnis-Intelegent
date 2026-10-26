import random, csv, re, json, sqlite3, os, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
R = random.Random(303)
OUT = r"c:/Users/TUF GAMING/OneDrive/Desktop/Bisnis Intelegent/praktikum-p03-mandiri/data"
K = {}


def cnt(k, n=1):
    K[k] = K.get(k, 0) + n


BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


def d_iso(d): return d.isoformat()
def d_slash(d): return d.strftime("%d/%m/%Y")
def d_dash(d): return d.strftime("%d-%m-%Y")
def d_id(d): return f"{d.day} {BULAN[d.month-1]} {d.year}"
def rdate(a, b): return a + datetime.timedelta(days=R.randint(0, (b - a).days))


# ---------------- PELANGGAN (CSV) ----------------
FN = ["Budi", "Siti", "Andi", "Dewi", "Rizki", "Putri", "Agus", "Rina", "Fajar", "Wulan", "Hendra", "Maya", "Dimas", "Lestari", "Yoga", "Intan", "Eko", "Ratna", "Bayu", "Nadia", "Tono", "Sari", "Arif", "Citra", "Joko", "Anisa", "Gilang", "Mega", "Rudi", "Tika"]
LN = ["Santoso", "Wijaya", "Pratama", "Lestari", "Hidayat", "Saputra", "Nugroho", "Kusuma", "Rahayu", "Wibowo", "Susanto", "Permata", "Setiawan", "Maharani", "Firmansyah", "Anggraini", "Gunawan", "Utami", "Kurniawan", "Syahputra"]
KOTA = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar", "Denpasar", "Semarang", "Yogyakarta"]
KALIAS = {"Jakarta": ["DKI Jakarta", "Jkt"], "Surabaya": ["Sby"], "Bandung": ["Bdg"]}
SEG = ["Reguler", "Premium", "Baru"]
cust = []
used = set()
for i in range(1, 121):
    while True:
        n = f"{R.choice(FN)} {R.choice(LN)}"
        if n not in used:
            used.add(n)
            break
    em = n.lower().replace(" ", ".") + "@" + R.choice(["gmail.com", "yahoo.com", "outlook.com"])
    hp = "08" + R.choice(["12", "13", "21", "52", "57", "78", "81", "95"]) + "".join(R.choice("0123456789") for _ in range(8))
    cust.append(dict(ID=f"PLG-{i:04d}", Nama=n, Kota=R.choice(KOTA), Email=em, HP=hp, Tgl=rdate(datetime.date(2024, 1, 1), datetime.date(2025, 6, 30)), Seg=R.choice(SEG)))


def fmt_hp(hp):
    r = R.random()
    if r < .10: return f"{hp[:4]}-{hp[4:8]}-{hp[8:]}", "hp_format"
    if r < .20: return f"+62 {hp[1:4]} {hp[4:8]} {hp[8:]}", "hp_format"
    if r < .28: return "62" + hp[1:], "hp_format"
    if r < .34: return hp[1:], "hp_format"
    if r < .37: return "", "hp_kosong"
    return hp, None


def dirty_cust(c):
    nama = c["Nama"]
    r = R.random()
    if r < .15:
        nama = nama.upper(); cnt("pel_nama_huruf")
    elif r < .27:
        nama = nama.lower(); cnt("pel_nama_huruf")
    if R.random() < .12:
        nama = R.choice([" ", "  "]) + nama + R.choice([" ", "  "]); cnt("pel_nama_spasi")
    if R.random() < .06:
        nama = nama.replace(" ", "  ", 1); cnt("pel_nama_spasi_dalam")
    kota = c["Kota"]
    r = R.random()
    if r < .08:
        kota = kota.lower(); cnt("pel_kota_variasi")
    elif r < .14:
        kota = kota.upper(); cnt("pel_kota_variasi")
    elif r < .22:
        kota = kota + " "; cnt("pel_kota_variasi")
    elif r < .27 and kota in KALIAS:
        kota = R.choice(KALIAS[kota]); cnt("pel_kota_alias")
    em = c["Email"]
    r = R.random()
    if r < .08:
        em = em.upper(); cnt("pel_email_huruf")
    elif r < .13:
        em = ""; cnt("pel_email_kosong")
    elif r < .17:
        em = em.replace("@", ""); cnt("pel_email_tidak_valid")
    elif r < .23:
        em = " " + em + " "; cnt("pel_email_spasi")
    hp, tag = fmt_hp(c["HP"])
    if tag: cnt("pel_" + tag)
    d = c["Tgl"]
    r = R.random()
    if r < .50: tg = d_iso(d)
    elif r < .75:
        tg = d_slash(d); cnt("pel_tgl_slash")
    elif r < .90:
        tg = d_id(d); cnt("pel_tgl_teks")
    else:
        tg = d_dash(d); cnt("pel_tgl_strip")
    seg = c["Seg"]
    r = R.random()
    if r < .08:
        seg = ""; cnt("pel_segmen_kosong")
    elif r < .18:
        seg = seg.lower() if R.random() < .5 else seg.upper(); cnt("pel_segmen_huruf")
    return [c["ID"], nama, kota, em, hp, tg, seg]


cust_rows = [dirty_cust(c) for c in cust]
dups = R.sample(range(len(cust_rows)), 6)
for i in sorted(dups, reverse=True):
    cust_rows.insert(i + 1, list(cust_rows[i]))
cnt("pel_duplikat", 6)
with open(f"{OUT}/pelanggan_segarmart.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ID_Pelanggan", "Nama", "Kota", "Email", "No_HP", "Tanggal_Daftar", "Segmen"])
    w.writerows(cust_rows)
K["pel_baris_file"] = len(cust_rows)

# ---------------- PRODUK (Excel) ----------------
P = [("Sembako", "Beras Premium 5kg", "kg", 72000), ("Sembako", "Minyak Goreng 2L", "pcs", 38000), ("Sembako", "Gula Pasir 1kg", "kg", 17500), ("Sembako", "Tepung Terigu 1kg", "kg", 13000), ("Sembako", "Telur Ayam 1kg", "kg", 31000), ("Sembako", "Mie Instan Goreng", "pak", 3200), ("Sembako", "Garam Dapur 250g", "pcs", 4500), ("Sembako", "Kecap Manis 600ml", "botol", 21000),
     ("Minuman", "Air Mineral 600ml", "pak", 42000), ("Minuman", "Teh Celup 25s", "pak", 9500), ("Minuman", "Kopi Bubuk 200g", "pcs", 27000), ("Minuman", "Susu UHT 1L", "pcs", 19500), ("Minuman", "Jus Jeruk 1L", "botol", 23000), ("Minuman", "Sirup Markisa 650ml", "botol", 25000), ("Minuman", "Minuman Isotonik 500ml", "botol", 8500), ("Minuman", "Kopi Sachet", "pak", 14000),
     ("Snack", "Keripik Singkong", "pcs", 11000), ("Snack", "Biskuit Cokelat", "pcs", 9000), ("Snack", "Wafer Keju", "pcs", 7500), ("Snack", "Kacang Panggang", "pcs", 12500), ("Snack", "Keripik Tempe", "pcs", 13500), ("Snack", "Permen Jahe", "pak", 6000), ("Snack", "Roti Tawar", "pcs", 16000), ("Snack", "Sereal Jagung", "pcs", 28000),
     ("Segar", "Apel Fuji 1kg", "kg", 42000), ("Segar", "Pisang Cavendish 1kg", "kg", 24000), ("Segar", "Tomat 500g", "pak", 9000), ("Segar", "Wortel 500g", "pak", 8000), ("Segar", "Bayam Ikat", "ikat", 4000), ("Segar", "Ayam Fillet 500g", "pak", 36000), ("Segar", "Ikan Bandeng 500g", "pak", 33000), ("Segar", "Tahu Putih 10pcs", "pak", 10000),
     ("Kebersihan", "Sabun Cuci Piring 800ml", "botol", 17500), ("Kebersihan", "Deterjen Bubuk 1kg", "pak", 24500), ("Kebersihan", "Sabun Mandi Cair 450ml", "botol", 22000), ("Kebersihan", "Sampo 170ml", "botol", 18500), ("Kebersihan", "Pasta Gigi 120g", "pcs", 12500), ("Kebersihan", "Tisu Gulung 4s", "pak", 15000), ("Kebersihan", "Pembersih Lantai 800ml", "botol", 19500), ("Kebersihan", "Pewangi Pakaian 900ml", "botol", 21500)]
SUP = ["CV Sumber Pangan", "PT Nusa Segar", "UD Berkah Jaya", "PT Mitra Dapur", "CV Tani Makmur"]
prod = []
for i, (k, n, s, h) in enumerate(P, 1):
    prod.append(dict(Kode=f"PRD-{i:03d}", Nama=n, Kat=k, Harga=h, Sat=s, Sup=R.choice(SUP), Stok=R.randint(8, 400), Aktif=R.random() < .88))
blank_price = {3, 21}
prod_rows = []
for i, p in enumerate(prod):
    kode = p["Kode"]
    r = R.random()
    if r < .10:
        kode = kode.lower(); cnt("prd_kode_huruf")
    elif r < .18:
        kode = " " + kode + " "; cnt("prd_kode_spasi")
    nama = p["Nama"]
    if R.random() < .10:
        nama = nama.upper(); cnt("prd_nama_huruf")
    kat = p["Kat"]
    r = R.random()
    if r < .12:
        kat = kat.lower(); cnt("prd_kat_variasi")
    elif r < .20:
        kat = kat.upper() + " "; cnt("prd_kat_variasi")
    elif r < .26:
        kat = " " + kat; cnt("prd_kat_variasi")
    harga = p["Harga"]
    if i in blank_price:
        harga = None; cnt("prd_harga_kosong")
    elif R.random() < .30:
        harga = "Rp " + f"{p['Harga']:,}".replace(",", "."); cnt("prd_harga_teks")
    stok = p["Stok"]
    r = R.random()
    if r < .08:
        stok = -R.randint(1, 5); cnt("prd_stok_negatif")
    elif r < .14:
        stok = None; cnt("prd_stok_kosong")
    elif r < .18:
        stok = "habis"; cnt("prd_stok_teks")
    ak = "Ya" if p["Aktif"] else "Tidak"
    if R.random() < .45:
        ak = {"Ya": R.choice(["Y", "ya", "TRUE", "Aktif"]), "Tidak": R.choice(["N", "tidak", "FALSE", "Nonaktif"])}[ak]; cnt("prd_aktif_variasi")
    prod_rows.append([kode, nama, kat, harga, p["Sat"], p["Sup"], stok, ak])
for i in sorted(R.sample(range(len(prod_rows)), 2), reverse=True):
    prod_rows.insert(i + 1, list(prod_rows[i]))
cnt("prd_duplikat", 2)
wb = Workbook()
ws = wb.active
ws.title = "Produk"
ws["A1"] = "DAFTAR PRODUK SEGARMART"
ws["A1"].font = Font(bold=True, size=14)
ws["A2"] = "Diperbarui: 31 Mei 2025 oleh Gudang Pusat"
ws.append([])
ws.append(["Kode_Produk", "Nama_Produk", "Kategori", "Harga", "Satuan", "Supplier", "Stok", "Aktif"])
for c in ws[4]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="0B7A5A")
for r in prod_rows:
    ws.append(r)
ws.append([])
ws.append([f"Total: {len(prod_rows)} baris"])
for col, wd in zip("ABCDEFGH", [14, 28, 14, 14, 9, 20, 8, 10]):
    ws.column_dimensions[col].width = wd
ws2 = wb.create_sheet("Catatan")
ws2["A1"] = "Catatan admin gudang. Bukan data produk."
ws2["A2"] = "Harga kosong berarti belum diisi pemasok."
wb.save(f"{OUT}/produk_segarmart.xlsx")
K["prd_baris_data_file"] = len(prod_rows)

# ---------------- TRANSAKSI (SQL) ----------------
price = {p["Kode"]: p["Harga"] for p in prod}
blank_codes = {prod[i]["Kode"] for i in blank_price}
STAT = ["Selesai", "Selesai", "Selesai", "Dikirim", "Diproses", "Batal"]
MET = ["Transfer Bank", "COD", "E-Wallet", "Kartu Kredit"]
MVAR = {"Transfer Bank": ["transfer", "TRANSFER BANK", "Transfer  Bank", "Transfer bank "], "COD": ["cod", "Cash on Delivery", "COD "], "E-Wallet": ["ewallet", "E Wallet", "e-wallet", "Gopay", "OVO"], "Kartu Kredit": ["kartu kredit", "CC", "KARTU KREDIT"]}
trx = []
N = 450
orphan_c_idx = set(R.sample(range(N), 8))
orphan_p_idx = set(R.sample([i for i in range(N) if i not in orphan_c_idx], 5))
for i in range(N):
    pid = f"PLG-{R.randint(1, 120):04d}"
    kode = prod[R.randrange(len(prod))]["Kode"]
    if i in orphan_c_idx: pid = f"PLG-{R.randint(121, 130):04d}"
    if i in orphan_p_idx: kode = f"PRD-{R.randint(41, 45):03d}"
    qty = R.choices(range(1, 11), weights=[18, 18, 14, 12, 10, 8, 6, 5, 5, 4])[0]
    disc = R.choice([0, 0, 0, 5, 10, 15])
    hp = price.get(kode, R.choice([9000, 12500, 25000, 40000]))
    trx.append(dict(Tgl=rdate(datetime.date(2025, 1, 1), datetime.date(2025, 6, 30)), PID=pid, Kode=kode, Qty=qty, Harga=hp, Disc=disc, Met=R.choice(MET), Stat=R.choice(STAT)))
trx.sort(key=lambda t: t["Tgl"])
for i, t in enumerate(trx, 1): t["ID"] = f"TRX-{i:05d}"
cnt("trx_orphan_pelanggan", len(orphan_c_idx))
cnt("trx_orphan_produk", len(orphan_p_idx))


def dirty_id(s):
    r = R.random()
    if r < .12: return s.lower(), "huruf"
    if r < .22: return " " + s + " ", "spasi"
    if r < .28: return s.replace("-", ""), "tanpa_strip"
    return s, None


trx_rows = []
for t in trx:
    pid, tg1 = dirty_id(t["PID"])
    kode, tg2 = dirty_id(t["Kode"])
    if tg1: cnt("trx_pid_" + tg1)
    if tg2: cnt("trx_kode_" + tg2)
    r = R.random()
    d = t["Tgl"]
    if r < .60: tg = d_iso(d)
    elif r < .85:
        tg = d_slash(d); cnt("trx_tgl_slash")
    else:
        tg = d_dash(d); cnt("trx_tgl_strip")
    qty = t["Qty"]
    qflag = None
    r = R.random()
    if r < .04:
        qty = None; qflag = "kosong"
    elif r < .06:
        qty = -qty; qflag = "tidak_wajar"
    elif r < .07:
        qty = 0; qflag = "tidak_wajar"
    elif r < .085:
        qty = qty * 100; qflag = "tidak_wajar"
    if qflag: cnt("trx_qty_" + qflag)
    harga = t["Harga"]
    if R.random() < .06 and t["Kode"] in price and t["Kode"] not in blank_codes:
        harga = None; cnt("trx_harga_null")
    disc = t["Disc"]
    r = R.random()
    if r < .45:
        ds = R.choice([f"{disc}%", f"{disc} %", f"{disc}"]); cnt("trx_diskon_format")
    elif r < .50:
        ds = ""; cnt("trx_diskon_kosong"); disc = 0
    else:
        ds = f"{disc}%"
    met = t["Met"]
    if R.random() < .35:
        met = R.choice(MVAR[met]); cnt("trx_metode_variasi")
    st = t["Stat"]
    r = R.random()
    if r < .10:
        st = st.lower(); cnt("trx_status_variasi")
    elif r < .16:
        st = st.upper() + " "; cnt("trx_status_variasi")
    elif r < .19:
        st = None; cnt("trx_status_null")
    trx_rows.append(dict(ID=t["ID"], Tgl=tg, PID=pid, Kode=kode, Qty=qty, Harga=harga, Disc=ds, Met=met, Stat=st))
for i in sorted(R.sample(range(len(trx_rows)), 12), reverse=True):
    trx_rows.insert(i + 1, dict(trx_rows[i]))
cnt("trx_duplikat", 12)
K["trx_baris_file"] = len(trx_rows)


def q(v):
    if v is None: return "NULL"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"


L = ["-- SegarMart | Tabel transaksi Semester 1 2025 (data mentah, belum dibersihkan)", "-- Dialek MySQL / MariaDB.",
     "CREATE DATABASE IF NOT EXISTS segarmart CHARACTER SET utf8mb4;", "USE segarmart;", "DROP TABLE IF EXISTS transaksi;",
     "CREATE TABLE transaksi (\n  ID_Transaksi      VARCHAR(12),\n  Tanggal_Transaksi VARCHAR(20),\n  ID_Pelanggan      VARCHAR(14),\n  Kode_Produk       VARCHAR(14),\n  Qty               INT NULL,\n  Harga_Satuan      DECIMAL(12,2) NULL,\n  Diskon            VARCHAR(8),\n  Metode_Bayar      VARCHAR(30),\n  Status            VARCHAR(15) NULL\n);", ""]
vals = [f"({q(r['ID'])},{q(r['Tgl'])},{q(r['PID'])},{q(r['Kode'])},{q(r['Qty'])},{q(None if r['Harga'] is None else float(r['Harga']))},{q(r['Disc'])},{q(r['Met'])},{q(r['Stat'])})" for r in trx_rows]
L.append("INSERT INTO transaksi VALUES\n" + ",\n".join(vals) + ";")
L += ["", "SELECT COUNT(*) AS jumlah_baris FROM transaksi;"]
open(f"{OUT}/transaksi_segarmart.sql", "w", encoding="utf-8").write("\n".join(L) + "\n")
sql = open(f"{OUT}/transaksi_segarmart.sql", encoding="utf-8").read()
sql = re.sub(r"CREATE DATABASE.*?;\n|USE .*?;\n|SELECT COUNT.*", "", sql).replace("CHARACTER SET utf8mb4", "")
con = sqlite3.connect(":memory:")
con.executescript(sql)
K["sql_check_baris"] = con.execute("select count(*) from transaksi").fetchone()[0]


# ---------------- VERIFIKASI: bersihkan dengan aturan, hitung kunci ----------------
def nid(s, w):
    m = re.match(r"^([A-Za-z]{3})-?(\d+)$", s.strip())
    return f"{m.group(1).upper()}-{int(m.group(2)):0{w}d}"


seen = set()
uniq = []
for r in trx_rows:
    if r["ID"] in seen: continue
    seen.add(r["ID"]); uniq.append(r)
K["trx_baris_setelah_dedup"] = len(uniq)
valid_c = {c["ID"] for c in cust}
valid_p = set(price)
K["trx_orphan_pelanggan_akhir"] = sum(1 for r in uniq if nid(r["PID"], 4) not in valid_c)
K["trx_orphan_produk_akhir"] = sum(1 for r in uniq if nid(r["Kode"], 3) not in valid_p)
tot = 0
used_rows = 0
per_kat = {}
excl = {"batal": 0, "qty": 0}
kat_of = {p["Kode"]: p["Kat"] for p in prod}
for r in uniq:
    kode = nid(r["Kode"], 3)
    stt = (r["Stat"] or "Tidak Diketahui").strip().title()
    if r["Qty"] is None or r["Qty"] <= 0 or r["Qty"] > 50:
        excl["qty"] += 1; continue
    if stt == "Batal":
        excl["batal"] += 1; continue
    h = r["Harga"] if r["Harga"] is not None else price[kode]
    ds = r["Disc"].replace("%", "").strip()
    dd = int(ds) if ds else 0
    v = r["Qty"] * float(h) * (1 - dd / 100)
    tot += v
    used_rows += 1
    kat = kat_of.get(kode, "Tidak Terdaftar")
    per_kat[kat] = per_kat.get(kat, 0) + v
K["total_penjualan_bersih"] = round(tot)
K["baris_dihitung"] = used_rows
K["dikecualikan"] = excl
K["per_kategori"] = {k: round(v) for k, v in sorted(per_kat.items())}
K["pelanggan_unik"] = len(cust)
K["produk_unik"] = len(prod)
K["produk_harga_kosong"] = sorted(blank_codes)
json.dump(K, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "key2.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(K, indent=1, ensure_ascii=False))
