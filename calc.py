# calc.py
# EX30向け：WLTPベースと理論最大（カタログ）ベースの両方を返す
# 保存名を calc.py にして、同じフォルダで python calc.py を実行してください。

def estimate_by_wltp(charge_kw, minutes, consumption_kwh_per_100km, efficiency=0.90):
    """WLTP/実用ベース（kWh/100km を使う）"""
    energy_in = charge_kw * (minutes / 60) * efficiency
    distance = energy_in / consumption_kwh_per_100km * 100
    return round(energy_in, 2), round(distance, 1)

def estimate_by_theory(charge_kw, minutes, claimed_range_km, battery_kwh, efficiency=0.90):
    """理論ベース（カタログ航続距離 ÷ バッテリー容量）"""
    km_per_kwh = claimed_range_km / battery_kwh
    energy_in = charge_kw * (minutes / 60) * efficiency
    distance = energy_in * km_per_kwh
    return round(km_per_kwh, 3), round(energy_in, 2), round(distance, 1)

def choose_charger():
    choices = { "1":150, "2":90, "3":50, "4":30 }
    print("充電器を選んでください:")
    print("1) 150 kW   2) 90 kW   3) 50 kW   4) 30 kW")
    c = input("番号を入力: ").strip()
    while c not in choices:
        c = input("1-4 の番号を入力してください: ").strip()
    return choices[c]

def main():
    print("=== EX30 充電→走行距離シミュレーター ===")
    charger_kw = choose_charger()
    minutes = float(input("充電時間（分）を入力してください: ").strip())

    # EX30 のデフォルト設定（ユーザーが編集可能）
    # 例：69 kWh / 公表 480 km（モデルにより変わるため入力可）
    battery_kwh = float(input("バッテリー容量(kWh)（デフォルト 69）を入力（Enterでデフォルト）: " or 69) or 69)
    claimed_range_km = float(input("公表航続距離(km)（例 480。Enterで480）: " or 480) or 480)
    consumption_kwh_per_100km = float(input("実走想定の電費 kWh/100km（例16.7。Enterで16.7）: " or 16.7) or 16.7)

    # 充電効率（デフォルト 90%）
    efficiency = input("充電効率（0-1、デフォルト0.90）: ").strip()
    efficiency = float(efficiency) if efficiency != "" else 0.90

    # WLTP/実用ベース
    energy_wltp, distance_wltp = estimate_by_wltp(charger_kw, minutes, consumption_kwh_per_100km, efficiency)

    # 理論（カタログ）ベース
    km_per_kwh, energy_theory, distance_theory = estimate_by_theory(charger_kw, minutes, claimed_range_km, battery_kwh, efficiency)

    print("\n--- 結果 ---")
    print(f"充電器出力: {charger_kw} kW, 充電時間: {minutes} 分, 充電効率: {efficiency}")
    print(f"(WLTP/実用) 充電で入る電力量: {energy_wltp} kWh -> 予想走行距離: {distance_wltp} km")
    print(f"(理論カタログ) 1 kWh あたり: {km_per_kwh} km/kWh, 充電で入る電力量: {energy_theory} kWh -> 予想走行距離: {distance_theory} km")
    print("\n注: 実際の走行可能距離は温度・速度・SOC・充電曲線・ロス等で変動します。")

if __name__ == "__main__":
    main()

