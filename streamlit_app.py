import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Assessment System",
    page_icon="🏆",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "students" not in st.session_state:
    st.session_state.students = []

# -----------------------------
# HELPERS
# -----------------------------
def get_status(total):
    if total >= 80:
        return "Excellent ⭐"
    elif total >= 60:
        return "Good 👍"
    elif total >= 40:
        return "Moderate"
    return "Need Improvement"

def recalculate_and_rank():
    for student in st.session_state.students:
        scores = student["scores"]
        total = round(
            float(scores["Tema"])
            + float(scores["Design"])
            + float(scores["Kreativiti"])
            + float(scores["Originality"]),
            2
        )
        student["total"] = total
        student["status"] = get_status(total)

    st.session_state.students.sort(
        key=lambda x: x["total"],
        reverse=True
    )

def ranked_dataframe():
    recalculate_and_rank()

    rows = []
    for index, student in enumerate(st.session_state.students, start=1):
        if index == 1:
            position = "🥇 1"
        elif index == 2:
            position = "🥈 2"
        elif index == 3:
            position = "🥉 3"
        else:
            position = str(index)

        rows.append({
            "Kedudukan": position,
            "Nama Murid": student["name"],
            "Tema /20": student["scores"]["Tema"],
            "Design /30": student["scores"]["Design"],
            "Kreativiti /30": student["scores"]["Kreativiti"],
            "Originality /20": student["scores"]["Originality"],
            "Jumlah /100": student["total"],
            "Status": student["status"],
        })

    return pd.DataFrame(rows)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sub-title {
        color: #64748B;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }

    .total-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        text-align: center;
    }

    .total-number {
        font-size: 2.4rem;
        font-weight: 800;
        color: #2563EB;
    }

    .status-text {
        font-size: 1.1rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="main-title">🏆 BORANG PENILAIAN MURID</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Student Assessment System • Sistem Pemarkahan & Kedudukan</div>',
    unsafe_allow_html=True
)

# -----------------------------
# INPUT FORM
# -----------------------------
left, right = st.columns([2, 1], gap="large")

with left:
    st.subheader("📝 Maklumat & Penilaian")

    name = st.text_input("Nama Murid")

    c1, c2 = st.columns(2)

    with c1:
        tema = st.number_input(
            "Tema /20",
            min_value=0.0,
            max_value=20.0,
            value=0.0,
            step=1.0
        )

        kreativiti = st.number_input(
            "Kreativiti /30",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=1.0
        )

    with c2:
        design = st.number_input(
            "Design /30",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=1.0
        )

        originality = st.number_input(
            "Originality /20",
            min_value=0.0,
            max_value=20.0,
            value=0.0,
            step=1.0
        )

current_total = round(tema + design + kreativiti + originality, 2)
current_status = get_status(current_total)

with right:
    st.subheader("📊 Jumlah Semasa")
    st.markdown(
        f"""
        <div class="total-card">
            <div>JUMLAH MARKAH</div>
            <div class="total-number">{current_total:g} / 100</div>
            <div class="status-text">{current_status}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# SAVE
# -----------------------------
st.write("")

b1, b2, b3 = st.columns([1.2, 1.2, 3])

with b1:
    save_clicked = st.button(
        "💾 SIMPAN PENILAIAN",
        type="primary",
        use_container_width=True
    )

with b2:
    calculate_all_clicked = st.button(
        "🧮 KIRA SEMUA MARKAH",
        use_container_width=True
    )

if save_clicked:
    clean_name = name.strip()

    if not clean_name:
        st.error("Sila masukkan nama murid.")
    else:
        st.session_state.students.append({
            "name": clean_name,
            "scores": {
                "Tema": tema,
                "Design": design,
                "Kreativiti": kreativiti,
                "Originality": originality,
            },
            "total": current_total,
            "status": current_status,
        })

        recalculate_and_rank()
        st.success(
            f"Penilaian {clean_name} berjaya disimpan — "
            f"{current_total:g}/100 ({current_status})"
        )

if calculate_all_clicked:
    if not st.session_state.students:
        st.warning("Tiada murid untuk dikira.")
    else:
        recalculate_and_rank()
        st.success("Semua markah dan kedudukan telah dikira semula.")

# -----------------------------
# RESULTS
# -----------------------------
st.divider()
st.subheader("🏆 Senarai Keputusan & Kedudukan")

if not st.session_state.students:
    st.info("Belum ada penilaian disimpan.")
else:
    df = ranked_dataframe()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # TOP 3
    st.subheader("🏅 Top 3 Winners")
    winners = st.session_state.students[:3]

    winner_cols = st.columns(3)

    medals = ["🥇", "🥈", "🥉"]

    for i, winner in enumerate(winners):
        with winner_cols[i]:
            st.metric(
                label=f"{medals[i]} Kedudukan {i + 1}",
                value=winner["name"],
                delta=f'{winner["total"]:g} / 100'
            )

    # DELETE
    st.subheader("🗑 Padam Penilaian")

    names = [student["name"] for student in st.session_state.students]
    selected_name = st.selectbox(
        "Pilih murid untuk dipadam",
        names
    )

    if st.button("PADAM MURID"):
        for i, student in enumerate(st.session_state.students):
            if student["name"] == selected_name:
                st.session_state.students.pop(i)
                break

        recalculate_and_rank()
        st.success(f"{selected_name} telah dipadam.")
        st.rerun()

    # CSV DOWNLOAD
    st.subheader("📥 Export")

    export_df = ranked_dataframe()
    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 DOWNLOAD CSV",
        data=csv_data,
        file_name="student_assessment_results.csv",
        mime="text/csv",
        type="primary"
    )

# -----------------------------
# RESET ALL
# -----------------------------
st.divider()

if st.button("🔄 RESET SEMUA DATA"):
    st.session_state.students = []
    st.success("Semua data telah direset.")
    st.rerun()

st.caption(
    "Student Assessment System • Tema 20 + Design 30 + Kreativiti 30 + Originality 20 = 100"
)