import streamlit as st

# ===========================
# 車種プリセット (分類とネスト構造に追加)
# ===========================
vehicle_presets = {
    "国産車": {
        "Hyundai": {
            "IONIQ 5 (Voyage)": {"battery": 58.0, "efficiency": 15.6},
        },
        "Lexus": {
            "RZ 450e": {"battery": 71.4, "efficiency": 16.7},
        },
        "Mazda": {
            "MX-30 EV MODEL": {"battery": 35.5, "efficiency": 15.9},
        },
        "Nissan": {
            "Ariya": {"battery": 66.0, "efficiency": 18.0},
            "Leaf": {"battery": 40.0, "efficiency": 15.0},
            "Sakura S": {"battery": 20.0, "efficiency": 12.4},
        },
        "Subaru": {
            "SOLTERRA ET-HS": {"battery": 71.4, "efficiency": 16.7},
        },
        "Toyota": {
            "bZ4X Z": {"battery": 71.4, "efficiency": 16.7},
        },
    },
    "輸入車": {
        "Audi": {
            "e-tron Sportback 55": {"battery": 95.0, "efficiency": 23.3},
        },
        "BMW": {
            "i4 eDrive40": {"battery": 83.9, "efficiency": 16.7},
            "iX3 M Sport": {"battery": 80.0, "efficiency": 17.5},
        },
        "Jaguar": {
            "I-PACE S EV400": {"battery": 90.0, "efficiency": 20.3},
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
        "Peugeot": {
            "e-208 Allure": {"battery": 50.0, "efficiency": 15.9},
            "e-2008 GT": {"battery": 50.0, "efficiency": 16.8},
            "e-RIFTER": {"battery": 50.0, "efficiency": 21.0},
        },
        "Porsche": {
            "Taycan 4S": {"battery": 79.2, "efficiency": 23.8},
        },
        "Tesla": {
            "Model 3 LR": {"battery": 78.1, "efficiency": 14.9},
            "Model 3 SR": {"battery": 57.5, "efficiency": 14.5},
            "Model Y RWD": {"battery": 57.5, "efficiency": 16.7},
        },
        "Volvo": {
            "C40 Recharge Ultimate": {"battery": 78.0, "efficiency": 18.0},
            "EX30 Single Motor": {"battery": 51.0, "efficiency": 16.7},
            "XC40 Recharge Ultimate": {"battery": 78.0, "efficiency": 18.0},
        },
    },
}

# ===========================
# UI のスタイル
# ===========================
st.markdown("""
<style>
body { font-family: sans-serif; }
/* st.radio の縦の隙間を減らしてコンパクトにする */
div[data-testid="stRadio"] label {
    margin: 0 !important;
}
div[data-testid="stRadio"] > div {
    gap: 0.5rem; /* ボタン間のスペース調整 */
}
</style>
""", unsafe_allow_html=True)

# ===========================
# タイトル
# ===========================
st.title("EV走行距離シミュレーター")

# 初期値設定
battery_default = 0.0
eff_default = 15.0


# ===========================
# 1. 車種プリセット (3段階選択)
# ===========================
st.subheader("1. 車種プリセットを選択")

# 1-1. 分類選択 (国産車/輸入車)
col1, col2 = st.columns(2)
with col1:
    category_list = list(vehicle_presets.keys())
    selected_category = st.selectbox("分類", category_list)

# 選択された分類に基づくブランドリストの取得
selected_brands_data = vehicle_presets.get(selected_category, {})
brand_list = sorted(list(selected_brands_data.keys()))

with col2:
    # 1-2. ブランド選択
    selected_brand = st.selectbox("ブランド", brand_list)

# 選択されたブランドに基づく車両リストの取得
if selected_brand:
    vehicle_data = selected_brands_data.get(selected_brand, {})
    vehicle_list = list(vehicle_data.keys())
else:
    vehicle_list = []

# 1-3. 車両選択
selected_vehicle = st.selectbox("車両モデル", vehicle_list)

if selected_vehicle:
    preset = vehicle_data[selected_vehicle]
    battery_default = float(preset["battery"])
    eff_default = float(preset["efficiency"])
elif selected_category:
    st.info("選択した分類/ブランドに該当する車両がありません。手動でパラメータを入力してください。")


# --- UI境界線 (表示領域の調整) ---
st.markdown("---")

# ===========================
# 2. 充電設定
# ===========================
st.subheader("2. 充電設定")

# 2-1. 充電器の出力 (st.radioでボタン選択に変更)
charger_power = st.radio(
    "充電器の出力を選択 (kW)",
    [150, 90, 50, 30],
    horizontal=True # 横並び表示
)

# ===========================
# 3. 充電時間入力
# ===========================
charge_minutes = st.number_input("充電時間（分）", min_value=0, step=1, key="charge_min")


# ===========================
# 4. 走行距離予測
# ===========================
st.subheader("3. 走行距離予測")

# 安全チェック（電費が0の場合のゼロ除算を防ぐ）
if eff_default > 0 and charge_minutes >= 0:
    charge_hours = charge_minutes / 60
    energy_added = charger_power * charge_hours
    possible_km = (energy_added / eff_default) * 100
    
    # 計算結果の表示を強調
    st.metric(
        label="走行可能距離（予測）",
        value=f"{possible_km:.1f} km",
        help="選択した充電時間と車両パラメータに基づく概算値です。",
    )
elif charge_minutes < 0:
     st.error("充電時間には正の値を入力してください。")
else:
    st.warning("計算に必要なデータが不足しています。")


# --- UI境界線 ---
st.markdown("---")


# ===========================
# 5. 車両パラメータ (カスタム入力)
# ===========================
st.subheader("4. 車両パラメータ（カスタム入力）")

# 入力欄を2列に分けてコンパクトに
col_param1, col_param2 = st.columns(2)

with col_param1:
    battery = st.number_input(
        "バッテリー容量（kWh）", 
        value=battery_default, 
        min_value=1.0, 
        step=0.1,
        format="%.1f"
    )

with col_param2:
    eff = st.number_input(
        "電費（kWh/100km）", 
        value=eff_default, 
        min_value=1.0, 
        max_value=50.0, 
        step=0.1,
        format="%.1f"
    )


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
