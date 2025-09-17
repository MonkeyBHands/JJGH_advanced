import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Single Player Analysis",
    page_icon='data/JJGH.jpeg',
)

# st.title("Single Player Deep Dive")
# st.write("This app will help you analyze NFL data effectively.")

def load_data():
    
    data1=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2020.parquet')
    data2=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2021.parquet')
    data3=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2022.parquet')
    data4=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2023.parquet')
    data5=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2024.parquet')
    data6=pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/stats_player/stats_player_week_2025.parquet')
    df=pd.concat([data1,data2,data3,data4,data5,data6])
    return df

pdata = pd.read_parquet('https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet')

df = load_data()
df['year_week'] = df['season'] + df['week']/25

name = st.sidebar.multiselect(
    "Select Player",
    df.player_display_name.unique(), max_selections=1, default=['Tom Brady'],
)

st.sidebar.write("Brought to you by:")
st.sidebar.image('data/JJGH.jpeg', width=300)

playerid=df[df['player_display_name'].isin(name)]['player_id'].unique().tolist()

player = pdata[pdata['gsis_id']== playerid[0]] if playerid else pd.DataFrame()
img_url = player['headshot'].values[0] if not player.empty else "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
st.image(img_url, width=500)

col1, col2 = st.columns(2)

with col1:
     if name==[]:
         st.write("Please select a player from the sidebar.")
     else:
        st.header(name[0] if name else "No Player Selected")
        st.write(f'Position: {player["position"].values[0] if not player.empty else ""}')
        st.write(f'Latest Team: {player["latest_team"].values[0] if not player.empty else ""}')
        st.write(f'Jersey Number: {int(player["jersey_number"].values[0]) if not player.empty and pd.notnull(player["jersey_number"].values[0]) else ""}')
        st.write(f'Draft Year: {int(player["draft_year"].values[0]) if not player.empty and pd.notnull(player["draft_year"].values[0]) else ""}')
        st.write(f'Last Season: {player["last_season"].values[0] if not player.empty else ""}')
        st.write(f'College Name: {player["college_name"].values[0] if not player.empty else ""}')
        st.write(f'Birth Date: {player["birth_date"].values[0] if not player.empty else ""}')
        st.write(f'Years of Experience: {player["years_of_experience"].values[0] if not player.empty else ""}')
        st.write(f'Height: {player["height"].values[0]*2.54:.2f} cm' if not player.empty else "")
        st.write(f'Weight: {player["weight"].values[0]/2.205:.2f} kg' if not player.empty else "")


with col2:
    
    career_stats = df[df['player_display_name'].isin(name)]
    if not career_stats.empty:
        st.header("Career Stats (2020+)")
        st.write(f"Total Games Played: {career_stats.shape[0]}")
        st.write(f"Total Passing Yards: {career_stats['passing_yards'].sum()}")
        st.write(f"Total Passing TD/Ints: {career_stats['passing_tds'].sum()} / {career_stats['passing_interceptions'].sum()}")
        st.write(f'Total Carries: {career_stats["carries"].sum()}')
        st.write(f"Total Rushing Yards: {career_stats['rushing_yards'].sum()}")
        st.write(f"Total Rushing Touchdowns: {career_stats['rushing_tds'].sum()}")
        st.write(f"Total Receiving Yards: {career_stats['receiving_yards'].sum()}")
        st.write(f"Total Receiving Touchdowns: {career_stats['receiving_tds'].sum()}")
        st.write(f"Total Receptions: {career_stats['receptions'].sum()} / {career_stats['targets'].sum()}")
        st.write(f"Total Fantasy Points: {career_stats['fantasy_points'].sum():.2f}")
    else:
        st.write("No data available for the selected player.")

st.markdown("---")

my_expander = st.expander(label='Graph Options', expanded=False)
with my_expander:
    
    years2 = st.slider("Season", 2020, 2025, (2024, 2025))
    week2 = st.slider("Week", 1, 18, (1, 18))
    post=st.checkbox("Include Post-Season")
    st.markdown("---")
    if post:
        week2p="POST"
    else:
        week2p="REG"
    
    ColA, ColB, ColC = st.columns(3)

    with ColA:
        st.write('Passing')
        option_1 = ColA.checkbox('Comp/Att/Int')
        option_2 = ColA.checkbox('Passing Yards')
        option_3 = ColA.checkbox('Passing EPA/CPOE')
        # option_4 = ColA.checkbox('Passing Touchdowns')
        option_5 = ColA.checkbox('PACR')
  
    with ColB:
        st.write('Receiving')
        # option_6 = ColB.checkbox('Receiving Touchdowns')
        option_7 = ColB.checkbox('Recep/Targ')
        # option_8 = ColB.checkbox('Targets')
        option_9 = ColB.checkbox('Receiving Yards')
        option_10 = ColB.checkbox('Receiving EPA')

    with ColC:
        st.write('Rushing')
        # option_11 = ColC.checkbox('Rushing Touchdowns')
        option_12 = ColC.checkbox('Carries')
        option_13 = ColC.checkbox('Rushing Yards')
        option_14 = ColC.checkbox('Rushing EPA')

    st.markdown("Miscellaneous")

    ColD, ColE, ColF = st.columns(3)

    with ColD:
       
        option_15 = ColD.checkbox('Touchdowns')
        option_16 = ColE.checkbox('Fumbles')
        option_17 = ColF.checkbox('Fantasy Points')

df['year_week'] = df['season'] + df['week']/25


df_filtered = df[(df["player_id"].isin(playerid)) & (df["season"].between(years2[0], years2[1])) & ((df["week"].between(week2[0], week2[1])) | (df["season_type"]==week2p))]

fig = plt.figure(figsize=(10,6))
if not df_filtered.empty:
    for name,group in df_filtered.groupby('player_display_name'):
        if option_1:
            plt.plot(group['year_week'],group['completions'],marker='o',label=f'{name} - Completions',alpha=0.7)
            plt.plot(group['year_week'],group['attempts'],marker='x',label=f'{name} - Pass Attempts',alpha=0.7)
            plt.plot(group['year_week'],group['passing_interceptions'],marker='*',label=f'{name} - Interceptions',alpha=0.7)
        if option_2:
            plt.plot(group['year_week'],group['passing_yards'],marker='o',label=f'{name} - Passing Yards',alpha=0.7)
        if option_3:
            plt.plot(group['year_week'],group['passing_epa'],marker='o',label=f'{name} - Passing EPA',alpha=0.7)
            plt.plot(group['year_week'],group['passing_cpoe'],marker='o',label=f'{name} - Passing CPOE',alpha=0.7)
        # if option_4:
            # plt.plot(group['year_week'],group['passing_tds'],marker='o',label=f'{name} - Passing Touchdowns',alpha=0.7)
        if option_5:
            plt.plot(group['year_week'],group['pacr'],marker='o',label=f'{name} - PACR',alpha=0.7)
        # if option_6:
            # plt.plot(group['year_week'],group['receiving_tds'],marker='s',label=f'{name} - Receiving TDs',alpha=0.7)
        if option_7:
            plt.plot(group['year_week'],group['receptions'],marker='s',label=f'{name} - Receptions',alpha=0.7)
            plt.plot(group['year_week'],group['targets'],marker='s',label=f'{name} - Targets',alpha=0.7)
        # if option_8:
            # plt.plot(group['year_week'],group['targets'],marker='s',label=f'{name} - Targets',alpha=0.7)
        if option_9:
            plt.plot(group['year_week'],group['receiving_yards'],marker='s',label=f'{name} - Receiving Yards',alpha=0.7)
        if option_10:
            plt.plot(group['year_week'],group['receiving_epa'],marker='s',label=f'{name} - Receiving EPA',alpha=0.7)
        # if option_11:
            # plt.plot(group['year_week'],group['rushing_tds'],marker='d',label=f'{name} - Rushing TDs',alpha=0.7)
        if option_12:
            plt.plot(group['year_week'],group['carries'],marker='d',label=f'{name} - Carries',alpha=0.7)
        if option_13:
            plt.plot(group['year_week'],group['rushing_yards'],marker='d',label=f'{name} - Rushing Yards',alpha=0.7)
        if option_14:
            plt.plot(group['year_week'],group['rushing_epa'],marker='d',label=f'{name} - Rushing EPA',alpha=0.7)
            
        if option_15:
            plt.plot(group['year_week'],group['passing_tds'],marker='*',label=f'{name} - Passing Touchdowns',alpha=0.7)
            plt.plot(group['year_week'],group['rushing_tds'],marker='*',label=f'{name} - Rushing Touchdowns',alpha=0.7)
            plt.plot(group['year_week'],group['receiving_tds'],marker='*',label=f'{name} - Receiving Touchdowns',alpha=0.7)
        if option_16:
            plt.plot(group['year_week'],group['sack_fumbles'],marker='v',label=f'{name} - Sack Fumbles',alpha=0.7)
            plt.plot(group['year_week'],group['receiving_fumbles'],marker='v',label=f'{name} - Receiving Fumbles',alpha=0.7)
            plt.plot(group['year_week'],group['rushing_fumbles'],marker='v',label=f'{name} - Rushing Fumbles',alpha=0.7)
        if option_17:
            plt.plot(group['year_week'],group['fantasy_points'],marker='x',label=f'{name} - Fantasy Points',alpha=0.7)
    # plt.title(f'Fantasy Points by Week')
    plt.xlabel('Week')
    # plt.ylabel('Points')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()
    if option_1 or option_2 or option_3 or option_5 or option_7  or option_9 or option_10 or option_12 or option_13 or option_14 or option_15 or option_16 or option_17:
        st.pyplot(fig)
        
    st.write(df_filtered[['completions','attempts','passing_interceptions','passing_yards','passing_epa','passing_cpoe','pacr','receptions','targets','receiving_yards','receiving_epa','carries','rushing_yards','rushing_epa','passing_tds','receiving_tds','rushing_tds','sack_fumbles','receiving_fumbles','rushing_fumbles','fantasy_points']].describe())
else:
    st.write("No data available for the selected player and filters.")

st.write("All data provided by https://github.com/nflverse/nflverse-data/releases")
st.write("Brought to you by JJGH - There ain't no glory hole like a Jerry Jones Glory Hole!")