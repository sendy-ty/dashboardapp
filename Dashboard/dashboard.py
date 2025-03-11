import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========================== #
# 🔹 Konfigurasi Dashboard 🔹 #
# ========================== #
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ========================== #
# 🔹 Membaca Dataset 🔹 #
# ========================== #
# Menggunakan relative path alih-alih absolute path
rfm_path = "customer_segmentation.csv"

df_rfm = None  # Inisialisasi variabel untuk menghindari error

if os.path.exists(rfm_path):
    df_rfm = pd.read_csv(rfm_path)
else:
    st.warning("⚠️ Data segmentasi customer tidak ditemukan. Dashboard tidak dapat menampilkan data.")

# ========================== #
# 🔹 Header Dashboard 🔹 #
# ========================== #
st.markdown("<h1 style='text-align: center;'>🚲 Customer Segmentation Dashboard 📊</h1>", unsafe_allow_html=True)

# ========================== #
# 🔹 Filter Data 🔹 #
# ========================== #
if df_rfm is not None:
    st.sidebar.header("🔎 Filter Data")
    segment_options = df_rfm['Customer_Segment'].unique().tolist()
    selected_segment = st.sidebar.multiselect("Pilih Segmentasi Customer", segment_options, default=segment_options)

    # ========================== #
    # 🔹 Tabel Segmentasi Customer 🔹 #
    # ========================== #
    st.subheader("📋 Tabel Segmentasi Customer")
    filtered_df = df_rfm[df_rfm['Customer_Segment'].isin(selected_segment)]
    st.dataframe(filtered_df.head(10))

    # ========================== #
    # 🔹 Visualisasi Distribusi Customer 🔹 #
    # ========================== #
    st.subheader("👥 Distribusi Customer Berdasarkan Segmentasi RFM")
    df_rfm['Customer_Segment'] = df_rfm['Customer_Segment'].astype(str)
    customer_count = df_rfm['Customer_Segment'].value_counts().reset_index()
    customer_count.columns = ["Segment", "Jumlah Customer"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=customer_count, x="Segment", y="Jumlah Customer", palette="pastel", ax=ax)
    ax.set_xlabel("Kategori Customer")
    ax.set_ylabel("Jumlah Customer")
    ax.set_title("Distribusi Customer Berdasarkan Segmentasi RFM")
    plt.xticks(rotation=30)
    st.pyplot(fig)

# ========================== #
# 🔹 Footer Dashboard 🔹 #
# ========================== #
st.markdown("---")
st.markdown("<p style='text-align: center;'> Sandy Tirta Yudha | © 2025</p>", unsafe_allow_html=True)