import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

# Fungsi untuk load data dan mengecek apakah data kosong
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            st.error("Data kosong! Silakan periksa file.")
            st.stop()  # Menghentikan eksekusi jika data kosong
        return df
    except Exception as e:
        st.error(f"Gagal membaca file data: {e}")
        st.stop()  # Menghentikan aplikasi jika ada error saat load data

# ==== Statistik Sentimen Umum ====
# Fungsi untuk menampilkan statistik sentimen
def tampilkan_kartu_sentimen(jumlah_pro, jumlah_kontra):
    total_data = jumlah_pro + jumlah_kontra  # Menghitung total data
    
    st.markdown(f"""
    <style>
        .card-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}
        .card {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 8px 15px;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            width: 300px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .card i {{
            font-size: 50px;
        }}
        .card h4 {{
            margin: 0;
            font-size: 20px;
        }}
        .card h2 {{
            margin: 0;
            font-size: 28px;
            padding-top: 2px;
        }}
        .card-pro {{ background-color: #4CAF50; }}
        .card-kontra {{ background-color: #f44336; }}
        .card-total {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 8px 15px;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            width: 300px;
            background-color: #FFB22C;
        }}
    </style>
    <div class="card-container">
        <div class="card card-pro">
            <i class="bi bi-emoji-smile-fill"></i>
            <div>
                <h4>Sentimen Pro</h4>
                <h2>{jumlah_pro}</h2>
            </div>
        </div>
        <div class="card card-kontra">
            <i class="bi bi-emoji-angry-fill"></i>
            <div>
                <h4>Sentimen Kontra</h4>
                <h2>{jumlah_kontra}</h2>
            </div>
        </div>
        <div class="card card-total">
            <i class="bi bi-bar-chart-fill"></i>
            <div>
                <h4>Total Data</h4>
                <h2>{total_data}</h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Fungsi untuk menampilkan statistik per platform
def tampilkan_kartu_platform(pro_x, kontra_x, pro_ig, kontra_ig):
    st.markdown("""
    <style>
        .card-outline {
            border: 1px solid #ccc;
            background-color: white;
            color: #333;
            font-size: 14px;
            width: 300px;
            padding: 10px 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        .card-outline i {
            font-size: 30px;
            margin-right: 10px;
        }
        .card-outline h4 {
            margin: 0;
            font-size: 16px;
            color: #666;
        }
        .card-outline h2 {
            margin: 0;
            margin-top: -20px;
            font-size: 22px;
        }
        .card-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
    </style>
    """, unsafe_allow_html=True)

    # HTML untuk kartu sentimen platform
    html_card = f"""
    <div class="card-container">
        <div class="card-outline">
            <h4>
                <i class="bi bi-twitter-x" style="color:#19282F; font-size: 16px; margin-right: 6px;"></i>
                Pro dari X (Twitter)
            </h4>
            <h2 style="margin-left: 25px;">{pro_x}</h2>
        </div>
        <div class="card-outline">
            <h4>
                <i class="bi bi-twitter-x" style="color:#19282F; font-size: 16px; margin-right: 6px;"></i>
                Kontra dari X (Twitter)
            </h4>
            <h2 style="margin-left: 25px;">{kontra_x}</h2>
        </div>
        <div class="card-outline">
            <h4>
                <i class="bi bi-instagram" style="color:#E1306C; font-size: 17px; margin-right: 6px;"></i>
                Pro dari Instagram
            </h4>
            <h2 style="margin-left: 25px;">{pro_ig}</h2>
        </div>
        <div class="card-outline">
            <h4>
                <i class="bi bi-instagram" style="color:#E1306C; font-size: 17px; margin-right: 6px;"></i>
                Kontra dari Instagram
            </h4>
            <h2 style="margin-left: 25px;">{kontra_ig}</h2>
        </div>
    </div>
    """

    # Menampilkan kartu statistik per platform
    st.markdown(html_card, unsafe_allow_html=True)


# Fungsi untuk menampilkan statistik dan grafik di dashboard
def tampilkan_statistik_dashboard(df):
    # Membuat menu dropdown dan checkbox untuk pilihan tahun dan platform
    col1, col3 = st.columns([3, 3])  # col1: filter, col3: ringkasan

    with col1:
        opsi_tampilan = st.selectbox("", ("2021–2024", "2021", "2022", "2023", "2024"))
        tampilkan_tweet = st.checkbox("X (Twitter)", value=True)
        tampilkan_instagram = st.checkbox("Instagram", value=True)

    # **Filter Data berdasarkan Checkbox**
    platform_terpilih = []
    if tampilkan_tweet:
        platform_terpilih.append("Tweet")
    if tampilkan_instagram:
        platform_terpilih.append("Instagram")

    df_filtered = df.copy()
    if opsi_tampilan != "2021–2024":
        df_filtered = df_filtered[df_filtered["Year"] == int(opsi_tampilan)]

    if platform_terpilih:
        df_filtered = df_filtered[df_filtered["Sosmed"].isin(platform_terpilih)]
        warning = False
    else:
        df_filtered = df_filtered.iloc[0:0]  # Kosongkan data jika tidak ada platform dipilih
        warning = True

    # **Hitung data ringkasan**
    total_semua = df_filtered.shape[0]
    total_pro = df_filtered[df_filtered["Label"] == "Pro"].shape[0] if not df_filtered.empty else 0
    total_kontra = df_filtered[df_filtered["Label"] == "Kontra"].shape[0] if not df_filtered.empty else 0
    total_tweet = df_filtered[df_filtered["Sosmed"] == "Tweet"].shape[0] if not df_filtered.empty else 0
    total_ig = df_filtered[df_filtered["Sosmed"] == "Instagram"].shape[0] if not df_filtered.empty else 0

    # **Tampilkan warning jika tidak ada platform dipilih**
    if warning:
        st.warning("Silakan pilih setidaknya satu platform untuk ditampilkan.")

    # **Tampilkan Ringkasan Data**
    with col3:
        st.markdown("""<style>
                .summary-card {
                    border: 1px solid #ccc;
                    padding: 15px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                .summary-card h4 {
                    margin: 0 0 10px 0;
                    font-size: 16px;
                    color: #444;
                }
            </style>""", unsafe_allow_html=True)

        st.markdown(f"""
            <style>
                .summary-card {{
                    border: 1px solid #ccc;
                    padding: 20px 20px;
                    border-radius: 8px;
                    font-size: 15px;
                    margin-bottom: 30px;
                }}
                .summary-row {{
                    display: flex;
                    justify-content: flex-start;
                    margin-bottom: 5px;
                }}
                .summary-row > div {{
                    width: 180px;  /* Atur lebar tetap agar sejajar */
                }}
            </style>
            <div class="summary-card">
                <h4>Ringkasan Data</h4>
                <div class="summary-row">
                    <div>🔍 X (Twitter): <strong>{total_tweet}</strong></div>
                    <div>😄 Pro: <strong style="color:#A1C398;">{total_pro}</strong></div>
                </div>
                <div class="summary-row">
                    <div>🔍 Instagram: <strong>{total_ig}</strong></div>
                    <div>😠 Kontra: <strong style="color:#FF6868;">{total_kontra}</strong></div>
                </div>
                <hr style="border: 0.1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;">
                <div class="summary-row" style="margin-top: 8px;">
                    <div>📊 Jumlah Data: <strong>{total_semua}</strong></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # **Filter Data untuk Grafik**
    df_chart = df[df["Sosmed"].isin(platform_terpilih)] if platform_terpilih else pd.DataFrame({"Year": [], "Label": [], "Jumlah": []})

    # Filter df_chart berdasarkan tahun yang dipilih
    if opsi_tampilan != "2021–2024":
        df_chart = df_chart[df_chart["Year"] == int(opsi_tampilan)]

    # **Cek jika df_chart kosong**
    if df_chart.empty:
        st.warning("Tidak ada data yang sesuai dengan filter tahun dan platform.")
        return

    # **Pemetaan Nama Bulan**
    bulan_mapping = {
        "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
        "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
        "09": "September", "10": "Oktober", "11": "November", "12": "Desember"
    }

    # **Bar Chart Statistik**
    col_kiri, col_kanan = st.columns([4, 2])  # Bar chart lebih lebar

    # **Bar Chart Statistik Tahunan atau Bulanan**
    with col_kiri:
        with st.container(border=True):
            st.markdown('<h5>Statistik Data Childfree Berdasarkan Tahun</h5>', unsafe_allow_html=True)

            chart_width = 800
            chart_height = 350

            # Filter data hingga 2024
            df_chart_filtered = df_chart[df_chart['Year'] <= 2024]

            if opsi_tampilan == "2021–2024":
                if not df_chart_filtered.empty:
                    # Data tahunan
                    data_tahunan = df_chart_filtered.groupby(["Year", "Label"]).size().unstack(fill_value=0)
                    chart = alt.Chart(data_tahunan.reset_index().melt(id_vars='Year', var_name='Label', value_name='Jumlah')).mark_bar().encode(
                        x=alt.X('Year:O', title="Tahun", axis=alt.Axis(labelAngle=0)),
                        y=alt.Y('Jumlah:Q', title="Jumlah"),
                        color=alt.Color('Label:N', scale=alt.Scale(domain=["Pro", "Kontra"], range=["#A1C398", "#FF6868"])),
                        tooltip=['Year', 'Label', 'Jumlah']
                    ).properties(width=chart_width, height=chart_height)
                else:
                    st.warning("Tidak ada data untuk tahun yang dipilih.")

            elif opsi_tampilan in ["2021", "2022", "2023", "2024"]:
                df_tahun = df_chart[df_chart['Year'] == int(opsi_tampilan)]
                if not df_tahun.empty:
                    df_tahun["Label-Bulan"] = df_tahun["Month-Year"].str[:2].map(bulan_mapping)
                    data_bulanan = df_tahun.groupby(["Label-Bulan", "Label"]).size().reset_index(name="Jumlah")

                    # Pastikan semua bulan muncul meskipun datanya kosong
                    bulan_urut = list(bulan_mapping.values())  # Urutan bulan
                    bulan_dummy = pd.DataFrame({
                        "Label-Bulan": bulan_urut * 2,  # Pro dan Kontra
                        "Label": ["Pro"] * 12 + ["Kontra"] * 12,
                        "Jumlah": [0] * 24
                    })

                    # Gabungkan data yang ada dengan bulan yang kosong
                    df_summary = pd.concat([data_bulanan, bulan_dummy], ignore_index=True)
                    df_summary = df_summary.groupby(["Label-Bulan", "Label"]).sum().reset_index()

                    chart = alt.Chart(df_summary).mark_bar().encode(
                        x=alt.X("Label-Bulan:N",
                            title="Bulan",
                            sort=bulan_urut,
                            axis=alt.Axis(labelAngle=0, labelFontSize=10),
                            scale=alt.Scale(domain=bulan_urut)),  # Ini yang memaksa semua bulan tampil
                        y=alt.Y("Jumlah:Q", title="Jumlah"),
                        color=alt.Color("Label:N", scale=alt.Scale(domain=["Pro", "Kontra"], range=["#A1C398", "#FF6868"])),
                        tooltip=["Label-Bulan", "Label", "Jumlah"]
                    ).properties(width=chart_width, height=chart_height)
                else:
                    st.warning(f"Tidak ada data untuk tahun {opsi_tampilan}.")

            else:
                st.warning("Pilihan tampilan tidak dikenali.")

            if 'chart' in locals():
                st.altair_chart(chart, use_container_width=True)

# *Pie Chart Presentase Sentimen*
    with col_kanan:
        with st.container(border=True):  # Border tetap digunakan di container
            st.markdown('<h5>Presentase Sentimen</h5>', unsafe_allow_html=True)

            if df_chart.empty:
                st.warning("Tidak ada data yang sesuai dengan filter.")
            else:
                pie_data = df_chart["Label"].value_counts().reset_index()
                pie_data.columns = ["Label", "Jumlah"]
                fig_pie = px.pie(
                    pie_data,
                    names="Label",
                    values="Jumlah",
                    color="Label",
                    color_discrete_map={"Pro": "#A1C398", "Kontra": "#FF6868"},
                    hole=0.4  # Donut style
                )
                fig_pie.update_traces(textinfo="percent+label")

                fig_pie.update_layout(
                    legend_title="Label",
                    legend=dict(
                        title="Label",
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5
                    ),
                    width=700,
                    height=353
                )

                st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("""
        <style>
        /* MEDIA QUERY: Tampilan khusus untuk layar kecil (HP) */
        @media only screen and (max-width: 768px) {
            .card-container {
                flex-direction: column !important;
                align-items: center !important;
            }

            .card, .card-outline, .summary-card {
                width: 95% !important;            /* ubah dari 100% → 95% */
                margin-bottom: 8px !important;
                padding: 10px 14px !important;     /* sedikit lebih ramping */
                font-size: 13px !important;        /* ubah dari 14px */
            }

            .summary-row > div {
                width: 100% !important;
                margin-bottom: 5px !important;
            }

            .custom-title {
                font-size: 18px !important;
                padding: 16px 8px !important;
            }

            .center-header {
                font-size: 17px !important;
            }

            .scrollable-table {
                max-height: 250px !important;
                font-size: 11px !important;
            }

            .stSelectbox > div {
                font-size: 13px !important;
            }

            .stPlotlyChart {
                height: auto !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)

