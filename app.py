import streamlit as st

# ===========================
# 車種プリセット (ネスト構造: ブランド名 > 車両名 > スペック)
# 全ての公表データを追加し、ブランド名でアルファベット順に並び替え
# 単位は「kWh/100km」に統一
# ===========================
vehicle_presets = {
    "Audi": {
        "e-tron Sportback 55": {"battery": 95.0, "efficiency": 23.3},
    },
    "BMW": {
        "i4 eDrive40": {"battery": 83.9, "efficiency": 16.7},
        "iX3 M Sport": {"battery": 80.0, "efficiency": 17.5},
    },
    "Hyundai": {
        "IONIQ 5 (Voyage)": {"battery": 58.0, "efficiency": 15.6},
    },
    "Jaguar": {
        "I-PACE S EV400": {"battery": 90.0, "efficiency": 20.3},
    },
    "Lexus": {
        "RZ 450e": {"battery": 71.4, "efficiency": 16.7},
    },
    "Mazda": {
        "MX-30 EV MODEL": {"battery": 35.5, "efficiency": 15.9},
    },
    "Mercedes-Benz": {
        "EQA 250": {"battery": 66.5, "efficiency": 16.3},
        "EQB 250": {"battery": 66.5, "efficiency": 18.1},
        "EQE 350+": {"battery": 90.6, "efficiency": 17.2},
        "EQS 450+": {"battery": 107.8, "efficiency": 17.0},
    },
    "MINI": {
        "MINI COOPER S E": {"battery": 32.6, "efficiency": 16.6},
    },
    "Nissan": {
        "Ariya": {"battery": 66.0, "efficiency": 18.0},
        "Leaf": {"battery": 40.0, "efficiency": 15.0},
        "Sakura S": {"battery": 20.0, "efficiency": 12.4},
    },
    "Peugeot": {
        "e-208 Allure": {"battery": 50.0, "efficiency": 15.9},
        "e-2008 GT": {"battery": 50.0, "efficiency": 16.8},
        "e-RIFTER": {"battery": 50.0, "efficiency": 21.0},
    },
    "Porsche": {
        "Taycan 4S": {"battery": 79.2, "efficiency": 23.8},
    },
    "Subaru": {
        "SOLTERRA ET-HS": {"battery": 71.4, "efficiency": 16.7},
    },
    "Tesla": {
        "Model 3 LR": {"battery": 78.1, "efficiency": 14.9},
        "Model 3 SR": {"battery": 57.5, "efficiency": 14.5},
        "Model Y RWD": {"battery": 57.5, "efficiency": 16.7},
    },
    "Toyota": {
        "bZ4X Z": {"battery": 71.4, "efficiency": 16.7},
    },
    "Volvo": {
        "C40 Recharge Ultimate": {"battery": 78.0, "efficiency": 18.0},
        "EX30 Single Motor": {"battery": 51.0, "efficiency": 16.7},
        "XC40 Recharge Ultimate": {"battery": 78.0, "efficiency": 18.0},
    },
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
brand_list = sorted(list(vehicle_presets.keys())) # ブランドリストをソート
selected_brand = st.selectbox("ブランドを選択してください", brand_list)

# 初期値設定（選択がない場合の安全策）
battery_default = 0.0
eff_default = 15.0
selected_vehicle = None

if selected_brand:
    vehicle_data = vehicle_presets[selected_brand]
    vehicle_list = list(vehicle_data.keys())
    
    # 1-2. 車両選択 (選択されたブランドに応じてリストをフィルタリング)
    selected_vehicle = st.selectbox("車両モデルを選択してください", vehicle_list)

    if selected_vehicle:
        preset = vehicle_data[selected_vehicle]
        battery_default = float(preset["battery"])
        eff_default = float(preset["efficiency"])
    else:
        # ブランドが選択されているがモデルがない場合（空のリストの場合など）
        st.warning("選択されたブランドにモデルがありません。手動でパラメータを入力してください。")


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

# 安全チェック（電費が0の場合のゼロ除算を防ぐ）
if eff_default > 0 and charge_minutes > 0:
    charge_hours = charge_minutes / 60
    energy_added = charger_power * charge_hours
    possible_km = (energy_added / eff_default) * 100
    
    # 計算結果の項目名に「予測」を追加
    st.write(f"**約 {possible_km:.1f} km 走行可能（予測）**（入力した充電時間に基づく計算）")
elif charge_minutes == 0:
     st.write("充電時間（分）を入力してください。")
else:
    st.write("計算に必要なデータが選択または入力されていません。")


# ===========================
# 5. 車両パラメータ (カスタム入力)
# ===========================
st.subheader("4. 車両パラメータ（カスタム入力）")

# 電費に min/max の制御を追加
battery = st.number_input("バッテリー容量（kWh）", value=battery_default, min_value=1.0, step=0.1)
# 電費は min_value=1.0 に変更（現実的な最小値を考慮）
eff = st.number_input("電費（kWh/100km）", value=eff_default, min_value=1.0, max_value=50.0, step=0.1)


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
