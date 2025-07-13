import os
import joblib
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, ConfusionMatrixDisplay
)
from imblearn.combine import SMOTETomek
import matplotlib.pyplot as plt

# === Membaca data dari Google Sheets ===
url = 'https://docs.google.com/spreadsheets/d/1DFAAHJus_jsRH-hwkqdwA5z8_nn73dAH/edit#gid=1486612404'
path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]

try:
    df = pd.read_excel(path)
    print("Data berhasil dibaca dari Google Sheets.")
except Exception as e:
    print("Gagal membaca data:", e)
    exit()

# === Penanganan Missing Value ===
df['cleaned_text'] = df['cleaned_text'].fillna('')
df = df.dropna(subset=['Label'])

# === Fitur dan Label ===
X = df['cleaned_text']
y = df['Label']

# === TF-IDF Vectorizer sebelum split ===
vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=1500)
X_tfidf = vectorizer.fit_transform(X)

# === Split setelah TF-IDF ===
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.1, random_state=42, stratify=y
)

# === SMOTE-Tomek Oversampling hanya untuk train ===
smote_tomek = SMOTETomek(random_state=42)
X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train, y_train)

# === SVM Training ===
model = SVC(kernel='rbf', C=10, gamma=1, probability=True, random_state=42)
model.fit(X_train_resampled, y_train_resampled)

# === Prediksi dan Evaluasi ===
y_pred = model.predict(X_test)

print("=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=['Kontra', 'Pro']))

# === Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred, labels=['Kontra', 'Pro'])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Kontra', 'Pro'])

# === Simpan gambar confusion matrix ke folder Gambar ===
os.makedirs('Gambar_CM', exist_ok=True)
fig, ax = plt.subplots(figsize=(6, 6))
disp.plot(cmap=plt.cm.Blues, ax=ax)
plt.title("Confusion Matrix SVM RBF")
plt.savefig('Gambar_CM/confusion_matrix_svm_rbf.png', bbox_inches='tight')
plt.close()
print("Confusion matrix disimpan ke 'Gambar_CM/confusion_matrix_svm_rbf.png'")

# === Weighted Average Metrics ===
print("=== Weighted Average Metrics (Semua Kelas) ===")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.2%}")
print(f"Precision (weighted): {precision_score(y_test, y_pred, average='weighted'):.2%}")
print(f"Recall    (weighted): {recall_score(y_test, y_pred, average='weighted'):.2%}")
print(f"F1-Score  (weighted): {f1_score(y_test, y_pred, average='weighted'):.2%}")

# === Simpan Model dan Vectorizer ke folder model/ ===
os.makedirs('model', exist_ok=True)
joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')
joblib.dump(model, 'model/svm_best_model.pkl')
print("Model dan TF-IDF Vectorizer telah disimpan ke folder 'model'.")
