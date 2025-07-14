import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils.statistik_data import load_data, tampilkan_kartu_sentimen, tampilkan_kartu_platform, tampilkan_statistik_dashboard
from utils.wordcloud_utils import tampilkan_wordcloud
from utils.pesebarandata_spilt import display_graphs
from utils.hasilevalusi_model import tampilkan_grafik_perbandingan_full, tampilkan_akurasi_terbaik


def run():
        # ==== Style & CSS ====
        BOOTSTRAP_CDN = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
        """
        PADDING_STYLE = '<style>div.block-container{padding-top:1rem;}</style>'
        TITLE_STYLE = """
        <style>
        .custom-title {
            background-color: #4285F4;
            padding: 50px;
            text-align: center;
            border-bottom-left-radius: 25px;
            border-bottom-right-radius: 25px;
            font-size: 30px;
            font-weight: bold;
            color: #EEEEEE;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="custom-title">
            Dashboard Analisis Sentimen Fenomena Childfree di Media Sosial X dan Instagram
        </div>
        """

        # Render style
        st.markdown(BOOTSTRAP_CDN, unsafe_allow_html=True)
        st.markdown(PADDING_STYLE, unsafe_allow_html=True)
        st.markdown(TITLE_STYLE, unsafe_allow_html=True)

        # Load data dari 'Hasil_data_pre.xlsx'
        df = load_data("data/Hasil_Data_Pre.xlsx")
        if df.empty:
            st.stop() 
        
        # Hitung jumlah sentimen Pro dan Kontra
        jumlah_pro = (df["Label"] == "Pro").sum()
        jumlah_kontra = (df["Label"] == "Kontra").sum()

        # Menampilkan Kartu Sentimen
        tampilkan_kartu_sentimen(jumlah_pro, jumlah_kontra)

        # Menampilkan Statistik per Platform
        pro_x = df[(df["Label"] == "Pro") & (df["Sosmed"] == "Tweet")].shape[0]
        kontra_x = df[(df["Label"] == "Kontra") & (df["Sosmed"] == "Tweet")].shape[0]
        pro_ig = df[(df["Label"] == "Pro") & (df["Sosmed"] == "Instagram")].shape[0]
        kontra_ig = df[(df["Label"] == "Kontra") & (df["Sosmed"] == "Instagram")].shape[0]

        # Menampilkan Kartu Platform
        tampilkan_kartu_platform(pro_x, kontra_x, pro_ig, kontra_ig)

        # ==== Chart Statistik ==== 
        st.markdown("""<style>.center-header { text-align: center; font-size: 30px; }</style>""", unsafe_allow_html=True)
        st.markdown('<h3 class="center-header"><strong>Statistik Sentimen Childfree di Indonesia</strong></h3>', unsafe_allow_html=True)

        st.markdown("""<style>.custom-hr { border: 3px solid #313552; width: 300px; margin-bottom: 40px; margin-left: auto; margin-right: auto; }</style>""", unsafe_allow_html=True)
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

        # Menampilkan Statistik Dashboard
        tampilkan_statistik_dashboard(df)

        # ==== Wordcloud ====
        st.markdown("""<style>.center-header { text-align: center; font-size: 30px; }</style>""", unsafe_allow_html=True)
        st.markdown('<h3 class="center-header"><strong>Wordcloud Sentimen Childfree di Indonesia</strong></h3>', unsafe_allow_html=True)
        st.markdown("""<style>.custom-hr { border: 3px solid #313552; width: 300px; margin-bottom: 40px; margin-left: auto; margin-right: auto; }</style>""", unsafe_allow_html=True)
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
        # Tampilkan wordcloud
        tampilkan_wordcloud(df)

       # ==== Grafik Perbandingan Teknik Imbalance ====
        st.markdown("""<style>.center-header { text-align: center; font-size: 28px; }</style>""", unsafe_allow_html=True)
        st.markdown('<h3 class="center-header"><strong>Hasil Evaluasi Model SVM dengan Teknik Imbalance</strong></h3>', unsafe_allow_html=True)
        st.markdown("""<style>.custom-hr { border: 3px solid #313552; width: 300px; margin-bottom: 40px; margin-left: auto; margin-right: auto; }</style>""", unsafe_allow_html=True)
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

        # Menampilkan Grafik Perbandingan Teknik Imbalance
        tampilkan_grafik_perbandingan_full("data/HASIL EVALUASI.xlsx")
        st.header("Akurasi Terbaik")
        try:
            tampilkan_akurasi_terbaik("data/HASIL EVALUASI.xlsx")
        except Exception as e:
            st.warning(f"Terjadi kesalahan saat memuat hasil akurasi terbaik: {e}")

        # ==== MENAMPILKAN DATA SET ====
        st.markdown("""<style>.center-header { text-align: center; font-size: 30px; }</style>""", unsafe_allow_html=True)
        st.markdown('<h3 class="center-header"><strong>Data Sentimen Masyarakat Terkait Childfree di Indonesia</strong></h3>', unsafe_allow_html=True)
        st.markdown("""<style>.custom-hr { border: 3px solid #313552; width: 300px; margin-bottom: 40px; margin-left: auto; margin-right: auto; }</style>""", unsafe_allow_html=True)
        st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
        # Pemetaan Nama Bulan
        bulan_mapping = {
            "01": "Januari", "02": "Februari", "03": "Maret", "04": "April",
            "05": "Mei", "06": "Juni", "07": "Juli", "08": "Agustus",
            "09": "September", "10": "Oktober", "11": "November", "12": "Desember"
        }

        # Menambahkan kolom Bulan dan Tahun, serta Bulan dalam format teks
        df['Bulan'] = df['Month-Year'].str[:2]
        df['Tahun'] = df['Month-Year'].str[-4:]
        df['Bulan-Teks'] = df['Bulan'].map(bulan_mapping)  # Menambahkan kolom Bulan-Teks

        # Membuat kolom 'Bulan/Tahun' yang digabungkan
        df['Bulan-Tahun'] = df['Bulan-Teks'] + ' ' + df['Tahun']

        # Membuat urutan tahun dan bulan berdasarkan kolom 'Month-Year' yang ada
        df['Bulan-Angka'] = df['Bulan'].astype(int)

        # Urutkan berdasarkan Tahun dan Bulan-Angka
        df_sorted = df.sort_values(by=['Tahun', 'Bulan-Angka'])

        # Menambahkan dropdown filter untuk Sosmed dan Sentimen
        sosmed_options = df['Sosmed'].unique().tolist()
        sosmed_options.insert(0, 'Semua')  # Menambahkan opsi 'Semua' di awal daftar

        sentimen_options = ['Semua', 'Pro', 'Kontra']

        # Membuat dua kolom untuk dropdown
        col1, col2 = st.columns(2)

        with col1:
            # Filter dropdown untuk Sosmed
            selected_sosmed = st.selectbox('Pilih Platform Sosmed', sosmed_options)

        with col2:
            # Filter dropdown untuk Sentimen
            selected_sentimen = st.selectbox('Pilih Sentimen', sentimen_options)

        # Filter dataframe berdasarkan pilihan dropdown
        if selected_sosmed != 'Semua':
            df_filtered = df_sorted[df_sorted['Sosmed'] == selected_sosmed]
        else:
            df_filtered = df_sorted

        if selected_sentimen != 'Semua':
            df_filtered = df_filtered[df_filtered['Label'] == selected_sentimen]

        # Reset index dan mulai dari 1
        df_filtered.reset_index(drop=True, inplace=True)
        df_filtered.index += 1  # Mulai indeks dari 1

        # Ganti nama indeks menjadi "No"
        df_filtered.index.name = 'No'

        # Menampilkan Data yang sudah difilter dalam Card dengan Scroll
        st.markdown("""<style>.scrollable-table { max-height: 400px; overflow-y: scroll; }</style>""", unsafe_allow_html=True)
        st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
        st.dataframe(df_filtered[['Bulan-Tahun', 'full_text', 'Label', 'Sosmed']].rename(columns={
            'Bulan-Tahun': 'Bulan/Tahun',
            'full_text': 'Komentar',
            'Sosmed': 'Sosmed',
            'Label': 'Label Pro/Kontra'
        }))
        st.markdown('</div>', unsafe_allow_html=True)
