import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk menampilkan grafik perbandingan penuh
def tampilkan_grafik_perbandingan_full(file_path):
    df = pd.read_excel(file_path)

    # Mengatur kolom dan data untuk perbandingan teknik imbalance
    df_clean = df.iloc[1:, [0, 1, 2, 9, 10, 11, 12]]
    df_clean.columns = ['Teknik Imbalance', 'Kernel SVM', 'Skenario Data Spilt', 'Accuracy', 'Precision', 'Recall', 'F1-score']

    skenarios = ['90:10', '80:20', '70:30', '60:40']

    # Membuat grafik perbandingan untuk setiap skenario
    for i in range(0, len(skenarios), 2):
        col1, col2 = st.columns(2)

        for col, idx in zip([col1, col2], [i, i + 1]):
            if idx < len(skenarios):
                skenario = skenarios[idx]
                with col:
                    st.subheader(f'Skenario: {skenario}')
                    df_filtered = df_clean[df_clean['Skenario Data Spilt'] == skenario]
                    df_melted = df_filtered.melt(
                        id_vars=['Teknik Imbalance', 'Kernel SVM'],
                        value_vars=['Accuracy', 'Precision', 'Recall', 'F1-score'],
                        var_name='Metric', value_name='Score'
                    )
                    df_melted['Score'] = df_melted['Score'] * 100  # Mengonversi ke persen
                    df_melted['Score_Text'] = df_melted['Score'].apply(lambda x: f"{x:.2f}%")  # Format sebagai persentase

                    fig = px.bar(
                        df_melted,
                        x='Metric',
                        y='Score',
                        color='Kernel SVM',
                        barmode='group',
                        text='Score_Text',
                        facet_col='Teknik Imbalance',
                        color_discrete_sequence=["#09B4A2", "#3F63CF", "#EA4590"]
                    )

                    # Hapus label 'Teknik Imbalance=' → agar hanya tampil SMOTE, SMOTE Tomek, ADASYN, dst.
                    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].strip()))

                    fig.update_traces(textfont=dict(size=16))
                    fig.update_layout(
                        height=550,
                        title=f'{skenario}',
                        title_font=dict(size=20),
                        xaxis_title='Metric',
                        yaxis_title='Nilai (%)',
                        xaxis_title_font=dict(size=16),
                        yaxis_title_font=dict(size=16),
                        legend_title='Kernel SVM',
                        legend_font=dict(size=14),
                        margin=dict(t=50, l=20, r=20, b=20)
                    )

                    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk menampilkan Akurasi Terbaik
def tampilkan_akurasi_terbaik(file_path):
    df = pd.read_excel(file_path)

    # Mengatur kolom dan data untuk perbandingan teknik imbalance
    df_clean = df.iloc[1:, [0, 1, 2, 9, 10, 11, 12]]
    df_clean.columns = ['Teknik Imbalance', 'Kernel SVM', 'Skenario Data Spilt', 'Accuracy', 'Precision', 'Recall', 'F1-score']

    best_row = df_clean.loc[df_clean['Accuracy'].astype(float).idxmax()]

    # Siapkan data untuk bar chart Akurasi terbaik
    data_best = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-score'],
        'Score': [
            best_row['Accuracy'] * 100,  # Mengonversi ke persen
            best_row['Precision'] * 100,
            best_row['Recall'] * 100,
            best_row['F1-score'] * 100
        ]
    }
    df_best = pd.DataFrame(data_best)
    df_best['Score_Text'] = df_best['Score'].apply(lambda x: f"{x:.2f}%")  # Format sebagai persentase

    fig_best = px.bar(
        df_best,
        x='Metric',
        y='Score',
        text='Score_Text',
        color='Metric',
        color_discrete_sequence=["#09B4A2", "#3F63CF", "#EA4590", '#FFA500']
    )

    fig_best.update_traces(textposition='outside', textfont_size=14)
    fig_best.update_layout(
        title=f"{best_row['Teknik Imbalance']} | {best_row['Kernel SVM']} | {best_row['Skenario Data Spilt']}",
        title_font=dict(size=18),
        xaxis_title='Metric',
        yaxis_title='Nilai (%)',
        yaxis_range=[0, 110],
        height=400,
        margin=dict(t=50, l=20, r=20, b=20),
        showlegend=False
    )

    st.plotly_chart(fig_best, use_container_width=True)

# Fungsi untuk menampilkan Evaluasi K-Fold menggunakan Line Chart
def tampilkan_evaluasi_kfold(file_path):
    df = pd.read_excel(file_path)
    
    # Memeriksa kolom yang ada dalam data K-Fold
    required_columns = ['Fold', 'Accuracy Fold', 'Precision Fold', 'Recall Fold', 'F1-score Fold']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Kolom berikut tidak ditemukan dalam data K-Fold: {', '.join(missing_columns)}")
        return

    df_folds = df[['Fold', 'Accuracy Fold', 'Precision Fold', 'Recall Fold', 'F1-score Fold']]

    # Menghitung rata-rata untuk setiap metrik K-Fold
    avg_accuracy = df_folds['Accuracy Fold'].mean() * 100  # Mengonversi ke persen
    avg_precision = df_folds['Precision Fold'].mean() * 100
    avg_recall = df_folds['Recall Fold'].mean() * 100
    avg_f1 = df_folds['F1-score Fold'].mean() * 100

    # Membuat grafik line chart untuk setiap metrik K-Fold
    fig_combined = go.Figure()

    # Menambahkan line chart untuk setiap metrik
    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=df_folds['Accuracy Fold'] * 100,  # Mengonversi ke persen
        mode='lines+markers',
        name='Accuracy',
        marker_color='rgb(0, 123, 255)',
        text=df_folds['Accuracy Fold'].apply(lambda x: f"{x * 100:.2f}%"),  # Format sebagai persentase
        textposition='top center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=df_folds['Precision Fold'] * 100,  # Mengonversi ke persen
        mode='lines+markers',
        name='Precision',
        marker_color='rgb(40, 167, 69)',
        text=df_folds['Precision Fold'].apply(lambda x: f"{x * 100:.2f}%"),  # Format sebagai persentase
        textposition='top center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=df_folds['Recall Fold'] * 100,  # Mengonversi ke persen
        mode='lines+markers',
        name='Recall',
        marker_color='rgb(255, 193, 7)',
        text=df_folds['Recall Fold'].apply(lambda x: f"{x * 100:.2f}%"),  # Format sebagai persentase
        textposition='top center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=df_folds['F1-score Fold'] * 100,  # Mengonversi ke persen
        mode='lines+markers',
        name='F1-score',
        marker_color='rgb(255, 69, 0)',
        text=df_folds['F1-score Fold'].apply(lambda x: f"{x * 100:.2f}%"),  # Format sebagai persentase
        textposition='top center'
    ))

    # Menambahkan garis rata-rata untuk setiap metrik
    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=[avg_accuracy] * len(df_folds),
        mode='lines',
        name='Average Accuracy',
        line=dict(color='rgb(0, 123, 255)', dash='dash'),
        text=[f"Avg: {avg_accuracy:.2f}%" for _ in df_folds['Fold']],
        textposition='bottom center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=[avg_precision] * len(df_folds),
        mode='lines',
        name='Average Precision',
        line=dict(color='rgb(40, 167, 69)', dash='dash'),
        text=[f"Avg: {avg_precision:.2f}%" for _ in df_folds['Fold']],
        textposition='bottom center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=[avg_recall] * len(df_folds),
        mode='lines',
        name='Average Recall',
        line=dict(color='rgb(255, 193, 7)', dash='dash'),
        text=[f"Avg: {avg_recall:.2f}%" for _ in df_folds['Fold']],
        textposition='bottom center'
    ))

    fig_combined.add_trace(go.Scatter(
        x=df_folds['Fold'],
        y=[avg_f1] * len(df_folds),
        mode='lines',
        name='Average F1-score',
        line=dict(color='rgb(255, 69, 0)', dash='dash'),
        text=[f"Avg: {avg_f1:.2f}%" for _ in df_folds['Fold']],
        textposition='bottom center'
    ))

    # Update layout
    fig_combined.update_layout(
        title="K-Fold Cross Validation Performance",
        xaxis_title='Fold',
        yaxis_title='Nilai (%)',
        height=500,
        margin=dict(t=50, l=40, r=40, b=40),
        showlegend=True
    )

    st.plotly_chart(fig_combined, use_container_width=True)
