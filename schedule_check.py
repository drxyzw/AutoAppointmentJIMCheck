from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://sto.imi.gov.my/e-temujanji/step2.php")

select_element = driver.find_element_by_id("jim")
Select(select_element).select_by_visible_text("JIM JOHOR")

wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "bhgn")))
select_element = driver.find_element_by_id("bhgn")
Select(select_element).select_by_visible_text("IBU PEJ IMI JOHOR")

wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "urusan")))
select_element = driver.find_element_by_id("urusan")
Select(select_element).select_by_visible_text("VISA, PAS DAN PERMIT -[ LEVEL 10 ] PERMOHONAN BARU (NEW) / LANJUTAN (RENEWAL) PAS LAWATAN SOSIAL JANGKA PANJANG (LONG TERM PASS)")

startDate = dt.now()
df = pd.DataFrame(columns=["result"])
for i in range(100):
    date = startDate + timedelta(days = i)
    dateStr = date.strftime("%d-%m-%Y")
    wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "from")))
    select_element = driver.find_element_by_id("from")
    driver.execute_script("sendvalue('" + dateStr + "')")
    alert = driver.switch_to.alert
    alert.accept()
    if i == 0:
        wait = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "slotdiv")))
    else:
        wait = WebDriverWait(driver, 60, poll_frequency=1)
        wait.until(lambda drv: drv.find_element_by_id("slotdiv").text != result)
    select_element = driver.find_element_by_id("slotdiv")
    result = select_element.text
    df.loc[date] = result
df.to_csv("JIM_schedule.csv")
print("finished")
