import streamlit as st

# ===========================
# 車種プリセット (略：変更なし)
# ===========================
vehicle_presets = {
    # ... (前回のコードのvehicle_presetsの内容をそのまま使用) ...
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
# UI のスタイル (略：変更なし)
# ===========================
st.markdown("""
<style>
/* ... (カスタムCSSの内容をそのまま使用) ... */
h1 { display: none; } 
h2 { 
    font-size: 2.3rem; 
    line-height: 1.1; 
    margin-bottom: 0.5rem;
}
.st-emotion-cache-10trblm { 
    padding-top: 0rem !important;
    padding-bottom: 0.5rem !important;
}
.st-emotion-cache-z5rd5k { 
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
}
div[data-testid="stRadio"] label {
    margin: 0 !important;
}
div[data-testid="stRadio"] > div {
    gap: 0.5rem;
}
label[data-testid="stWidgetLabel"] {
    font-size: 0.9em;
    margin-bottom: 0.1rem;
}
[data-testid="stMetricLabel"] {
    padding-bottom: 0px !important;
}
[data-testid="stMetricValue"] {
    padding-top: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# ===========================
# タイトル
# ===========================
st.markdown("## EV走行距離<br>シミュレーター", unsafe_allow_html=True)

# 初期値設定
battery_default = 0.0
eff_default = 15.0


# ===========================
# 1. 車種プリセット (2段階選択)
# ===========================
st.markdown("##### 1. 車種プリセットを選択")

brand_list = sorted(list(vehicle_presets.keys()))

col1, col2 = st.columns(2)

# 1-1. ブランド選択
with col1:
    selected_brand = st.selectbox("ブランド", brand_list, key="select_brand")

# 選択されたブランドに基づく車両リストの取得
if selected_brand:
    vehicle_data = vehicle_presets.get(selected_brand, {})
    vehicle_list = list(vehicle_data.keys())
else:
    vehicle_list = []

# 1-2. 車両選択
with col2:
    selected_vehicle = st.selectbox("車両モデル", vehicle_list, key="select_vehicle")

if selected_vehicle:
    preset = vehicle_data[selected_vehicle]
    battery_default = float(preset["battery"])
    eff_default = float(preset["efficiency"])
else:
    st.info("モデルを選択してください。", icon="ℹ️")


# **【修正 A】プリセット選択値とカスタム入力値を統合する**
# プリセットが選択された場合、カスタム入力の初期値をセッションステートに設定し直す。
# これにより、カスタム入力欄と計算ロジックがプリセット値で確実に更新される。
if selected_vehicle:
    if 'battery' not in st.session_state or st.session_state.battery != battery_default:
        st.session_state.battery = battery_default
    if 'eff' not in st.session_state or st.session_state.eff != eff_default:
        st.session_state.eff = eff_default
elif 'battery' not in st.session_state:
    # 初回アクセス時など、セッションステートが存在しない場合の初期化
    st.session_state.battery = battery_default
    st.session_state.eff = eff_default

# ===========================
# 2. 充電設定と3. 充電時間入力
# ===========================
st.markdown("##### 2. 充電設定と時間入力")

col_power, col_time = st.columns([1, 1])

# 2-1. 充電器の出力 (st.radio)
with col_power:
    st.markdown("充電器の出力 (kW)")
    charger_power = st.radio(
        "充電器の出力を選択 (kW)",
        [150, 90, 50, 30],
        horizontal=True,
        key="select_power",
        label_visibility="collapsed"
    )

# 3. 充電時間入力
with col_time:
    charge_minutes = st.number_input("充電時間（分）", min_value=0, step=1, key="charge_min")


# --- UI境界線 ---
st.markdown("---")


# ===========================
# 4. 走行距離予測 (修正後の計算ロジック)
# ===========================
st.markdown("##### 3. 走行距離予測")

# **【修正 B】計算には必ずセッションステートの値（カスタム入力欄の値）を使用する**
current_battery = st.session_state.battery
current_eff = st.session_state.eff


# 安全チェック
if current_eff > 0 and charge_minutes >= 0 and current_battery > 0:
    
    charge_hours = charge_minutes / 60
    
    # 充電時間に基づいた計算上の追加エネルギー量
    calculated_energy_added = charger_power * charge_hours
    
    # バッテリー容量を超えないようにエネルギー量を制限する
    energy_added_final = min(calculated_energy_added, current_battery)
    
    # 制限がかかったかどうかのチェック
    is_limited = energy_added_final < calculated_energy_added
    
    # 走行可能距離の計算
    possible_km = (energy_added_final / current_eff) * 100
    
    # 計算結果を最も目立つように表示
    st.metric(
        label="走行可能距離（予測）",
        value=f"{possible_km:.1f} km",
        help="選択した充電時間と車両パラメータに基づく概算値です。",
    )
    
    if is_limited:
        st.caption(f"⚠️ **バッテリー容量 ({current_battery:.1f} kWh) で制限されています。**")
    
    # 修正により、選択した車両の電費が正しく表示される
    st.caption(f"（計算に使用された電費: {current_eff:.1f} kWh/100km）")

elif charge_minutes < 0:
     st.error("充電時間には正の値を入力してください。")
elif current_battery <= 0:
    st.error("バッテリー容量を正しく入力してください。")
else:
    st.warning("計算に必要なデータが不足しています。")


# --- 以降は重要度の低いフッター領域 ---
st.markdown("---")


# ===========================
# 5. 車両パラメータ (カスタム入力)
# ===========================
st.markdown("##### 4. 車両パラメータ（カスタム入力）")

col_param1, col_param2 = st.columns(2)

with col_param1:
    # プリセットが選択されると、この入力欄の値がセッションステートを通じて自動更新される
    battery = st.number_input(
        "バッテリー容量（kWh）", 
        # value引数ではなく、st.session_state.battery を初期値として使用
        value=st.session_state.battery, 
        min_value=1.0, 
        step=0.1,
        format="%.1f",
        key="battery" 
    )

with col_param2:
    # プリセットが選択されると、この入力欄の値がセッションステートを通じて自動更新される
    eff = st.number_input(
        "電費（kWh/100km）", 
        # value引数ではなく、st.session_state.eff を初期値として使用
        value=st.session_state.eff, 
        min_value=1.0, 
        max_value=50.0, 
        step=0.1,
        format="%.1f",
        key="eff"
    )


# ===========================
# 免責事項・利用規約 (フッター)
# ===========================
st.markdown("---")
st.markdown("##### 利用規約・免責事項")

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
