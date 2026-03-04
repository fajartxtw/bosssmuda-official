import pandas as pd
import plotext as plt
import sys
import os

class AnalisisKepemilikanSaham:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_and_clean_data()

    def load_and_clean_data(self):
        if not os.path.exists(self.file_path):
            print(f"\n[Ralat] File '{self.file_path}' tidak ditemukan!")
            sys.exit()

        print(f"\nMemuatkan data dari '{self.file_path}', mohon tunggu...")
        
        try:
            if self.file_path.lower().endswith('.csv'):
                df = pd.read_csv(self.file_path)
            elif self.file_path.lower().endswith(('.xlsx', '.xls')):
                try:
                    df = pd.read_excel(self.file_path)
                except ImportError:
                    print("\n[Ralat] Anda perlu menginstal library 'openpyxl'. (pip install openpyxl)")
                    sys.exit()
            else:
                print("\n[Ralat] Format file tidak didukung.")
                sys.exit()
            
            # Membersihkan angka
            kolom_angka = ['HOLDINGS_SCRIPLESS', 'HOLDINGS_SCRIP', 'TOTAL_HOLDING_SHARES']
            for col in kolom_angka:
                if col in df.columns: 
                    df[col] = df[col].astype(str).str.replace('.', '', regex=False)
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Membersihkan persentase
            if 'PERCENTAGE' in df.columns:
                df['PERCENTAGE'] = df['PERCENTAGE'].astype(str).str.replace(',', '.', regex=False)
                df['PERCENTAGE'] = pd.to_numeric(df['PERCENTAGE'], errors='coerce').fillna(0.0)
                
            # --- MENGUBAH NAMA HEADER MENJADI LEBIH SINGKAT ---
            rename_mapping = {
                'DATE': 'TGL',
                'SHARE_CODE': 'KODE',
                'ISSUER_NAME': 'EMITEN',
                'INVESTOR_NAME': 'INVESTOR',
                'INVESTOR_TYPE': 'TIPE',
                'LOCAL_FOREIGN': 'L/F',
                'NATIONALITY': 'ASAL',
                'DOMICILE': 'DOMISILI',
                'HOLDINGS_SCRIPLESS': 'SCRIPLESS',
                'HOLDINGS_SCRIP': 'SCRIP',
                'TOTAL_HOLDING_SHARES': 'TOTAL_SAHAM',
                'PERCENTAGE': 'PERSEN(%)'
            }
            df = df.rename(columns=rename_mapping)
            
            # Memastikan nama investor tidak kosong menggunakan nama header baru
            if 'INVESTOR' in df.columns:
                df['INVESTOR'] = df['INVESTOR'].fillna('UNKNOWN')
                
            print(f"Berhasil! {len(df)} baris data siap digunakan.\n")
            return df
            
        except Exception as e:
            print(f"\n[Ralat] Gagal memuat data: {e}")
            sys.exit()

    def get_list_saham(self):
        if self.df.empty: return
        saham_unik = self.df[['KODE', 'EMITEN']].drop_duplicates().sort_values('KODE')
        print("\n--- DAFTAR KODE SAHAM TERSEDIA ---")
        print(saham_unik.head(20).to_string(index=False))
        print(f"... (dan masih banyak lagi. Total emiten unik: {len(saham_unik)})")

    def _buat_grafik(self, labels, values, title, format_nilai="{}"):
        """Fungsi internal untuk menghasilkan grafik batang terminal dengan label presisi."""
        if not labels or not values:
            return
            
        # Memotong nama label yang terlalu panjang dan menambahkan NILAInya langsung di teks label
        labels_presisi = []
        for lbl, val in zip(labels, values):
            lbl_pendek = str(lbl)[:20] + '..' if len(str(lbl)) > 20 else str(lbl)
            nilai_diformat = format_nilai.format(val)
            labels_presisi.append(f"{lbl_pendek} [{nilai_diformat}]")
            
        values_float = [float(val) for val in values]
        
        # Membalik urutan agar nilai tertinggi ada di paling atas
        labels_presisi.reverse()
        values_float.reverse()
        
        print(f"\n--- GRAFIK: {title} ---")
        
        try:
            plt.clf()
        except AttributeError:
            try:
                plt.clear_figure()
            except:
                pass
        
        plt.bar(labels_presisi, values_float, orientation="horizontal", width=0.6)
        plt.title(title)
        plt.theme("clear")
        plt.show()

    def cari_berdasarkan_kode(self, kode_saham):
        kode_saham = kode_saham.upper()
        hasil = self.df[self.df['KODE'] == kode_saham].copy()
        
        if hasil.empty:
            print(f"\n[!] Data untuk emiten '{kode_saham}' tidak ditemukan.")
            return

        hasil = hasil.sort_values(by='PERSEN(%)', ascending=False)
        
        # --- LOGIKA FREE FLOAT (MASYARAKAT) DENGAN FULL HEADER ---
        total_persen = hasil['PERSEN(%)'].sum()
        if total_persen < 99.9:  
            sisa_persen = 100.0 - total_persen
            
            # Menyiapkan dictionary kosong dengan semua kolom dari dataframe asli
            baris_masyarakat_dict = {col: '-' for col in self.df.columns}
            baris_masyarakat_dict['TGL'] = hasil['TGL'].iloc[0] if 'TGL' in hasil.columns else '-'
            baris_masyarakat_dict['KODE'] = kode_saham
            baris_masyarakat_dict['EMITEN'] = hasil['EMITEN'].iloc[0] if 'EMITEN' in hasil.columns else '-'
            baris_masyarakat_dict['INVESTOR'] = 'MASYARAKAT / FREE FLOAT'
            baris_masyarakat_dict['SCRIPLESS'] = 0
            baris_masyarakat_dict['SCRIP'] = 0
            baris_masyarakat_dict['TOTAL_SAHAM'] = 0
            baris_masyarakat_dict['PERSEN(%)'] = sisa_persen
            
            baris_masyarakat = pd.DataFrame([baris_masyarakat_dict])
            hasil = pd.concat([hasil, baris_masyarakat], ignore_index=True)
            hasil = hasil.sort_values(by='PERSEN(%)', ascending=False)

        print(f"\n--- DATA KEPEMILIKAN SAHAM (FULL): {kode_saham} ---")
        # Menampilkan seluruh kolom sesuai header asli yang sudah dipersingkat
        print(hasil.to_string(index=False))

        # Render grafik otomatis (Top 10) dengan persentase presisi
        top_n = 10
        data_grafik = hasil.head(top_n)
        self._buat_grafik(
            data_grafik['INVESTOR'].tolist(), 
            data_grafik['PERSEN(%)'].tolist(), 
            f"Top {len(data_grafik)} Pemegang Saham {kode_saham} (%)",
            format_nilai="{:.2f}%"
        )

    def cari_berdasarkan_investor(self, nama_investor):
        nama_investor = nama_investor.upper()
        hasil = self.df[self.df['INVESTOR'].str.upper().str.contains(nama_investor, na=False)].copy()
        
        if hasil.empty:
            print(f"\n[!] Tidak ada portofolio untuk investor '{nama_investor}'.")
            return

        hasil = hasil.sort_values(by='PERSEN(%)', ascending=False)
        print(f"\n--- PORTOFOLIO INVESTOR FULL KOLOM: {nama_investor} ---")
        
        # Menampilkan tabel lengkap untuk Menu 3
        print(hasil.to_string(index=False))

        # Render grafik otomatis dengan persentase presisi
        top_n = 15
        data_grafik = hasil.head(top_n)
        self._buat_grafik(
            data_grafik['KODE'].tolist(), 
            data_grafik['PERSEN(%)'].tolist(), 
            f"Porsi {nama_investor} di Berbagai Emiten (%)",
            format_nilai="{:.2f}%"
        )

    def peringkat_investor_terbanyak_lembar(self, top_n=30):
        """Peringkat berdasarkan TOTAL LEMBAR SAHAM yang dimiliki secara keseluruhan."""
        df_valid = self.df[~self.df['INVESTOR'].str.upper().isin(['UNKNOWN', 'MASYARAKAT / FREE FLOAT'])]
        peringkat = df_valid.groupby('INVESTOR')['TOTAL_SAHAM'].sum().reset_index()
        peringkat = peringkat.sort_values(by='TOTAL_SAHAM', ascending=False).head(top_n)
        
        if peringkat.empty:
            print("\n[!] Data peringkat tidak tersedia.")
            return
            
        print(f"\n--- TOP {top_n} INVESTOR BERDASARKAN TOTAL LEMBAR SAHAM ---")
        print(peringkat.to_string(index=False))

        self._buat_grafik(
            peringkat['INVESTOR'].tolist(), 
            peringkat['TOTAL_SAHAM'].tolist(), 
            f"Top {top_n} Investor (Total Lembar Saham)",
            format_nilai="{:,.0f} Lbr"
        )

    def peringkat_investor_terbanyak_emiten(self, top_n=30):
        """Peringkat berdasarkan JUMLAH EMITEN (saham berbeda) yang dimiliki (Diversifikasi)."""
        df_valid = self.df[~self.df['INVESTOR'].str.upper().isin(['UNKNOWN', 'MASYARAKAT / FREE FLOAT'])]
        # Menghitung unique value dari KODE saham untuk setiap INVESTOR
        peringkat = df_valid.groupby('INVESTOR')['KODE'].nunique().reset_index()
        peringkat.columns = ['INVESTOR', 'TOTAL_EMITEN']
        peringkat = peringkat.sort_values(by='TOTAL_EMITEN', ascending=False).head(top_n)
        
        if peringkat.empty:
            print("\n[!] Data peringkat tidak tersedia.")
            return
            
        print(f"\n--- TOP {top_n} INVESTOR BERDASARKAN DIVERSIFIKASI PORTOFOLIO (JUMLAH EMITEN) ---")
        print(peringkat.to_string(index=False))

        self._buat_grafik(
            peringkat['INVESTOR'].tolist(), 
            peringkat['TOTAL_EMITEN'].tolist(), 
            f"Top {top_n} Investor (Jumlah Emiten Saham)",
            format_nilai="{:.0f} Emiten"
        )

def main():
    print("\n" + "="*50)
    print("   DASHBOARD KEPEMILIKAN SAHAM (VERSI TERINTEGRASI)")
    print("="*50)
    
    file_input = input("Nama file (contoh: DataSaham.xlsx) [Tekan Enter untuk default]: ").strip()
    if not file_input:
        file_input = 'Data_Kepemilikan_Saham_27_Feb_2026_FULL.xlsx - Sheet1.csv'
        
    app = AnalisisKepemilikanSaham(file_input)

    while True:
        print("\n" + "="*55)
        print("            MENU UTAMA DATA SAHAM (TERINTEGRASI)       ")
        print("="*55)
        print("1. Lihat Daftar Kode Saham")
        print("2. Cari Emiten (+ Tampil Full Kolom & Free Float)")
        print("3. Cari Portofolio Investor (+ Tampil Full Kolom)")
        print("4. Top 30 Investor: Total Lembar Saham Terbanyak")
        print("5. Top 30 Investor: Portofolio Emiten Terbanyak")
        print("-"*55)
        print("6. 🕸️  Visualisasi Network Graph (Jaring Laba-Laba)")
        print("7. 📈 Data Harga Saham Real-Time (Yahoo Finance)")
        print("8. 📄 Ekspor Laporan PDF Otomatis")
        print("9. 🌐 Buka Web Dashboard (Streamlit)")
        print("-"*55)
        print("0. Keluar")
        print("="*55)
        
        pilihan = input("Pilih menu (0-9): ")

        if pilihan == '1':
            app.get_list_saham()
        elif pilihan == '2':
            kode = input("\nMasukkan kode emiten (contoh: AADI): ")
            app.cari_berdasarkan_kode(kode)
        elif pilihan == '3':
            nama = input("\nMasukkan nama investor/instansi (contoh: BLACKROCK): ")
            app.cari_berdasarkan_investor(nama)
        elif pilihan == '4':
            app.peringkat_investor_terbanyak_lembar(top_n=30)
        elif pilihan == '5':
            app.peringkat_investor_terbanyak_emiten(top_n=30)

        # ========= MODUL BARU =========

        elif pilihan == '6':
            # Network Graph
            try:
                from network_graph import buat_network_emiten, buat_network_investor
                print("\n--- VISUALISASI NETWORK GRAPH ---")
                print("a. Network berdasarkan EMITEN (siapa saja pemegang sahamnya)")
                print("b. Network berdasarkan INVESTOR (emiten apa saja yang dimiliki)")
                sub = input("Pilih (a/b): ").strip().lower()
                if sub == 'a':
                    kode = input("Masukkan kode emiten (contoh: AADI): ").strip()
                    buat_network_emiten(app.df, kode)
                elif sub == 'b':
                    nama = input("Masukkan nama investor (contoh: BLACKROCK): ").strip()
                    buat_network_investor(app.df, nama)
                else:
                    print("[!] Pilihan tidak valid.")
            except ImportError:
                print("\n[!] Modul belum terinstall. Jalankan: pip install networkx pyvis")

        elif pilihan == '7':
            # Data Harga Saham
            try:
                from stock_data import ambil_data_saham, bandingkan_saham
                print("\n--- DATA HARGA SAHAM (YAHOO FINANCE) ---")
                print("a. Lihat data satu emiten")
                print("b. Bandingkan beberapa emiten")
                sub = input("Pilih (a/b): ").strip().lower()
                if sub == 'a':
                    kode = input("Masukkan kode emiten (contoh: BBCA): ").strip()
                    ambil_data_saham(kode)
                elif sub == 'b':
                    kode_list = input("Masukkan kode emiten (pisah koma, contoh: BBCA,TLKM,AADI): ").strip()
                    list_kode = [k.strip() for k in kode_list.split(',') if k.strip()]
                    bandingkan_saham(list_kode)
                else:
                    print("[!] Pilihan tidak valid.")
            except ImportError:
                print("\n[!] Modul belum terinstall. Jalankan: pip install yfinance")

        elif pilihan == '8':
            # Ekspor PDF
            try:
                from pdf_report import buat_laporan_pdf
                print("\n--- EKSPOR LAPORAN PDF ---")
                kode = input("Masukkan kode emiten (contoh: AADI): ").strip()
                
                # Opsional: sertakan data harga
                info_harga = None
                tambah_harga = input("Sertakan data harga pasar? (y/n): ").strip().lower()
                if tambah_harga == 'y':
                    try:
                        from stock_data import ambil_data_saham
                        info_harga = ambil_data_saham(kode)
                    except ImportError:
                        print("[!] yfinance tidak tersedia, PDF dibuat tanpa data pasar.")
                
                buat_laporan_pdf(app.df, kode, info_harga=info_harga)
            except ImportError:
                print("\n[!] Modul belum terinstall. Jalankan: pip install fpdf2 matplotlib")

        elif pilihan == '9':
            # Buka Streamlit Web Dashboard
            print("\n--- MEMBUKA WEB DASHBOARD ---")
            print("Menjalankan Streamlit... (tekan Ctrl+C di terminal untuk berhenti)")
            try:
                import subprocess
                script_dir = os.path.dirname(os.path.abspath(__file__))
                streamlit_file = os.path.join(script_dir, 'app_streamlit.py')
                subprocess.Popen(['streamlit', 'run', streamlit_file], cwd=script_dir)
                print("[✓] Dashboard sedang dibuka di browser...")
                print("    URL default: http://localhost:8501")
            except FileNotFoundError:
                print("[!] Streamlit belum terinstall. Jalankan: pip install streamlit plotly")
            except Exception as e:
                print(f"[!] Gagal membuka dashboard: {e}")

        elif pilihan == '0':
            print("\nKeluar dari program. Semoga penyusunan skripsinya berjalan lancar!")
            break
        else:
            print("\n[!] Pilihan tidak valid. Silakan masukkan angka 0-9.")

if __name__ == "__main__":
    main()
