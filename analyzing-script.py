
# ! this entire scripts does the following:
    # ! reads in the data collected using the data-collection-script.py
    # ! makes minor tweaks to allow for merging
    # ! merge the two files together to get the number of wins for each team for each year, along with their stats for that year
    # ! plots the relationship between free throw % and number of wins for each year
    # ! runs a simple linear regression on the entire dataset, might change year-to-year



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


stats = pd.read_csv("stats_history.csv")
winners = pd.read_csv("winners_history.csv")

# not sure how we got data for 2020 in the winners df, it wasnt available on the site
# regardless, the NCAA tounrament didnt happen this year so we need to remove it
stats = stats[stats["YEAR"] != 2020]
winners = winners[winners["YEAR"] != 2020]

# when we collected our stats data, the table we scraped from included whether or not that team made the tournament
# EXAMPLE: if Alabama made the tournament in 2010, then when we scraped the team name it came out as 'Alabama NCAA'
# this is not the case for our winners data, so when we merge, we get NO matches
# need to replace the " NCAA" with nothing so we can get matches
substring = " NCAA"
stats["TEAM"] = stats["TEAM"].apply(lambda x: x.replace(substring, ""))


# rename this column to match the one in the stats df
# this is because we need to merge them later on this column and they need to have the same name
winners = winners.rename(columns={"WINNERS":"TEAM"})


# group the winners df by TEAM and YEAR. this gives us the number of wins for each team in each year
# we then reset the index and renamed the aggregated column to WINS (AKA number of wins)
# ! NOTE: before i was not resetting the index, this meant that team and year are being forced into the index and messed up my merge later
# ! by resetting the index, this puts team and year back into columns in the df, along with the count
winner_counts = winners.groupby("TEAM")["YEAR"].value_counts().reset_index(name="WINS")


# merge the two dataframes on the TEAM using an inner join
# this gives us each team and each year with their number of wins for that year and their stats from that year
FTs_with_win_counts = pd.merge(stats, winner_counts, on = ["TEAM", "YEAR"], how = "inner")

file_base = "/Users/drewc/OneDrive/Documents/2024/Python/March Madness/"
FTs_with_win_counts.to_csv(file_base + "stats_with_wins.csv", index = False)

# the years are from 2010-2023 (excluding 2020) which is 13 years, thats why the plots are a 3x5 grid
unique_years = sorted(FTs_with_win_counts["YEAR"].unique())
num_rows = 5
num_cols = 3
total_plots = num_rows * num_cols

# set up the grid of the subplot
# axs is a 2D array of axes objects that can accessed through traditional indexing axs[row, col]
# fig represents that entire canvas or figure that the subplots are plotted on
fig, axs = plt.subplots(nrows = num_rows, ncols = num_cols, figsize = (25, 20), sharex = True, sharey = True)
fig.suptitle("Amount of Wins during March Madness vs Team Free Throw Percentage (2010-2023)", fontsize = 20, fontweight = "bold")
subtitle = "2020 Excluded Due to Covid Cancelling the Tournament"
fig.text(x = 0.5, y = 0.95, s = subtitle, fontsize = 16, fontweight = "normal", ha = "center")


# enumerate returns the index value (i), and the actual value (year)
for i, year in enumerate(unique_years):
    # for every index value in our list, we can determine where it will go in our figure based on the layout we established above
    row = i // num_cols # integer division (this returns the integer of the quotion and discards the remainder) EXAMPLE: 0 // 3 = 0 --- 4 // 3 = 1 --- 10 // 3 = 3
    col = i % num_cols # modulus operator (this returns the remainder and discards the integer portion) EXAMPLE: 0 % 3 = 0 --- 1 % 3 = 1 --- 4 % 3 = 1

    # filter our df by the year
    df_year = FTs_with_win_counts[FTs_with_win_counts["YEAR"] == year]

    # a regplot is a scatter plot with a linear regrssion plotted on top of it, very convienent
    # https://seaborn.pydata.org/generated/seaborn.regplot.html
    # scatter_kws and line_kws are additional arguements that help style the plot
    sns.regplot(data=df_year, x='FT_PCT', y='WINS', ax=axs[row, col], scatter_kws={'s': 50}, line_kws={'color': 'red'})
    axs[row, col].set_title(f"Year: {year}")
    axs[row, col].set_xlabel("Free Throw Percentage")
    axs[row, col].set_ylabel("Tournament Wins")


# our plots are not a clean number that will form a perfect grid (we have 13 plots arranged in a 3x5 grid, there will be 2 empty plots)
# we get get rid of these plots by looping through the range start at the end of our years and going until the total number of plots in our figure
# once we get the positions, we set the axis at that position to be off
for i in range(len(unique_years), total_plots):
    row = i // num_cols
    col = i % num_cols
    axs[row, col].axis('off')


# pad = 3 just adds some space between each subplot
plt.tight_layout(pad = 3)
#plt.show()
plt.savefig(file_base + "wins_ft-pct_relationship.png")

# ^ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ^ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ^ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

x = FTs_with_win_counts["FT_PCT"].values.reshape(-1,1)
y = FTs_with_win_counts["WINS"].values

model = LinearRegression().fit(x,y)

print("Model Performance Summary and Formula:")
print(f"R-squared: {model.score(x,y)}")
print(f"Intercept: {model.intercept_}")
print(f"Slope: {model.coef_}")
print(f"Formula: wins = ({model.coef_}*FT_PCT) + {model.intercept_}")

model_results = pd.DataFrame({"R-Sqaured":model.score(x,y),
                 "Intercept":model.intercept_,
                 "Slope":model.coef_,
                 "Formula":f"wins = ({model.coef_}*FT_PCT) + {model.intercept_}"})

model_results.to_csv(file_base + "model_results.csv", index = False)

