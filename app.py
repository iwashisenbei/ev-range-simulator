import streamlit as st

st.set_page_config(page_title="EV走行距離シミュレーター", layout="centered")

# -------------------------------
# CSS（エラーが出ない安全な方法）
# -------------------------------
st.markdown("""
<style>
body {
    font-family: sans-serif;
}
.title {
    font-size: 2rem;
    margin-bottom: 1rem;
}
.section-label {
    margin-top: 20px;
    font-weight: bold;
    font-size: 1.1rem;
}
.result-box {
    margin-top: 25px;
    padding: 15px;
    background: #f0f0f0;
    border-radius: 10px;
    font-size: 1.2rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
# -------------------------------
st.markdown("<div class='title'>EV走行距離シミュレーター</div>", unsafe_allow_html=True)

# -------------------------------
# 車種プリセット
# -------------------------------
st.markdown("<div class='section-label'>車種プリセットを選択してください</div>", unsafe_allow_html=True)

preset = st.selectbox(
    "",
    (
        "選択してください",
        "Volvo EX30（51kWh / 16.7）",
        "Mercedes-Benz EQB（66.5kWh / 18.1）",
        "Peugeot e-208（50kWh / 15.4）",
        "Tesla Model 3 RWD（57.5kWh / 14.9）",
        "Nissan Leaf（40kWh / 18.0）",
        "Nissan Ariya（66kWh / 18.2）"
    )
)

preset_data = {
    "Volvo EX30（51kWh / 16.7）": (51, 16.7),
    "Mercedes-Benz EQB（66.5kWh / 18.1）": (66.5, 18.1),
    "Peugeot e-208（50kWh / 15.4）": (50, 15.4),
    "Tesla Model 3 RWD（57.5kWh / 14.9）": (57.5, 14.9),
    "Nissan Leaf（40kWh / 18.0）": (40, 18.0),
    "Nissan Ariya（66kWh / 18.2）": (66, 18.2),
}

# -------------------------------
# プリセット反映
# -------------------------------
if preset in preset_data:
    battery_default, consumption_default = preset_data[preset]
else:
    battery_default, consumption_default = 50, 16.0  # デフォルト

# -------------------------------
# 車両パラメータ入力（編集可）
# -------------------------------
st.markdown("<div class='section-label'>車両パラメータ</div>", unsafe_allow_html=True)

battery = st.number_input("バッテリー容量（kWh）", value=battery_default, step=0.1)
consumption = st.number_input("100kmあたりの消費電力量（kWh/100km）", value=consumption_default, step=0.1)

# -------------------------------
# 充電器選択
# -------------------------------
st.markdown("<div class='section-label'>充電器の出力を、お選びください（kW）</div>", unsafe_allow_html=True)

charger = st.selectbox("", [3, 6, 50, 90, 150])

# -------------------------------
# 充電時間（分入力）
# -------------------------------
minutes = st.number_input("充電時間（分）", min_value=1, value=30, step=1)

# -------------------------------
# 計算
# -------------------------------
hours = minutes / 60
charged_energy = charger * hours
available_energy = min(charged_energy, battery)
estimated_range = (available_energy / consumption) * 100

# -------------------------------
# 結果表示
# -------------------------------
st.markdown("<div class='result-box'>推定走行距離： {:.1f} km</div>".format(estimated_range), unsafe_allow_html=True)
