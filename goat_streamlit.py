import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.title('Who is the Greatest of All Time?')
st.divider()
st.image('https://dailyevergreen.com/wp-content/uploads/2023/02/2023-02-10-16.58.05-900x562.jpg')
st.subheader('This dashboard allows you to explore the careers of Michael Jordan and Lebron James through the lens of advanced analytics.')
st.link_button('Learn more about my project here', 'https://brady-heinig.github.io/')
st.divider()
st.subheader("Stats vs Different NBA Teams")
df = pd.read_csv('goat.csv')
selected_player = st.selectbox('Select a Player', df['Player'].unique(), key = 1)
selected_teams = st.multiselect('Select a Team', df['Opp Team'].unique(), default=['BOS','MIA','PHO','POR','DEN'])
selected_stat = st.selectbox('Select a Stat', options = ['Points','Assists','Field Goal %','3 Point Field Goal %','Free Throw %', 'Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers','Usage %', 'True Shooting %', 'Effective Fg %','Offensive Rating', 'Defensive Rating', 'Game Score'], key = 2)
result_df = df.groupby(['Player', 'Opp Team']).agg({f'{selected_stat}': 'mean'}).reset_index()
# result_df= result_df.sort_values(by=['Player', 'Points'], ascending=[True, False])
# result_df = result_df.groupby('Player').head(5)
player_df = result_df[result_df['Player'] == selected_player]
final_df = player_df[player_df['Opp Team'].isin(selected_teams)]
fig = px.bar(final_df, x="Opp Team", y=f"{selected_stat}", orientation='v', color = 'Opp Team', color_discrete_sequence=px.colors.qualitative.Prism, labels={'Opp Team':'Opposing Team', f'{selected_stat}':f'{selected_stat} per Game'})
fig.update_layout(title_text=f'{selected_player} {selected_stat} per Game vs Team', title_x=0.3)
st.plotly_chart(fig)
st.divider()

st.subheader("Stats by Season")
play = st.selectbox('Choose a Player', df['Player'].unique(), key = 3)
stat = st.selectbox('Select a Stat', options = ['Points','Assists','Field Goal %','3 Point Field Goal %','Free Throw %', 'Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers','Usage %', 'True Shooting %', 'Effective Fg %','Offensive Rating', 'Defensive Rating', 'Game Score'], key = 4)
playoff_df = df.groupby(['Season', 'Player','Playoffs']).agg({f'{stat}': 'mean'}).reset_index()
playoff_df = playoff_df.sort_values(by=['Player', 'Playoffs', 'Season'])
playoff_df = playoff_df[playoff_df['Player'] == play]
fig2 = px.line(playoff_df, x='Season', y=f'{stat}', color='Playoffs', color_discrete_sequence=["Purple", "LimeGreen"],
                 labels={f'{stat}': f'{stat} per Game','Season': 'Season', 'Player':'Player Name'},
                 hover_data=['Player'])
fig2.update_layout(title_text=f'{play} {stat} per Game for Each Season of Career', title_x=0.175)
st.plotly_chart(fig2)
st.divider()
st.subheader("Best Career Game Scores vs Usage Rate %")

games = st.slider('Games', min_value=1, max_value=100, value=30, step=1, key=5)
playoff_selected = st.selectbox('Playoffs?', df['Playoffs'].unique(), key = 6)

result_df = df[df['Playoffs'] == playoff_selected]
result_df= result_df.sort_values(by=['Player', 'Game Score'], ascending=[True, False])
result_df = result_df.groupby('Player').head(games)
fig3 = px.scatter(result_df, x="Game Score", y="Usage %", color="Player",
                  hover_data=['Player','Date','Opp Team', 'Result'], color_discrete_sequence=["LimeGreen", "Purple"])
fig3.update_layout(title_text=f'Top {games} Career Game Scores vs Usage Rates', title_x=0.2)
st.plotly_chart(fig3)
