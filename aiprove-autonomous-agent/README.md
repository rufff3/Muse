# AIProve Autonomous Agent

Agent Python otonom untuk arena bounty AIProve. Agent membaca daftar bounty open,
mencoba masuk ke setiap bounty, lalu mengerjakan bounty forecast BTC dan NVDA
dengan data pasar publik.

## Menjalankan

```bash
pip install requests eth_account
python3 agent.py
```

Dependensi juga akan dipasang otomatis bila belum tersedia.

Arahkan ke host API lain:

```bash
API_BASE_URL=https://contoh-host python3 agent.py
```

Gunakan handle sendiri bila diperlukan:

```bash
AGENT_HANDLE=nama-agent python3 agent.py
```

Uji pembacaan API tanpa melakukan write call:

```bash
python3 agent.py --dry-run
```

Loop agent melakukan hal berikut:

1. Membaca `/skill.md` dan mencatat 500 karakter pertamanya.
2. Membuat keypair Ethereum baru di memori.
3. Melakukan autentikasi challenge/signature.
4. Mengambil semua bounty dengan status `open`.
5. Mencoba masuk ke setiap bounty.
6. Menghitung dan mengirim prediksi BTC serta NVDA bila data pasar tersedia.
7. Mencatat bounty lain sebagai pekerjaan yang membutuhkan manusia atau pekerjaan eksternal.
8. Menulis ringkasan ke stdout dan `run_log.json`.

Keypair baru dibuat pada setiap proses. Private key tidak pernah dicetak,
disimpan ke file, atau dikirim ke API. Token autentikasi hanya disimpan di memori
selama proses berjalan.
