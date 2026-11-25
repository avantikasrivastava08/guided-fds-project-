import streamlit as st
import pandas as pd
import plotly.express as px
from src.analytics import load_data, add_metrics, select_best_xi
st.set_page_config(page_title="Boundary | Cricket Intelligence",page_icon="🏏",layout="wide")
st.markdown("""<style>.stApp{background:linear-gradient(135deg,#0b1220,#111c2e);color:#eef2ff}[data-testid="stMetric"]{background:#17243a;padding:18px;border:1px solid #2a3d58;border-radius:14px}section[data-testid="stSidebar"]{background:#111c2e}h1,h2,h3{color:#f8fafc}</style>""",unsafe_allow_html=True)
st.title("🏏 BOUNDARY"); st.caption("CRICKET INTELLIGENCE STUDIO · T20 WORLD CUP ANALYTICS")
bat,bowl,matches=load_data(); bat=add_metrics(bat,bowl)
with st.sidebar:
 st.header("Control room"); countries=["All"]+sorted(bat.country.dropna().unique().tolist())
 country=st.selectbox("Country",countries); role=st.selectbox("Player role",["All"]+sorted(bat.role.dropna().unique().tolist()))
 search=st.text_input("Find a player",placeholder="e.g. Suryakumar")
 st.divider(); st.subheader("Bring your own data"); up=st.file_uploader("Upload batting CSV",type=["csv"])
 if up:
  try: bat=add_metrics(pd.read_csv(up),bowl); st.success("Batting data loaded for this session.")
  except Exception as e: st.error(f"Could not read CSV: {e}")
 st.caption("Required: player, country, role, matches, innings, runs, balls_faced, not_outs.")
df=bat.copy()
if country!="All": df=df[df.country==country]
if role!="All": df=df[df.role==role]
if search: df=df[df.player.str.contains(search,case=False,na=False)]
t1,t2,t3,t4,t5=st.tabs(["Overview","Batting lab","Bowling lab","Player face-off","Dream XI"])
with t1:
 st.subheader("Tournament overview"); c1,c2,c3,c4=st.columns(4)
 c1.metric("Players",f"{bat.player.nunique():,}"); c2.metric("Total runs",f"{int(bat.runs.sum()):,}")
 c3.metric("Total wickets",f"{int(bowl.wickets.sum()):,}"); c4.metric("Countries",f"{bat.country.nunique()}")
 a,b=st.columns(2)
 with a: st.plotly_chart(px.bar(df.sort_values("runs").tail(10),x="runs",y="player",orientation="h",color="country",title="Top run scorers",template="plotly_dark"),use_container_width=True)
 with b: st.plotly_chart(px.scatter(df,x="strike_rate",y="batting_average",size="runs",color="country",hover_name="player",title="Batting impact map",template="plotly_dark"),use_container_width=True)
 st.dataframe(df.sort_values("runs",ascending=False),use_container_width=True,hide_index=True)
with t2:
 st.subheader("Batting performance explorer"); metric=st.selectbox("Rank players by",["runs","batting_average","strike_rate","boundary_percentage","highest_score"])
 v=df.sort_values(metric,ascending=False).head(15)
 st.plotly_chart(px.bar(v,x=metric,y="player",orientation="h",color="country",title=f"Top players by {metric}",template="plotly_dark"),use_container_width=True)
 st.dataframe(v[["player","country","role","matches","runs","batting_average","strike_rate","highest_score"]],use_container_width=True,hide_index=True)
with t3:
 st.subheader("Bowling performance explorer"); bd=bowl.copy()
 bd["economy"]=bd.runs_conceded/bd.overs.replace(0,pd.NA); bd["bowling_average"]=bd.runs_conceded/bd.wickets.replace(0,pd.NA)
 bd["strike_rate"]=bd.overs*6/bd.wickets.replace(0,pd.NA)
 sort=st.selectbox("Rank bowlers by",["wickets","economy","bowling_average","strike_rate"])
 v=bd.sort_values(sort,ascending=(sort!="wickets")).head(15)
 st.plotly_chart(px.bar(v,x=sort,y="player",orientation="h",color="country",title=f"Bowling leaderboard: {sort}",template="plotly_dark"),use_container_width=True)
 st.dataframe(v,use_container_width=True,hide_index=True)
with t4:
 st.subheader("Head-to-head player comparison"); names=sorted(bat.player.unique())
 p1=st.selectbox("Player one",names,index=0); p2=st.selectbox("Player two",names,index=min(1,len(names)-1))
 comp=bat[bat.player.isin([p1,p2])].set_index("player")
 st.plotly_chart(px.bar(comp.reset_index(),x="player",y=["runs","batting_average","strike_rate"],barmode="group",title="Batting metrics comparison",template="plotly_dark"),use_container_width=True)
 st.dataframe(comp,use_container_width=True)
with t5:
 st.subheader("Build your best possible XI"); st.write("Role-aware shortlist using batting and bowling indicators.")
 xi=select_best_xi(bat,bowl); st.dataframe(xi,use_container_width=True,hide_index=True)
 st.metric("Selected squad",f"{len(xi)} / 11")
 st.download_button("⬇ Download Dream XI",xi.to_csv(index=False),"dream_xi.csv","text/csv")
st.divider(); st.caption("Demo dataset is illustrative, not verified tournament scorecards. Replace it with verified data before drawing factual conclusions.")
