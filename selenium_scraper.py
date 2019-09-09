from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


class selenium_scraper:
    def __init__(self, from_file='data.csv', to_file='data.csv'):
        self.from_file = from_file
        self.to_file = to_file
        self.driver = webdriver.Chrome()
        self.start = time.time()

    def scrape_urls(self, format='gen7ou'):
        df = pd.read_csv(self.from_file)
        self.driver.get('https://replay.pokemonshowdown.com')
        self.driver.find_element(By.NAME, value='format').send_keys(format + Keys.ENTER)
        time.sleep(2)

        while True:
            try:
                self.driver.find_element(By.XPATH, value="//button[@name='moreResults']").click()

            except Exception as e:
                if type(e) is NoSuchElementException:
                    break

                else:
                    print(type(e))

                continue

        with open(self.to_file, 'a') as f:
            for url in [d.get_attribute("href") for d in self.driver.find_elements(By.XPATH, value="//ul[@class='linklist']/li/a")]:
                if df[df['battle_url'] == url].empty:
                    f.write(url + '\n')

    def scrape_battles(self, save_interval=100):
        df = pd.read_csv(self.from_file)
        for index, row in df.iterrows():
            # Ignore rows that are already populated
            if not row.isnull().values.any():
                continue

            if index % save_interval == 0:
                df.to_csv(self.to_file, index=False)
                print("Saving @", (time.time() - self.start)/60)

            try:
                self.driver.get(row['battle_url'])

                # Fast forward to end of game (Loads log)
                self.driver.find_element(By.XPATH, value="//div[@class='chooser soundchooser']/div/button[@value='off']").click()
                self.driver.find_element(By.XPATH, value="//div[@class='replay-controls']/button").click()
                self.driver.find_element(By.XPATH, value="//div[@class='replay-controls']/button[@data-action='ffto']").click()
                popup = self.driver.switch_to.alert
                popup.send_keys('1000' + Keys.ENTER)
                popup.accept()

                # Scrape game data
                num_turns = int(self.driver.find_elements(By.XPATH, value="//h2[@class='battle-history']")[-1].text.split(' ')[-1])
                player_1 = self.driver.find_elements(By.XPATH, value="//div[@class='wrapper replay-wrapper']/h1/a")[0].text.strip()
                player_2 = self.driver.find_elements(By.XPATH, value="//div[@class='wrapper replay-wrapper']/h1/a")[1].text.strip()
                team_1 = self.driver.find_elements(By.XPATH, value="//div[@class='chat battle-history']/em")[0].text
                team_2 = self.driver.find_elements(By.XPATH, value="//div[@class='chat battle-history']/em")[1].text
                winner = self.driver.find_elements(By.XPATH, value="//div[@class='battle-history']/strong")[-1].text.strip()

                # Preprocess data
                if winner == player_1:
                    result = 'T1'
                elif winner == player_2:
                    result = 'T2'
                else:
                    result = 'ERR'

                team_1 = [x.strip() for x in team_1.split('/')]
                team_2 = [x.strip() for x in team_2.split('/')]

                # Update dataframe
                df.at[index, 'team_1'] = team_1
                df.at[index, 'team_2'] = team_2
                df.at[index, 'num_turns'] = num_turns
                df.at[index, 'result'] = result

            # Occurs when game ends before 1st turn
            except IndexError:
                continue

            # To catch any unexpected error
            except Exception as e:
                print(type(e), row['battle_url'])
                print(e)
                continue

        df.to_csv(self.to_file, index=False)
        print((time.time() - self.start)/60)

if __name__ == '__main__':
    ss = selenium_scraper()
    ss.scrape_urls()
    # ss.scrape_battles()
