import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import sys

def login_with_facebook(driver, email, password):
    # On the homepage click on the 'Sign in' button
    click_by_xpath(driver, "Failed on clicking on homepage sign-in button", '//a[@ng-click="$ctrl.signin()"]')

    # Select Facebook as login method
    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#dialogContent_0 > md-dialog-content > div.modal-login__social > div"))).click()
    except:
        print("Failed on selecting the Facebook log-in method")

    # Switch to the fb popup window
    window_website = driver.window_handles[0]
    window_fb_popup = driver.window_handles[1]

    driver.switch_to_window(window_fb_popup)

    # Accept the facebook cookies in English
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[2]"))).click()
    except:
        print("Failed on selecting the Facebook cookies in English")

    # Enter facebook email in textfield
    try:
        driver.find_element_by_css_selector("#email").send_keys(email)
    except:
        print("Failed on entering Facebook email")

    # Enter facebook password in textfield
    try:
        driver.find_element_by_css_selector("#pass").send_keys(password)
    except:
        print("Failed on entering Facebook email")

    # Click on the facebook login button and switch back to the GS website
    click_by_xpath(driver, "Failed on clicking the log into Facebook button", "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]")

    driver.switch_to_window(window_website)

def click_by_xpath(driver, message, xpath, timeout=1, duration=1):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        time.sleep(duration)
    except:
        print(message)

def click_by_css_selector(driver, message, css_selector, timeout= 1, duration=1):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))).click()
        time.sleep(duration)
    except:
        print(message)  
def program(email_argument, password_argument):
    start_time = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    email = email_argument
    password = password_argument

    driver.get("https://gurushots.com")
    time.sleep(1)

    login_with_facebook(driver, email, password)

    try:
        # Must start with index 2
        # challenge_iterator = 2
        challenge_iterator = 1
        picture_iterator = 1

        driver.implicitly_wait(10) # seconds

        # challenges_count =  driver.find_elements_by_tag_name("challenges-item")
        challenges = driver.find_elements_by_xpath("//*//challenges-item//div[contains(@class, 'c-challenges-item__exposure__footer')]/div/i")

        # while True: 
        for challenge in challenges:
            isVoting = True
            # try:
            click_by_css_selector(driver, "No end of challenge popup", "body > div.md-dialog-container > md-dialog > md-dialog-actions > div.c-modal-broadcast--closed__next", timeout=3, duration=1)
            click_by_css_selector(driver, "Unable to claim challenge rewards", "body > div.md-dialog-container > md-dialog > div.c-modal-broadcast--closed__close-btn", timeout=3, duration=1)
                    
            try:
                driver.implicitly_wait(10) # seconds
                challenge.click()
            except:
                print("Failed on selecting a challenge")

            print(f"Challenge: {challenge_iterator}/{len(challenges)}")
            # Click on the LET'S GO button
            try:
                driver.implicitly_wait(10) # seconds
                try:

                    challenge_name = driver.find_elements_by_xpath("//gs-modals//modal-vote/div[2]/span")
                    # challenge_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//gs-modals//modal-vote/div[2]/span"))).get_text()
                    print(f"CHALLENGE NAME: {challenge_name.text}")
                except:
                    print("Unable to find challenge title")

                
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/gs-modals/div/modal-vote/div[4]/div//div[contains(string(), "LET\'S GO")]'))).click()
                
                time.sleep(0.5)
            except:
                print("Challenge: voting starting soon")

                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/gs-modals/div/modal-vote/div[4]/div//div[contains(string(), "CLOSE")]'))).click()
                    time.sleep(0.5)
                    isVoting = False
                    # challenge_iterator += 1
                except:
                    print("Failed on closing the 'voting starting soon window'")
                    break

            driver.implicitly_wait(10) # seconds
            try:

                challenge_name = driver.find_elements_by_xpath("//gs-modals//modal-vote/div[2]/span")
                # challenge_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//gs-modals//modal-vote/div[2]/span"))).get_text()
                print(f"CHALLENGE NAME: {challenge_name.text}")
            except:
                print("Unable to find challenge title")

            if isVoting:
                # loop over pics
                vote_counter = 1

                pictures = "//modal-vote//img[1]"

                for p in range(picture_iterator, 120):
                    if vote_counter <= 4:
                        # Vote on pictures
                        click_by_xpath(driver, "Failed on voting", f'/html/body/div[1]/gs-modals/div/modal-vote/div[1]/div/div[{p}]/div[1]', timeout=10, duration= 0.3)

                    if vote_counter == 8:
                        vote_counter = 0
                    vote_counter += 1      

                # Click on the submit vote button
                click_by_xpath(driver, "Failed on submitting", f'/html/body/div[1]/gs-modals/div/modal-vote/div[3]/div[2]', timeout=10, duration= 2)

                # Click on the Done button
                click_by_xpath(driver, "Failed on done button", f'/html/body/div[1]/gs-modals/div/modal-vote/div[4]/div/div[2]/div[2]', timeout=10, duration= 2)

                picture_iterator += 1
                # challenge_iterator += 1
            challenge_iterator += 1
        
        
        time.sleep(5)
        driver.quit()

    except:
        print("Something terrible went wrong")
    

    elapsed_seconds = time.time() - start_time
    print(f"Elapsed timed: {str(datetime.timedelta(seconds=elapsed_seconds))}")


def main():
    arguments_length = len(sys.argv)
    email = ""
    password = ""

    if arguments_length == 5:
        if sys.argv[1] == "-p" and sys.argv[3] == "-e":
            email = sys.argv[4]
            password = sys.argv[2]

            program(email, password)
        else:
            print("Invalid arguments: -p <password> -e <email>")
    else:
        print("Pass password and email")

if __name__ == "__main__":
    main()
    