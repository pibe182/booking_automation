from appium.webdriver.common.mobileby import MobileBy
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AppiumActions:
    def __init__(self, driver, close_registration_view_xpath, start_saving_today_id, go_to_select_room, select_item, reserve_these_options, credit_card_needed):
        self.driver = driver
        self.close_registration_view_xpath = close_registration_view_xpath
        self.start_saving_today_id = start_saving_today_id
        self.go_to_select_room = go_to_select_room
        self.select_item = select_item
        self.reserve_these_options = reserve_these_options
        self.credit_card_needed = credit_card_needed

    def scroll_to_element(self, element):
        action = TouchAction(self.driver)
        action.press(None, element).move_to(None, 0, 400).release().perform()

    def close_registration_view(self):
        try:
            close_registration_element = self.driver.find_element(MobileBy.XPATH, self.close_registration_view_xpath)
            close_registration_element.click()
        except Exception as e:
            print("Failed to close the registration view:", str(e))

    def verify_rewards_and_wallet(self):
        try:
            start_saving_today_element = self.driver.find_element(MobileBy.ID, self.start_saving_today_id)
            if start_saving_today_element.is_displayed():
                start_saving_today_element.click()
                time.sleep(2)
                self.driver.press_keycode(4)  # Press the BACK key
                time.sleep(2)
        except Exception as e:
            print("Failed to verify Rewards & Wallet:", str(e))

    def select_room(self):
        try:
            time.sleep(2)  # Sleep for 2 seconds
            self.driver.find_element(By.ID, self.go_to_select_room).click()
            time.sleep(5)  # Wait for 5 seconds for the room selection page to load

            try:
                self.driver.find_element(By.ID, "com.booking:id/listitem_info_icon").click()
                time.sleep(12)
                self.driver.find_element(By.ID, self.select_item).click()
                time.sleep(10)
            except Exception:
                self.driver.find_element(By.ID, self.reserve_these_options).click()
                time.sleep(10)
        except Exception as e:
            raise Exception("Failed to select a room: " + str(e))

    def reserve_room(self, name, last_name, mail, address, zip_code, city, country, phone_number):
        try:
            forms_part_i = self.driver.find_elements(MobileBy.XPATH, "//android.widget.EditText")
            auto_complete_view = self.driver.find_elements(MobileBy.XPATH, "//android.widget.AutoCompleteTextView")

            if len(forms_part_i) == 5:
                forms_part_i[0].send_keys(name)
                time.sleep(1)
                forms_part_i[1].send_keys(last_name)
                time.sleep(1)
                auto_complete_view[0].send_keys(mail)
                time.sleep(1)
                forms_part_i[2].send_keys(address)
                time.sleep(1)
                forms_part_i[3].send_keys(zip_code)
                time.sleep(1)
                forms_part_i[4].send_keys(city)
                self.driver.find_element(MobileBy.ID, "com.booking:id/action_button").click()
                time.sleep(3)

                forms_part_i = self.driver.find_elements(MobileBy.XPATH, "//android.widget.EditText")
                auto_complete_view = self.driver.find_elements(MobileBy.XPATH, "//android.widget.AutoCompleteTextView")

                auto_complete_view[1].clear()
                auto_complete_view[1].send_keys(country)
                time.sleep(1)
                forms_part_i[3].send_keys(phone_number)
                self.driver.find_element(MobileBy.ID, "com.booking:id/action_button").click()
                time.sleep(3)
            else:
                forms_part_i[0].send_keys(name)
                time.sleep(1)
                forms_part_i[1].send_keys(last_name)
                time.sleep(1)
                auto_complete_view[0].send_keys(mail)
                time.sleep(1)
                auto_complete_view[1].clear()
                auto_complete_view[1].send_keys(country)
                time.sleep(1)
                forms_part_i[2].send_keys(phone_number)
                self.driver.find_element(MobileBy.ID, "com.booking:id/action_button").click()
                time.sleep(3)

            time.sleep(10)  # Wait for 10 seconds
        except Exception as ignored:
            pass

    def fill_credit_card(self, PAM, name, expdate):
        if not self.credit_card_needed:
            return

        try:
            pam_field = self.driver.find_element(MobileBy.ID, "com.booking:id/action_pam")
            pam_field.send_keys(PAM)
            self.driver.press_keycode(66)  # Sending keycode for Enter key
            pam_field.send_keys(name)
            self.driver.press_keycode(66)  # Sending keycode for Enter key
            pam_field.send_keys(expdate)
        except Exception as ignored:
            pass
