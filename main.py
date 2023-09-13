import pandas
import random
import numpy as np
from matplotlib import pyplot as plt

with open("datasets/comic_characters.csv") as file:
    data = pandas.read_csv(file)

mvl = "Marvel"
dc = "DC"

# __________ List that info will be sorted to:
mvl_heroes = []
dc_heroes = []
mvl_neutrals = []
dc_neutrals = []
mvl_villains = []
dc_villains = []
dc_total_chars = 0
mvl_total_chars = 0

universe = data["Universe"].to_list()
alignment = data["Alignment"].to_list()
characters_names = data["Name"].to_list()
is_alive = data["Alive"].to_list()
appearances = data["Appearances"].to_list()
first_appeared = data["First_appeared"].to_list()
eyes = data["Eyes"].to_list()
hair = data["Hair"].to_list()
sex = data["Sex"].to_list()

# __________ Character sorter:

for name in characters_names:
    data_index = characters_names.index(name)

    if universe[data_index] == "DC":
        dc_total_chars += 1
        if alignment[data_index] == "Good":
            dc_heroes.append(name)
        elif alignment[data_index] == "Bad":
            dc_villains.append(name)
        else:
            dc_neutrals.append(name)
    elif universe[data_index] == "Marvel":
        mvl_total_chars += 1
        if alignment[data_index] == "Good":
            mvl_heroes.append(name)
        elif alignment[data_index] == "Bad":
            mvl_villains.append(name)
        else:
            mvl_neutrals.append(name)


# __________ Death rate finder

def find_death_rate(univ_name, alnmt_type):
    alive = 0
    dead = 0

    for char_name in characters_names:
        idx = characters_names.index(char_name)
        if universe[idx] == univ_name and alignment[idx] == alnmt_type:
            if is_alive[idx] == "Yes":
                alive += 1
            else:
                dead += 1
    death_rate = round(dead / (alive + dead) * 100, 2)
    return death_rate


def find_universe_dr(univ_name):
    alive = 0
    dead = 0

    for char_name in characters_names:
        idx = characters_names.index(char_name)
        if universe[idx] == univ_name:
            if is_alive[idx] == "Yes":
                alive += 1
            else:
                dead += 1

    death_rate = round((dead / (alive + dead)) * 100, 2)
    # print(f"The death rate for {univ_name} characters is {death_rate}%")
    return death_rate


# __________ Death Rates for individual categories
mvl_hero_dr = find_death_rate(mvl, "Good")
mvl_vil_dr = find_death_rate(mvl, "Bad")
dc_hero_dr = find_death_rate(dc, "Good")
dc_vil_dr = find_death_rate(dc, "Bad")
mvl_all_dr = find_universe_dr(mvl)
dc_all_dr = find_universe_dr(dc)

# _____________________ Bar Graph for death rates

bg_names = ["Marvel Heroes", "DC Heroes", "Marvel Villains", "DC Villains", "All Marvel\nCharacters",
            "All DC\nCharacters"]
bg_numbers = [mvl_hero_dr, dc_hero_dr, mvl_vil_dr, dc_vil_dr, mvl_all_dr, dc_all_dr]

fig = plt.figure(figsize=(10, 5))
plt.bar(bg_names, bg_numbers, color=["maroon", "navy"])
plt.title("Death rate of comic characters")

# Shows percentages for each bar
for index, value in enumerate(bg_numbers):
    if index % 2 == 0 or index == 0:
        temp_color = "maroon"
    else:
        temp_color = "navy"
    plt.text(index, value, f"{value}% ", color=temp_color)
plt.show()

# _____________________ Ranking Characters by appearances


# Checks validity of input
while True:
    TOP_NUM = input("Give an integer to sort by (e.g. 5 for top 5, 10 for top 10,"
                    " etc): ")
    try:
        TOP_NUM = int(TOP_NUM)
    except ValueError:
        print("Please only type numbers\n")
    else:
        break

# Creates a list of dictionaries with # of appearances as key and character_names as values
top_x = sorted(zip(appearances, characters_names), reverse=True)[:TOP_NUM]

# __________ Create a pie chart based on given top number:

# Separate lists for the top characters with their appearances
top_x_names = []
top_x_apprs = []
for item in top_x:
    top_x_apprs.append(item[0])
    top_x_names.append(item[1])

# Count total appearances across all characters
total_num_of_appearances = 0
for item in appearances:
    total_num_of_appearances += item

# Count total appearances for only specified top characters
overall_top_x_apprs = 0
for item in top_x_apprs:
    overall_top_x_apprs += item

# Sets numbers to percentages for graph
top_x_apprs_for_graph = []
for item in top_x_apprs:
    percent = (item / overall_top_x_apprs) * 100
    top_x_apprs_for_graph.append(percent)

# Double checks for any remaining values for percent
percent_check = 0
for item in top_x_apprs_for_graph:
    percent_check += item
if percent_check < 100:
    top_x_apprs_for_graph.append(100 - percent_check)
    if top_x_apprs_for_graph[-1] < 5:
        top_x_names.append("Other characters")
    else:
        top_x_names.append("")

y = np.array(top_x_apprs_for_graph)
label = []
temp_indx = 0
top_percentage = 0.00
for item in top_x_names:
    newstring = f"{item}\n{top_x_apprs[temp_indx]} appearances\n" \
                f"({round((top_x_apprs[temp_indx] / total_num_of_appearances) * 100, 2)}% of overall appearances)"
    top_percentage += (top_x_apprs[temp_indx])
    temp_indx += 1
    label.append(newstring)

top_percentage = round((top_percentage / total_num_of_appearances) * 100)
plt.pie(y, labels=label)
plt.title(f"The top {top_percentage}% of appearances")
plt.show()

top_x_as_string = f"Top {TOP_NUM} by order of appearance. \n"
placing = 1
for appearance, name in top_x:
    if placing == 1:
        top_x_as_string += f"In first place, is {name} with {appearance} overall appearances. \n"
    elif placing == 2:
        top_x_as_string += f"In second place, is {name} with {appearance} appearances. \n"
    elif placing == 3:
        top_x_as_string += f"In third place, is {name} with {appearance} appearances. \n"
    else:
        useful_words = ["Following right after", "Up Next", "Next", "Then", "After"]
        if placing == TOP_NUM:
            word = "Lastly"
        else:
            word = random.choice(useful_words)
        top_x_as_string += f"{word}, is {name} with {appearance} appearances. \n"
    placing += 1
# Can print information to screen if desired with:
# print(top_x_as_string)


# _____________________ Bar Graph directly comparing top x heroes vs top x villains

# Sorts top hero appearances categorically:
top_mvl_hero_apprs = {}
top_mvl_vil_apprs = {}

top_dc_hero_apprs = {}
top_dc_vil_apprs = {}

temp_index = 0
for item in universe:
    if item == "Marvel":
        if alignment[temp_index] == "Good":
            top_mvl_hero_apprs[characters_names[temp_index]] = appearances[temp_index]
        elif alignment[temp_index] == "Bad":
            top_mvl_vil_apprs[characters_names[temp_index]] = appearances[temp_index]
    else:
        if alignment[temp_index] == "Good":
            top_dc_hero_apprs[characters_names[temp_index]] = appearances[temp_index]
        elif alignment[temp_index] == "Bad":
            top_dc_vil_apprs[characters_names[temp_index]] = appearances[temp_index]
    temp_index += 1

top_mvl_hero_apprs = sorted(top_mvl_hero_apprs.items(), key=lambda ex: ex[1], reverse=True)
top_mvl_vil_apprs = sorted(top_mvl_vil_apprs.items(), key=lambda ex: ex[1], reverse=True)
top_dc_hero_apprs = sorted(top_dc_hero_apprs.items(), key=lambda ex: ex[1], reverse=True)
top_dc_vil_apprs = sorted(top_dc_vil_apprs.items(), key=lambda ex: ex[1], reverse=True)

# Cleans up the lists so that they are only the length of specified top number
while len(top_mvl_hero_apprs) > TOP_NUM:
    top_mvl_hero_apprs.pop(-1)
while len(top_mvl_vil_apprs) > TOP_NUM:
    top_mvl_vil_apprs.pop(-1)
while len(top_dc_hero_apprs) > TOP_NUM:
    top_dc_hero_apprs.pop(-1)
while len(top_dc_vil_apprs) > TOP_NUM:
    top_dc_vil_apprs.pop(-1)

# __________  Create a line graph to show the amount of character additions per year for each universe


years_appeared_dict = {}
for item in first_appeared:
    item = int(item[:4])

    if item in years_appeared_dict:
        years_appeared_dict[item] += 1
    else:
        years_appeared_dict[item] = 1

years_appeared_dict = dict(sorted(years_appeared_dict.items()))
year_appearance_count = list(years_appeared_dict.values())
the_years = list(years_appeared_dict.keys())

y = year_appearance_count
x = the_years
plt.plot(x, y)
plt.title("Number of character debuts per year")
plt.xlabel("Years")
plt.ylabel("Character debuts")
plt.show()

# _____________________ Pie chart to compare ratio of heroes in existence to villains (one for each universe)


# MVL Side
label = ["Heroes", "Neutral Characters", "Villains"]
y = [len(mvl_heroes), len(mvl_neutrals), len(mvl_villains)]
temp_indx = 0
for item in label:
    new_string = f"\n{round(((y[temp_indx] / mvl_total_chars) * 100), 2)}% of Marvel characters"
    label[temp_indx] += new_string
    temp_indx += 1
plt.pie(y, labels=label)
plt.title(f"Marvel Hero-to-Villain Ratio")
plt.show()

# DC Side
label = ["Heroes", "Neutral Characters", "Villains"]
y = [len(dc_heroes), len(dc_neutrals), len(dc_villains)]
temp_indx = 0
for item in label:
    new_string = f"\n{round(((y[temp_indx] / dc_total_chars) * 100), 2)}% of DC characters"
    label[temp_indx] += new_string
    temp_indx += 1
plt.pie(y, labels=label)
plt.title(f"DC Hero-to-Villain Ratio")
plt.show()

# Overall
label = ["Marvel Heroes", "Marvel Neutral Characters", "Marvel Villains", "DC Heroes", "DC Neutral Characters",
         "DC Villains"]
y = [len(mvl_heroes), len(mvl_neutrals), len(mvl_villains), len(dc_heroes), len(dc_neutrals), len(dc_villains)]

overall_char_cnt = mvl_total_chars + dc_total_chars
temp_indx = 0
for item in label:
    new_string = f"\n{round(((y[temp_indx] / overall_char_cnt) * 100), 2)}% of all characters"
    label[temp_indx] += new_string
    temp_indx += 1

plt.pie(y, labels=label)
plt.title(f"Overall Character ratio")
plt.show()

