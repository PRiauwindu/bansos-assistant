import streamlit as st
import google.generativeai as genai
import time
import pytesseract
from PIL import Image

# Configure Gemini API Key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Bansos Assistant", page_icon="🧾")
st.sidebar.title("📂 Navigasi")
page = st.sidebar.selectbox("Pilih Fitur", ["🤖 Chatbot Bansos", "📷 Cek Registrasi dari KTP", "📊 Cek Kelayakan Penerima Bansos"])

# --- Full Prompt for Gemini Chatbot ---
system_prompt = """
Anda adalah Asisten Digital Bansos Indonesia. Tahami dan bantu pengguna tentang bantuan sosial seperti PKH, BPNT, BLT, DTKS, dan cara mendapatkan bantuan. Jawaban harus sopan, ringkas, mudah dimengerti, dan jika perlu beri contoh.

Q: Apa itu BPNT?
A: BPNT adalah bantuan pangan seperti beras, telur, atau minyak yang diberikan melalui kartu KKS dan diambil di e-warong.

Q: Bedanya BPNT dan PKH?
A: PKH adalah bantuan uang tunai untuk ibu hamil, anak sekolah, lansia, dll. BPNT bantuan pangan lewat e-warong.

Q: Saya buruh harian, bisa dapat bantuan?
A: Bisa. Silakan ajukan ke RT/RW atau kelurahan untuk diusulkan masuk DTKS.

Q: Bagaimana cara daftar DTKS?
A: Bawa KTP & KK ke RT/RW. Anda akan diajukan dan disurvei oleh petugas.

Q: Saya belum dapat bantuan padahal miskin, kenapa?
A: Mungkin belum masuk DTKS. Coba cek status di cekbansos.kemensos.go.id atau ajukan ke RT/RW.

Q: Saya mau lapor pungli, ke mana?
A: Hubungi pendamping, dinas sosial setempat, atau call center Kemensos 1500-297.
"""

# --- Chatbot Tab ---
if page == "🤖 Chatbot Bansos":
    st.title("🤖 Bansos Chatbot Indonesia")
    st.markdown("Tanya apa saja tentang bantuan sosial seperti PKH, BPNT, BLT, dan cara daftar DTKS.")
    user_input = st.text_input("💬 Pertanyaan Anda:")
    if user_input:
        with st.spinner("Sedang menjawab..."):
            response = model.generate_content(f"{system_prompt}\n\nQ: {user_input}")
            st.success(response.text)

# --- Cek Registrasi Bansos Page ---
elif page == "📷 Cek Registrasi dari KTP":
    st.title("📷 Cek Registrasi Bansos dari Foto KTP")
    st.markdown("Unggah foto KTP Anda untuk mengecek apakah Anda **terdaftar di DTKS sebagai penerima bansos**. (Simulasi untuk demo hackathon)")

    uploaded_file = st.file_uploader("📤 Unggah Foto KTP", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Foto KTP Anda", use_column_width=True)
        st.markdown("🔍 **Menjalankan ekstraksi data menggunakan AI...**")

        with st.spinner("Mengekstrak data dari KTP..."):
            response = model.generate_content([
                "Tolong ekstrak informasi dari KTP berikut. Ambil data: Nama, NIK, Provinsi, Kabupaten/Kota, Kecamatan, dan Kelurahan. Formatkan hasil dalam JSON.",
                image
            ])
            st.success("✅ Data berhasil diekstrak:")
            st.code(response.text, language="json")

        st.markdown("🔗 **Mengecek ke sistem DTKS Kemensos (simulasi)...**")
        with st.spinner("Menghubungkan ke API Kemensos..."):
            time.sleep(2)

            if "Putranegara Riauwindu" in response.text:
                is_registered = False
                bansos_type = "BPNT"
                tahap = "Tahap 2 - 2025"
            else:
                is_registered = False

        if is_registered:
            st.success(f"🎉 Anda terdaftar sebagai penerima **{bansos_type} ({tahap})**.")
            st.markdown("📍 Silakan cek pencairan bantuan Anda di e-Warong terdekat atau melalui aplikasi Cek Bansos.")
        else:
            st.error("⚠️ Anda belum terdaftar di DTKS.")
            st.markdown("""
            👉 Langkah berikutnya:
            - Kunjungi RT/RW Anda dan minta diusulkan masuk ke DTKS
            - Atau daftar melalui aplikasi **Cek Bansos Kemensos** di Android
            - Pastikan data NIK dan alamat sesuai Dukcapil
            """)

# --- Cek Kelayakan Penerima Tab ---
elif page == "📊 Cek Kelayakan Penerima Bansos":
    st.title("📊 Cek Kelayakan Penerima Bansos")
    st.markdown("Isi informasi di bawah untuk mengetahui apakah Anda *berpotensi layak* menerima bantuan sosial (simulasi).")

    with st.form("eligibility_form"):
        umur = st.number_input("Umur Kepala Keluarga", min_value=17, max_value=100)
        income = st.number_input("Penghasilan Bulanan (Rp)", step=100000)
        job_type = st.selectbox("Jenis Pekerjaan", ["Formal", "Informal", "Tidak bekerja"])
        dependents = st.number_input("Jumlah Tanggungan (anak, lansia, disabilitas)", min_value=0)
        has_school_child = st.radio("Memiliki anak usia sekolah?", ["Ya", "Tidak"])
        has_elderly_or_disabled = st.radio("Ada lansia atau disabilitas dalam keluarga?", ["Ya", "Tidak"])
        house_ownership = st.selectbox("Status Kepemilikan Rumah", ["Milik Sendiri", "Kontrak", "Menumpang / Tidak tetap"])
        submitted = st.form_submit_button("🔍 Cek Kelayakan")

    if submitted:
        is_eligible = (
            income < 1500000 and (
                has_school_child == "Ya" or
                has_elderly_or_disabled == "Ya" or
                job_type in ["Informal", "Tidak bekerja"]
            )
        )

        st.subheader("📋 Hasil Analisis Kelayakan:")
        if is_eligible:
            st.success("✅ Anda *berpotensi layak* menerima bansos.")
        else:
            st.error("❌ Anda *mungkin belum memenuhi kriteria utama* bansos.")

        with st.expander("🔎 Penjelasan"):
            explanation_prompt = f"""
Saya ingin menjelaskan kepada pengguna apakah mereka layak menerima bansos berdasarkan data berikut:

- Umur: {umur}
- Penghasilan: {income}
- Jenis pekerjaan: {job_type}
- Tanggungan: {dependents}
- Anak usia sekolah: {has_school_child}
- Ada lansia/disabilitas: {has_elderly_or_disabled}
- Kepemilikan rumah: {house_ownership}

Jawab secara sopan dan mudah dipahami. Jelaskan kenapa mereka layak / tidak layak. Hindari istilah teknis.
"""
            with st.spinner("Membuat penjelasan..."):
                response = model.generate_content(explanation_prompt)
                st.markdown(response.text)
