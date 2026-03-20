import sys
sys.path.insert(0, 'src')
from data_loader_new import load_cbot_corn_futures, load_dce_corn_futures

cbot_df = load_cbot_corn_futures()
dce_df = load_dce_corn_futures()

print("=== CBOT columns ===")
print(cbot_df.columns.tolist())
print("\n=== CBOT sample ===")
print(cbot_df.head(3))

print("\n=== DCE columns ===")
print(dce_df.columns.tolist())
print("\n=== DCE sample ===")
print(dce_df.head(3))
