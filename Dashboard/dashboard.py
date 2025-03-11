import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========================== #
# 🔹 Konfigurasi Dashboard 🔹 #
# ========================== #
st.set_page_config(
    page_title="Bike Sharing & Customer Segmentation Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ========================== #
# 🔹 Membaca Dataset 🔹 #
# ========================== #
file_path = "D:/Submission/Dashboard/data.csv"
rfm_path = "D:/Submission/Dashboard/customer_segmentation.csv"

try:
    df = pd.read_csv(file_path)
    st.success("✅ Dataset berhasil dimuat!")
except FileNotFoundError:
    st.error(f"❌ File '{file_path}' tidak ditemukan. Periksa kembali lokasi file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")
    st.stop()

try:
    df_rfm = pd.read_csv(rfm_path)
    st.success("✅ Dataset RFM berhasil dimuat!")
except FileNotFoundError:
    st.error(f"❌ File '{rfm_path}' tidak ditemukan. Periksa kembali lokasi file!")
    st.stop()
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat membaca file: {e}")
    st.stop()

# ========================== #
# 🔹 Header Dashboard 🔹 #
# ========================== #
st.markdown("<h1 style='text-align: center;'>🚲 Bike Sharing & Customer Segmentation 📊</h1>", unsafe_allow_html=True)

# ========================== #
# 🔹 Filter Data 🔹 #
# ========================== #
st.sidebar.header("🔎 Filter Data")
segment_options = df_rfm['Customer_Segment'].unique().tolist()
selected_segment = st.sidebar.multiselect("Pilih Segmentasi Customer", segment_options, default=segment_options)

# ========================== #
# 🔹 Tabel Segmentasi Customer 🔹 #
# ========================== #
st.subheader("📋 Tabel Segmentasi Customer")

# Filter berdasarkan pilihan pengguna
filtered_df = df_rfm[df_rfm['Customer_Segment'].isin(selected_segment)]
st.dataframe(filtered_df.head(10))  # Menampilkan 10 data pertama

# ========================== #
# 🔹 Visualisasi Distribusi Customer 🔹 #
# ========================== #
st.subheader("👥 Distribusi Customer Berdasarkan Segmentasi RFM")

# Mengecek apakah kolom 'Customer_Segment' tersedia
df_rfm['Customer_Segment'] = df_rfm['Customer_Segment'].astype(str)  # Pastikan format teks
customer_count = df_rfm['Customer_Segment'].value_counts().reset_index()
customer_count.columns = ["Segment", "Jumlah Customer"]

# Membuat visualisasi
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=customer_count, x="Segment", y="Jumlah Customer", palette="pastel", ax=ax)
ax.set_xlabel("Kategori Customer")
ax.set_ylabel("Jumlah Customer")
ax.set_title("Distribusi Customer Berdasarkan Segmentasi RFM")
plt.xticks(rotation=30)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# ========================== #
# 🔹 Statistik Ringkasan 🔹 #
# ========================== #
st.sidebar.subheader("📊 Statistik Ringkasan")

# Menampilkan jumlah total customer per segment jika kolom "Customer_ID" ada
if "Customer_ID" in df_rfm.columns:
    total_customer = df_rfm.groupby("Customer_Segment")["Customer_ID"].count().reset_index()
    total_customer.columns = ["Segment", "Total Customer"]
    st.sidebar.write("Total Customer per Segmentasi:")
    st.sidebar.dataframe(total_customer)

# ========================== #
# 🔹 Footer Dashboard 🔹 #
# ========================== #
st.markdown("---")
st.markdown("<p style='text-align: center;'> Sandy Tirta Yudha | © 2025</p>", unsafe_allow_html=True)