![madness](/images/march-madness-cover.jpg)

# Gotta Hit Your Free Throws
March madness is widely regarded as the best post-season in all of sports. The excitement is unmatched and the pressure is turned all the way up; with just one loss, one bad game, and you go home. Part of what makes it so good 
is the madness aspect of it. The games are usually always incredibly close and every advantage you can get you need to take. One of the biggest factors that can change the outcome of these games is 
free throws. In most of these games, free throws will be the way to put a team away and free throws will allow a team to comeback from a deficit. This is what lead to the question that my good friend asked me:
Does a teams' overall free throw percentage impact how many games they win in the tournament?


## The Data
There is no premade dataset available for use. But that is okay, I have the means to get our own data. Using selenium webdriver, I scraped the [sports reference website](https://www.sports-reference.com/cbb/)
to find historical free throw data as well as historical tournament winners. I decided to collect 13 years worth of data, from 2010-2023 *(there is no data for 2020 due to COVID-19 cancelling the tournament)*.
The website has a nice table for us containing team stats *(see image below)* where we were able to get the following: **TEAM_NAME, YEAR, FTA, FTM, FT_PCT**

![stats](/images/stats-example.jpeg)

<br>
<br>

Getting the winners was a bit different, the site has a bracket and button menu to switch between each region *(see below)*. For the winners I had to get all of the teams listed with a 
class of 'winner'. This had to be done for each region and final four. The final data collected was the following: **YEAR, TEAM_NAME** where TEAM_NAME is the winner of each round. 

![winners](/images/bracket-example.jpeg)

<br>

In both cases, I need to get all of these stats for each year from 2010-2023.

<br>

## The Analysis
Once the winners were counted for each year, this was merged with the stats for those teams in those years. A simple linear regression was fit to the data
and it was found that team free throw percentage does not play a large role in the number of wins a team will have in the tournament. With an R-Squared value 0.00035, it basically 
means that free throws alone do not determine wins in the tournament. When looking at the chart below of each year, I see that some years there's a relatively strong positive relationship
and other years there's a negative relationship. Overall it is pretty scattered and it depends on the year, but this isn't as helpful because this offers no predicitve power for the current year. 

![plot](/images/wins_ft-pct_relationship.png)

<br>

Full results can be found in *Gotta Hit Your Free Throws.xlsx* found in this repository. You can mess around with different combos and see how many wins they got vs how many wins were expected.

<br>
<br>

## Conclusion & Limitations
Sports are naturally unpredictable. There is always a human element that cannot be taken into account when modeling wins. In this case, I was only looking at one variable and one aspect of the game, albeit a very important one.
Additionally, the free throws will matter the most towards the end of the game, so if I were able to get clutch time free throws (under 5 minutes remaining) in these games, that might be a much better predictor for determining the number of wins.
As it stands now, this analysis only looked at team free throw percentage for the whole year. As I mentioned in the beginning, March Madness is the best because of how chaotic and unpredictable it is. But regardless of what the model says, you still 
gotta hit your free throws. 

