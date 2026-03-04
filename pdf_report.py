"""
Modul Pembuat Laporan PDF Otomatis
Menggunakan: fpdf2 (fpdf) + matplotlib
Menghasilkan file PDF lengkap dengan tabel dan grafik.
"""

import os
import tempfile
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def _sanitize_text(text):
    """Sanitize text agar kompatibel dengan font Helvetica (Latin-1).
    Mengganti karakter Unicode yang tidak didukung."""
    replacements = {
        '\u2014': '-',   # em dash
        '\u2013': '-',   # en dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2026': '...', # ellipsis
        '\u2022': '*',   # bullet
        '\u00a0': ' ',   # non-breaking space
        '\u2010': '-',   # hyphen
        '\u2011': '-',   # non-breaking hyphen
        '\u2012': '-',   # figure dash
        '\u2015': '-',   # horizontal bar
        '\u2032': "'",   # prime
        '\u2033': '"',   # double prime
        '\u00b7': '.',   # middle dot
        '\u200b': '',    # zero-width space
        '\u200e': '',    # left-to-right mark
        '\u200f': '',    # right-to-left mark
        '\ufeff': '',    # byte order mark
    }
    text = str(text)
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: replace any remaining non-latin1 chars
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text


class LaporanPDF(FPDF):
    """Kelas PDF kustom dengan header dan footer."""

    def __init__(self, kode_emiten, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kode_emiten = kode_emiten

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, _sanitize_text(f'Laporan Kepemilikan Saham - {self.kode_emiten}'), align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Halaman {self.page_no()}/{{nb}}', align='C')


def _buat_pie_chart(data, kode_saham, filepath):
    """Membuat pie chart kepemilikan saham dan menyimpan sebagai PNG."""
    top_data = data.head(8).copy()

    # Jika ada sisa, gabungkan ke "Lainnya"
    if len(data) > 8:
        sisa = data.iloc[8:]
        persen_sisa = sisa['PERSEN(%)'].sum()
        baris_lain = pd.DataFrame([{'INVESTOR': 'Lainnya', 'PERSEN(%)': persen_sisa}])
        top_data = pd.concat([top_data, baris_lain], ignore_index=True)

    labels = top_data['INVESTOR'].apply(lambda x: x[:25] + '..' if len(str(x)) > 25 else x).tolist()
    sizes = top_data['PERSEN(%)'].tolist()

    # Warna premium
    colors = ['#E040FB', '#00E5FF', '#FFD740', '#FF5252', '#69F0AE',
              '#448AFF', '#FF6E40', '#EA80FC', '#B2FF59']

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#1A1A2E')
    ax.set_facecolor('#1A1A2E')

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        colors=colors[:len(sizes)],
        startangle=90, pctdistance=0.82,
        textprops={'fontsize': 8, 'color': 'white'}
    )

    for autotext in autotexts:
        autotext.set_fontsize(7)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    # Buat donut
    centre_circle = plt.Circle((0, 0), 0.55, fc='#1A1A2E')
    ax.add_artist(centre_circle)

    ax.text(0, 0, kode_saham, ha='center', va='center',
            fontsize=16, fontweight='bold', color='#E040FB')

    ax.set_title(f'Komposisi Kepemilikan Saham {kode_saham}',
                 fontsize=13, fontweight='bold', color='white', pad=20)

    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#1A1A2E')
    plt.close()


def _buat_bar_chart(data, kode_saham, filepath):
    """Membuat bar chart horizontal dan menyimpan sebagai PNG."""
    top_data = data.head(10).copy()
    top_data = top_data.sort_values(by='PERSEN(%)', ascending=True)

    labels = top_data['INVESTOR'].apply(lambda x: x[:30] + '..' if len(str(x)) > 30 else x).tolist()
    values = top_data['PERSEN(%)'].tolist()

    colors_bar = ['#E040FB', '#00E5FF', '#FFD740', '#FF5252', '#69F0AE',
                  '#448AFF', '#FF6E40', '#EA80FC', '#B2FF59', '#FFAB40']

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('#1A1A2E')
    ax.set_facecolor('#1A1A2E')

    bars = ax.barh(labels, values, color=colors_bar[:len(values)], edgecolor='none', height=0.6)

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{val:.2f}%', va='center', fontsize=8, color='white')

    ax.set_xlabel('Persentase (%)', color='white', fontsize=10)
    ax.set_title(f'Top 10 Pemegang Saham {kode_saham}', fontsize=13,
                 fontweight='bold', color='white')
    ax.tick_params(colors='white', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#444')
    ax.spines['bottom'].set_color('#444')
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))

    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='#1A1A2E')
    plt.close()


def buat_laporan_pdf(df, kode_saham, info_harga=None, output_dir="."):
    """
    Membuat laporan PDF lengkap untuk satu emiten.
    
    Parameters:
        df: DataFrame lengkap
        kode_saham: Kode emiten (misal 'AADI')
        info_harga: dict dari stock_data.ambil_data_saham() (opsional)
        output_dir: Folder output
    """
    import pandas as pd  # import lokal untuk keamanan

    kode_upper = kode_saham.upper()
    data = df[df['KODE'] == kode_upper].copy()

    if data.empty:
        print(f"\n[!] Data untuk emiten '{kode_upper}' tidak ditemukan.")
        return None

    data = data.sort_values(by='PERSEN(%)', ascending=False)

    # Hitung free float
    total_persen = data['PERSEN(%)'].sum()
    if total_persen < 99.9:
        sisa = 100.0 - total_persen
        baris_ff = {col: '-' for col in data.columns}
        baris_ff['KODE'] = kode_upper
        baris_ff['INVESTOR'] = 'MASYARAKAT / FREE FLOAT'
        baris_ff['PERSEN(%)'] = sisa
        baris_ff['TOTAL_SAHAM'] = 0
        data = pd.concat([data, pd.DataFrame([baris_ff])], ignore_index=True)
        data = data.sort_values(by='PERSEN(%)', ascending=False)

    emiten_name = data['EMITEN'].iloc[0] if 'EMITEN' in data.columns else kode_upper

    # ======= BUAT PDF =======
    pdf = LaporanPDF(kode_upper, orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- Halaman 1: Ringkasan & Tabel ---
    pdf.add_page()

    # Judul
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 15, 'Laporan Kepemilikan Saham', ln=True, align='C')
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(100, 0, 200)
    pdf.cell(0, 10, _sanitize_text(f'{kode_upper} - {emiten_name}'), ln=True, align='C')
    pdf.ln(5)

    # Garis pemisah
    pdf.set_draw_color(200, 200, 200)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(8)

    # Info ringkasan
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, _sanitize_text(f'Jumlah pemegang saham tercatat: {len(data)}'), ln=True)
    pdf.cell(0, 6, _sanitize_text(f'Total persentase tercatat: {data["PERSEN(%)"].sum():.2f}%'), ln=True)
    if 'TGL' in data.columns:
        tanggal = data['TGL'].iloc[0]
        pdf.cell(0, 6, _sanitize_text(f'Tanggal data: {tanggal}'), ln=True)
    pdf.ln(8)

    # Tabel pemegang saham
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(45, 45, 80)
    pdf.set_text_color(255, 255, 255)

    col_widths = [8, 55, 20, 25, 25, 22, 25]
    headers = ['No', 'Investor', 'Tipe', 'L/F', 'Total Saham', 'Persen(%)', 'Asal']

    for w, h_text in zip(col_widths, headers):
        pdf.cell(w, 8, h_text, border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(30, 30, 30)

    for idx, (_, row) in enumerate(data.iterrows(), 1):
        # Warna selang-seling
        if idx % 2 == 0:
            pdf.set_fill_color(240, 240, 250)
            fill = True
        else:
            pdf.set_fill_color(255, 255, 255)
            fill = True

        investor_name = _sanitize_text(str(row.get('INVESTOR', '-'))[:35])
        tipe = _sanitize_text(str(row.get('TIPE', '-'))[:12])
        lf = _sanitize_text(str(row.get('L/F', '-'))[:8])
        total_s = row.get('TOTAL_SAHAM', 0)
        total_str = f"{total_s:,.0f}" if isinstance(total_s, (int, float)) and total_s > 0 else '-'
        persen = f"{row['PERSEN(%)']:.2f}%" if isinstance(row['PERSEN(%)'], (int, float)) else '-'
        asal = _sanitize_text(str(row.get('ASAL', '-'))[:15])

        pdf.cell(col_widths[0], 6, str(idx), border=1, align='C', fill=fill)
        pdf.cell(col_widths[1], 6, investor_name, border=1, fill=fill)
        pdf.cell(col_widths[2], 6, tipe, border=1, align='C', fill=fill)
        pdf.cell(col_widths[3], 6, lf, border=1, align='C', fill=fill)
        pdf.cell(col_widths[4], 6, total_str, border=1, align='R', fill=fill)
        pdf.cell(col_widths[5], 6, persen, border=1, align='C', fill=fill)
        pdf.cell(col_widths[6], 6, asal, border=1, align='C', fill=fill)
        pdf.ln()

        if pdf.get_y() > 260:
            pdf.add_page()

    # --- Halaman 2: Grafik ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 12, 'Visualisasi Kepemilikan Saham', ln=True, align='C')
    pdf.ln(5)

    tmpdir = tempfile.mkdtemp()

    # Pie chart
    pie_path = os.path.join(tmpdir, "pie_chart.png")
    try:
        _buat_pie_chart(data, kode_upper, pie_path)
        pdf.image(pie_path, x=15, w=180)
        pdf.ln(5)
    except Exception as e:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, _sanitize_text(f'[Gagal membuat pie chart: {e}]'), ln=True)

    # Bar chart (halaman baru jika perlu)
    if pdf.get_y() > 140:
        pdf.add_page()
    
    bar_path = os.path.join(tmpdir, "bar_chart.png")
    try:
        _buat_bar_chart(data, kode_upper, bar_path)
        pdf.image(bar_path, x=15, w=180)
    except Exception as e:
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, _sanitize_text(f'[Gagal membuat bar chart: {e}]'), ln=True)

    # --- Halaman 3: Info Harga (opsional) ---
    if info_harga:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 12, _sanitize_text(f'Data Pasar - {kode_upper}'), ln=True, align='C')
        pdf.ln(5)

        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(30, 30, 30)
        for key, val in info_harga.items():
            pdf.cell(90, 8, _sanitize_text(str(key)), border=0)
            pdf.cell(0, 8, _sanitize_text(str(val)), border=0, ln=True)

    # Simpan PDF
    output_filename = f"Laporan_Kepemilikan_{kode_upper}.pdf"
    output_path = os.path.join(output_dir, output_filename)
    pdf.output(output_path)

    print(f"\n[✓] Laporan PDF berhasil dibuat: {output_path}")

    # Cleanup temp files
    try:
        os.remove(pie_path)
        os.remove(bar_path)
        os.rmdir(tmpdir)
    except Exception:
        pass

    return output_path
