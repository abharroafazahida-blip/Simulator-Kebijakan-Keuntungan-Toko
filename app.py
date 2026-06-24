import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# =====================================
# CUSTOM CSS TEMA SOFT PINK
# =====================================
st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F7ECE9;
}

/* Kotak Metric */
[data-testid="metric-container"] {
    background-color: #F7ECE9;
    border: 2px solid #D8A7B1;
    padding: 15px;
    border-radius: 15px;
}

/* Subjudul */
h3 {
    color: #8F6A73 !important;
}

/* Garis pemisah */
hr {
    border-color: #D8A7B1;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# DATA TRAINING
# =====================================
X_train = np.array([
    [5, 10],
    [10, 20],
    [15, 5],
    [20, 25],
    [25, 15]
])

y_train = np.array([
    50,
    80,
    110,
    90,
    150
])

# =====================================
# MELATIH MODEL
# =====================================
model = LinearRegression()
model.fit(X_train, y_train)

# =====================================
# BASELINE
# =====================================
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# =====================================
# FUNGSI SIMULASI
# =====================================
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])

    prediction = model.predict(intervention_input)[0]

    delta = prediction - baseline_pred

    return prediction, delta


# =====================================
# JUDUL APLIKASI
# =====================================
st.markdown("""
<div style="
    background-color:#D8A7B1;
    padding:18px;
    border-radius:20px;
    text-align:center;
    margin-bottom:15px;
">
    <h1 style="
        color:white;
        margin:0;
        font-size:32px;
        white-space: nowrap;
        overflow: hidden;
    ">
        🌸 Simulator Kebijakan Keuntungan Toko 🌸
    </h1>
</div>
""", unsafe_allow_html=True)

st.caption("Praktikum Pemodelan dan Simulasi - Minggu 14")

st.write(
    "Gunakan slider untuk menguji skenario What-If dan melihat dampaknya terhadap keuntungan toko."
)

# =====================================
# INFORMASI BASELINE
# =====================================
st.markdown(
    f"""
    <div style="
        background:#F7ECE9;
        padding:18px;
        border-radius:15px;
        border-left:6px solid #D8A7B1;
        margin-bottom:20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
    ">
        <h4 style="color:#8F6A73;">🌷 Kondisi Baseline</h4>
        <p>• Anggaran Iklan : 10 Juta</p>
        <p>• Diskon : 10%</p>
        <p>• Prediksi Keuntungan : Rp {baseline_pred:.2f} Juta</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# SIDEBAR
# =====================================
st.sidebar.header("🎀 Tuas Kebijakan (Intervensi)")

iklan_slider = st.sidebar.slider(
    "Anggaran Iklan (Juta)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "Besaran Diskon (%)",
    min_value=0,
    max_value=50,
    value=10
)

# =====================================
# MENJALANKAN SIMULASI
# =====================================
hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# =====================================
# HASIL SIMULASI
# =====================================
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="💰 Prediksi Keuntungan",
        value=f"Rp {hasil_pred:.2f} Juta",
        delta=f"{delta:.2f} Juta"
    )

with col2:
    st.metric(
        label="📌 Keuntungan Baseline",
        value=f"Rp {baseline_pred:.2f} Juta"
    )

# =====================================
# ANALISIS HASIL
# =====================================
st.subheader("📊 Hasil Analisis")

if delta > 0:
    pesan = f"Keuntungan meningkat sebesar {delta:.2f} Juta dibandingkan kondisi awal."
elif delta < 0:
    pesan = f"Keuntungan menurun sebesar {abs(delta):.2f} Juta dibandingkan kondisi awal."
else:
    pesan = "Nilai masih sama dengan kondisi baseline."

st.markdown(
    f"""
    <div style="
        background:#F7ECE9;
        padding:18px;
        border-radius:15px;
        border-left:6px solid #D8A7B1;
        margin-bottom:20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
    ">
        <p style="
            margin:0;
            font-size:18px;
            color:#8F6A73;
            font-weight:500;
        ">
            {pesan}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# GRAFIK PERBANDINGAN
# =====================================
st.subheader("📈 Perbandingan Baseline dan Intervensi")

data_plot = pd.DataFrame({
    "Skenario": ["Baseline", "Intervensi"],
    "Keuntungan": [baseline_pred, hasil_pred]
})

st.bar_chart(
    data=data_plot,
    x="Skenario",
    y="Keuntungan"
)