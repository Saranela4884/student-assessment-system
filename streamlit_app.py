import streamlit as st
import pandas as pd


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Student Assessment System",
    page_icon="🏆",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "student_names" not in st.session_state:
    st.session_state.student_names = []


# =========================================================
# FUNCTIONS
# =========================================================

def get_status(total):

    if total >= 80:
        return "Excellent ⭐"

    elif total >= 60:
        return "Good 👍"

    elif total >= 40:
        return "Moderate"

    else:
        return "Need Improvement"


def calculate_total(tema, design, kreativiti, originality):

    total = (
        float(tema)
        + float(design)
        + float(kreativiti)
        + float(originality)
    )

    return round(total, 2)


def recalculate_and_rank():

    for student in st.session_state.students:

        scores = student["scores"]

        total = calculate_total(
            scores["Tema"],
            scores["Design"],
            scores["Kreativiti"],
            scores["Originality"]
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

    for index, student in enumerate(
        st.session_state.students,
        start=1
    ):

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

            "Tema /20":
                student["scores"]["Tema"],

            "Design /30":
                student["scores"]["Design"],

            "Kreativiti /30":
                student["scores"]["Kreativiti"],

            "Originality /20":
                student["scores"]["Originality"],

            "Jumlah /100":
                student["total"],

            "Status":
                student["status"]
        })

    return pd.DataFrame(rows)


# =========================================================
# LOAD STUDENT NAMES FROM EXCEL
# =========================================================

try:

    excel_df = pd.read_excel(
        "SENARAI NAMA 4 BARATHI  22025.xlsx",
        sheet_name="4B",
        header=None
    )

    # Student names are in column B
    # Real student names begin from Excel row 9
    names = (
        excel_df.iloc[8:, 1]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    # Remove empty cells
    names = [
        name
        for name in names
        if name
    ]

    # Remove duplicate names
    names = list(
        dict.fromkeys(names)
    )

    st.session_state.student_names = names

except Exception as error:

    st.error(
        f"❌ Student list cannot be loaded: {error}"
    )


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0px;
}

.sub-title {
    color: #808080;
    margin-top: 5px;
    margin-bottom: 25px;
}

.total-card {

    border: 1px solid #555;

    border-radius: 18px;

    padding: 30px;

    text-align: center;
}

.total-title {

    font-size: 15px;

    opacity: 0.7;

    font-weight: bold;
}

.total-number {

    font-size: 45px;

    font-weight: 800;

    margin-top: 8px;
}

.status-text {

    font-size: 20px;

    font-weight: 700;

    margin-top: 8px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🏆 BORANG PENILAIAN MURID</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
    Student Assessment System • Sistem Pemarkahan & Kedudukan
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STUDENT LIST INFORMATION
# =========================================================

if st.session_state.student_names:

    st.success(
        f"✅ {len(st.session_state.student_names)} "
        f"nama murid berjaya dimuatkan."
    )

else:

    st.warning(
        "⚠️ Tiada nama murid ditemui."
    )


# =========================================================
# MAIN ASSESSMENT
# =========================================================

st.divider()

left, right = st.columns(
    [2, 1],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.subheader(
        "📝 Maklumat & Penilaian"
    )


    # =====================================================
    # STUDENT NAME
    # =====================================================

    if st.session_state.student_names:

        name = st.selectbox(
            "Nama Murid",
            st.session_state.student_names,
            index=None,
            placeholder="Pilih nama murid..."
        )

    else:

        name = None

        st.warning(
            "Senarai nama murid tidak tersedia."
        )


    # =====================================================
    # MARKS
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

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


    with col2:

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


# =========================================================
# CURRENT TOTAL
# =========================================================

current_total = calculate_total(
    tema,
    design,
    kreativiti,
    originality
)

current_status = get_status(
    current_total
)


# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.subheader(
        "📊 Jumlah Semasa"
    )

    st.markdown(
        f"""
        <div class="total-card">

            <div class="total-title">
                JUMLAH MARKAH
            </div>

            <div class="total-number">
                {current_total:g} / 100
            </div>

            <div class="status-text">
                {current_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BUTTONS
# =========================================================

st.write("")

button1, button2 = st.columns(2)


with button1:

    save_clicked = st.button(
        "💾 SIMPAN PENILAIAN",
        type="primary",
        use_container_width=True
    )


with button2:

    calculate_all_clicked = st.button(
        "🧮 KIRA SEMUA MARKAH",
        use_container_width=True
    )


# =========================================================
# SAVE STUDENT
# =========================================================

if save_clicked:

    if name is None:

        st.error(
            "❌ Sila pilih nama murid."
        )

    else:

        new_student = {

            "name": name,

            "scores": {

                "Tema": tema,

                "Design": design,

                "Kreativiti": kreativiti,

                "Originality": originality
            },

            "total": current_total,

            "status": current_status
        }


        # =================================================
        # CHECK EXISTING STUDENT
        # =================================================

        existing_student = None

        for student in st.session_state.students:

            if student["name"] == name:

                existing_student = student

                break


        # =================================================
        # UPDATE EXISTING STUDENT
        # =================================================

        if existing_student:

            existing_student["scores"] = (
                new_student["scores"]
            )

            existing_student["total"] = (
                current_total
            )

            existing_student["status"] = (
                current_status
            )

            st.success(
                f"✅ Markah {name} telah dikemas kini — "
                f"{current_total:g}/100"
            )


        # =================================================
        # ADD NEW STUDENT
        # =================================================

        else:

            st.session_state.students.append(
                new_student
            )

            st.success(
                f"✅ Penilaian {name} berjaya disimpan — "
                f"{current_total:g}/100"
            )


        recalculate_and_rank()


# =========================================================
# CALCULATE ALL
# =========================================================

if calculate_all_clicked:

    if not st.session_state.students:

        st.warning(
            "⚠️ Belum ada markah murid."
        )

    else:

        recalculate_and_rank()

        st.success(
            "✅ Semua markah telah dikira dan kedudukan dikemas kini."
        )


# =========================================================
# RESULTS
# =========================================================

st.divider()

st.subheader(
    "🏆 Senarai Keputusan & Kedudukan"
)


if not st.session_state.students:

    st.info(
        "Belum ada penilaian disimpan."
    )


else:

    result_df = ranked_dataframe()

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # TOP 3 WINNERS
    # =====================================================

    st.subheader(
        "🏅 Top 3 Winners"
    )

    winners = (
        st.session_state.students[:3]
    )

    winner_columns = st.columns(3)

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]


    for index, winner in enumerate(
        winners
    ):

        with winner_columns[index]:

            st.metric(
                label=(
                    f"{medals[index]} "
                    f"Kedudukan {index + 1}"
                ),

                value=winner["name"],

                delta=(
                    f'{winner["total"]:g} / 100'
                )
            )


    # =====================================================
    # DELETE STUDENT
    # =====================================================

    st.divider()

    st.subheader(
        "🗑 Padam Penilaian"
    )

    saved_names = [

        student["name"]

        for student
        in st.session_state.students
    ]


    selected_delete = st.selectbox(
        "Pilih murid untuk dipadam",
        saved_names
    )


    if st.button(
        "🗑 PADAM MURID"
    ):

        st.session_state.students = [

            student

            for student
            in st.session_state.students

            if student["name"] != selected_delete
        ]

        recalculate_and_rank()

        st.success(
            f"✅ {selected_delete} telah dipadam."
        )

        st.rerun()


    # =====================================================
    # DOWNLOAD RESULTS
    # =====================================================

    st.divider()

    st.subheader(
        "📥 Download Keputusan"
    )

    export_df = ranked_dataframe()

    csv_data = export_df.to_csv(
        index=False
    ).encode(
        "utf-8-sig"
    )


    st.download_button(
        label="📥 DOWNLOAD CSV",
        data=csv_data,
        file_name="student_assessment_results.csv",
        mime="text/csv",
        type="primary"
    )


# =========================================================
# RESET
# =========================================================

st.divider()


if st.button(
    "🔄 RESET SEMUA KEPUTUSAN"
):

    st.session_state.students = []

    st.success(
        "✅ Semua keputusan telah direset."
    )

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Student Assessment System • "
    "Tema 20 + Design 30 + Kreativiti 30 + Originality 20 = 100"
)
