from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import sys
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from myconfig import path_to_driver


options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.778 Yowser/2.5 Safari/537.36")
options.add_argument('--headless')

url = 'https://www.isuct.ru/student/schedule'
driver = webdriver.Chrome(executable_path=f'{path_to_driver}', 
                          options=options) 

print('[+] Connection...')
driver.maximize_window()
driver.get(url=url)
time.sleep(1)
print('#' * 20, '\n[+] Apply the group')
button = driver.find_element(By.ID, 'edit-type-currentstudentsgroups')
button_location = button.location_once_scrolled_into_view
button.click()
time.sleep(1)
print('[+] 3')
driver.find_element(By.ID, 'edit-idgr').send_keys('1/244')
time.sleep(1)
print('[+] 2')
driver.find_element(By.ID, 'edit-idgr').send_keys(Keys.ARROW_DOWN + Keys.ENTER)
print('[+] 1')
driver.find_element(By.CLASS_NAME, 'ajax-processed').click()
time.sleep(1)
driver.execute_script("document.body.style.zoom='72%'")
time.sleep(0.2)
print('[+] Complete...')
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
table = driver.find_element(By.TAG_NAME, 'table')
scroll = table.location_once_scrolled_into_view
screenshot = table.screenshot('Data/schedule.png')
rows = table.find_elements(By.TAG_NAME, 'tr')
for row in rows:
    cells = row.find_elements(By.TAG_NAME, 'td')
    for cell in cells:
        bg_color = cell.value_of_css_property('background-color')
        if bg_color == 'rgba(251, 219, 105, 1)':
            location = cell.location
            size = cell.size
            y1 = location['y'] 
            y2 = location['y'] + size['height'] 
        if cell.text == 'нед':
            location = cell.location
            x0 = location['x']
            y0 = location['y'] 
        elif cell.text == 'Четверг':
            location = cell.location
            size = cell.size
            x1 = location['x'] 
            x2 = location['x'] + size['width'] 

image = Image.open("Data/schedule.png").convert('RGBA')
screenshot_loc = table.location
x1 = int((x1 - 45) * 0.72)
x2 = int((x2 - 45) * 0.72)
y1 = int((y1 - screenshot_loc['y'])*0.72)
y2 = int((y2 - screenshot_loc['y'])*0.72)

cropped_image = image.crop((x1, y1, x2, y2))
cropped_image.save("Data/res.png")

driver.close()
driver.quit()
