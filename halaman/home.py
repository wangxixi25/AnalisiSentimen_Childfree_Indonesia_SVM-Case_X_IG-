import streamlit as st
import pandas as pd
import plotly.express as px
import base64


def run():
    from streamlit_option_menu import option_menu

    # ===== Fungsi untuk convert gambar ke base64 =====
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # ===== Load Data =====
    df = pd.read_excel("data/Hasil_data_pre.xlsx")

    # ===== Header Image =====
    img_base64 = get_base64_image("asset/Gambar2.png")

    # ===== CSS Header =====
    st.markdown(
    f"""
    <style>
        .header-container {{
            background-color: #4285F4;
            padding: 60px 50px;
            display: flex;
            flex-direction: column;
            gap: 40px;
            margin-bottom: 40px;
            color: white;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 60px;
            flex-wrap: wrap;
        }}
        .header-text {{
            flex: 2;
        }}
        .header-text h1 {{
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 12px;
            color: #FFFFFF;
        }}
        .header-subtitle {{
            font-size: 16px;
            line-height: 1.5;
            margin-top: 8px;
            color: #E5E7EB; /* putih keabu-abuan */
        }}
        .header-image {{
            flex: 2;
            max-width: 500px;
        }}
        .header-image img {{
            width: 100%;
            max-height: 500px;
            height: auto;
        }}
    </style>

    <div class="header-container">
        <div class="header-top">
            <div class="header-text">
                <h1>Fenomena Childfree di Platform Media Sosial X dan Instagram</h1>
                <p class="header-subtitle">
                    Pilihan untuk hidup tanpa anak atau childfree menjadi sorotan di media sosial, yang mencerminkan pergeseran nilai dan prioritas hidup generasi muda. Visualisasi ini menyajikan analisis opini publik dari platform X dan Instagram selama tahun 2021–2024 menggunakan metode klasifikasi Support Vector Machine.
                </p>
            </div>
            <div class="header-image">
                <img src="data:image/png;base64,{img_base64}" />
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

    # ===== CSS Deskripsi =====
    st.markdown(
        """
        <style>
            .header {
                font-size: 30px; 
                margin-bottom: 5px;
            }
            .custom-hr {
                border: 3px solid #313552;
                width: 500px;
                margin-top: 5px;
                margin-bottom: 20px;
                margin-left: 0;
            }
            .justify-text {
                text-align: justify;
                text-justify: inter-word;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ===== Judul & Deskripsi =====
    st.markdown(
        '<h3 class="header"><strong>Munculnya Isu Childfree di Media Sosial</strong></h3>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="justify-text">
        Childfree adalah keputusan individu atau pasangan untuk tidak memiliki anak. 
        Fenomena ini semakin populer karena pengaruh globalisasi, budaya Barat, serta gerakan feminisme 
        yang menekankan hak perempuan untuk memilih. Faktor ekonomi dan kesehatan mental juga menjadi pertimbangan, 
        dimana biaya hidup tinggi dan stres saat mengasuh anak sering dijadikan alasan. 
        Di Indonesia, program "Dua Anak Cukup" dari BKKBN mendorong masyarakat untuk membatasi jumlah anak, 
        yang turut membuka ruang bagi pilihan childfree. 
        Fenomena ini ramai di media sosial sejak 2021, kemudian semakin trend kembali pada 2023, 
        hal ini dikarenakan setelah publik figur seperti Gita Savitri mengungkapkan pilihan hidup mereka untuk tidak memiliki anak. 
        Menurut data Badan Pusat Statistik, sekitar 8% perempuan Indonesia memilih untuk tidak memiliki anak, 
        dengan 71.000 di antaranya mendukung fenomena childfree. 
        Walaupun mendapat resistensi dari nilai-nilai tradisional, penggunaan media sosial sebagai ruang diskusi 
        terbuka telah membuat masyarakat menjadi lebih menerima childfree sebagai pilihan hidup yang sah.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===== CSS Card Pro & Kontra =====
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
        <style>
            .card-container {
                display: flex;
                justify-content: center;
                gap: 30px; 
                margin-top: 20px;
                margin-bottom: 20px;
                flex-wrap: wrap; 
            }
            .card {
                border-radius: 10px;
                margin-bottom: 20px;
                padding: 20px;
                color: #FFFFFF;         
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                width: 600px;
            }
            .card.pro {
                background-color: #4CAF50;
            }
            .card.kontra {
                background-color: #FF4C4C;
            }
            .card h3 {
                margin-top: 0;
                margin-bottom: 5px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .card p {
                font-size: 15px;
                line-height: 1.5;
                text-align: justify;
            }
            .bi {
                font-size: 22px;
                color: #FFFFFF;
            }
        </style>

        <div class="card-container">
            <div class="card pro">
                <h3><i class="bi bi-emoji-smile-fill"></i>Pro</h3>
                <p>Pandangan yang mendukung childfree, seperti menganggapnya sebagai pilihan hidup yang baik, rasional, atau memberikan kebebasan lebih.</p>
            </div>
            <div class="card kontra">
                <h3><i class="bi bi-emoji-angry-fill"></i>Kontra</h3>
                <p>Pandangan yang menentang childfree, seperti menganggapnya sebagai pilihan yang salah, egois, atau bertentangan dengan norma sosial.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===== Diagram Pie =====
    df["Pro"] = df["Label"].apply(lambda x: 1 if x == "Pro" else 0)
    df["Kontra"] = df["Label"].apply(lambda x: 1 if x == "Kontra" else 0)
    data = df[["Pro", "Kontra"]].sum().reset_index(name="value")
    data.columns = ["label", "value"]
    pie_data = data.copy()
    pie_data["percent"] = (pie_data["value"] / pie_data["value"].sum() * 100).round(1)

    fig_pie = px.pie(
        pie_data,
        names="label",
        values="value",
        color="label",
        color_discrete_map={"Pro": "#A1C398", "Kontra": "#FF6868"},
        hole=0.4,
    )

    fig_pie.update_traces(textinfo="percent+label", textfont_size=14)
    fig_pie.update_layout(
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(t=20, b=0),
        width=350,
        height=250,
    )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### Data Childfree Indonesia (Instagram & X, 2021–2024)")
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown(
                """
                <div style="font-size: 15px; color: #374151; margin-top: 4px;">
                    Mayoritas masyarakat Indonesia memilih untuk childfree sebesar <strong>67,8%</strong> dan sisanya memilih untuk memiliki anak.
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        with st.container(border=True):
            st.markdown("### Kesimpulan Alasan Pro dan Kontra")
            st.markdown(
                """
                <div style="margin-bottom:35px;">
                    <div style="font-size:16px; font-weight:bold; margin-bottom:6px;">Alasan Pro</div>
                        <p style="text-align: justify; font-size: 14px;">
                            Banyak yang mendukung pilihan hidup childfree karena mereka merasa prinsip hidup yang mengutamakan kebebasan pribadi dan kualitas hidup lebih penting daripada mengikuti norma sosial tradisional.
                            Selain itu, tingginya biaya hidup membuat banyak orang memilih childfree sebagai langkah yang lebih bijak secara finansial.
                        </p>
                </div>
                <div>
                    <div style="font-size:16px; font-weight:bold; margin-bottom:6px;">Alasan Kontra</div>
                        <p style="text-align: justify; font-size: 14px;">
                            Sebagian masyarakat menentang gaya hidup childfree karena alasan agama yang mengajarkan pentingnya melanjutkan keturunan sebagai bagian dari ibadah.
                            Ada pula pandangan budaya yang menganggap memiliki anak sebagai kewajiban sosial dan nilai keluarga yang harus dijaga.
                        </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
