import requests
import time
import plotly.express as px

leaderboard = requests.get("https://api.manarion.com/leaderboards/highest_damage_spell_rank?page=1&gameMode=0").json()
guildlist = requests.get("https://api.manarion.com/guilds?gameMode=0").json()
names = []

# Obtaining names from the leaderboard
for i in leaderboard['Entries']:
    names.append(i['Name'])

playerdata = []

# Fetching player data for the names in the leaderboard
for name in names[:5]:
    url = f"https://api.manarion.com/players/{name}"
    playerdata.append(requests.get(url).json())
    time.sleep(2)

incomes = []
guildIDs = []

# Calculating incomes for names in leaderboard based on playerdata.
for name in playerdata:
    income = (((0.0001 * (name['Enemy'] + 150) ** 2 + (name['Enemy'] + 150) ** 1.2 + 10 * (name['Enemy'] + 150)) 
            * (1.01 ** (((name['Enemy'] + 150) - 150000) / 2000))) 
            * (1 + name['TotalBoosts']['121']/100) 
            * (1 + name['TotalBoosts']['101']/100) 
            * 27400
            * (1 + name['TotalBoosts'].get('161',0) * 0.002))
    incomes.append(income)

# Taking guild IDs from playerdata.
for i in playerdata:
    guild = i['GuildID']
    guildIDs.append(guild)

# Translating guildID to guildname.
guildname = []
for i in guildIDs:
    found = False

    for j in guildlist:
        if j["ID"] == i:
            guildname.append(j["Name"])
            found = True
            break
    if not found:
        guildname.append("No guild")

# Sorting the two lists to descending income values.
combined = list(zip(incomes, names, guildname))
combined.sort(reverse=True)

incomes, names, guildname = zip(*combined)

incomes = list(incomes)
names = list(names)
guildname = list(guildname)

# Plotting the names and corresponding incomes
fig = px.bar(
    x = incomes,
    y = names,
    orientation = "h",
    labels = {"x":"Daily untaxed dust income", "y": "Battlor"},
    title = "Top100 battlor income",
    color = guildname,
    category_orders = {'y': names}
)
fig.update_traces(width = 0.2)
fig.update_layout(height=max(400, len(names) * 40))
fig.write_html("docs/top100battlor.html")