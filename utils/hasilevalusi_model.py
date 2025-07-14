import streamlit as st
import pandas as pd
import plotly.express as px

def tampilkan_grafik_perbandingan_full(file_path):
    df = pd.read_excel(file_path)

    # Ambil dan bersihkan data
    df_clean = df.iloc[1:, [0, 1, 2, 9, 10, 11, 12]]
    df_clean.columns = ['Teknik Imbalance', 'Kernel SVM', 'Skenario Data Split', 'Accuracy', 'Precision', 'Recall', 'F1-score']

    skenarios = ['90:10', '80:20', '70:30', '60:40']

    for i in range(0, len(skenarios), 2):
        cols = st.columns(2)

        for j in range(2):
            if i + j < len(skenarios):
                skenario = skenarios[i + j]
                df_filtered = df_clean[df_clean['Skenario Data Split'] == skenario]

                df_melted = df_filtered.melt(
                    id_vars=['Teknik Imbalance', 'Kernel SVM'],
                    value_vars=['Accuracy', 'Precision', 'Recall', 'F1-score'],
                    var_name='Metric', value_name='Score'
                )

                df_melted['Score'] = df_melted['Score'] * 100
                df_melted['Score_Text'] = df_melted['Score'].apply(lambda x: f"{x:.2f}%")

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
                    margin=dict(t=50, l=30, r=20, b=60),  # ubah b=20 → b=60 agar ada spasi bawah
                    title=f'Skenario Data Split {skenario}',
                    title_font=dict(size=20),
                    title_x=0.0,  # 0.0 = kiri, 0.5 = tengah, 1.0 = kanan
                    legend_title='Kernel SVM',
                    legend_font=dict(size=13),
                )
                fig.update_traces(
                    textposition='inside',
                    textfont_size=14
                )

                fig.for_each_xaxis(lambda x: x.update(
                    title='Metric',
                    tickangle=45,
                    tickfont=dict(size=11),
                    title_font=dict(size=12)
                ))

                fig.for_each_yaxis(lambda y: y.update(
                    tick0=0, dtick=30,range=[0, 90],
                    title_font=dict(size=14)
                ))

                with cols[j]:
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
