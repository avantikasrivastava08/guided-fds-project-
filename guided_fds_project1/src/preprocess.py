"""Convert raw JSON scorecards to CSV. Supports lists and nested JSON objects."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data/raw"; OUT=ROOT/"data/processed"
def records(obj):
 if isinstance(obj,list): return sum((records(x) for x in obj),[])
 if isinstance(obj,dict):
  if all(not isinstance(v,(dict,list)) for v in obj.values()): return [obj]
  return sum((records(v) for v in obj.values() if isinstance(v,(dict,list))),[])
 return []
for name in ["match_summary","batting_summary","bowling_summary"]:
 p=RAW/f"{name}.json"
 if p.exists():
  df=pd.json_normalize(records(json.loads(p.read_text(encoding="utf-8")))).drop_duplicates().dropna(axis=1,how="all")
  df.to_csv(OUT/f"{name}.csv",index=False); print(f"{name}: {len(df)} rows")
 else: print(f"Skipped {name}: raw JSON not found")
