import sys
sys.path.insert(0, 'src')
from data_loader_new import load_all_spread_data

data = load_all_spread_data()

print("\n=== Data Summary ===")
for key, val in data.items():
    if val is not None:
        if hasattr(val, 'shape'):
            print(f"{key}: {val.shape}")
        elif isinstance(val, dict):
            print(f"{key}: dict with {len(val)} keys")
        else:
            print(f"{key}: {type(val)}")
