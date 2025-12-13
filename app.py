import streamlit as st

# ===========================
# 車種プリセット (ネスト構造に変更: ブランド名 > 車両名 > スペック)
# 単位を統一し、ブランド名でアルファベット順に並び替え
# ===========================
vehicle_presets = {
    "Mercedes": {
        "EQB": {"battery": 66.5, "efficiency": 18.1}, # 66.5kWh / 18.1kWh/100km
    },
    "Nissan": {
        "Ariya": {"battery": 66.0, "efficiency": 18.0},  # 66kWh / 18.0kWh/100km
        "Leaf": {"battery": 40.0, "efficiency": 15.0},   # 40kWh / 15.0kWh/100km
    },
    "Peugeot": {
        "e-208": {"battery": 50.0, "efficiency": 15.9},  # 50kWh / 15.9kWh/100km
    },
    "Tesla": {
        "Model 3 SR": {"battery": 57.5, "efficiency": 14.5}, # 57.5kWh / 14.5kWh/100km
    },
    "Volvo": {
        "EX30": {"battery": 51.0, "efficiency": 16.7},   # 51kWh / 16.7kWh/100km
    }
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
# 1. 車種プリセット (2段階選択)
# ===========================
st.subheader("1. 車種プリセットを選択")

# 1-1. ブランド選択
brand_list = list(vehicle_presets.keys())
selected_brand = st.selectbox("ブランドを選択してください", brand_list)

# 1-2. 車両選択 (選択されたブランドに応じてリストをフィルタリング)
if selected_brand:
    vehicle_list = list(vehicle_presets[selected_brand].keys())
    selected_vehicle = st.selectbox("車両モデルを選択してください", vehicle_list)

    if selected_vehicle:
        preset = vehicle_presets[selected_brand][selected_vehicle]
        battery_default = float(preset["battery"])
        eff_default = float(preset["efficiency"])
    else:
        # 車両モデルが選択されていない場合（通常は発生しないが、安全策として）
        battery_default = 0.0
        eff_default = 15.0
else:
    # ブランドが選択されていない場合（通常は発生しないが、安全策として）
    battery_default = 0.0
    eff_default = 15.0


# ===========================
# 2. 充電設定
# ===========================
st.subheader("2. 充電設定")

# 単位を明記 (kW)
charger_power = st.selectbox(
    "充電器の出力を、お選びください (kW)",
    [150, 90, 50, 30]
)

# ===========================
# 3. 充電時間入力
# ===========================
charge_minutes = st.number_input("充電時間（分）", min_value=0, step=1)

# ===========================
# 4. 走行距離予測
# ===========================
st.subheader("3. 走行距離予測")

charge_hours = charge_minutes / 60
energy_added = charger_power * charge_hours
possible_km = (energy_added / eff_default) * 100

# 計算結果の項目名に「予測」を追加
st.write(f"**約 {possible_km:.1f} km 走行可能（予測）**（入力した充電時間に基づく計算）")

# ===========================
# 5. 車両パラメータ (カスタム入力)
# ===========================
st.subheader("4. 車両パラメータ（カスタム入力）")

# 電費に min/max の制御を追加
battery = st.number_input("バッテリー容量（kWh）", value=battery_default, min_value=1.0, step=0.1)
eff = st.number_input("電費（kWh/100km）", value=eff_default, min_value=5.0, max_value=30.0, step=0.1)


# ===========================
# 免責事項・利用規約
# ===========================
st.markdown("---")
st.subheader("利用規約・免責事項")

st.markdown("""
<div style="border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
<p>
<strong>本シミュレーターの計算結果の利用について</strong>
</p>
<p style="font-size: 0.9em;">
本サービスで算出された<strong>走行距離予測などの計算結果</strong>は、以下の条件に従う限り、商用・非商用を問わず、自由に使用・複製・改変・頒布・公開できます。
</p>
<ul style="font-size: 0.9em; margin-left: 20px;">
    <li>本シミュレーターはあくまで<strong>概算値</strong>を提示するものであり、実際の走行条件（気温、路面状況、運転方法など）によって結果は大きく変動します。</li>
    <li>本サービスの利用、および計算結果の使用により生じた損害について、当サービスは一切の責任を負いません。</li>
    <li>利用者は、計算結果の利用にあたり、<strong>免責事項に同意したものとみなします。</strong></li>
</ul>
<p style="font-size: 0.9em; text-align: right; margin-top: 10px;">
（© EV走行距離シミュレーター）
</p>
</div>
""", unsafe_allow_html=True)
