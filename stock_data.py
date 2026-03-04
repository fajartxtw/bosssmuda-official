"""
Modul Data Harga Saham Real-Time
Menggunakan: yfinance (Yahoo Finance API)
Mengambil harga penutupan, volume, market cap, dll untuk saham-saham IDX.
"""

import yfinance as yf
import pandas as pd


def _kode_ke_yahoo(kode_emiten):
    """Konversi kode saham IDX ke format Yahoo Finance (tambah .JK)."""
    kode = kode_emiten.upper().strip()
    if not kode.endswith('.JK'):
        kode = kode + '.JK'
    return kode


def ambil_data_saham(kode_emiten):
    """
    Mengambil data harga saham real-time dari Yahoo Finance.
    Return: dictionary berisi info saham, atau None jika gagal.
    """
    ticker_symbol = _kode_ke_yahoo(kode_emiten)
    kode_upper = kode_emiten.upper().strip()

    print(f"\n⏳ Mengambil data pasar untuk {kode_upper} ({ticker_symbol})...")

    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        if not info or info.get('regularMarketPrice') is None:
            # Coba ambil dari history sebagai fallback
            hist = ticker.history(period="5d")
            if hist.empty:
                print(f"[!] Data Yahoo Finance tidak tersedia untuk {kode_upper}.")
                return None
            
            last_close = hist['Close'].iloc[-1]
            last_volume = hist['Volume'].iloc[-1]
            hasil = {
                'Kode': kode_upper,
                'Ticker Yahoo': ticker_symbol,
                'Harga Terakhir (IDR)': f"Rp {last_close:,.0f}",
                'Volume Terakhir': f"{last_volume:,.0f}",
                'Market Cap': 'N/A',
                '52W High': 'N/A',
                '52W Low': 'N/A',
                'P/E Ratio': 'N/A',
                'Dividend Yield': 'N/A',
                'Sumber': 'Yahoo Finance (History Fallback)',
            }
        else:
            harga = info.get('regularMarketPrice', info.get('previousClose', 0))
            volume = info.get('regularMarketVolume', info.get('volume', 0))
            mcap = info.get('marketCap', 0)
            high52 = info.get('fiftyTwoWeekHigh', 0)
            low52 = info.get('fiftyTwoWeekLow', 0)
            pe = info.get('trailingPE', None)
            div_yield = info.get('dividendYield', None)

            hasil = {
                'Kode': kode_upper,
                'Ticker Yahoo': ticker_symbol,
                'Nama Perusahaan': info.get('longName', info.get('shortName', kode_upper)),
                'Harga Terakhir (IDR)': f"Rp {harga:,.0f}" if harga else 'N/A',
                'Volume Terakhir': f"{volume:,.0f}" if volume else 'N/A',
                'Market Cap (IDR)': _format_rupiah_besar(mcap) if mcap else 'N/A',
                '52W High': f"Rp {high52:,.0f}" if high52 else 'N/A',
                '52W Low': f"Rp {low52:,.0f}" if low52 else 'N/A',
                'P/E Ratio': f"{pe:.2f}" if pe else 'N/A',
                'Dividend Yield': f"{div_yield*100:.2f}%" if div_yield else 'N/A',
                'Sektor': info.get('sector', 'N/A'),
                'Industri': info.get('industry', 'N/A'),
                'Sumber': 'Yahoo Finance',
            }

        # Tampilkan di terminal
        print(f"\n{'='*50}")
        print(f"  📊 DATA PASAR: {kode_upper}")
        print(f"{'='*50}")
        for key, val in hasil.items():
            print(f"  {key:.<30} {val}")
        print(f"{'='*50}")

        return hasil

    except Exception as e:
        print(f"\n[Ralat] Gagal mengambil data untuk {kode_upper}: {e}")
        return None


def ambil_histori_harga(kode_emiten, period="1mo"):
    """
    Mengambil histori harga saham.
    period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    Return: DataFrame histori harga atau None.
    """
    ticker_symbol = _kode_ke_yahoo(kode_emiten)

    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return None
        return hist
    except Exception:
        return None


def bandingkan_saham(list_kode):
    """
    Membandingkan beberapa saham sekaligus.
    Input: list kode emiten misal ['AADI', 'BBCA', 'TLKM']
    """
    hasil_list = []
    for kode in list_kode:
        data = ambil_data_saham(kode)
        if data:
            hasil_list.append(data)

    if not hasil_list:
        print("\n[!] Tidak ada data yang berhasil diambil.")
        return None

    df_compare = pd.DataFrame(hasil_list)
    print(f"\n--- PERBANDINGAN SAHAM ---")
    print(df_compare.to_string(index=False))
    return df_compare


def _format_rupiah_besar(angka):
    """Format angka besar ke format Triliun/Miliar."""
    if angka >= 1e12:
        return f"Rp {angka/1e12:,.2f} T"
    elif angka >= 1e9:
        return f"Rp {angka/1e9:,.2f} M"
    elif angka >= 1e6:
        return f"Rp {angka/1e6:,.2f} Jt"
    else:
        return f"Rp {angka:,.0f}"
