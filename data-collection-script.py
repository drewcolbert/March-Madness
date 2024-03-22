from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EDGEOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time

# ^ this class is here to define the process for getting each element and each data point
# ^ this is meant to make the data collection class cleaner and allow us to use each method easily
class HelperMethods:

    # ^ define the driver, I wanted to use headless but I kept getting third party errors
    def __init__(self):
       # self.edge_options = EDGEOptions()
       # self.edge_options.add_argument("--disable-gpu")
       # self.edge_options.add_argument("--no-sandbox")
       # self.edge_options.add_argument("--headless")
       # self.driver = webdriver.Edge(options = self.edge_options)
        # ^ establish the driver as Edge
        # ^ the wait time is how long we wait in between collecting each data point
        # ^ the wait time is long we wait for the element to be present befor eraising a timeout error
        self.driver = webdriver.Edge()
        self.wait_time = 5
    

    # ^ these method construct our urls, luckily this is simple and all we need to do is replace the year
    # ^ once the url is made, we get that url using our driver
    def get_stats_url(self, year):
        base_url = "https://www.sports-reference.com/cbb/seasons/men/"
        url_endpoint = f"{year}-school-stats.html"

        full_url = base_url + url_endpoint
        self.driver.get(full_url)
    

    def get_winners_url(self, year):
        base_url = "https://www.sports-reference.com/cbb/postseason/men/"
        url_endpoint = f"{year}-ncaa.html"

        full_url = base_url + url_endpoint
        self.driver.get(full_url)
    
    # ^ define the XPATH for the element we want, we just need to replace the row number of the table
    # ^ I need to wait until the element is present before trying to access it
    # ^ NOTE: this could probably be condensed further, but this works and I am going to leave it
    # ^ the other functions are the same process, just getting a different stat in the table
    def get_team_name(self, row_num):
        xpath = f"//*[@id='basic_school_stats']/tbody/tr[{row_num}]/td[1]"
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        team_name = elem.text

        return team_name
    
    def get_free_throws_made(self, row_num):
        xpath = f"//*[@id='basic_school_stats']/tbody/tr[{row_num}]/td[28]"
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        free_throws_made = elem.text

        return free_throws_made
    
    def get_free_throws_attempted(self, row_num):
        xpath = f"//*[@id='basic_school_stats']/tbody/tr[{row_num}]/td[29]"
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        free_throws_attempted = elem.text

        return free_throws_attempted
    
    def get_free_throw_percentage(self, row_num):
        xpath = f"//*[@id='basic_school_stats']/tbody/tr[{row_num}]/td[30]"
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        free_throw_percentage = elem.text

        return free_throw_percentage
    
    def click_region_filter(self, index_num):
        xpath = f"//*[@class='switcher filter']/div[{index_num}]"
        WebDriverWait(self.driver, self.wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


    def get_winners(self):
        xpath = "//*[@class='winner']/a[1]"
        winners = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        return winners


# ^ this class is what loops through all of our values and actually collects the data
# ^ it inherits the methods and attributes from above
class CollectStats(HelperMethods):
    
    def __init__(self):
        # ^ using super() here allows us to use the __init__ attributes of the inherited class
        # ^ this is needed to get the driver from the parent class
        super().__init__()

        # ^ define the length of the table and the amount of years we want to collect for
        # ^ create an empty dictionary that will hold all of our data
        # ^ the sleep.time is how long we wait between getting a stat, I made this to not get kicked from the site, but that didnt end up mattering
        self.rows = list(range(1,382))
        self.years = list(range(2010, 2024))
        self.data = {"TEAM":[],
                     "YEAR":[],
                     "FTM":[],
                     "FTA":[],
                     "FT_PCT":[]}
        self.sleep_time = 0
        self.filters = list(range(1,5))
        self.winners = {"YEAR":[],
                        "WINNERS":[]}

    # ^ the following methods all loop through the urls and the rows to get each stat
    def collect_team_names(self):
        for year in self.years:
            self.get_stats_url(year)
            time.sleep(self.sleep_time)
            for row in self.rows:
                try:
                    self.data["TEAM"].append(self.get_team_name(row))
                    self.data["YEAR"].append(year)
                    time.sleep(self.sleep_time)
                except:
                    print(f"Could not get team name for year: {year} and row {row}.")
                    pass


    def collect_free_throws_made(self):
        for year in self.years:
            self.get_stats_url(year)
            time.sleep(self.sleep_time)
            for row in self.rows:
                try:
                    self.data["FTM"].append(self.get_free_throws_made(row))
                    time.sleep(self.sleep_time)
                except:
                    print(f"Could not get free throws made for year: {year} and row {row}.")
                    pass
    
    def collect_free_throws_attempted(self):
        for year in self.years:
            self.get_stats_url(year)
            time.sleep(self.sleep_time)
            for row in self.rows:
                try:
                    self.data["FTA"].append(self.get_free_throws_attempted(row))
                    time.sleep(self.sleep_time)
                except:
                    print(f"Could not get free throws attempted for year: {year} and row {row}.")
                    pass

    def collect_free_throw_percentage(self):
        for year in self.years:
            self.get_stats_url(year)
            time.sleep(self.sleep_time)
            for row in self.rows:
                try:
                    self.data["FT_PCT"].append(self.get_free_throw_percentage(row))
                    time.sleep(self.sleep_time)
                except Exception as e:
                    print(f"Could not get free throw percentage for year: {year} and row {row}.")
                    pass

    # ^ this method is used to return the final dictionary after collection is done
    def collect_all_stats(self):

        return self.data
    
    # ^ in order to avoid having to do this every time, you can put the dictionary into a df, and then write that df to a csv file for convienence later
    def write_data_to_csv(self, data, file_name):
        file_path_base = "/Users/drewc/OneDrive/Documents/2024/Python/March Madness/"
        file_path_full = file_path_base + file_name
        if data == "stats":
            data_to_use = self.data
        elif data == "winners":
            data_to_use = self.winners

        df = pd.DataFrame(data_to_use)
        df.to_csv(file_path_full, index = False)

    
    def collect_winners(self):
        for year in self.years:
            if year == 2020:
                pass
            else:
                self.get_winners_url(year)
            for filter in self.filters:
                self.click_region_filter(filter)
                winners = self.get_winners()
                for winner in winners:
                    if winner.text == '':
                        pass
                    else:
                        self.winners["WINNERS"].append(winner.text)
                        self.winners["YEAR"].append(year)
    
    def return_winners_dict(self):
        return self.winners
    
        






get_stats_object = CollectStats()
get_stats_object.collect_team_names()
get_stats_object.collect_free_throws_made()
get_stats_object.collect_free_throws_attempted()
get_stats_object.collect_free_throw_percentage()
get_stats_object.write_data_to_csv("stats","stats_history.csv")


get_winners_object = CollectStats()
get_winners_object.collect_winners()
get_winners_object.write_data_to_csv("winners", "winners_history.csv")



