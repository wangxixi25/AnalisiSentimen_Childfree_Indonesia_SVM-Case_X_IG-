import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import nltk
import joblib
import streamlit as st
import os

# Pastikan stopwords sudah didownload
nltk.download('stopwords')

# ========== Load Kamus Normalisasi ==========
# Tentukan base directory dan path file Excel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kamus_path = os.path.join(BASE_DIR, "data", "kamuskatabaku.xlsx")
stopwords_path = os.path.join(BASE_DIR, "data", "stopwords_tambahan.xlsx")

# Load data dari Excel menggunakan path absolut relatif
kamus_df = pd.read_excel(kamus_path).dropna(subset=['tidak_baku', 'kata_baku'])
excel_stopwords = pd.read_excel(stopwords_path).iloc[:, 0].dropna().astype(str).tolist()

# Buat dictionary normalisasi
kamus_normalisasi = dict(zip(kamus_df['tidak_baku'], kamus_df['kata_baku']))

# Load stopwords NLTK, Sastrawi, Excel, dan custom
nltk_stopwords = stopwords.words('indonesian')

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
sastrawi_stopwords = StopWordRemoverFactory().get_stop_words()

excel_stopwords = pd.read_excel("data/stopwords_tambahan.xlsx").iloc[:, 0].dropna().astype(str).tolist()

custom_stopwords = [
    'banget', 'aja', 'kok', 'nih', 'ya', 'deh', 'lah', 'dong', 'mah',
    'tau', 'gitu', 'btw', 'cmn', 'cm', 'jd', 'gw', 'gue', 'lu', 'loe',
    'loh', 'sih', 'yaudah', 'udah', 'dah', 'masa', 'wkwk', 'wkwwk', 'haha',
    'lol', 'lmao', 'ampun', 'anjay', 'anjir', 'buset', 'parah', 'fix',
    'bang', 'mbak', 'bro', 'sis', 'woy', 'cuy', 'oi', 'yee', 'yaa',
    'hadeh', 'huh', 'hadehh', 'cie', 'ciee', 'ehh', 'yaa', 'yhaa', 'santai',
    'okeh', 'ok', 'oke', 'sip', 'mantap', 'mantul', 'nggak', 'ngga', 'ga',
    'dikit', 'gak', 'iyaa', 'iyaaah', 'hmmm', 'hmm', 'yakin', 'lahh',
    'lho', 'eaa','iya', 'nderr','nder', 'gita','gitasav','gitasap','si' ,'lo', 'aka', 'yes', 'i', 'is', 'anjg'
]

all_stopwords = set(nltk_stopwords + sastrawi_stopwords + excel_stopwords + custom_stopwords)

# Kata penting yang harus dilindungi agar tidak terhapus
protected_words = {'alasan', 'jangan', 'tujuan', 'setuju', 'tidak', 'melihat', 'keturunan', 'berketurunan', 'menikah', 'nikah', 'gerakan', 'ingat'}
for w in protected_words:
    all_stopwords.discard(w)

# Stemmer
stemmer = StemmerFactory().create_stemmer()

def preprocess(text):
    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            return ''
    text = text.lower()

    # 2. Cleansing
    text = re.sub(r'https?://\S+|www\.\S+', '', text)     # Hapus URL
    text = re.sub(r'@\w+', '', text)                      # Hapus mention
    text = text.replace('-', ' ')                          # Ganti - dengan spasi
    text = re.sub(r'[^\w\s]', '', text)                   # Hapus simbol
    text = re.sub(r'\d+', '', text)                        # Hapus angka
    text = ''.join(char for char in text if ord(char) < 128)  # Hapus non-ASCII
    text = re.sub(r'\s+', ' ', text).strip()              # Hapus spasi berlebih

    # 3. Tokenizing sederhana dengan split (bisa diganti word_tokenize jika mau)
    tokens = text.split()

    # 4. Normalisasi kata tidak baku ke baku
    tokens = [kamus_normalisasi.get(word, word) for word in tokens]

    # 5. Stopword Removal (kecuali protected words)
    tokens = [word for word in tokens if word not in all_stopwords]

    # 6. Stemming dengan perlindungan kata penting
    tokens = [word if word in protected_words else stemmer.stem(word) for word in tokens]

    # Gabungkan kembali jadi kalimat
    return ' '.join(tokens)


# ========== Load Model & Vectorizer ==========
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
model = joblib.load('models/svm_best_model.pkl')

# ========== Streamlit App ==========
def run():
    st.title("Analisis Sentimen Childfree: Pro vs Kontra")

    user_input = st.text_area(
        "Tulis kalimatmu di sini (Contoh: 'Aku sih mendukung Gerakan Childfree')", 
        "Aku sih mendukung Gerakan Childfree"
    )

    if st.button("Uji Kalimat"):

        if user_input.strip() == "":
            st.warning("⚠️ Masukkan kalimat terlebih dahulu.")
            return

        try:
            # Preprocessing
            cleaned_input = preprocess(user_input)
            vectorized_input = vectorizer.transform([cleaned_input])

            # Prediksi
            probabilities = model.predict_proba(vectorized_input)
            pro = probabilities[0][1] * 100
            kontra = probabilities[0][0] * 100
            result = "Pro" if pro > kontra else "Kontra"

            # Output
            st.subheader(f"🔍 Hasil Prediksi: {result} (Childfree)")
            st.write(f"😄 Probabilitas Pro: {pro:.2f}%")
            st.write(f"😠 Probabilitas Kontra: {kontra:.2f}%")
            # st.caption(f"🧼 Kalimat setelah preprocessing: *{cleaned_input}*")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses: {e}")