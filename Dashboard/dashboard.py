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
# Menggunakan relative path alih-alih absolute path
file_path = "data.csv"
rfm_path = "customer_segmentation.csv"

df, df_rfm = None, None  # Inisialisasi variabel untuk menghindari error

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    st.warning("⚠️ Data utama tidak ditemukan. Dashboard tetap berjalan tanpa dataset utama.")

if os.path.exists(rfm_path):
    df_rfm = pd.read_csv(rfm_path)
else:
    st.warning("⚠️ Data segmentasi customer tidak ditemukan. Beberapa fitur mungkin tidak tersedia.")

# ========================== #
# 🔹 Header Dashboard 🔹 #
# ========================== #
st.markdown("<h1 style='text-align: center;'>🚲 Bike Sharing & Customer Segmentation 📊</h1>", unsafe_allow_html=True)

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

# Menambahkan visualisasi data bike sharing jika dataset tersedia
if df is not None:
    st.markdown("---")
    st.subheader("📈 Analisis Data Bike Sharing")
    
    # Visualisasi 1: Total penggunaan sepeda berdasarkan waktu (jika kolom tanggal tersedia)
    if 'date' in df.columns or 'dteday' in df.columns:
        date_col = 'date' if 'date' in df.columns else 'dteday'
        df[date_col] = pd.to_datetime(df[date_col])
        df['month'] = df[date_col].dt.month
        df['year'] = df[date_col].dt.year
        
        # Agregasi berdasarkan bulan dan tahun
        if 'cnt' in df.columns:  # Kolom jumlah total penyewaan
            monthly_usage = df.groupby(['year', 'month'])['cnt'].sum().reset_index()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            plt.plot(range(len(monthly_usage)), monthly_usage['cnt'], marker='o', linestyle='-')
            plt.title('Total Penggunaan Sepeda per Bulan')
            plt.xlabel('Month-Year Index')
            plt.ylabel('Jumlah Penyewaan')
            plt.grid(True, alpha=0.3)
            st.pyplot(fig)
    
    # Visualisasi 2: Distribusi penggunaan sepeda berdasarkan season/musim (jika kolom season tersedia)
    if 'season' in df.columns and 'cnt' in df.columns:
        # Mapping nilai numerik season ke label yang lebih deskriptif
        season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
        if df['season'].dtype == 'int64' or df['season'].dtype == 'float64':
            df['season_name'] = df['season'].map(season_mapping)
        else:
            df['season_name'] = df['season']
            
        season_usage = df.groupby('season_name')['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=season_usage, x='season_name', y='cnt', palette='viridis', ax=ax)
        ax.set_xlabel('Musim')
        ax.set_ylabel('Total Penyewaan')
        ax.set_title('Total Penggunaan Sepeda Berdasarkan Musim')
        plt.xticks(rotation=0)
        st.pyplot(fig)
    
    # Visualisasi 3: Perbandingan penyewaan sepeda berdasarkan hari dalam seminggu (jika tersedia)
    if 'weekday' in df.columns and 'cnt' in df.columns:
        # Mapping nilai numerik weekday ke label hari
        weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
        if df['weekday'].dtype == 'int64' or df['weekday'].dtype == 'float64':
            df['weekday_name'] = df['weekday'].map(weekday_mapping)
        else:
            df['weekday_name'] = df['weekday']
            
        weekday_usage = df.groupby('weekday_name')['cnt'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=weekday_usage, x='weekday_name', y='cnt', palette='muted', ax=ax)
        ax.set_xlabel('Hari')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_title('Rata-rata Penggunaan Sepeda Berdasarkan Hari')
        plt.xticks(rotation=30)
        st.pyplot(fig)

# ========================== #
# 🔹 File Uploader untuk Upload Data 🔹 #
# ========================== #
st.markdown("---")
st.subheader("📤 Upload Data")
st.write("Jika data tidak tersedia, Anda dapat mengupload file CSV secara langsung:")

uploaded_file = st.file_uploader("Upload file CSV data bike sharing", type="csv", key="bike_data")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data berhasil diupload!")
    st.dataframe(df.head())

uploaded_rfm = st.file_uploader("Upload file CSV segmentasi customer", type="csv", key="rfm_data")
if uploaded_rfm is not None:
    df_rfm = pd.read_csv(uploaded_rfm)
    st.success("✅ Data segmentasi berhasil diupload!")
    st.dataframe(df_rfm.head())

# ========================== #
# 🔹 Footer Dashboard 🔹 #
# ========================== #
st.markdown("---")
st.markdown("<p style='text-align: center;'> Sandy Tirta Yudha | © 2025</p>", unsafe_allow_html=True)