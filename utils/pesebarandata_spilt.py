import pandas as pd
import plotly.graph_objects as go

def display_graphs(df, st):
    # Warna untuk setiap Teknik Imbalance
    colors_pro = "#A1C398"  # Warna untuk Pro (pastikan ini adalah string, bukan tuple)
    colors_kontra = "#FF6868"  # Warna untuk Kontra (pastikan ini adalah string, bukan tuple)

    # Membuat layout 2x2 untuk menampilkan grafik
    col1, col2 = st.columns(2)  # Membagi layar menjadi dua kolom untuk bagian atas
    col3, col4 = st.columns(2)  # Membagi layar menjadi dua kolom untuk bagian bawah

    # Fungsi untuk menggambar grafik
    def plot_bar_graph(scenario, filtered_data, col):
        # Membuat diagram batang dengan Plotly
        fig = go.Figure()

        bar_width = 0.35  # Lebar bar
        gap = 0.37  # Gap lebih besar antara Pro dan Kontra
        
        # Bar untuk Data Training Pro
        fig.add_trace(go.Bar(
            x=filtered_data['Teknik Imbalance Numeric'] - gap / 2,  # Menggeser sedikit agar berada di tengah
            y=filtered_data['Data Training Pro'],
            name="Pro",  # Hanya menampilkan 'Pro' di legend
            marker_color=colors_pro,  # Gunakan warna yang sudah didefinisikan
            width=bar_width,
            text=filtered_data['Data Training Pro'],  # Display values inside the bars
            textposition='inside',  # Place the text inside the bars
            insidetextanchor='middle'  # Ensure the text is centered inside
        ))

        # Bar untuk Data Training Kontra (diberikan sedikit offset pada x agar ada gap)
        fig.add_trace(go.Bar(
            x=filtered_data['Teknik Imbalance Numeric'] + gap / 2,  # Menggeser sedikit agar berada di tengah
            y=filtered_data['Data Training Kontra'],
            name="Kontra",  # Hanya menampilkan 'Kontra' di legend
            marker_color=colors_kontra,  # Gunakan warna yang sudah didefinisikan
            width=bar_width,
            text=filtered_data['Data Training Kontra'],  # Display values inside the bars
            textposition='inside',  # Place the text inside the bars
            insidetextanchor='middle'  # Ensure the text is centered inside
        ))

        # Menambahkan layout dan judul
        fig.update_layout(
            barmode='group',  # Bar berdampingan
            xaxis_title='Teknik Imbalance',
            yaxis_title='Jumlah Data',
            title=f'Distribusi Data Training Pro dan Kontra untuk Skenario {scenario}',
            height=400,
            xaxis=dict(
                tickmode='array',
                tickvals=filtered_data['Teknik Imbalance Numeric'].unique(),
                ticktext=filtered_data['Teknik Imbalance'].unique(),  # Menampilkan label kategori asli di x-axis
                tickangle=0,  # Menjaga agar label tidak miring
                tickfont=dict(size=12),  # Menyesuaikan ukuran font jika diperlukan
                tickson='labels',  # Pastikan label berada di tengah sumbu
                ticks='inside',  # Menampilkan tanda pada sumbu
                showline=True,  # Menampilkan garis sumbu
                showgrid=True  # Menampilkan grid untuk memudahkan pembacaan
            ),
            xaxis_tickangle=0,  # Tidak miringkan label
        )
        
        # Tampilkan grafik di Streamlit dalam kolom yang sesuai
        col.plotly_chart(fig)

    # Pastikan file memiliki kolom yang sesuai untuk teknik imbalance
    # Loop untuk setiap Skenario Data Split dan plot di kolom yang sesuai
    for i, scenario in enumerate(df['Skenario Data Spilt'].unique()):
        filtered_data = df[df['Skenario Data Spilt'] == scenario]

        # Urutkan teknik imbalance
        order = ["No Imbalance", "SMOTE", "SMOTE TOMEK", "ADASYN"]
        filtered_data['Teknik Imbalance'] = pd.Categorical(filtered_data['Teknik Imbalance'], categories=order, ordered=True)

        # Convert 'Teknik Imbalance' to numeric values for x-axis plotting
        filtered_data['Teknik Imbalance Numeric'] = filtered_data['Teknik Imbalance'].astype('category').cat.codes
        
        # Menampilkan grafik berdasarkan skenario
        if scenario == "90:10":
            plot_bar_graph(scenario, filtered_data, col1)  # Menampilkan di kolom pertama atas
        elif scenario == "80:20":
            plot_bar_graph(scenario, filtered_data, col2)  # Menampilkan di kolom kedua atas
        elif scenario == "70:30":
            plot_bar_graph(scenario, filtered_data, col3)  # Menampilkan di kolom pertama bawah
        elif scenario == "60:40":
            plot_bar_graph(scenario, filtered_data, col4)  # Menampilkan di kolom kedua bawah
