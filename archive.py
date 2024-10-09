import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

grids = []

# Visit the archive page
archive_url = "https://wafflegame.net/archive"
driver.get(archive_url)

# Allow the page to load
time.sleep(3)

# Get the list of archived waffle games (you might need to inspect the page to get the right class or ID)
games = driver.find_elements(By.CLASS_NAME, 'item')  # Replace with actual class or ID
print(len(games))

# Iterate through each game, take a screenshot, and process it
for game in games[:100]:
    # Open the game
    game.click()

    # Wait for the game to load
    time.sleep(3)

    letters = driver.find_elements(By.CLASS_NAME, 'tile.draggable')
    print(len(letters))
    grid = ''
    for letter in letters:
        grid += letter.text
        print(letter.text)

    grids.append(grid)

    # Close the current game and go back to the archive
    button = driver.find_element(By.CLASS_NAME, 'button--back')
    button.click()

    # Wait before processing the next game
    time.sleep(2)

# Close the browser once done
driver.quit()

print(grids)
