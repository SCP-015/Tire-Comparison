import streamlit as st
import os
import json
from collections import Counter
import plotly.express as px
from data_handler import load_ban_list
from electre import electre_with_steps
from utils import sub_kriteria, bobot_opsi_per_kriteria, get_all_reverse_maps

st.set_page_config(page_title="SPK Pemilihan Ban Mobil", layout="wide")

# ===== SIDEBAR =====
with st.sidebar:
    st.title("🛞 Website Sistem Pendukung Keputusan")
    st.markdown("---")
    
    # Main Navigation
    page = st.selectbox(
        "📱 Pilih Halaman:",
        ["🏠 Dashboard", "📊 Tire Comparison", "📝 Reviews & Feedback", "🔥 Hot Comparison"]
    )
    st.session_state["page"] = page

    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Status Perbandingan")
    ban_count = len(load_ban_list())
    selected_count = len(st.session_state.get("selected_ids", []))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Ban", ban_count)
    with col2:
        st.metric("Dipilih", selected_count)
    
    # # Progress indicator
    # if selected_count > 0:
    #     progress = min(selected_count / 5, 1.0)  # Assuming max 5 selections
    #     st.progress(progress)
    #     st.caption(f"Progress: {int(progress*100)}%")
    
    st.markdown("---")
    
    # # Quick Actions
    # st.subheader("🔧 Aksi Cepat")
    
    # if st.button("🔄 Reset Semua", use_container_width=True):
    #     for key in list(st.session_state.keys()):
    #         del st.session_state[key]
    #     st.rerun()
    
    # if selected_count > 0:
    #     if st.button("📋 Lihat Pilihan", use_container_width=True):
    #         st.session_state["show_selected"] = True
    
    # st.markdown("---")
    
    # # System Info
    # st.subheader("ℹ️ Informasi")
    # st.info("Sistem Pendukung Keputusan untuk memilih ban mobil terbaik menggunakan metode ELECTRE")
    
    # Help
    with st.expander("❓ Informasi"):
        st.markdown("""
        **Langkah Penggunaan:**
        1. Pilih ban (min. 2)
        2. Tentukan preferensi kriteria
        3. Temukan ban terbaik
        4. Lihat hasil rekomendasi
        """)

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"
    
# ===== MAIN CONTENT =====
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    
    # Welcome message
    st.markdown("#### Selamat datang di Sistem Pendukung Keputusan Pemilihan Ban Mobil! 🚗")
    # st.markdown("Sistem ini menggunakan metode ELECTRE untuk membantu Anda memilih ban mobil terbaik.")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Ban Tersedia",
            value=len(load_ban_list()),
            delta="Data terbaru"
        )
    
    with col2:
        st.metric(
            label="🎯 Ban Dipilih",
            value=len(st.session_state.get("selected_ids", [])),
            delta="Sesi aktif"
        )
    
    with col3:
        st.metric(
            label="⚖️ Kriteria Penilaian",
            value=len(sub_kriteria),
            delta="Standart pakar"
        )
    
    # with col4:
    #     analysis_done = "electre_result" in st.session_state
    #     st.metric(
    #         label="📊 Status",
    #         value="Sudah dibandingkan" if analysis_done else "Belum dibandingkan",
    #         delta="Hasil tersedia" if analysis_done else "Klik untuk mulai"
    #     )

    
    st.markdown("---")
    
    # Quick Start Guide
    st.subheader("🚀 Panduan Cepat")
    
    tab1, tab2, tab3 = st.tabs(["📖 Cara Penggunaan", "🎯 Kriteria Ban", "⚙️ Tentang Sistem"])
    
    with tab1:
        st.markdown("""
        #### Langkah-langkah Penggunaan:
        
        1. **Pilih Menu** "Tire Comparison" di sidebar
        2. **Pilih ban** yang ingin dibandingkan (minimal 2 ban)
        3. **Tentukan preferensi** untuk menentukan kebutuhan anda
        4. **Klik tombol** "Tampilkan Hasil Perbandingan"
        5. **Lihat hasil** Hasil perbandingan ban akan ditampilkan dalam bentuk ranking
        """)
        
        if st.button("🎯 Bandingkan Sekarang"):
            page == "📊 Tire Comparison"
            st.session_state.page = "📊 Tire Comparison"
            st.rerun()
    
    with tab2:
        st.markdown("#### Kriteria Penilaian Ban:")
        for i, (krit, desc) in enumerate(sub_kriteria.items(), 1):
            st.markdown(f"**{i}. {krit.capitalize()}**")
            # Add brief description for each criteria
            if krit == "harga":
                st.caption("💰 Harga ban yang tertera menggunakan mata uang rupiah")
            elif krit == "merk":
                st.caption("🏷️ Merk yang digunakan merupakan merk yang terkenal dan terpercaya serta sudah tersebar di seluruh toko di indonesia")
            elif krit == "diameter ban":
                st.caption("📏 Diameter ban harus disesuaikan dengan standar pabrikan kendaraan untuk menjaga performa dan keselamatan")
            elif krit == "kecepatan maksimum":
                st.caption("🚀 Kecepatan maksimum menunjukkan batas kecepatan aman yang ditoleransi ban")
            elif krit == "beban maksimum":
                st.caption("⚖️ Beban maksimum adalah kapasitas muatan tertinggi yang dapat ditanggung ban")
            elif krit == "kondisi medan":
                st.caption("🌍 Kesesuaian ban terhadap berbagai kondisi medan seperti aspal, tanah, atau off-road")
            elif krit == "pola tapak":
                st.caption("🔳 Pola tapak memengaruhi traksi, pembuangan air, dan performa di berbagai kondisi jalan")

                
    with tab3:
        st.markdown("""
        #### Tentang Sistem Perbandingan Ban :
        **Fitur utama sistem ini:**

        - 🎯 **Perbandingan menyeluruh** : Sistem ini akan membandingkan ban-ban terbaik di pasar berdasarkan kriteria yang telah ditentukan.
        - ⚖️ **Rekomendasi yang objektif** : Hasil perbandingan akan memberikan rekomendasi yang objektif dan transparan, berdasarkan data yang ada.
        - 📊 **Memudahkan pengambilan keputusan**: Dengan sistem ini, kamu bisa membuat keputusan lebih cepat dan tepat tanpa kebingungan.

        Sistem ini cocok untuk siapa saja yang ingin memilih ban mobil dengan lebih mudah dan terinformasi, baik itu untuk mobil pribadi maupun kendaraan lainnya.
        """)

    
    # Recent Activity (if any)
    if st.session_state.get("selected_ids") or st.session_state.get("electre_result"):
        st.markdown("---")
        st.subheader("🔄 Aktivitas Terbaru")
        
        if st.session_state.get("selected_ids"):
            st.success(f"✅ Anda telah memilih {len(st.session_state['selected_ids'])} kandidat ban")
        
        if st.session_state.get("electre_result"):
            st.success("✅ Perbandingan telah selesai - hasil perbandingan tersedia")
            if st.button("📊 Lihat Hasil Analisis"):
                st.session_state["page"] = "📊 Tire Comparison"
                st.rerun()

elif page == "📊 Tire Comparison":
    st.title("📊 Yuk Cari Tahu Ban Seperti Apa Yang Kamu Butuhkan!")
    
    # ===== LOAD DATA =====
    ban_list = load_ban_list()
    krit = list(sub_kriteria.keys())

    # ================================
    # 1. Pilih Ban
    # ================================
    st.header("Pilih ban untuk dibandingkan")
    st.markdown("Pilih minimal 2 ban untuk dibandingkan:")
    
    cols = st.columns(5)
    for i, ban in enumerate(ban_list):
        with cols[i % 5]:
            try:
                st.image(ban['gambar'], caption=ban['nama'], use_container_width=True)
            except:
                st.image("https://dummyimage.com/150x100/eeeeee/000000&text=No+Image", caption=ban['nama'], use_container_width=True)
            
            # Check if already selected
            is_selected = ban['id'] in st.session_state.get("selected_ids", [])
            button_text = "✅ Terpilih" if is_selected else "Pilih"
            button_type = "secondary" if is_selected else "primary"
            
            if st.button(button_text, key=f"pilih_{ban['id']}", type=button_type):
                st.session_state.setdefault("selected_ids", [])
                if ban['id'] not in st.session_state["selected_ids"]:
                    st.session_state["selected_ids"].append(ban['id'])
                    st.rerun()

    # ================================
    # 2. Tampilkan Pilihan
    # ================================
    st.header("Ban yang dipilih")
    if st.session_state.get("selected_ids"):
        selected_ban = [b for b in ban_list if b['id'] in st.session_state["selected_ids"]]
        
        cols = st.columns(len(selected_ban))
        for i, ban in enumerate(selected_ban):
            with cols[i]:
                st.image(ban['gambar'], caption=ban['nama'], use_container_width=True)
                st.markdown(f"**{ban['nama']}**")
                if st.button("❌ Hapus", key=f"remove_{ban['id']}"):
                    st.session_state["selected_ids"].remove(ban['id'])
                    st.rerun()
        
        st.success(f"✅ {len(selected_ban)} ban terpilih")
    else:
        st.warning("⚠️ Belum ada kandidat yang dipilih.")
        
    # ================================
    # 3. Nilai Kriteria Setiap Ban
    # ================================
    # st.header("Kriteria Setiap Ban yang Dipilih")
    # if st.session_state.get("selected_ids"):
    #     rev_maps = get_all_reverse_maps()
    #     table = []
    #     for ban in selected_ban:
    #         row = {"Nama": ban["nama"]}
    #         for k in krit:
    #             nilai_mentah = ban["kriteria"][k]
    #             skor = ban["skor_kriteria"][k]
    #             label = rev_maps[k].get(skor, f"⚠️ {skor}")
    #             row[k.capitalize()] = f"{nilai_mentah} → {label}"
    #         table.append(row)
    #     st.dataframe(table, use_container_width=True)
    # else:
    #     st.info("ℹ️ Pilih ban terlebih dahulu untuk melihat nilai kriterianya.")
    
        st.header("Kriteria Setiap Ban yang Dipilih")
    if st.session_state.get("selected_ids"):
        table = []
        for ban in selected_ban:
            row = {"Nama": ban["nama"]}
            for k in krit:
                nilai_mentah = ban["kriteria"][k]
                row[k.capitalize()] = f"{nilai_mentah}"
            table.append(row)
        st.dataframe(table, use_container_width=True)
    else:
        st.info("ℹ️ Pilih ban terlebih dahulu untuk melihat nilai kriterianya.")


    # ================================
    # 4. Preferensi Bobot Kriteria
    # ================================
    st.header("Masukkan kriteria ban yang ingin dicari")
    st.markdown("Tentukan berdasarkan kebutuhan anda :")
    preferensi = {}
    valid_preferensi = True
    cols = st.columns(len(krit))
    #kalau mau horizontal
    # for i, k in enumerate(krit):
    #     with cols[i]:
    #         opsi = ["-- Pilih --"] + list(bobot_opsi_per_kriteria[k].keys())
    #         selected = st.selectbox(
    #             f"**{k.capitalize()}**:", 
    #             opsi, 
    #             key=f"pref_{k}",
    #             help=f"Pilih tingkat kepentingan untuk kriteria {k}"
    #         )
    #         if selected == "-- Pilih --":
    #             st.warning(f"⚠️ Pilih preferensi {k}")
    #             valid_preferensi = False
    #         else:
    #             preferensi[k] = bobot_opsi_per_kriteria[k][selected]
    #             st.success(f"✅ {selected}")

# #kalau mau vertikal
    for k in krit:
            opsi = ["-- Pilih --"] + list(bobot_opsi_per_kriteria[k].keys())
            selected = st.selectbox(
            f"**{k.capitalize()}**:", 
            opsi, 
            key=f"pref_{k}",
            help=f"Pilih tingkat kepentingan untuk kriteria {k}"
        )

            if selected == "-- Pilih --":
                st.warning(f"⚠️ Pilih preferensi {k}")
                valid_preferensi = False
            else:
                preferensi[k] = bobot_opsi_per_kriteria[k][selected]
                st.success(f"✅ {selected}")

            if st.session_state.get("selected_ids"):
                selected_ban = [b for b in ban_list if b['id'] in st.session_state["selected_ids"]]
            else:
                selected_ban = []
    # ================================
    # 5. Proses ELECTRE
    # ================================
    if not valid_preferensi:
        st.warning("⚠️ Lengkapi preferensi kriteria terlebih dahulu")
        st.stop()

    if st.button("🚀 Temukan ban anda sekarang!", type="primary", use_container_width=True):
        if not st.session_state.get("selected_ids"):
            st.error("❌ Pilih kandidat ban terlebih dahulu")
        elif len(selected_ban) < 2:
            st.error("❌ Pilih minimal 2 kandidat ban")
        else:
            with st.spinner("🔄 Sedang melakukan perhitungan ELECTRE..."):
                # Hitung ELECTRE
                result = electre_with_steps(
                    [{"nama": b["nama"], "kriteria": b["skor_kriteria"]} for b in selected_ban],
                    preferensi
                )
                st.session_state["electre_result"] = result
                st.session_state["step"] = 1

                # === Simpan log hasil ranking ke file JSON ===
                ranking_names = [selected_ban[idx]["nama"] for idx in result["ranking"]]
                log_path = "log_skenario.json"

                # Baca file lama
                if os.path.exists(log_path):
                    try:
                        with open(log_path, "r") as f:
                            logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
                else:
                    logs = []

                # Tambahkan entri baru
                from datetime import datetime
                logs.append({
                    "skenario": len(logs) + 1,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ranking": ranking_names
                })

                # Tulis ulang ke file
                with open(log_path, "w") as f:
                    json.dump(logs, f, indent=4)

            st.success("✅ Perhitungan selesai! Lihat hasil di bawah.")
            st.rerun()

    # Pastikan selected_ban selalu di-generate lagi setelah rerun
    if st.session_state.get("selected_ids"):
        selected_ban = [b for b in ban_list if b['id'] in st.session_state["selected_ids"]]
    else:
        selected_ban = []

    # ================================
    # Tampilkan hasil ranking
    # ================================
    if "electre_result" in st.session_state:
        result = st.session_state["electre_result"]
        st.markdown("---")
        st.header("🏆 Hasil Akhir Pemilihan Ban (Ranking)")
        st.balloons()

        for i, idx in enumerate(result["ranking"], 1):
            ban = selected_ban[idx]
            current_ban = selected_ban[idx]
            dominasi = []

            # Cari kriteria yang dominan
            for k in krit:
                skor = current_ban["skor_kriteria"][k]
                if i == 1:
                    lebih_bagus = all(
                        skor >= other["skor_kriteria"][k]
                        for j, other in enumerate(selected_ban) if j != idx
                    )
                else:
                    lebih_bagus = sum(
                        skor >= other["skor_kriteria"][k]
                        for j, other in enumerate(selected_ban) if j != idx
                    ) >= len(selected_ban) // 2
                if lebih_bagus:
                    dominasi.append(k.capitalize())

            # Tampilkan berdasarkan peringkat
            if i == 1:
                st.success(f"🥇 **Peringkat {i}: {ban['nama']}**")
                if dominasi:
                    st.caption(f"📌 Ban ini menempati posisi pertama karena unggul dalam kriteria: **{', '.join(dominasi)}**.")
                else:
                    st.caption("📌 Ban ini memiliki keunggulan menyeluruh dibandingkan ban lainnya.")
            elif i == 2:
                st.info(f"🥈 **Peringkat {i}: {ban['nama']}**")
                if dominasi:
                    st.caption(f"ℹ️ Ban ini hampir menyaingi peringkat pertama, terutama pada kriteria: **{', '.join(dominasi)}**.")
                else:
                    st.caption("ℹ️ Ban ini menunjukkan performa stabil di berbagai kriteria.")
            elif i == 3:
                st.warning(f"🥉 **Peringkat {i}: {ban['nama']}**")
                if dominasi:
                    st.caption(f"💡 Ban ini masih kompetitif, menonjol pada aspek: **{', '.join(dominasi)}**.")
                else:
                    st.caption("💡 Ban ini memiliki kinerja yang cukup baik secara umum.")
            else:
                st.markdown(f"**Peringkat {i}: {ban['nama']}**")

#  — Skor F: {f_score:.2f}

elif page == "📝 Reviews & Feedback":
    import os
    import json

    st.title("📝 Reviews & Feedback")
    st.markdown("Berikan penilaian dan saran untuk meningkatkan sistem ini")

    REVIEW_FILE = "reviews.json"

    # Load data review
    if os.path.exists(REVIEW_FILE):
        try:
            with open(REVIEW_FILE, "r") as f:
                all_reviews = json.load(f)
        except json.JSONDecodeError:
            all_reviews = []
    else:
        all_reviews = []

    # Form input review
    with st.form("review_form"):
        st.subheader("📋 Formulir Review")

        col1, col2 = st.columns(2)
        with col1:
            rating = st.select_slider(
                "Rating sistem (1-5):",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: "⭐" * x
            )

            category = st.selectbox(
                "Kategori feedback:",
                ["Kemudahan Penggunaan", "Akurasi Hasil", "Kecepatan Sistem",
                 "Tampilan Interface", "Fitur Tambahan", "Bug Report", "Lainnya"]
            )

        with col2:
            user_name = st.text_input("Nama (opsional):")
            user_email = st.text_input("Email (opsional):")

        review_text = st.text_area(
            "Tulis review/saran Anda:",
            placeholder="Bagikan pengalaman Anda...",
            height=150
        )

        submitted = st.form_submit_button("📤 Kirim Review", type="primary", use_container_width=True)

        if submitted:
            if review_text.strip():
                new_review = {
                    'name': user_name if user_name else 'Anonymous',
                    'email': user_email,
                    'rating': rating,
                    'category': category,
                    'text': review_text
                }

                all_reviews.append(new_review)

                try:
                    with open(REVIEW_FILE, "w") as f:
                        json.dump(all_reviews, f, indent=4)
                    st.success("✅ Review berhasil dikirim dan disimpan!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal menyimpan review: {e}")
            else:
                st.error("❌ Mohon isi review/feedback terlebih dahulu.")

    # Tampilan hasil review
    st.markdown("---")
    st.subheader("📊 Review Pengguna")

    if all_reviews:
        # State untuk toggle tampilkan semua
        if "show_all_reviews" not in st.session_state:
            st.session_state.show_all_reviews = False

        # Hitung statistik
        avg_rating = sum(r['rating'] for r in all_reviews) / len(all_reviews)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Reviews", len(all_reviews))
        with col2:
            st.metric("Rating Rata-rata", f"{avg_rating:.1f}/5")
        with col3:
            st.metric("Rating Tertinggi", f"{max(r['rating'] for r in all_reviews)}/5")

        # Batasi review yang ditampilkan
        reviews_to_display = all_reviews if st.session_state.show_all_reviews else all_reviews[:4]

        # Tampilkan review (dibalik supaya terbaru di atas)
        for review in reversed(reviews_to_display):
            with st.expander(f"⭐ {review['rating']}/5 - {review['category']} - {review['name']}"):
                st.write(review['text'])

        # Tombol untuk toggle
        if len(all_reviews) > 4:
            if st.session_state.show_all_reviews:
                if st.button("🔼 Sembunyikan"):
                    st.session_state.show_all_reviews = False
                    st.rerun()
            else:
                if st.button("🔽 Tampilkan Semua Review"):
                    st.session_state.show_all_reviews = True
                    st.rerun()
    else:
        st.info("Belum ada review yang masuk.")


elif page == "🔥 Hot Comparison":
    st.title("🔥 Hot Comparison - Dominasi Ban")
    st.markdown("🔍 Statistik ban yang paling sering muncul sebagai juara 1, 2, dan 3 dari hasil semua perbandingan.")

    file_path = "log_skenario.json"

    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        st.warning("⚠️ Belum ada data skenario yang tersimpan.")
    else:
        with open(file_path, "r") as f:
            data = json.load(f)

        if len(data) == 0:
            st.info("Data skenario masih kosong.")
        else:
            juara1 = Counter()
            juara2 = Counter()
            juara3 = Counter()
            total_top3 = Counter()

            for skenario in data:
                ranking = skenario.get("ranking", [])
                if len(ranking) > 0:
                    juara1[ranking[0]] += 1
                if len(ranking) > 1:
                    juara2[ranking[1]] += 1
                if len(ranking) > 2:
                    juara3[ranking[2]] += 1
                for ban in ranking[:3]:
                    total_top3[ban] += 1

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🥇 Juara 1 Terbanyak")
                for nama, jumlah in juara1.most_common(5):
                    st.markdown(f"**{nama}** — {jumlah}x")

                st.subheader("🥈 Juara 2 Terbanyak")
                for nama, jumlah in juara2.most_common(5):
                    st.markdown(f"{nama} — {jumlah}x")

            with col2:
                st.subheader("🥉 Juara 3 Terbanyak")
                for nama, jumlah in juara3.most_common(5):
                    st.markdown(f"{nama} — {jumlah}x")

                st.subheader("🏁 Total Top 3")
                for nama, jumlah in total_top3.most_common(5):
                    st.markdown(f"{nama} — {jumlah}x")

            st.markdown("---")
            st.subheader("📊 Grafik Dominasi Juara 1")

            if juara1:
                df_juara1 = [{"Ban": nama, "Juara 1": jumlah} for nama, jumlah in juara1.items()]
                fig = px.bar(df_juara1, x="Ban", y="Juara 1", color="Ban", title="Ban Paling Sering Juara 1")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada data Juara 1.")



# ===== FOOTER =====
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🛞 <strong>Sistem Pendukung Keputusan Ban Mobil</strong> - Menggunakan Metode ELECTRE</p>
        <p>© 2024 SPK Ban Mobil | Developed with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)