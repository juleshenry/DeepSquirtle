from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize Chrome driver and start timer
driver = webdriver.Chrome()
start = time.time()

while time.time() < start + 100:
    # Go to website
    driver.get("https://replay.pokemonshowdown.com")

    # Search for games of desired format
    format = "gen7ou"
    driver.find_element(By.NAME, value="format").send_keys(format + Keys.ENTER)
    time.sleep(1)

    # Click newest game
    driver.find_element(By.XPATH, value="//ul[@class='linklist']/li").click()
    time.sleep(1)

    # Fast forward to end of game
    driver.find_element(By.XPATH, value="//div[@class='replay-controls']/button").click()
    driver.find_element(By.XPATH, value="//div[@class='chooser soundchooser']/div/button[@value='off']").click()
    driver.find_element(By.XPATH, value="//div[@class='replay-controls']/button[@data-action='ffto']").click()
    popup = driver.switch_to.alert
    popup.send_keys('1000' + Keys.ENTER)
    popup.accept()

    # Text from log
    time.sleep(1)
    battle_id = driver.find_element(By.XPATH, value="//pre[@class='urlbox']").text.split('-')[1]
    player1 = driver.find_elements(By.XPATH, value="//div[@class='wrapper replay-wrapper']/h1/a")[0].text.strip()
    player2 = driver.find_elements(By.XPATH, value="//div[@class='wrapper replay-wrapper']/h1/a")[1].text.strip()
    roster1 = driver.find_elements(By.XPATH, value="//div[@class='chat battle-history']/em")[0].text
    roster2 = driver.find_elements(By.XPATH, value="//div[@class='chat battle-history']/em")[1].text
    winner = driver.find_elements(By.XPATH, value="//div[@class='battle-history']/strong")[-1].text
    result = 'T1' if winner == player1 else 'T2'

    # Save to dataframe
    roster1 = [x.strip() for x in roster1.split('/')]
    roster2 = [x.strip() for x in roster2.split('/')]

    df = pd.DataFrame(columns=['Battle_ID', 'Team 1', 'Team 2', 'Result'])
    df = df.append({'Battle_ID': battle_id, 'Team 1': roster1, 'Team 2': roster2, 'Result': result}, ignore_index=True)

    # Wait for next request
    time.sleep(10)

# Append to data.csv
df.to_csv('data.csv', index=False, header=False, mode='a')

driver.close()
