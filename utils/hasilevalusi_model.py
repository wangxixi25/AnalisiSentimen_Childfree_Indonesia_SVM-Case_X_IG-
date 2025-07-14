import streamlit as st
import pandas as pd
import plotly.express as px

def tampilkan_grafik_perbandingan_full(file_path):
    df = pd.read_excel(file_path)

    # Ambil dan bersihkan data
    df_clean = df.iloc[1:, [0, 1, 2, 9, 10, 11, 12]].copy()
    df_clean.columns = ['Teknik Imbalance', 'Kernel SVM', 'Skenario Data Split',
                        'Accuracy', 'Precision', 'Recall', 'F1-score']

    # Hapus baris dengan nilai kosong pada kolom penting
    df_clean = df_clean.dropna(subset=["Teknik Imbalance", "Kernel SVM", "Skenario Data Split"])

    skenarios = ['90:10', '80:20', '70:30', '60:40']

    for i in range(0, len(skenarios), 2):
        cols = st.columns(2)

        for j in range(2):
            if i + j < len(skenarios):
                skenario = skenarios[i + j]
                df_filtered = df_clean[df_clean['Skenario Data Split'] == skenario].copy()

                # Pastikan tidak ada NaN
                df_filtered = df_filtered.dropna(subset=['Accuracy', 'Precision', 'Recall', 'F1-score'])

                # Ubah ke format long
                df_melted = df_filtered.melt(
                    id_vars=['Teknik Imbalance', 'Kernel SVM'],
                    value_vars=['Accuracy', 'Precision', 'Recall', 'F1-score'],
                    var_name='Metric', value_name='Score'
                )

                df_melted['Score'] = df_melted['Score'].astype(float) * 100
                df_melted['Score_Text'] = df_melted['Score'].apply(lambda x: f"{x:.2f}%")
                df_melted['Teknik Imbalance'] = df_melted['Teknik Imbalance'].astype(str).str.strip()

                fig = px.bar(
                    df_melted,
                    x='Metric',
                    y='Score',
                    color='Kernel SVM',
                    text='Score_Text',
                    barmode='group',
                    facet_col='Teknik Imbalance',
                    color_discrete_map={
                        'Linier': '#09B4A2',
                        'RBF': '#3F63CF',
                        'Polynomial': '#EA4590'
                    }
                )

                fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

                fig.update_layout(
                    height=350,
                    margin=dict(t=40, l=30, r=20, b=20),
                    title_font=dict(size=16),
                    title_x=0.0,  # Judul kiri
                    legend_title='Kernel SVM',
                    legend_font=dict(size=13),
                )

                fig.update_traces(
                    textposition='inside',
                    textfont_size=16
                )

                fig.for_each_xaxis(lambda x: x.update(
                    title='Metric',
                    tickangle=45,
                    tickfont=dict(size=11),
                    title_font=dict(size=12)
                ))

                fig.for_each_yaxis(lambda y: y.update(
                    tick0=0, dtick=20, range=[0, 82],
                    title_font=dict(size=14)
                ))

                with cols[j]:
                    st.markdown(f"### Skenario {skenario}", unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True)

    # Tambahan CSS agar responsif di HP
    st.markdown("""
    <style>
    @media only screen and (max-width: 768px) {
        .st-emotion-cache-1avcm0n, .st-emotion-cache-1qg05tj {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        h5 {
            font-size: 16px !important;
            margin-top: 10px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


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
