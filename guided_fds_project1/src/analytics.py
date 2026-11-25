import pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load_data():
 return (pd.read_csv(ROOT/"data/processed/batting_summary.csv"),pd.read_csv(ROOT/"data/processed/bowling_summary.csv"),pd.read_csv(ROOT/"data/processed/match_summary.csv"))
def add_metrics(bat,bowl=None):
 x=bat.copy()
 x["batting_average"]=x.runs/(x.innings-x.not_outs).replace(0,pd.NA)
 x["strike_rate"]=100*x.runs/x.balls_faced.replace(0,pd.NA)
 x["boundary_runs"]=4*x.fours+6*x.sixes
 x["boundary_percentage"]=100*x.boundary_runs/x.runs.replace(0,pd.NA)
 return x
def select_best_xi(bat,bowl):
 b=add_metrics(bat); w=bowl.copy()
 w["economy"]=w.runs_conceded/w.overs.replace(0,pd.NA)
 w["bowling_average"]=w.runs_conceded/w.wickets.replace(0,pd.NA)
 w["bowling_score"]=w.wickets*3-w.economy.fillna(99)
 b["bat_score"]=b.runs*.35+b.batting_average.fillna(0)*.35+b.strike_rate.fillna(0)*.30
 m=b.merge(w[["player","wickets","economy","bowling_score"]],on="player",how="left")
 m["wickets"]=m.wickets.fillna(0); m["economy"]=m.economy.fillna(99)
 m["selection_score"]=m.bat_score+m.bowling_score.fillna(0)*.8
 quotas={"Wicketkeeper":1,"Top Order":3,"Middle Order":2,"All Rounder":2,"Bowler":3}; chosen=[]
 for r,n in quotas.items(): chosen.extend(m[m.role==r].sort_values("selection_score",ascending=False).head(n).to_dict("records"))
 s=pd.DataFrame(chosen).drop_duplicates("player")
 if len(s)<11: s=pd.concat([s,m[~m.player.isin(s.player)].sort_values("selection_score",ascending=False).head(11-len(s))])
 return s[["player","country","role","runs","batting_average","strike_rate","wickets","economy","selection_score"]].sort_values("selection_score",ascending=False).head(11).round(2)
