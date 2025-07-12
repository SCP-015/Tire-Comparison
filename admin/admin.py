import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import json
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_handler import load_ban_list 

st.set_page_config(page_title="Adminpanel SPK", layout="wide")

# Fungsi untuk menyimpan data ban (simulasi)
def save_ban_data(ban_data):
    """Simpan data ban ke file JSON"""
    try:
        # Baca data existing
        existing_data = load_ban_list()
        
        # Tambah data baru
        existing_data.append(ban_data)
        
        # Simulasi penyimpanan (dalam implementasi nyata, simpan ke file)
        if 'ban_data' not in st.session_state:
            st.session_state['ban_data'] = existing_data
        else:
            st.session_state['ban_data'] = existing_data
        
        return True
    except Exception as e:
        st.error(f"Error menyimpan data: {str(e)}")
        return False

# Fungsi untuk menghapus data ban
def delete_ban_data(index):
    """Hapus data ban berdasarkan index"""
    try:
        if 'ban_data' in st.session_state:
            del st.session_state['ban_data'][index]
        return True
    except Exception as e:
        st.error(f"Error menghapus data: {str(e)}")
        return False

# Fungsi untuk generate data analytics
def generate_analytics_data():
    """Generate data dummy untuk analytics"""
    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    users = [random.randint(10, 50) for _ in range(30)]
    analyses = [random.randint(5, 25) for _ in range(30)]
    
    return {
        'dates': dates,
        'users': users,
        'analyses': analyses
    }

def show_admin_panel():
    st.title("⚙️ Admin Tools")
    st.markdown("Panel administrator untuk mengelola sistem")
    
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False

    if not st.session_state['admin_logged_in']:
        st.warning("🔒 Akses terbatas - Masukkan kredensial admin")
        
        with st.form("admin_login"):
            username = st.text_input("Username:")
            password = st.text_input("Password:", type="password")
            
            if st.form_submit_button("🔐 Login"):
                if username == "admin" and password == "admin123":
                    st.session_state['admin_logged_in'] = True
                    st.success("✅ Login berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
    
    else:
        st.success("✅ Selamat datang, Admin!")
        
        if st.button("🚪 Logout"):
            st.session_state['admin_logged_in'] = False
            st.rerun()
        
        st.markdown("---")
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🛠️ Kelola Data", "📈 Analytics", "⚙️ Settings"])
        
        with tab1:
            st.subheader("📊 Dashboard Admin")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Pengguna", "156", "↗️ +12")
            with col2:
                st.metric("Analisis Hari Ini", "23", "↗️ +5")
            with col3:
                total_reviews = len(st.session_state.get('reviews', [])) + 4
                st.metric("Total Reviews", total_reviews, "↗️ +2")
            with col4:
                st.metric("Sistem Uptime", "99.9%", "🟢 Normal")
            
            st.markdown("---")
            st.subheader("📈 Grafik Penggunaan")
            
            # Generate dan tampilkan grafik
            analytics_data = generate_analytics_data()
            
            # Grafik penggunaan harian dengan native chart
            st.markdown("**📈 Penggunaan Sistem Harian (30 hari terakhir)**")
            df_usage = pd.DataFrame({
                'Tanggal': analytics_data['dates'],
                'Pengguna': analytics_data['users']
            })
            df_usage = df_usage.set_index('Tanggal')
            st.line_chart(df_usage)
            
            # Grafik analisis mingguan
            st.markdown("**📊 Analisis Mingguan Terakhir**")
            df_analysis = pd.DataFrame({
                'Tanggal': analytics_data['dates'][-7:],
                'Analisis': analytics_data['analyses'][-7:]
            })
            df_analysis = df_analysis.set_index('Tanggal')
            st.bar_chart(df_analysis)

        with tab2:
            st.subheader("🛠️ Kelola Data Ban")
            
            # Form untuk menambah ban baru
            with st.expander("➕ Tambah Ban Baru", expanded=False):
                with st.form("add_ban_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        nama_ban = st.text_input("Nama Ban*")
                        merk = st.text_input("Merk/Brand*")
                        ukuran = st.text_input("Ukuran Ban (contoh: 80/90-14)*")
                        harga = st.number_input("Harga (Rp)*", min_value=0, step=10000)
                    
                    with col2:
                        # Kriteria penilaian SPK (sesuaikan dengan sistem Anda)
                        kualitas_ban = st.selectbox("Kualitas Ban", ["Sangat Baik", "Baik", "Cukup", "Kurang"])
                        daya_tahan = st.slider("Daya Tahan (1-10)", 1, 10, 5)
                        grip_jalan = st.slider("Grip/Cengkeram Jalan (1-10)", 1, 10, 5)
                        kenyamanan = st.slider("Kenyamanan (1-10)", 1, 10, 5)
                        ketahanan_cuaca = st.slider("Ketahanan Cuaca (1-10)", 1, 10, 5)
                    
                    keterangan = st.text_area("Keterangan Tambahan")
                    
                    if st.form_submit_button("💾 Simpan Ban"):
                        if nama_ban and merk and ukuran and harga:
                            new_ban = {
                                "nama": nama_ban,
                                "merk": merk,
                                "ukuran": ukuran,
                                "harga": harga,
                                "kualitas_ban": kualitas_ban,
                                "daya_tahan": daya_tahan,
                                "grip_jalan": grip_jalan,
                                "kenyamanan": kenyamanan,
                                "ketahanan_cuaca": ketahanan_cuaca,
                                "keterangan": keterangan,
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            if save_ban_data(new_ban):
                                st.success("✅ Ban berhasil ditambahkan!")
                                st.rerun()
                        else:
                            st.error("❌ Mohon lengkapi semua field yang wajib (*)")
            
            st.markdown("---")
            st.subheader("📋 Daftar Ban")
            
            # Tampilkan data ban dalam bentuk tabel yang mudah dibaca
            try:
                ban_list = st.session_state.get('ban_data', load_ban_list())
                
                if ban_list:
                    st.write(f"**Total Ban: {len(ban_list)}**")
                    
                    # Tampilkan setiap ban dalam card format
                    for i, ban in enumerate(ban_list):
                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background-color: #f9f9f9;">
                                <h4 style="margin-top: 0; color: #333;">🛞 {ban.get('nama', 'N/A')} - {ban.get('merk', 'N/A')}</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>Ukuran:</strong> {ban.get('ukuran', 'N/A')}</div>
                                    <div><strong>Harga:</strong> Rp {ban.get('harga', 0):,}</div>
                                    <div><strong>Kualitas:</strong> {ban.get('kualitas_ban', ban.get('kualitas', 'N/A'))}</div>
                                    <div><strong>Daya Tahan:</strong> {ban.get('daya_tahan', 'N/A')}/10</div>
                                    <div><strong>Grip Jalan:</strong> {ban.get('grip_jalan', ban.get('grip', 'N/A'))}/10</div>
                                    <div><strong>Kenyamanan:</strong> {ban.get('kenyamanan', ban.get('comfort', 'N/A'))}/10</div>
                                    <div><strong>Ketahanan Cuaca:</strong> {ban.get('ketahanan_cuaca', 'N/A')}/10</div>
                                </div>
                                {f"<div style='margin-top: 10px;'><strong>Keterangan:</strong> {ban.get('keterangan', 'Tidak ada keterangan')}</div>" if ban.get('keterangan') else ""}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Tombol aksi untuk setiap ban
                            col1, col2, col3 = st.columns([1, 1, 4])
                            with col1:
                                if st.button("✏️ Edit", key=f"edit_{i}"):
                                    st.session_state[f'edit_ban_{i}'] = True
                            with col2:
                                if st.button("🗑️ Hapus", key=f"delete_{i}"):
                                    if delete_ban_data(i):
                                        st.success("✅ Ban berhasil dihapus!")
                                        st.rerun()
                            
                            # Form edit inline
                            if st.session_state.get(f'edit_ban_{i}', False):
                                with st.form(f"edit_form_{i}"):
                                    st.markdown("**✏️ Edit Ban**")
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        nama_edit = st.text_input("Nama Ban", value=ban.get('nama', ''), key=f"nama_{i}")
                                        merk_edit = st.text_input("Merk", value=ban.get('merk', ban.get('brand', '')), key=f"merk_{i}")
                                        ukuran_edit = st.text_input("Ukuran", value=ban.get('ukuran', ''), key=f"ukuran_{i}")
                                        harga_edit = st.number_input("Harga", value=ban.get('harga', 0), min_value=0, step=10000, key=f"harga_{i}")
                                    
                                    with col2:
                                        kualitas_edit = st.selectbox("Kualitas", ["Sangat Baik", "Baik", "Cukup", "Kurang"], 
                                                                   index=["Sangat Baik", "Baik", "Cukup", "Kurang"].index(ban.get('kualitas_ban', ban.get('kualitas', 'Baik'))), 
                                                                   key=f"kualitas_{i}")
                                        daya_tahan_edit = st.slider("Daya Tahan", 1, 10, ban.get('daya_tahan', 5), key=f"daya_{i}")
                                        grip_edit = st.slider("Grip Jalan", 1, 10, ban.get('grip_jalan', ban.get('grip', 5)), key=f"grip_{i}")
                                        kenyamanan_edit = st.slider("Kenyamanan", 1, 10, ban.get('kenyamanan', ban.get('comfort', 5)), key=f"comfort_{i}")
                                        cuaca_edit = st.slider("Ketahanan Cuaca", 1, 10, ban.get('ketahanan_cuaca', 5), key=f"cuaca_{i}")
                                    
                                    keterangan_edit = st.text_area("Keterangan", value=ban.get('keterangan', ''), key=f"ket_{i}")
                                    
                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        if st.form_submit_button("💾 Update"):
                                            updated_ban = {
                                                "nama": nama_edit,
                                                "merk": merk_edit,
                                                "ukuran": ukuran_edit,
                                                "harga": harga_edit,
                                                "kualitas_ban": kualitas_edit,
                                                "daya_tahan": daya_tahan_edit,
                                                "grip_jalan": grip_edit,
                                                "kenyamanan": kenyamanan_edit,
                                                "ketahanan_cuaca": cuaca_edit,
                                                "keterangan": keterangan_edit,
                                                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            }
                                            st.session_state['ban_data'][i] = updated_ban
                                            st.session_state[f'edit_ban_{i}'] = False
                                            st.success("✅ Ban berhasil diupdate!")
                                            st.rerun()
                                    
                                    with col_cancel:
                                        if st.form_submit_button("❌ Batal"):
                                            st.session_state[f'edit_ban_{i}'] = False
                                            st.rerun()
                            
                            st.markdown("---")
                else:
                    st.info("📝 Belum ada data ban. Silakan tambahkan ban baru menggunakan form di atas.")
                    
            except Exception as e:
                st.error(f"Error memuat data ban: {str(e)}")

        with tab3:
            st.subheader("📈 Analytics & Reports")
            
            # Analytics data
            analytics_data = generate_analytics_data()
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📊 Statistik Penggunaan**")
                
                # Chart sederhana untuk platform
                platform_data = pd.DataFrame({
                    'Platform': ['Desktop', 'Mobile', 'Tablet'],
                    'Pengguna': [45, 30, 25]
                })
                st.bar_chart(platform_data.set_index('Platform'))
                
                # Metrics tambahan
                st.metric("Rata-rata Analisis per Hari", f"{sum(analytics_data['analyses'])/len(analytics_data['analyses']):.1f}")
                st.metric("Peak Usage", f"{max(analytics_data['users'])} users")
                
            with col2:
                st.markdown("**⭐ Review Analytics**")
                if st.session_state.get('reviews'):
                    reviews = st.session_state['reviews']
                    avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
                    st.metric("Rating Rata-rata User Reviews", f"{avg_rating:.1f}/5")
                    
                    # Chart distribusi rating
                    rating_counts = pd.Series([r['rating'] for r in reviews]).value_counts().sort_index()
                    st.bar_chart(rating_counts)
                else:
                    st.info("Belum ada review dari user")
                    
                    # Contoh data rating
                    dummy_ratings = pd.Series([4, 5, 3, 4, 5, 4, 3, 5, 4, 4]).value_counts().sort_index()
                    st.markdown("**Contoh Distribusi Rating:**")
                    st.bar_chart(dummy_ratings)
            
            # Tabel detail analytics
            st.markdown("**📊 Detail Analytics**")
            df_analytics = pd.DataFrame({
                'Tanggal': analytics_data['dates'][-10:],
                'Pengguna': analytics_data['users'][-10:],
                'Analisis': analytics_data['analyses'][-10:]
            })
            st.dataframe(df_analytics, use_container_width=True)

        with tab4:
            st.subheader("⚙️ System Settings")
            
            # Initialize settings if not exists
            if 'system_settings' not in st.session_state:
                st.session_state['system_settings'] = {
                    'enable_debug': False,
                    'max_selections': 5,
                    'maintenance_mode': False,
                    'auto_backup': True,
                    'notification_enabled': True
                }
            
            st.markdown("**Konfigurasi Sistem**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔧 Pengaturan Umum**")
                enable_debug = st.checkbox("Enable Debug Mode", 
                                         value=st.session_state['system_settings']['enable_debug'])
                max_selections = st.slider("Max Ban Selections", 2, 10, 
                                         st.session_state['system_settings']['max_selections'])
                maintenance_mode = st.checkbox("Mode Maintenance", 
                                             value=st.session_state['system_settings']['maintenance_mode'])
                
            with col2:
                st.markdown("**📧 Notifikasi & Backup**")
                auto_backup = st.checkbox("Auto Backup Harian", 
                                        value=st.session_state['system_settings']['auto_backup'])
                notification_enabled = st.checkbox("Notifikasi Email", 
                                                  value=st.session_state['system_settings']['notification_enabled'])
                
                # Pengaturan backup
                if auto_backup:
                    backup_time = st.time_input("Waktu Backup Harian", value=datetime.strptime("02:00", "%H:%M").time())
            
            # Status sistem
            st.markdown("**📊 Status Sistem**")
            status_col1, status_col2, status_col3 = st.columns(3)
            with status_col1:
                st.metric("CPU Usage", "45%", "🟢 Normal")
            with status_col2:
                st.metric("Memory Usage", "67%", "🟡 Moderate")
            with status_col3:
                st.metric("Disk Space", "23%", "🟢 Available")
            
            # Tombol aksi
            col_save, col_reset, col_backup = st.columns(3)
            with col_save:
                if st.button("💾 Simpan Konfigurasi", use_container_width=True):
                    st.session_state['system_settings'] = {
                        'enable_debug': enable_debug,
                        'max_selections': max_selections,
                        'maintenance_mode': maintenance_mode,
                        'auto_backup': auto_backup,
                        'notification_enabled': notification_enabled
                    }
                    st.success("✅ Konfigurasi tersimpan!")
            
            with col_reset:
                if st.button("🔄 Reset ke Default", use_container_width=True):
                    st.session_state['system_settings'] = {
                        'enable_debug': False,
                        'max_selections': 5,
                        'maintenance_mode': False,
                        'auto_backup': True,
                        'notification_enabled': True
                    }
                    st.success("✅ Reset berhasil!")
                    st.rerun()
            
            with col_backup:
                if st.button("💾 Backup Manual", use_container_width=True):
                    st.info("🔄 Memulai backup...")
                    # Simulasi backup
                    import time
                    time.sleep(1)
                    st.success("✅ Backup berhasil!")
            
            # Log aktivitas
            st.markdown("**📋 Log Aktivitas Terbaru**")
            log_data = [
                {"Waktu": "2024-01-15 14:30", "Aktivitas": "Admin login", "Status": "✅ Sukses"},
                {"Waktu": "2024-01-15 14:25", "Aktivitas": "Ban baru ditambahkan", "Status": "✅ Sukses"},
                {"Waktu": "2024-01-15 14:20", "Aktivitas": "Backup otomatis", "Status": "✅ Sukses"},
                {"Waktu": "2024-01-15 14:15", "Aktivitas": "Update konfigurasi", "Status": "✅ Sukses"},
                {"Waktu": "2024-01-15 14:10", "Aktivitas": "User analisis", "Status": "✅ Sukses"},
            ]
            st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True)

# 🔁 Tambahkan ini supaya bisa dijalankan langsung
if __name__ == "__main__":
    show_admin_panel()