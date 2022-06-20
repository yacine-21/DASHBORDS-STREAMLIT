import csv
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --------------------
NAME_APP = "FINAL BOARD"
LOGO="LOGO.png"

# --------------------

# Settings App
st.set_page_config(
    page_title=NAME_APP,
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Define my columns
col1, col2, col3 = st.columns(3)

# READ CSV 
with open('ff14_weapons_250.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

# Defive my dataframe
df = pd.DataFrame(data[1:], columns=data[0])
df.drop(df.columns[[6,7]], axis=1, inplace=True)

st.sidebar.title("Select your weapon")
weapons = df["category"].drop_duplicates()
weapon = st.sidebar.selectbox("Weapon", weapons)
st.session_state.weapon = weapon
    
st.sidebar.title("Select your stat")
column_stat = df.iloc[:,8:19]
stat = pd.DataFrame(column_stat.columns)
stat = st.sidebar.selectbox("Stat", stat)
st.session_state.stat = stat



with col1:

    weaponChoice = st.session_state.get('weapon')
    statChoice = st.session_state.get('stat')

    # select the weapon with the highest stat, I accept multiple weapons with the same stat
    weaponList = df[df["category"] == weaponChoice].sort_values(by=statChoice, ascending=False).head(5)
    weaponList2 = df[df["category"] == weaponChoice].sort_values(by=statChoice, ascending=False).head(1)
    # display the weapon with the highest stat , but only one column
    weaponList = weaponList[["level","name", statChoice]]
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown("**Top 5 weapons with the highest {}**".format(statChoice), unsafe_allow_html=True)
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # st.write(weaponList)
    st.table(weaponList)
    # plt.bar(weaponList["name"], weaponList[statChoice],align="center", alpha=0.5, color="red")
    sorted = weaponList.sort_values(by=statChoice, ascending=False)
    plt.bar(weaponList["name"], sorted[statChoice],align="center", alpha=0.8, color="red")
    plt.xticks(rotation=90)
    plt.title("Top 5 weapons with the highest {}".format(statChoice))   
    plt.xlabel("Weapon", fontsize=16)
    plt.ylabel(statChoice, fontsize=16)
    st.pyplot(fig=plt)

with col2:
    st.code("""
#### How to use this app?
1. Select your weapon
2. Select your stat
3. See the top 5 weapons with the highest stat
4. See the weapon of your choice with the highest stat
""")

    url = weaponList2['category'].values[0].replace("-","").lower().replace(" ", "").replace("'","").strip()
    st.image("images/{}.jpg".format(url), width=650)

    st.markdown("**Weapon of {} with the highest {}**".format(weaponChoice,statChoice), unsafe_allow_html=True)
    # select the weapon with the highest stat
    weaponList2 = df[df["category"] == weaponChoice].head(1)
    st.dataframe(weaponList2)