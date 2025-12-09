import streamlit as st

st.set_page_config(page_title="EX30 充電→走行距離シミュレーター", layout="centered")

st.title("EX30 充電→走行距離シミュレーター")

# ---------------------------
# 1. 充電器の選択
# ---------------------------
st.subheader("充電器を選んでください")
charger = st.radio("充電器出力 (kW)", options=[150, 90, 50, 30], index=0)

# ---------------------------
# 2. 充電時間の入力
# ---------------------------
minutes = st.number_input("充電時間（分）", min_value=1.0, value=15.0, step=1.0)

# ---------------------------
# ■ 内部計算パラメータ（表示のみ）
# ---------------------------
with st.expander("車両・計算パラメータ（参考値・変更不可）", expanded=False):
    st.write("・バッテリー容量（kWh）: 69.0")
    st.write("・公表航続距離（km）: 480")
    st.write("・実走想定の電費（kWh/100km）: 16.7")
    st.write("・充電効率（損失を考慮）: 0.90")

battery_kwh = 69.0
wltp_km = 480.0
real_consumption = 16.7
efficiency = 0.90
wltp_consumption = 100 * battery_kwh / wltp_km

# ---------------------------
# 計算
# ---------------------------
energy_in = charger * (minutes / 60) * efficiency
wltp_km_per_kwh = 100 / wltp_consumption

theory_km = energy_in * wltp_km_per_kwh
real_km = energy_in * (100 / real_consumption)

# ---------------------------
# 3. 走行距離予測（メイン表示）
# ---------------------------
st.markdown("---")
st.subheader("走行距離予測（目安）")
st.write(f"- **WLTP換算（公表値ベース）**: {theory_km:.1f} km")
st.write(f"- **実走想定**: {real_km:.1f} km")

# ---------------------------
# 4. 結果（目安）
# ---------------------------
st.markdown("---")
st.subheader("計算に使った値（参考）")
st.write(f"- 充電器出力: **{charger} kW**")
st.write(f"- 充電時間: **{minutes} 分**")
st.write(f"- 充電効率: **{efficiency:.2f}**")
st.write(f"- 推定で車に入る電力量: **{energy_in:.2f} kWh**")
