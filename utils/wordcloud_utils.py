import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
from collections import Counter

# Fungsi untuk membuat wordcloud
def generate_wordcloud(text, title):
    words = text.split()
    word_freq = Counter(words)
    most_common_words = dict(word_freq.most_common(50))

    wordcloud = WordCloud(width=800, height=680, background_color='white', colormap='viridis').generate_from_frequencies(most_common_words)
    st.image(wordcloud.to_array(), caption=title)
    return word_freq

# Gabungkan teks menjadi satu
def get_combined_text_for_wordcloud(df_sub):
    return " ".join(df_sub["cleaned_text"].astype(str).tolist())

# Diagram batang kata paling sering muncul
def generate_bar_chart(word_freq):
    word_freq = Counter(word_freq)
    most_common_10_words = list(word_freq.most_common(10))
    words, counts = zip(*most_common_10_words)
    df_bar = pd.DataFrame({'Kata': words, 'Frekuensi': counts})

    chart = alt.Chart(df_bar).mark_bar().encode(
        x=alt.X('Kata:N', title='Kata', sort='-y', axis=alt.Axis(labelAngle=0, labelFontSize=12, labelOverlap=True)),
        y=alt.Y('Frekuensi:Q', title='Frekuensi'),
        color=alt.Color('Kata:N').legend(None),
        tooltip=['Kata', 'Frekuensi']
    ).properties(
        width='container',
        height=250
    )

    st.altair_chart(chart, use_container_width=True)

# CSS responsif untuk layout 4 kolom → 1 kolom di HP
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
        overflow-x: auto !important;
    }
    .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }
    .st-emotion-cache-1avcm0n {  /* Streamlit column wrapper */
        width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# Fungsi utama tampilkan
def tampilkan_wordcloud(df):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        with st.container(border=True):
            st.markdown('<h5>📊 Semua Sentimen</h5>', unsafe_allow_html=True)
            all_text = get_combined_text_for_wordcloud(df)
            word_freq_all = generate_wordcloud(all_text, "WordCloud Semua Sentimen")

    with col2:
        with st.container(border=True):
            st.markdown('<h5>😄 Sentimen Pro</h5>', unsafe_allow_html=True)
            pro_text = get_combined_text_for_wordcloud(df[df["Label"] == "Pro"])
            word_freq_pro = generate_wordcloud(pro_text, "WordCloud Sentimen Pro")

    with col3:
        with st.container(border=True):
            st.markdown('<h5>😠 Sentimen Kontra</h5>', unsafe_allow_html=True)
            kontra_text = get_combined_text_for_wordcloud(df[df["Label"] == "Kontra"])
            word_freq_kontra = generate_wordcloud(kontra_text, "WordCloud Sentimen Kontra")

    with col4:
        with st.container(border=True):
            st.markdown('<h5>📊 10 Kata Paling Sering Muncul</h5>', unsafe_allow_html=True)
            word_freq_combined = word_freq_pro + word_freq_kontra
            generate_bar_chart(word_freq_combined)
