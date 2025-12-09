<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EV走行距離シミュレーター</title>
  <style>
    body { font-family: sans-serif; padding: 20px; background: #f7f7f7; }
    label { display: block; margin-top: 14px; font-weight: bold; }
    select, input { padding: 8px; margin-top: 6px; width: 260px; }
    h1 { margin-bottom: 6px; }
    .unit { padding-left: 6px; }
    .result {
      margin-top: 24px;
      font-size: 1.4rem;
      font-weight: bold;
      background: white;
      padding: 14px;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      width: 280px;
    }
  </style>
</head>
<body>
  <h1>EV走行距離シミュレーター</h1>

  <!-- 車種プリセット -->
  <label>
    車種プリセットを選択してください
    <select id="carPreset">
      <option value="">選択してください</option>
      <option value="EX30">Volvo EX30（51kWh / 16.7kWh/100km）</option>
      <option value="EQB">Mercedes-Benz EQB（66.5kWh / 18.1kWh/100km）</option>
      <option value="e208">Peugeot e-208（50kWh / 15.4kWh/100km）</option>
      <option value="Tesla3">Tesla Model 3 RWD（57.5kWh / 14.9kWh/100km）</option>
      <option value="Leaf">Nissan Leaf（40kWh / 18.0kWh/100km）</option>
      <option value="Ariya">Nissan Ariya（66kWh / 18.2kWh/100km）</option>
    </select>
  </label>

  <!-- バッテリー容量 -->
  <label>
    バッテリー容量（kWh）
    <input id="battery" type="number" />
  </label>

  <!-- 消費電力量 -->
  <label>
    100kmあたりの消費電力量（kWh/100km）
    <input id="consumption" type="number" step="0.1" />
  </label>

  <!-- 充電器出力 -->
  <label>
    充電器の出力を、お選びください（kW）
    <select id="charger">
      <option value="3">3kW（普通充電）</option>
      <option value="6">6kW（普通充電）</option>
      <option value="50">50kW（急速）</option>
      <option value="90">90kW（急速）</option>
      <option value="150">150kW（急速）</option>
    </select>
  </label>

  <!-- 充電時間（分） -->
  <label>
    充電時間（分）
    <input id="minutes" type="number" step="1" min="1" />
  </label>

  <div class="result" id="resultRange"></div>

  <script>
    // プリセット値
    const presetData = {
      EX30: { battery: 51, consumption: 16.7 },
      EQB: { battery: 66.5, consumption: 18.1 },
      e208: { battery: 50, consumption: 15.4 },
      Tesla3: { battery: 57.5, consumption: 14.9 },
      Leaf: {
