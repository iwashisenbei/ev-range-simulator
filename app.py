import streamlit as st

st.set_page_config(page_title="EX30 充電→走行距離シミュレーター", layout="centered")

st.title("EX30 充電→走行距離シミュレーター")

st.subheader("充電器を選んでください")
charger = st.radio("充電器出力 (kW)", options=[150, 90, 50, 30], index=0)

minutes = st.number_input("充電時間（分）", min_value=1.0, value=15.0, step=1.0)

st.subheader("車両・計算パラメータ（必要なら変更）")
battery_kwh = st.number_input("バッテリー容量 (kWh)", value=69.0)
wltp_km = st.number_input("公表航続距離 (km)", value=480.0)
wltp_consumption = 100 * battery_kwh / wltp_km if wltp_km > 0 else 16.7
real_consumption = st.number_input("実走想定の電費 (kWh/100km)", value=16.7)
efficiency = st.slider("充電効率 (損失を考慮)", min_value=0.5, max_value=1.0, value=0.90, step=0.01)

energy_in = charger * (minutes / 60) * efficiency
wl_tp_km_per_kwh = 100 / wltp_consumption
theory_km = energy_in * wl_tp_km_per_kwh
real_km = energy_in * (100 / real_consumption)

st.markdown("---")
st.subheader("結果（目安）")
st.write(f"- 選択充電器: **{charger} kW**")
st.write(f"- 充電時間: **{minutes} 分**")
st.write(f"- 充電効率: **{efficiency:.2f}**")
st.write(f"- 充電で車に入る電力量（推定）: **{energy_in:.2f} kWh**")

st.write("")
st.markdown("**走行距離予測**")
st.write(f"- WLTPベース（公表値換算）: **{theory_km:.1f} km**")
st.write(f"- 実走想定: **{real_km:.1f} km**")
