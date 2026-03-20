import json

with open('dashboard/data/spread_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Data keys:', list(data.keys()))
print('DCE seasonal labels count:', len(data.get('dce_spreads_seasonal', {}).get('labels', [])))
print('DCE seasonal datasets:', list(data.get('dce_spreads_seasonal', {}).get('datasets', {}).keys()))
print('Wheat corn seasonal datasets:', list(data.get('wheat_corn_spreads_seasonal', {}).get('datasets', {}).keys()))
