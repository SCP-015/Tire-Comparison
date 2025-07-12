import streamlit as st
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
        ["🏠 Dashboard", "📊 Tire Comparison", "📝 Reviews & Feedback", "Hot Comparison"]
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

    # ================================
    # 5. Proses ELECTRE
    # ================================
    if not valid_preferensi:
        st.warning("⚠️ Lengkapi preferensi kriteria terlebih dahulu")
        st.stop()
    # st.header("5. Analisis ELECTRE")
    if st.button("🚀 Temukan ban anda sekarang!", type="primary", use_container_width=True):
        if not st.session_state.get("selected_ids"):
            st.error("❌ Pilih kandidat ban terlebih dahulu")
        elif len(selected_ban) < 2:
            st.error("❌ Pilih minimal 2 kandidat ban")
        else:
            with st.spinner("🔄 Sedang melakukan perhitungan ELECTRE..."):
                st.session_state["electre_result"] = electre_with_steps(
                    [{"nama": b["nama"], "kriteria": b["skor_kriteria"]} for b in selected_ban],
                    preferensi
                )
                st.session_state["step"] = 1
            st.success("✅ Perhitungan selesai! Lihat hasil di bawah.")
            st.rerun()

    # Display ELECTRE Results
    # if "electre_result" in st.session_state and "step" in st.session_state:
    #     result = st.session_state["electre_result"]
    #     step = st.session_state["step"]
        
    #     st.markdown("---")
    #     st.header(f"📊 Hasil Perhitungan ELECTRE - Tahap {step}/8")

    #     steps_label = [
    #         ("5.1 Matriks Keputusan", "matriks"),
    #         ("5.2 Normalisasi Matriks", "norm"),
    #         ("5.3 Matriks Terbobot", "terbobot"),
    #         ("5.4 Matriks Concordance (C)", "C"),
    #         ("5.5 Matriks Discordance (D)", "D")
    #     ]

    #     if step <= 5:
    #         st.subheader(steps_label[step - 1][0])
    #         st.dataframe(result[steps_label[step - 1][1]], use_container_width=True)
    #     elif step == 6:
    #         st.subheader("5.6 Ambang Batas")
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             st.metric("C̄ (Concordance Threshold)", f"{result['cbar']:.4f}")
    #         with col2:
    #             st.metric("D̄ (Discordance Threshold)", f"{result['dbar']:.4f}")
    #     elif step == 7:
    #         st.subheader("5.7 Skor Dominasi (F)")
    #         for i, f in enumerate(result["F"]):
    #             st.markdown(f"**{i+1}. {selected_ban[i]['nama']}** → Skor F = {f:.2f}")
    #     elif step == 8:
    #         st.subheader("🏆 5.8 Ranking Akhir")
    #         st.balloons()
            
    #         for i, idx in enumerate(result["ranking"], 1):
    #             ban = selected_ban[idx]
    #             f_score = result["F"][idx]
                
    #             if i == 1:
    #                 st.success(f"🥇 **Peringkat {i}: {ban['nama']}** — Skor F: {f_score:.2f}")
    #             elif i == 2:
    #                 st.info(f"🥈 **Peringkat {i}: {ban['nama']}** — Skor F: {f_score:.2f}")
    #             elif i == 3:
    #                 st.warning(f"🥉 **Peringkat {i}: {ban['nama']}** — Skor F: {f_score:.2f}")
    #             else:
    #                 st.markdown(f"**Peringkat {i}: {ban['nama']}** — Skor F: {f_score:.2f}")

    #     # Navigation buttons
    #     col1, col2, col3 = st.columns([1, 2, 1])
    #     with col1:
    #         if step > 1 and st.button("⬅️ Kembali", use_container_width=True):
    #             st.session_state["step"] -= 1
    #             st.rerun()
    #     with col2:
    #         st.progress(step / 8)
    #         st.caption(f"Tahap {step} dari 8")
    #     with col3:
    #         if step < 8 and st.button("Lanjut ➡️", use_container_width=True):
    #             st.session_state["step"] += 1
    #             st.rerun()

    # # Reset button
    # if st.session_state.get("selected_ids"):
    #     st.markdown("---")
    #     if st.button("🔄 Reset Kandidat", type="secondary"):
    #         st.session_state["selected_ids"] = []
    #         if "electre_result" in st.session_state:
    #             del st.session_state["electre_result"]
    #         if "step" in st.session_state:
    #             del st.session_state["step"]
    #         st.rerun()
    
    # Display only ELECTRE Final Ranking
if "electre_result" in st.session_state:
    result = st.session_state["electre_result"]
    
    st.markdown("---")
    st.header("🏆 Hasil Akhir Pemilihan Ban (Ranking)")

    st.balloons()
    for i, idx in enumerate(result["ranking"], 1):
        ban = selected_ban[idx]
        f_score = result["F"][idx]

        # Ambil data ban untuk dianalisis
        current_ban = selected_ban[idx]
        dominasi = []
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
                ) >= len(selected_ban) // 2  # Dominasi sebagian
            if lebih_bagus:
                dominasi.append(k.capitalize())

        # Tampilkan berdasarkan peringkat
        if i == 1:
            st.success(f"🥇 **Peringkat {i}: {ban['nama']}**")
            if dominasi:
                alasan = ", ".join(dominasi)
                st.caption(f"📌 Ban ini menempati posisi pertama karena unggul dalam kriteria: **{alasan}**.")
            else:
                st.caption("📌 Ban ini memiliki keunggulan menyeluruh dibandingkan ban lainnya.")
        
        elif i == 2:
            st.info(f"🥈 **Peringkat {i}: {ban['nama']}**")
            if dominasi:
                alasan = ", ".join(dominasi)
                st.caption(f"ℹ️ Ban ini hampir menyaingi peringkat pertama, terutama pada kriteria: **{alasan}**.")
            else:
                st.caption("ℹ️ Ban ini menunjukkan performa stabil di berbagai kriteria.")

        elif i == 3:
            st.warning(f"🥉 **Peringkat {i}: {ban['nama']}**")
            if dominasi:
                alasan = ", ".join(dominasi)
                st.caption(f"💡 Ban ini masih kompetitif, menonjol pada aspek: **{alasan}**.")
            else:
                st.caption("💡 Ban ini memiliki kinerja yang cukup baik secara umum.")

        else:
            st.markdown(f"**Peringkat {i}: {ban['nama']}**")


#  — Skor F: {f_score:.2f}

elif page == "📝 Reviews & Feedback":
    st.title("📝 Reviews & Feedback")
    st.markdown("Berikan penilaian dan saran untuk meningkatkan sistem ini")
    
    # Review form
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
                ["Kemudahan Penggunaan", "Akurasi Hasil", "Kecepatan Sistem", "Tampilan Interface", "Fitur Tambahan", "Bug Report", "Lainnya"]
            )
        
        with col2:
            user_name = st.text_input("Nama (opsional):")
            user_email = st.text_input("Email (opsional):")
        
        review_text = st.text_area(
            "Tulis review/saran Anda:",
            placeholder="Bagikan pengalaman menggunakan sistem ini, saran perbaikan, atau laporkan masalah yang ditemukan...",
            height=150
        )
        
        submitted = st.form_submit_button("📤 Kirim Review", type="primary", use_container_width=True)
        
        if submitted:
            if review_text.strip():
                st.success("✅ Review berhasil dikirim! Terima kasih atas feedback Anda.")
                st.balloons()
                
                # Store in session state (in real app, save to database)
                if 'reviews' not in st.session_state:
                    st.session_state['reviews'] = []
                
                new_review = {
                    'name': user_name if user_name else 'Anonymous',
                    'email': user_email,
                    'rating': rating,
                    'category': category,
                    'text': review_text,
                    'timestamp': st.session_state.get('review_count', 0) + 1
                }
                st.session_state['reviews'].append(new_review)
                st.session_state['review_count'] = st.session_state.get('review_count', 0) + 1
                
            else:
                st.error("❌ Mohon isi review/feedback terlebih dahulu")
    
    # Display reviews
    st.markdown("---")
    st.subheader("📊 Review Pengguna")
    
    # Sample reviews + user reviews
    sample_reviews = [
        {"name": "Ahmad S.", "rating": 5, "category": "Kemudahan Penggunaan", "text": "Sistem sangat mudah digunakan dan intuitif. Proses step-by-step ELECTRE membantu memahami perhitungan."},
        {"name": "Maria L.", "rating": 4, "category": "Akurasi Hasil", "text": "Hasil rekomendasi cukup akurat dengan preferensi yang saya set. Sangat membantu dalam memilih ban."},
        {"name": "Budi T.", "rating": 4, "category": "Tampilan Interface", "text": "Interface bersih dan modern. Sidebar navigation memudahkan navigasi antar fitur."},
        {"name": "Sari D.", "rating": 5, "category": "Fitur Tambahan", "text": "Fitur visualisasi step-by-step ELECTRE sangat membantu untuk pembelajaran metode SPK."}
    ]
    
    all_reviews = sample_reviews + st.session_state.get('reviews', [])
    
    # Statistics
    if all_reviews:
        avg_rating = sum(r['rating'] for r in all_reviews) / len(all_reviews)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reviews", len(all_reviews))
        with col2:
            st.metric("Rating Rata-rata", f"{avg_rating:.1f}/5")
        with col3:
            st.metric("Rating Tertinggi", f"{max(r['rating'] for r in all_reviews)}/5")
    
    # Display reviews
    for i, review in enumerate(all_reviews):
        with st.expander(f"⭐ {review['rating']}/5 - {review['category']} - {review['name']}"):
            st.write(review['text'])
            # if 'timestamp' in review:
            #     st.caption(f"Review #{review['timestamp']}")



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
