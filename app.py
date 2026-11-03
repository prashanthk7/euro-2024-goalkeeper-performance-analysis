from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

D=Path("data/processed")
st.set_page_config(page_title="Euro 2024 Goalkeeper Profiles",page_icon="🧤",layout="wide")
st.title("UEFA Euro 2024 | Goalkeeper Performance Profiles")
st.caption("Shot danger zone • Claims & punches • Distribution • Summary • Z-score profile")
files=["goalkeeper_summary.csv","shots.csv","goalkeeper_events.csv","goal_kicks.csv"]
if not all((D/f).exists() for f in files):
 st.warning("Processed data missing. Run scripts/download_data.py and python -m src.build_analysis.");st.stop()
s=pd.read_csv(D/files[0]);shots=pd.read_csv(D/files[1]);events=pd.read_csv(D/files[2]);kicks=pd.read_csv(D/files[3])
s["claims_pm"]=s.claims/s.matches_with_goalkeeper_events.replace(0,np.nan)
s["punches_pm"]=s.punches/s.matches_with_goalkeeper_events.replace(0,np.nan)
s["sweeper_pm"]=s.sweeper_actions/s.matches_with_goalkeeper_events.replace(0,np.nan)
rad=["save_percentage","gsae_attributed","claims_pm","punches_pm","sweeper_pm","average_goal_kick_length"]
for m in rad:
 v=pd.to_numeric(s[m],errors="coerce");sd=v.std(ddof=0);s[m+"_z"]=(v-v.mean())/sd if pd.notna(sd) and sd else np.nan
eligible=s[s.matches_with_goalkeeper_events>=4].sort_values("gsae_attributed",ascending=False)
top=eligible.head(3).goalkeeper.tolist()
profiles=top+(["Manuel Neuer"] if "Manuel Neuer" not in top else [])
st.markdown("**Top-three rule:** highest reconstructed GSaE (xG faced − goals conceded), minimum four matches with goalkeeper events. Manuel Neuer is shown as a requested comparison profile.")
def pitch(title):
 f=go.Figure();green="#27823b"
 f.add_shape(type="rect",x0=0,y0=0,x1=120,y1=80,line=dict(color="white",width=2),fillcolor=green,layer="below")
 f.add_shape(type="line",x0=60,y0=0,x1=60,y1=80,line=dict(color="white"))
 f.add_shape(type="circle",x0=50,y0=30,x1=70,y1=50,line=dict(color="white"))
 for a,b in [(0,18),(102,120)]:f.add_shape(type="rect",x0=a,y0=18,x1=b,y1=62,line=dict(color="white"))
 for a,b in [(0,6),(114,120)]:f.add_shape(type="rect",x0=a,y0=30,x1=b,y1=50,line=dict(color="white"))
 f.update_layout(title=title,height=300,margin=dict(l=5,r=5,t=35,b=5),plot_bgcolor=green,paper_bgcolor="rgba(0,0,0,0)",xaxis=dict(range=[-2,122],visible=False,scaleanchor="y"),yaxis=dict(range=[-2,82],visible=False),legend=dict(orientation="h",y=-.15))
 return f
def points(f,d,x,y,name,color,symbol="circle"):
 if {x,y}.issubset(d.columns):
  q=d.dropna(subset=[x,y])
  if len(q):f.add_trace(go.Scatter(x=q[x],y=q[y],mode="markers",name=name,marker=dict(color=color,size=9,symbol=symbol,line=dict(color="white",width=.5))))
def draw(name):
 row=s[s.goalkeeper.astype(str)==name]
 if row.empty:st.warning("No summary data available for this profile.");return
 r=row.iloc[0];pid=r.goalkeeper_id
 sh=shots[shots.goalkeeper_id==pid].copy();ev=events[events.goalkeeper_id==pid].copy();kg=kicks[kicks.goalkeeper_id==pid].copy()
 st.header(name)
 st.caption(f"{int(r.matches_with_goalkeeper_events)} matches with goalkeeper events | {int(r.shots_faced_attributed)} attributed shots")
 metric_fig=go.Figure(go.Bar(x=["Save %"],y=[r.save_percentage],marker_color="#21918c",text=[f"{r.save_percentage:.1f}%" if pd.notna(r.save_percentage) else "n/a"],textposition="outside"))
 metric_fig.update_layout(title=f"{name} — shot-stopping efficiency",yaxis_title="Save percentage (%)",yaxis=dict(range=[0,100]),height=250,showlegend=False,margin=dict(l=10,r=10,t=45,b=10))
 st.plotly_chart(metric_fig,use_container_width=True)
 m=st.columns(5)
 for c,l,v,fmt in zip(m,["Save %","GSaE","xG faced","Saves","Goals conceded"],[r.save_percentage,r.gsae_attributed,r.xg_faced_attributed,r.saves,r.goals_conceded_attributed],["{:.1f}%","{:+.2f}","{:.2f}","{:.0f}","{:.0f}"]):
  c.metric(l,fmt.format(v) if pd.notna(v) else "n/a")
 a,b,c=st.columns(3)
 f=pitch("Shot danger zone")
 if "shot_x" in sh:
  for out,col in [("Goal","#ff5252"),("Saved","#ffe066"),("Saved to Post","#ffe066"),("Blocked","#67c7e8"),("Off T","#eeeeee"),("Wayward","#aaaaaa")]:points(f,sh[sh.shot_outcome==out],"shot_x","shot_y",out,col)
 a.plotly_chart(f,use_container_width=True)
 f=pitch("Claims & punches")
 if "keeper_x" in ev:
  points(f,ev[ev.action.astype(str).str.contains("claim|collected",case=False,regex=True)],"keeper_x","keeper_y","Claims","#ffe066")
  points(f,ev[ev.action.astype(str).str.contains("punch",case=False)],"keeper_x","keeper_y","Punches","#ff5252","square")
 b.plotly_chart(f,use_container_width=True)
 f=pitch("Long distribution (≥32m)")
 if {"start_x","start_y","end_x","end_y"}.issubset(kg.columns):
  q=kg[kg.kick_length>=32].dropna(subset=["start_x","start_y","end_x","end_y"])
  for _,v in q.iterrows():f.add_shape(type="line",x0=v.start_x,y0=v.start_y,x1=v.end_x,y1=v.end_y,line=dict(color="#f39c35",width=1.5))
 c.plotly_chart(f,use_container_width=True)
 x,y=st.columns(2)
 f=pitch("Short distribution (<32m)")
 if {"start_x","start_y","end_x","end_y"}.issubset(kg.columns):
  q=kg[kg.kick_length<32].dropna(subset=["start_x","start_y","end_x","end_y"])
  for _,v in q.iterrows():f.add_shape(type="line",x0=v.start_x,y0=v.start_y,x1=v.end_x,y1=v.end_y,line=dict(color="#48a9e6",width=1.5))
 x.plotly_chart(f,use_container_width=True)
 y.markdown("#### Shots & set-piece summary")
 y.dataframe(pd.DataFrame([["Shots faced",int(r.shots_faced_attributed)],["Shots on target",int(r.shots_on_target_attributed)],["Saves",int(r.saves)],["Goals conceded",int(r.goals_conceded_attributed)],["Claims",int(r.claims)],["Punches",int(r.punches)],["Sweeper actions",int(r.sweeper_actions)],["Goal kicks",int(r.goal_kicks)],["Average kick length",f"{r.average_goal_kick_length:.1f}m" if pd.notna(r.average_goal_kick_length) else "n/a"],["Short / long kicks",f"{int((kg.kick_length<32).sum())} / {int((kg.kick_length>=32).sum())}"]],columns=["Metric","Value"]),hide_index=True,use_container_width=True)
 st.markdown("#### Z-score profile")
 z=[r.get(k+"_z",np.nan) for k in rad];labels=["Save %","GSaE","Claims/match","Punches/match","Sweeper/match","Avg kick length"]
 if pd.Series(z).notna().sum()>=3:
  f=go.Figure(go.Scatterpolar(r=z+[z[0]],theta=labels+[labels[0]],fill="toself",name=name));f.update_layout(height=350,polar=dict(radialaxis=dict(visible=True)),showlegend=False);st.plotly_chart(f,use_container_width=True)
 st.caption("Radar Z-scores are recalculated across the tournament goalkeeper population; they are not a composite rating. Missing coordinates are not estimated.")
tabs=st.tabs(["Tournament shortlist"]+profiles)
with tabs[0]:
 st.subheader("Top three by reconstructed GSaE")
 st.dataframe(eligible[["goalkeeper","matches_with_goalkeeper_events","shots_faced_attributed","save_percentage","xg_faced_attributed","goals_conceded_attributed","gsae_attributed"]].head(10),hide_index=True,use_container_width=True)
 comparison=s[s.goalkeeper.astype(str).isin(profiles)].copy().set_index("goalkeeper").reindex(profiles).dropna(subset=["goalkeeper_id"])
 if not comparison.empty:
  left,right=st.columns(2)
  with left:
   fig=go.Figure(go.Bar(x=comparison.index,y=comparison.gsae_attributed,marker_color="#21918c",text=[f"{v:+.2f}" for v in comparison.gsae_attributed],textposition="outside"))
   fig.update_layout(title="GSaE comparison",yaxis_title="GSaE (xG faced − goals conceded)",height=380,margin=dict(l=10,r=10,t=45,b=80),xaxis_tickangle=-20)
   st.plotly_chart(fig,use_container_width=True)
  with right:
   fig=go.Figure(go.Bar(x=comparison.index,y=comparison.save_percentage,marker_color="#f39c35",text=[f"{v:.1f}%" if pd.notna(v) else "n/a" for v in comparison.save_percentage],textposition="outside"))
   fig.update_layout(title="Save percentage comparison",yaxis_title="Save percentage (%)",yaxis=dict(range=[0,100]),height=380,margin=dict(l=10,r=10,t=45,b=80),xaxis_tickangle=-20)
   st.plotly_chart(fig,use_container_width=True)
 st.caption("Top three are selected by GSaE with a four-match minimum; Manuel Neuer is the comparison profile.")
for tab,name in zip(tabs[1:],profiles):
 with tab:draw(name)
st.caption("Source: StatsBomb Open Data. Credit StatsBomb and review its publication terms before sharing.")
