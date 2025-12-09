import streamlit as st

# ===========================
# 車種プリセット
# ===========================
vehicle_presets = {
    "Volvo EX30（51kWh / 16.7kWh/100km）": {"battery": 51.0, "efficiency": 16.7},
    "Mercedes EQB（66.5kWh / 18.1）": {"battery": 66.5, "efficiency": 18.1},
    "Peugeot e-208（50kWh / 15.9）": {"battery": 50.0, "efficiency": 15.9},
    "Nissan Leaf（40kWh / 15.0）": {"battery": 40.0, "efficiency": 15.0},
    "Nissan Ariya（66kWh / 18.0）": {"battery": 66.0, "efficiency": 18.0},
    "Tesla Model 3 SR（57.5kWh / 14.5）": {"battery": 57.5, "efficiency": 14.5},
}

# ===========================
# UI のスタイル
# ===========================
st.markdown("""
<style>
body { font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# ===========================
# タイトル
# ===========================
st.title("EV走行距離シミュレーター")

# ===========================
# 1. 車種プリセット
# ===========================
selected = st.selectbox("車種プリセットを選択してください", list(vehicle_presets.keys()))
preset = vehicle_presets[selected]

battery_default = float(preset["battery"])
eff_default = float(preset["efficiency"])

# ===========================
# 2. 充電設定
# ===========================
st.subheader("充電設定")

charger_power = st.selectbox(
    "充電器の出力を、お選びください",
    [150, 90, 50, 30]
)

# ===========================
# 3. 充電時間入力
# ===========================
charge_minutes = st.number_input("充電時間（分）", min_value=0, step=1)

# ===========================
# 4. 走行距離予測（順番を繰り上げ）
# ===========================
st.subheader("走行距離予測")

charge_hours = charge_minutes / 60
energy_added = charger_power * charge_hours
possible_km = (energy_added / eff_default) * 100

st.write(f"**約 {possible_km:.1f} km 走行可能**（入力した充電時間に基づく計算）")

# ===========================
# 5. 車両パラメータ（最後に表示）
# ===========================
st.subheader("車両パラメータ")

battery = st.number_input("バッテリー容量（kWh）", value=battery_default, step=0.1)
eff = st.number_input("電費（kWh/100km）", value=eff_default, step=0.1)
