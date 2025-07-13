import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
from collections import Counter

# Fungsi untuk membuat wordcloud
def generate_wordcloud(text, title):
    words = text.split()
    word_freq = Counter(words)
    most_common_words = dict(word_freq.most_common(50))  # Ambil 50 kata teratas

    # Membuat WordCloud
    wordcloud = WordCloud(width=800, height=680, background_color='white', colormap='viridis').generate_from_frequencies(most_common_words)

    # Plot WordCloud
    st.image(wordcloud.to_array(), caption=title)  # Display wordcloud directly in streamlit as image

    return word_freq  # Mengembalikan word_freq untuk digunakan pada diagram batang

# Fungsi untuk menggabungkan teks menjadi satu string untuk wordcloud
def get_combined_text_for_wordcloud(df_sub):
    return " ".join(df_sub["cleaned_text"].astype(str).tolist())  # Gabungkan seluruh teks dari dataset

# Fungsi untuk membuat diagram batang vertikal untuk 10 kata paling sering muncul
def generate_bar_chart(word_freq):
    word_freq = Counter(word_freq)
    most_common_10_words = list(word_freq.most_common(10))
    words, counts = zip(*most_common_10_words)
    df_bar = pd.DataFrame({'Kata': words, 'Frekuensi': counts})

    chart = alt.Chart(df_bar).mark_bar().encode(
       x=alt.X('Kata:N', title='Kata', sort='-y', axis=alt.Axis(labelAngle=0, labelOverlap=False)),  # sort='-y' → Urutkan dari besar ke kecil
        y=alt.Y('Frekuensi:Q', title='Frekuensi'),
        color=alt.Color('Kata:N').legend(None),  # Hilangkan legend
        tooltip=['Kata', 'Frekuensi']
    ).properties(
        width=800,
        height=250
    )

    st.altair_chart(chart, use_container_width=True)

# Fungsi utama untuk menampilkan wordcloud
    st.markdown("""
    <style>
    @media only screen and (max-width: 768px) {
        .element-container .stMarkdown h5 {
            font-size: 14px !important;
            text-align: center;
        }
        .stImage img {
            width: 100% !important;
            height: auto !important;
        }
        .stAltairChart {
            width: 100% !important;
            overflow-x: scroll !important;
        }
        .block-container {
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def tampilkan_wordcloud(df):
    # === Layout Wordcloud 4 Kolom ===
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        with st.container(border=True):
            st.markdown('<h5>📊 Semua Sentimen</h5>', unsafe_allow_html=True)
            all_text = get_combined_text_for_wordcloud(df)  # Menggunakan df asli untuk semua data
            word_freq_all = generate_wordcloud(all_text, "WordCloud Semua Sentimen")

    with col2:
        with st.container(border=True):
            st.markdown('<h5>😄 Sentimen Pro</h5>', unsafe_allow_html=True)
            pro_text = get_combined_text_for_wordcloud(df[df["Label"] == "Pro"])  # Menggunakan df asli untuk "Pro"
            word_freq_pro = generate_wordcloud(pro_text, "WordCloud Sentimen Pro")

    with col3:
        with st.container(border=True):
            st.markdown('<h5>😠 Sentimen Kontra</h5>', unsafe_allow_html=True)
            kontra_text = get_combined_text_for_wordcloud(df[df["Label"] == "Kontra"])  # Menggunakan df asli untuk "Kontra"
            word_freq_kontra = generate_wordcloud(kontra_text, "WordCloud Sentimen Kontra")

    with col4:
        with st.container(border=True):
            st.markdown('<h5>📊 10 Kata Paling Sering Muncul</h5>', unsafe_allow_html=True)
            # Gabungkan frekuensi kata dari semua sentimen untuk diagram batang
            word_freq_combined = word_freq_pro + word_freq_kontra  # Menambahkan frekuensi kata
            generate_bar_chart(word_freq_combined)  # Menampilkan diagram batang untuk keseluruhan dataset
