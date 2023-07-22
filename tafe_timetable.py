import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select


def timetable_lookup():
    options = Options()
    options.headless = True
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://timetables.tafeqld.edu.au/Group")

    dropdown = driver.find_element("id","Database")
    dd = Select(dropdown)
    dd.select_by_value("TQBN")
    search_table = driver.find_element("id","CelcatGroupNames")
    search_table.send_keys("ICT30120 Cert III Information Technology (Web) Jul 2023 South Bank")
    time.sleep(0.5) # Temp solution to wait until webpage updates to load in timetable
                    # This part takes a while to load on server side. If anything happens, increase the timer.

    search_table_selector = driver.find_element("xpath", "//ul[@class='ui-menu ui-widget ui-widget-content ui-autocomplete ui-front']//li[@class='ui-menu-item']/div")
    search_table_selector.click()
    time.sleep(0.1) # Needed for contents to laod inorder to take a screenshot.

    # Takes a screenshot of the timetable.
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
    driver.find_element("xpath","//div[@id='GroupTable']").screenshot('timetable.png')

    driver.quit()
