"""
Modul Visualisasi Network Graph (Jaring Laba-Laba Konglomerasi)
Menggunakan: networkx + pyvis
Menghasilkan file HTML interaktif yang bisa dibuka di browser.
"""

import networkx as nx
from pyvis.network import Network
import webbrowser
import os

# Palet warna premium
WARNA_NODE_PUSAT = "#E040FB"     # Magenta/Ungu terang
WARNA_EMITEN = "#00E5FF"         # Cyan neon
WARNA_INVESTOR = "#FFD740"       # Amber/Emas
WARNA_EDGE = "#B0BEC5"           # Abu-abu lembut


def buat_network_investor(df, nama_investor, output_dir="."):
    """
    Membuat network graph dengan investor sebagai node pusat
    dan semua emiten yang dimilikinya sebagai node cabang.
    """
    nama_upper = nama_investor.upper()
    data = df[df['INVESTOR'].str.upper().str.contains(nama_upper, na=False)].copy()

    if data.empty:
        print(f"\n[!] Tidak ada data untuk investor '{nama_investor}'.")
        return None

    data = data.sort_values(by='PERSEN(%)', ascending=False)

    # Ambil nama investor yang paling sering muncul
    nama_tampil = data['INVESTOR'].mode().iloc[0] if not data['INVESTOR'].mode().empty else nama_investor

    G = nx.Graph()

    # Node pusat: Investor
    G.add_node(nama_tampil, size=50, color=WARNA_NODE_PUSAT, 
               title=f"<b>{nama_tampil}</b><br>Total emiten: {data['KODE'].nunique()}",
               font={"size": 18, "color": "white", "face": "Inter, sans-serif"})

    # Node cabang: Setiap emiten yang dimiliki
    for _, row in data.iterrows():
        kode = str(row['KODE'])
        emiten = str(row.get('EMITEN', kode))
        persen = float(row['PERSEN(%)'])
        total = row.get('TOTAL_SAHAM', 0)

        node_size = max(12, min(40, persen * 2))

        tooltip = (
            f"<b>{kode}</b> — {emiten}<br>"
            f"Kepemilikan: {persen:.2f}%<br>"
            f"Total Saham: {total:,.0f}"
        )

        G.add_node(kode, size=node_size, color=WARNA_EMITEN,
                   title=tooltip,
                   font={"size": 12, "color": "white", "face": "Inter, sans-serif"})

        # Edge dengan ketebalan proporsional
        edge_width = max(1, persen / 5)
        G.add_edge(nama_tampil, kode, 
                   value=edge_width, 
                   title=f"{persen:.2f}%",
                   color=WARNA_EDGE)

    # Render ke HTML interaktif
    net = Network(height="750px", width="100%", bgcolor="#0D1117", 
                  font_color="white", directed=False)
    net.from_nx(G)
    
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.008,
          "springLength": 180,
          "springConstant": 0.04
        },
        "solver": "forceAtlas2Based",
        "stabilization": {"iterations": 150}
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "zoomView": true,
        "dragView": true
      },
      "edges": {
        "smooth": {"type": "continuous"},
        "color": {"inherit": false}
      }
    }
    """)

    filename = f"network_investor_{nama_upper.replace(' ', '_')[:30]}.html"
    filepath = os.path.join(output_dir, filename)
    net.save_graph(filepath)

    print(f"\n[✓] Network graph berhasil dibuat: {filepath}")
    print(f"    → {data['KODE'].nunique()} emiten terhubung ke {nama_tampil}")
    
    try:
        webbrowser.open(os.path.abspath(filepath))
        print("    → File dibuka di browser.")
    except Exception:
        print("    → Silakan buka file HTML di browser secara manual.")

    return filepath


def buat_network_emiten(df, kode_saham, output_dir="."):
    """
    Membuat network graph dengan emiten sebagai node pusat
    dan semua investor/pemegang saham sebagai node cabang.
    """
    kode_upper = kode_saham.upper()
    data = df[df['KODE'] == kode_upper].copy()

    if data.empty:
        print(f"\n[!] Tidak ada data untuk emiten '{kode_saham}'.")
        return None

    data = data.sort_values(by='PERSEN(%)', ascending=False)
    emiten_name = data['EMITEN'].iloc[0] if 'EMITEN' in data.columns else kode_upper

    G = nx.Graph()

    # Node pusat: Emiten
    total_investors = len(data)
    G.add_node(kode_upper, size=55, color=WARNA_EMITEN,
               title=f"<b>{kode_upper}</b> — {emiten_name}<br>Jumlah pemegang: {total_investors}",
               font={"size": 20, "color": "white", "face": "Inter, sans-serif"})

    # Node cabang: Setiap investor
    for _, row in data.iterrows():
        investor = str(row['INVESTOR'])
        persen = float(row['PERSEN(%)'])
        tipe = str(row.get('TIPE', '-'))
        lf = str(row.get('L/F', '-'))

        node_size = max(10, min(45, persen * 2.5))
        
        # Warna berbeda untuk lokal vs asing
        warna = "#FFD740" if lf.upper() in ['L', 'LOKAL', 'LOCAL'] else "#FF5252"

        tooltip = (
            f"<b>{investor}</b><br>"
            f"Kepemilikan: {persen:.2f}%<br>"
            f"Tipe: {tipe} | {lf}"
        )

        G.add_node(investor, size=node_size, color=warna,
                   title=tooltip,
                   font={"size": 10, "color": "white", "face": "Inter, sans-serif"})

        edge_width = max(1, persen / 3)
        G.add_edge(kode_upper, investor,
                   value=edge_width,
                   title=f"{persen:.2f}%",
                   color=WARNA_EDGE)

    # Render ke HTML
    net = Network(height="750px", width="100%", bgcolor="#0D1117",
                  font_color="white", directed=False)
    net.from_nx(G)
    
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.04
        },
        "solver": "forceAtlas2Based",
        "stabilization": {"iterations": 150}
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "zoomView": true,
        "dragView": true
      },
      "edges": {
        "smooth": {"type": "continuous"},
        "color": {"inherit": false}
      }
    }
    """)

    filename = f"network_emiten_{kode_upper}.html"
    filepath = os.path.join(output_dir, filename)
    net.save_graph(filepath)

    print(f"\n[✓] Network graph berhasil dibuat: {filepath}")
    print(f"    → {total_investors} investor/pemegang saham terhubung ke {kode_upper}")

    try:
        webbrowser.open(os.path.abspath(filepath))
        print("    → File dibuka di browser.")
    except Exception:
        print("    → Silakan buka file HTML di browser secara manual.")

    return filepath
