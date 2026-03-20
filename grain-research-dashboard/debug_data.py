import sys
sys.path.insert(0, 'src')
from data_loader_new import load_all_spread_data

data = load_all_spread_data()

print("=== DCE spreads sample ===")
print(data['dce_spreads'].tail(5))

print("\n=== CBOT-DCE spreads sample ===")
print(data['cbot_dce_spreads'].tail(5))

print("\n=== Wheat-Corn spreads sample ===")
print(data['wheat_corn_spreads'].tail(5))

print("\n=== FOB basis ===")
for k, v in data['fob_basis'].items():
    print(f"  {k}: {v}")
