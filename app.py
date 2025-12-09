<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EV走行距離シミュレーター</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    label { display: block; margin-top: 12px; }
    select, input { padding: 6px; margin-top: 4px; width: 260px; }
    .result { margin-top: 20px; font-size: 1.2rem; font-weight: bold; }
  </style>
</head>
<body>
  <h1>EV走行距離シミュレーター</h1>

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

  <label>
    バッテリー容量（kWh）
    <input id="battery" type="number" />
  </label>

  <label>
    100kmあたりの消費電力量（kWh/100km）
    <input id="consumption" type="number" step="0.1" />
  </label>

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

  <label>
    充電時間（時間）
    <input id="hours" type="number" step="0.1" />
  </label>

  <div class="result" id="resultRange"></div>

  <script>
    const presetData = {
      EX30: { battery: 51, consumption: 16.7 },
      EQB: { battery: 66.5, consumption: 18.1 },
      e208: { battery: 50, consumption: 15.4 },
      Tesla3: { battery: 57.5, consumption: 14.9 },
      Leaf: { battery: 40, consumption: 18.0 },
      Ariya: { battery: 66, consumption: 18.2 }
    };

    const carPreset = document.getElementById("carPreset");
    const battery = document.getElementById("battery");
    const consumption = document.getElementById("consumption");
    const charger = document.getElementById("charger");
    const hours = document.getElementById("hours");
    const resultRange = document.getElementById("resultRange");

    carPreset.addEventListener("change", () => {
      const key = carPreset.value;
      if (presetData[key]) {
        battery.value = presetData[key].battery;
        consumption.value = presetData[key].consumption;
      }
      calculate();
    });

    [battery, consumption, charger, hours].forEach(el => {
      el.addEventListener("input", calculate);
    });

    function calculate() {
      const bat = parseFloat(battery.value);
      const cons = parseFloat(consumption.value);
      const pow = parseFloat(charger.value);
      const h = parseFloat(hours.value);

      if (isNaN(bat) || isNaN(cons) || isNaN(pow) || isNaN(h)) {
        resultRange.textContent = "";
        return;
      }

      const chargedEnergy = pow * h;
      const available = Math.min(chargedEnergy, bat);
      const range = (available / cons) * 100;

      resultRange.textContent = `推定走行距離：${range.toFixed(1)} km`;
    }
  </script>
</body>
</html>
