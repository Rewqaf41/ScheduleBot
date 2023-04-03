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


class Parser():

    def __init__(self, search_type, amount, tg_id):
        self.search_type = search_type
        self.amount = amount
        self.tg_id = tg_id
        self.driver = None
        self.table = None
        self.sizes = None

    def get_schedule_on_any_day(self, week, weekday):
        self.start_driver()
        self.choose_type_of_search()
        self.choose_group()
        self.get_screenshot_of_table()
        self.select_area_on_any_day(week, weekday)
        self.create_resoult()

    def get_schedule_today(self):
        self.start_driver()
        self.choose_type_of_search()
        self.choose_group()
        self.get_screenshot_of_table()
        self.select_area()
        self.create_resoult()

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.778 Yowser/2.5 Safari/537.36")
        options.add_argument('--headless')
        url = 'https://www.isuct.ru/student/schedule'
        self.driver = webdriver.Chrome(executable_path=f'{path_to_driver}', options=options)
        print('[+] Connection...')
        self.driver.maximize_window()
        self.driver.get(url=url)
        time.sleep(1)
        print('#' * 20, '\n[+] Apply the group')

    def choose_type_of_search(self):
        if self.search_type == 'группа':
            button = self.driver.find_element(By.ID, 'edit-type-currentstudentsgroups')
            button_location = button.location_once_scrolled_into_view
            button.click()
            time.sleep(1)
            print('[+] 3')
        elif self.search_type == 'препод':
            button = self.driver.find_element(By.ID, 'edit-type-prepod')
            button_location = button.location_once_scrolled_into_view
            button.click()
            time.sleep(1)
            print('[+] 3')
        elif self.search_type == 'аудитория':
            button = self.driver.find_element(By.ID, 'edit-type-auditorium')
            button_location = button.location_once_scrolled_into_view
            button.click()
            time.sleep(1)
            print('[+] 3')
        else:
            return 'Ошибка'

    def choose_group(self):
        if self.search_type == 'группа':
            self.driver.find_element(By.ID, 'edit-idgr').send_keys(f'{self.amount}')
            time.sleep(1)
            print('[+] 2')
            self.driver.find_element(By.ID, 'edit-idgr').send_keys(Keys.ARROW_DOWN + Keys.ENTER)
            print('[+] 1')
            self.driver.find_element(By.CLASS_NAME, 'ajax-processed').click()
            time.sleep(1)
        elif self.search_type == 'препод':
            self.driver.find_element(By.ID, 'edit-idprep').send_keys(f'{self.amount}')
            time.sleep(1)
            print('[+] 2')
            self.driver.find_element(By.ID, 'edit-idprep').send_keys(Keys.ARROW_DOWN + Keys.ENTER)
            print('[+] 1')
            self.driver.find_element(By.CLASS_NAME, 'ajax-processed').click()
            time.sleep(1)
        elif self.search_type == 'аудитория':
            self.driver.find_element(By.ID, 'edit-idaud').send_keys(f'{self.amount}')
            time.sleep(1)
            print('[+] 2')
            self.driver.find_element(By.ID, 'edit-idaud').send_keys(Keys.ARROW_DOWN + Keys.ENTER)
            print('[+] 1')
            self.driver.find_element(By.CLASS_NAME, 'ajax-processed').click()
            time.sleep(1)
        else:
            return 'Ошибка'

    def get_screenshot_of_table(self):
        self.driver.execute_script("document.body.style.zoom='72%'")
        time.sleep(0.2)
        print('[+] Complete...')
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        self.table = self.driver.find_element(By.TAG_NAME, 'table')
        scroll = self.table.location_once_scrolled_into_view
        screenshot = self.table.screenshot(f'Data/sch{self.tg_id}.png')

    def select_area(self):
        rows = self.table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                if cell.text == 'нед':
                    location = cell.location
                    x0 = location['x']
                    y0 = location['y']
                elif cell.text == 'Время':
                    location = cell.location
                    size = cell.size
                    time_x1 = location['x']
                    time_x2 = location['x'] + size['width']
                bg_color = cell.value_of_css_property('background-color')
                if bg_color == 'rgba(251, 219, 105, 1)':
                    if cell.text == '1' or cell.text == '2':
                        location = cell.location
                        size = cell.size
                        y1 = location['y'] 
                        y2 = location['y'] + size['height'] 
                    else:
                        location = cell.location
                        size = cell.size
                        x1 = location['x'] 
                        x2 = location['x'] + size['width'] 
        self.sizes = (x0, y0, x1, y1, x2, y2, time_x1, time_x2)

    def select_area_on_any_day(self, week, weekday):
        rows = self.table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            for cell in cells:
                if cell.text == 'нед':
                    location = cell.location
                    x0 = location['x']
                    y0 = location['y']
                elif cell.text == 'Время':
                    location = cell.location
                    size = cell.size
                    time_x1 = location['x']
                    time_x2 = location['x'] + size['width']
                if cell.text == f'{week}' :
                    location = cell.location
                    size = cell.size
                    y1 = location['y'] 
                    y2 = location['y'] + size['height'] 
                elif cell.text == f'{weekday}':
                    location = cell.location
                    size = cell.size
                    x1 = location['x'] 
                    x2 = location['x'] + size['width'] 
        self.sizes = (x0, y0, x1, y1, x2, y2, time_x1, time_x2)
            
    def create_resoult(self):
        x0 = self.sizes[0]
        y0 = self.sizes[1]
        x1 = self.sizes[2]
        y1 = self.sizes[3]
        x2 = self.sizes[4]
        y2 = self.sizes[5]
        time_x1 = self.sizes[6]
        time_x2 = self.sizes[7]
        image = Image.open(f"Data/sch{self.tg_id}.png").convert('RGBA')
        screenshot_loc = self.table.location
        x1 = int((x1 - 45) * 0.72)
        x2 = int((x2 - 45) * 0.72)
        y1 = int((y1 - screenshot_loc['y'])*0.72)
        y2 = int((y2 - screenshot_loc['y'])*0.72)
        time_x1 = int((time_x1 - 45) * 0.72)
        time_x2 = int((time_x2 - 45) * 0.72)
        cropped_image = image.crop((x1, y1, x2, y2))
        cropped_image_time = image.crop((time_x1, y1, time_x2, y2))
        image_width = cropped_image_time.width + cropped_image.width
        image_height = cropped_image_time.height
        res = Image.new('RGBA', (image_width, image_height))
        res.paste(cropped_image_time, (0, 0))
        res.paste(cropped_image, (cropped_image_time.width, 0))
        res.save(f'Data/res{self.tg_id}.png')

    def close_driver(self):
        self.driver.close()
        self.driver.quit()