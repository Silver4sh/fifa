# FIFA Data Viewer

FIFA Data Viewer adalah aplikasi GUI berbasis Python yang memungkinkan Anda untuk memuat data CSV FIFA, menampilkan informasi pemain dan tim, mengekspor summary data ke file Excel, menampilkan data top player (dengan filter berdasarkan Overall atau Posisi), menampilkan data top team, serta visualisasi distribusi rating Overall. Aplikasi ini dilengkapi dengan fitur autocomplete untuk input manual dan dropdown yang responsif, serta mendukung clickable URL pada hasil output.

## Fitur Utama

- **Memuat Data CSV**  
  Pengguna dapat memilih file CSV yang berisi data FIFA. Proyek secara otomatis menghapus kolom yang diawali "Unnamed" (misalnya "Unnamed: 0").

- **Info Player**  
  Menampilkan informasi lengkap pemain dalam tampilan Treeview dua kolom (Attribute & Value) dengan fitur autocomplete dan dropdown. URL pada hasil output dapat di-click (double-click) untuk membuka tautan di browser.

- **Info Team**  
  Menampilkan data tim dalam tampilan Treeview yang fit dan rapi dengan scrollbar horizontal dan vertikal, serta fitur autocomplete untuk input manual.

- **Summary**  
  Menghasilkan statistik ringkasan dari data (menggunakan `data_frame.describe()`) dan mengekspor hasilnya ke file Excel (.xlsx/.xls).

- **Top Player**  
  Menampilkan pemain dengan rating tertinggi berdasarkan Overall atau filter berdasarkan Posisi. Pengguna dapat memilih kriteria melalui radio button, dan jika memilih filter berdasarkan posisi, dropdown posisi akan muncul.

- **Top Team**  
  Menghitung rata-rata rating Overall per tim dan menampilkan tim dengan rata-rata tertinggi.

- **Visual Data**  
  Menampilkan histogram distribusi rating Overall menggunakan Matplotlib dalam jendela terpisah.