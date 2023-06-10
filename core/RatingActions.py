import os, time

from dotenv import load_dotenv
from termcolor import cprint
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

load_dotenv()

class RatingActions:
    def __init__(self) -> None:
        self.username = os.getenv('STUDENT_USERNAME')
        self.password = os.getenv('STUDENT_PASSWORD')
        self.is_logged_in = False

    def init_chrome_driver(self) -> None:
        """"Initializing chrome drivers"""
        try:
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            chrome_options = webdriver.ChromeOptions()

            prefs = {
                        "profile.managed_default_content_settings.images": 2,
                        "profile.default_content_settings.images": 2,
                    }

            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--log-level=OFF')
            chrome_options.add_argument('--disable-extensions')

            self.chrome_driver = webdriver.Chrome(executable_path=os.getenv('CHROME_DRIVER_PATH'), options=chrome_options)
        except Exception as e:
            raise ConnectionError("Couldn't init chrome drivers" + str(e))

    def login(self) -> None:
        self.chrome_driver.get('http://sisweb.buc.edu.om/portal/pls/portal/logsisw.cow_start')
        time.sleep(5)

        cprint("Start Log in process...", "yellow")
        choose_student_button = self.chrome_driver.find_element_by_xpath("/html/body/table[7]/tbody/tr/td[3]/p/a")
        choose_student_button.click()
        time.sleep(5)

        try:
            username = self.chrome_driver.find_element_by_xpath('//input[@name="ssousername"]')
            username.clear()
            username.send_keys(self.username)

            password = self.chrome_driver.find_element_by_xpath("//input[@name='password']")
            password.clear()
            password.send_keys(self.password)

            password.send_keys(keys.Keys.RETURN)
        except NoSuchElementException as e:
            cprint("username & password inputs field does not exsist!")

        cprint("Login process finished Successfully (:", "green")

    def logout(self) -> None:
        cprint("Start Logout Process...", "yellow")

        logout_link = self.chrome_driver.find_element_by_xpath('//table[@class="stu_header"]/tbody/tr[1]/td[2]/a')
        logout_link.click()

        cprint("Logout process finished successfully :)", "green")
        self.chrome_driver.quit()

    def redirect_to_rating_page(self) -> None:
        cprint("redirect to the reating page...", "blue")

        rating_page_link = self.chrome_driver.find_element_by_xpath("//ul[@id='stu_info']/li[11]/a").get_attribute('href')
        self.chrome_driver.get(rating_page_link)

    def rating_professors(self):
        try:
            # Number of courses (max: 6)
            for i in range(2, 8):
                try:
                    alert = Alert(self.chrome_driver)
                    alert.accept()
                except:
                    pass

                proffesor_page_link = self.chrome_driver.find_element_by_xpath(f"//table[@bordercolor='#808040']/tbody/tr[{i}]/td[3]/a").get_attribute('href')

                print("Redirect to " + self.chrome_driver.find_element_by_xpath(f"//table[@bordercolor='#808040']/tbody/tr[{i}]/td[3]/a/font").text + " evaluation page")

                self.chrome_driver.get(proffesor_page_link)

                # Evaluation page numbers (max: 4)
                for x in range(1, 5):
                    print(f"Evaluate Page {x}")
                    if (x == 1):
                        # page one contains 6 questions
                        for y in range(2, 8):
                            self.chrome_driver.find_element_by_xpath(f"//table[@class='STU_INST_EVAL_TABLE_EVAL_Table']/tbody/tr[{y}]/td[2]/font/select/option[@value='{3}']").click()

                        self.chrome_driver.find_element_by_xpath("//input[@name='SUBMIT']").click()
                        time.sleep(5)
                        self.chrome_driver.find_element_by_xpath("//input[@name='NEXT']").click()
        
                    if (x == 2 or x == 3):
                        time.sleep(5) 
                        try:
                            alert = Alert(self.chrome_driver)
                            alert.accept()
                        except:
                            pass

                        # these pages contains 5 questions
                        for y in range(2, 7):
                            self.chrome_driver.find_element_by_xpath(f"//table[@class='STU_INST_EVAL_TABLE_EVAL_Table']/tbody/tr[{y}]/td[2]/font/select/option[@value='{3}']").click()

                        self.chrome_driver.find_element_by_xpath("//input[@name='SUBMIT']").click()
                        time.sleep(5)
                        self.chrome_driver.find_element_by_xpath("//input[@name='NEXT']").click()

                    if (x == 4):
                        time.sleep(5)
                        try:
                            alert = Alert(self.chrome_driver)
                            alert.accept()
                        except:
                            pass
                        # page contain 3 question with comment section
                        for y in range(2, 5):
                            self.chrome_driver.find_element_by_xpath(f"//table[@class='STU_INST_EVAL_TABLE_EVAL_Table']/tbody/tr[{y}]/td[2]/font/select/option[@value='{3}']").click()

                        textarea = self.chrome_driver.find_element_by_xpath("//textarea[@name='GComments']")
                        
                        textarea.send_keys("Thank you")

                        self.chrome_driver.find_element_by_xpath("//input[@name='SUBMIT']").click()
        except Exception as e:
            cprint("Error: Something went wrong :(", "red")

        cprint("Professors are rated successfully (:", "green")

    def start(self) -> None:
        self.init_chrome_driver()
        self.login()
        time.sleep(5)
        self.redirect_to_rating_page()
        time.sleep(5)
        self.rating_professors()
        time.sleep(5)
        self.logout()

        cprint("Thank you for using my tool ;)", "red")