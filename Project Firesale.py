from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# Function to get the name of skin to search for
def createSearchString():
    # Local Variables
    global searchString
    global ware
    global statTrack
    global skinType
    searchString = ""
    userInput    = ""
    skinType     = ""
    statTrack    = False
    ware         = 0
    isNumber     = False
    
    # Adds a star if it is a knife or glove
    while (userInput.lower() != "y" and userInput.lower() != "n"):
        userInput = input("Is your skin a knife Y/N: ")
        if (userInput.lower() == "y"):
            searchString += "★ "
            skinType = "knife"
        elif (userInput.lower() == "n"):
            userInput = input("Is your skin a glove Y/N: ")
            if(userInput.lower() == "y"):
                searchString += "★ "
                skinType = "gloves"
        if (userInput.lower() != "y" and userInput.lower() != "n"):
            print("Invalid input, try again \n")

    # Get the type of skin that it is 
    if (skinType == "knife"):
        searchString += input("What type of knife is your skin: ") + " | "
    elif (skinType == "gloves"):
        searchString += input("What type of gloves are your skin: ") + " | "
    else:
        searchString += input ("What type of gun is your skin: ") + " | "

    # Get the name of the actual skin and return the full name of the skin
    searchString += input("Enter name of skin to search for: ")

    # Reset userInput
    userInput = ""

    # Get if it is stat track
    while (userInput.lower() != "y" and userInput.lower() != "n" and skinType != "gloves"):
        userInput = input("Is the skin stat track? Y/N: ")
        if (userInput.lower() == "y"):
            statTrack = True

    # Get the ware of the skin and store it as a number for selecting the filter
    while (isNumber == False):
        userInput = input("\n1. Factory New\n2. Minimal Ware\n3. Field Tested\n4. Well Worn\n5. Battle Scarred\n6. Any\n\nSelect a ware: ")
        if (userInput == "1"):
            ware = 1
            isNumber = True
        elif (userInput == "2"):
            ware = 2
            isNumber = True
        elif (userInput == "3"):
            ware = 3
            isNumber = True
        elif (userInput == "4"):
            ware = 4
            isNumber = True
        elif (userInput == "5"):
            ware = 5
            isNumber = True
        elif (userInput == "6"):
            isNumber = True
        else:
            print("\nPlease enter a valid number and try again")

    return searchString

def CSMoney():
    # Initialize variables
    count = 0
    searchString = createSearchString()

    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    # Set up the WebDriver for Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Open the cs.money website
    driver.get("https://cs.money/csgo/trade/")

    # Wait for cookies to pop up and accept cookies 
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="notifications"]/div/div[2]/div/div/button[1]')))
    driver.find_element(By.XPATH, '//*[@id="notifications"]/div/div[2]/div/div/button[1]').click()

    # Search in text area
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/input')))
    textArea = driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/input')
    textArea.send_keys(searchString)

    # Wait until autofill shows skins
    time.sleep(1)

    # Sets elements to all of the skins from the autofill
    elements = driver.find_elements(By.CLASS_NAME, 'InventorySearchDesktop_button_with_item__ou4YF')

    # If there are no elements in the autofill box
    if len(elements) < 1:
        print("\nNo Skins Found By The Name Of %s" %(searchString))
    else:
        # Click the second element unless the skin type is gloves
        if (skinType != "gloves"):
            elements[1].click()
        else:
            elements[0].click()

        # Expand "exterior" field
        driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div/div').click()

        # Click the ware of the skin
        if (ware == 1):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div[2]/div[1]/div/a/div/span').click()
        elif (ware == 2):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div[2]/div[2]/div/a/div/span').click()
        elif (ware == 3):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div[2]/div[3]/div/a/div/span').click()
        elif (ware == 4):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div[2]/div[4]/div/a/div/span').click()
        elif (ware == 5):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[5]/div[2]/div[5]/div/a/div/span').click()

        # Select statTrack if user is searching for statTrack
        if (statTrack == True):
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[8]/div').click()
            driver.find_element(By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[8]/div[2]/div[1]/div/a/div/span').click()

        # Search by the lowest price skin
        elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "csm_ui__body_16_regular__6542e", " " ))]')
        elements[1].click()
        elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "csm_ui__text__6542e csm_ui__body_14_regular__6542e", " " ))]')
        elements[7].click()

        # If no elements found from actual search
        if (not(EC.presence_of_element_located((By.XPATH, '//*[@id="layout-page-content-area"]/div/div/div[1]/div/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]')))):
            print("No Skins Found By The Name Of %s" %(searchString))
        else:
            # Click first skin
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "actioncard_card__19Ydi")))
            clickSkin = driver.find_element(by=By.CLASS_NAME, value="actioncard_card__19Ydi")
            clickSkin.click()

            # Prints the price of skin
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal"]/div/div[3]/div/div/div[2]/div/div[2]/div[5]/div[2]/div[2]/div[1]/div[2]/span')))
            price = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div[3]/div/div/div[2]/div/div[2]/div[5]/div[2]/div[2]/div[1]/div[2]/span').text
            print("\nThe cheapest %s is " %(searchString)+ price)

    # Close the web page
    driver.quit()


CSMoney()
