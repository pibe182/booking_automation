from appium_actions import AppiumActions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Desired capabilities
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '13',
    'deviceName': 'emulator-5554',
    'appPackage': 'com.booking',
    'appActivity': 'com.booking.activity.ClsSplash',
    'automationName': 'UiAutomator2'
}

# Your element identifiers or XPaths
close_registration_view_xpath = "//android.widget.ImageButton[@content-desc='Navigate up']"
start_saving_today_id = "com.booking:id/bui_empty_state_primary_action"
go_to_select_room = "Your_ID_for_GoToSelectRoom"
select_item = "Your_ID_for_SelectItem"
reserve_these_options = "Your_ID_for_ReserveTheseOptions"

# Define XPaths for check-in and check-out dates
start_date_xpath = "//android.view.View[@content-desc='14/02/24']"
final_date_xpath = "//android.view.View[@content-desc='28/02/24']"

travelerInfo = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout[1]/android.widget.LinearLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.ViewGroup/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.widget.ScrollView/android.view.ViewGroup[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.TextView"
plusAdultsButton = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup[2]/android.widget.LinearLayout/android.widget.Button[2]"
plusChildrenButton = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup[3]/android.widget.LinearLayout/android.widget.Button[2]"
ageXpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.NumberPicker/android.widget.Button[1]"
searchfieldID = "com.booking:id/facet_search_box_basic_field_label"
scrollelementID = "com.booking:id/calendar_month_list"
okbuttonID = "android:id/button1"
applybuttonID = "com.booking:id/applyButton"
hotellistxpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.ImageView"
step2priceID = "com.booking:id/title"

# Credit card need status
credit_card_needed = True  # Change to False if credit card is not needed

# Initialize driver
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Initialize the AppiumActions object
appium_actions = AppiumActions(driver, close_registration_view_xpath, start_saving_today_id, go_to_select_room, select_item, reserve_these_options, credit_card_needed)

# Implement the rest of your script with function calls
appium_actions.close_registration_view()
appium_actions.verify_rewards_and_wallet()

# Rest of your script here

# Step 1: Search for a hotel
search_field = wait.until(EC.presence_of_element_located((By.ID, searchfieldID)))
search_field.click()
search_field.send_keys('CUSCO')

# Select the check-in date
scroll_element = driver.find_element(By.ID, scrollelementID)
appium_actions.scroll_to_element(scroll_element)
date_element = driver.find_element(By.XPATH, start_date_xpath)
date_element.click()

# Select the check-out date
scroll_element = driver.find_element(By.ID, scrollelementID)
appium_actions.scroll_to_element(scroll_element)
date_element = driver.find_element(By.XPATH, final_date_xpath)
date_element.click()

time.sleep(4)  # Sleep for 4 seconds
driver.find_element(MobileBy.XPATH, travelerInfo).click()

driver.find_element(MobileBy.XPATH, plusAdultsButton).click()

driver.find_element(MobileBy.XPATH, plusChildrenButton).click()
time.sleep(3)  # Wait for 3 seconds

for j in range(13):
    driver.find_element(MobileBy.XPATH, ageXpath).click()
    time.sleep(3)  # Wait for 3 seconds

ok_button = driver.find_element_by_id(okbuttonID)
ok_button.click()

apply_button = driver.find_element_by_id(applybuttonID)
apply_button.click()

# Step 2: Select a hotel and room
hotel_list = driver.find_element_by_xpath(hotellistxpath)

appium_actions.select_room()

# Capture the price in step 2
step2_price = driver.find_element_by_id(step2priceID).text

# Step 3: Fill in personal info
appium_actions.reserve_room("Jose", "Hurtado", "josehurtado@mail.com", "xxx", "9999", "Lima", "Peru", "930000000")

# Step 4: Select purpose of the trip
# leisure_radio_button = driver.find_element_by_id('leisure_radio_button_id')
# leisure_radio_button.click()

# next_button = driver.find_element_by_id('next_button_id')
# next_button.click()

# Step 5: Verify reservation data

# Capture the price in step 5
step5_price = driver.find_element_by_id(step2priceID ).text  #es otro pero el ID es igual porque es otra pagina

# Example assertion comparing the prices
assert step2_price == step5_price, "Price in step 5 does not match the one in step 2"

# Call the function to fill in credit card details
appium_actions.fill_credit_card("4557880632323232", "Jose Hurtado", "0827")

# No need to actually book
# book_now_button = driver.find_element_by_id('book_now_button_id')
# book_now_button.click()


# Close the app
driver.quit()
