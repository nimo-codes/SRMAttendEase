from fastapi import FastAPI, HTTPException, Depends
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fastapi.responses import JSONResponse
import json
from tabulate  import tabulate
from time import sleep as tt




Alphabetical_order = {"A":0,"B":1,"C":2,"D":3,"F":4,"G":5,"E":6,"H":7}
Day_orders = [[["EMPTY","EMPTY","EMPTY"],[0,0,0]],[["A","F","G"],[2,2,1]],[["B","G","A"],[2,2,1]],[["C","A","B","D"],[2,1,1,1]],[["D","B","E","C"],[2,1,1,1]],[["E","C","F","D"],[2,1,1,1]]]
table_date={'1-7': 0, '2-7': 0, '3-7': 0, '4-7': 1, '5-7': 2, '6-7': 3, '7-7': 4, '8-7': 0, '9-7': 0, '10-7': 5, '11-7': 1, '12-7': 2, '13-7': 3, '14-7': 4, '15-7': 0, '16-7': 0, '17-7': 5, '18-7': 1, '19-7': 2, '20-7': 3, '21-7': 4, '22-7': 0, '23-7': 0, '24-7': 5, '25-7': 1, '26-7': 2, '27-7': 3, '28-7': 4, '29-7': 0, '30-7': 0, '31-7': 5, '1-8': 1, '2-8': 2, '3-8': 3, '4-8': 4, '5-8': 0, '6-8': 0, '7-8': 5, '8-8': 1, '9-8': 2, '10-8': 3, '11-8': 4, '12-8': 0, '13-8': 0, '14-8': 5, '15-8': 0, '16-8': 1, '17-8': 2, '18-8': 3, '19-8': 0, '20-8': 0, '21-8': 4, '22-8': 5, '23-8': 0, '24-8': 0, '25-8': 1, '26-8': 0, '27-8': 0, '28-8': 2, '29-8': 3, '30-8': 4, '31-8': 5, '1-9': 1, '2-9': 0, '3-9': 0, '4-9': 2, '5-9': 3, '6-9': 4, '7-9': 5, '8-9': 1, '9-9': 0, '10-9': 0, '11-9': 2, '12-9': 3, '13-9': 4, '14-9': 5, '15-9': 1, '16-9': 0, '17-9': 0, '18-9': 0, '19-9': 2, '20-9': 3, '21-9': 4, '22-9': 5, '23-9': 0, '24-9': 0, '25-9': 1, '26-9': 2, '27-9': 3, '28-9': 0, '29-9': 0, '30-9': 0, '1-10': 0, '2-10': 0, '3-10': 0, '4-10': 4, '5-10': 5, '6-10': 1, '7-10': 2, '8-10': 0, '9-10': 3, '10-10': 4, '11-10': 5, '12-10': 1, '13-10': 2, '14-10': 0, '15-10': 0, '16-10': 3, '17-10': 4, '18-10': 5, '19-10': 1, '20-10': 2, '21-10': 0, '22-10': 0, '23-10': 0, '24-10': 0, '25-10': 3, '26-10': 4, '27-10': 5, '28-10': 0, '29-10': 0, '30-10': 1, '31-10': 2, '1-11': 3, '2-11': 4, '3-11': 5, '4-11': 0, '5-11': 0, '6-11': 1, '7-11': 2, '8-11': 3, '9-11': 4, '10-11': 5, '11-11': 0, '12-11': 0, '13-11': 1, '14-11': 2, '15-11': 3, '16-11': 4, '17-11': 5, '18-11': 0, '19-11': 0, '20-11': 1, '21-11': 2, '22-11': 3, '23-11': 4, '24-11': 5, '25-11': 0, '26-11': 0, '27-11': 1, '28-11': 2, '29-11': 3, '30-11': 4}
print_list_final = []
headers = ["Course Code","Course Title","Old Attendance","New Percentage After OD"]

from pydantic import BaseModel


app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(login_request: LoginRequest):
    flag = True
    try:
        email = login_request.email
        password = login_request.password
    ###########################################  Chrome Options  #################################################################################
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("detach", True)


    ###########################################  Setting of webdriver  #################################################################################
        driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")
        driver.get("https://academia.srmist.edu.in/")
        wait = WebDriverWait(driver,10)
    ###########################################  Variables  #################################################################################
       
        try:
            iframe = wait.until(EC.presence_of_element_located((By.XPATH,"//iframe[@name='zohoiam']")))
            driver.switch_to.frame(iframe)
            login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_id')))
            login.click()
            login.clear()
            login.send_keys(email)
            click_next_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nextbtn"]')))
            click_next_1.click()
            driver.implicitly_wait(2)
            pass1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
            pass1.click()
            pass1.clear()
            pass1.send_keys(password)
            click_next_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nextbtn"]')))
            click_next_2.click()
        except Exception as e:
            flag = False
            return "Wrong creds"
        if(flag==True):
            tt(2)
            driver.get('https://academia.srmist.edu.in/#Page:My_Attendance')
            driver.implicitly_wait(10)
            table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="zc-viewcontainer_My_Attendance"]/div/div[4]/div/table[3]')))
            rows = table.find_elements_by_tag_name("tr")
            Course_Code = []
            Course_Title = []
            Slot = []
            Hours_Conducted = []
            Hours_Absent = []
            Attendance_Percentage = []
            new_percentage = []
            for row in rows:
                columns = row.find_elements_by_tag_name("td")
                Course_Code.append(columns[0].text)
                Course_Title.append(columns[1].text)
                Slot.append(columns[4].text)
                Hours_Conducted.append(columns[5].text)
                Hours_Absent.append(columns[6].text)
                Attendance_Percentage.append(columns[7].text)
            driver.close()
            data = {
                "Hours_absent":Hours_Absent,
                "Hours_conducted":Hours_Conducted,
                "Course_code":Course_Code,
                "Course_Title":Course_Title,
                "slot":Slot,
                "Attendance_Percentage":Attendance_Percentage
                
            }
            response = JSONResponse(content=data)
            response.set_cookie(key="fakesession", value="fake-cookie-session-value")
            return response
    except HTTPException as http_exception:
        return http_exception
    except Exception as e:
            print(f"error: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        

@app.post("/dates")
def map_date_dayorder(dates,obj):
    final_day_orders = []
    new_percentage = []
    for i in dates:
        if "-" in i:
            date,month = i.split("-")
            final_day_orders.append(table_date[f"{date}-{month}"])
    for j in final_day_orders:
        for i in range(len(Day_orders[j][0])):
          if Day_orders[j][0][i] in obj['slot']:
            obj['Hours_absent'][Alphabetical_order[Day_orders[j][0][i]]]-= Day_orders[j][1][i]    
    for i in range(0,len(obj['Hours_conducted'])):
        new_percentage.append(((obj['Hours_conducted'][i]-obj["Hours_absent"][i])/obj['Hours_conducted'][i]).__round__(4))
    return new_percentage
    
   
    




    



