from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from tabulate  import tabulate
from time import sleep as tt
import keyring
import logging 
import getpass

###########################################  Chrome Options  #################################################################################
options = Options()
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("detach", True)

###########################################  Setting of webdriver  #################################################################################
driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/jarvis/pymycod/automation/chromedriver")
driver.get("https://academia.srmist.edu.in/")
wait = WebDriverWait(driver,10)

###########################################  Setting logger  #################################################################################
logging.basicConfig(filename="/Users/jarvis/pymycod/automation/sp_scraper/academia_scraper/logs.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

###########################################  Functions  #################################################################################
table_data =[]
Course_Code = []
Course_Title = []
Slot = []
Hours_Conducted = []
Hours_Absent = []
Attendance_Percentage = []
new_percentage = []
Alphabetical_order = {"A":0,"B":1,"C":2,"D":3,"F":4,"G":5,"E":6,"H":7}
Day_orders = [[["EMPTY","EMPTY","EMPTY"],[0,0,0]],[["A","F","G"],[2,2,1]],[["B","G","A"],[2,2,1]],[["C","A","B","D"],[2,1,1,1]],[["D","B","E","C"],[2,1,1,1]],[["E","C","F","D"],[2,1,1,1]]]
table_date={'18-1':2,'1-7': 0, '2-7': 0, '3-7': 0, '4-7': 1, '5-7': 2, '6-7': 3, '7-7': 4, '8-7': 0, '9-7': 0, '10-7': 5, '11-7': 1, '12-7': 2, '13-7': 3, '14-7': 4, '15-7': 0, '16-7': 0, '17-7': 5, '18-7': 1, '19-7': 2, '20-7': 3, '21-7': 4, '22-7': 0, '23-7': 0, '24-7': 5, '25-7': 1, '26-7': 2, '27-7': 3, '28-7': 4, '29-7': 0, '30-7': 0, '31-7': 5, '1-8': 1, '2-8': 2, '3-8': 3, '4-8': 4, '5-8': 0, '6-8': 0, '7-8': 5, '8-8': 1, '9-8': 2, '10-8': 3, '11-8': 4, '12-8': 0, '13-8': 0, '14-8': 5, '15-8': 0, '16-8': 1, '17-8': 2, '18-8': 3, '19-8': 0, '20-8': 0, '21-8': 4, '22-8': 5, '23-8': 0, '24-8': 0, '25-8': 1, '26-8': 0, '27-8': 0, '28-8': 2, '29-8': 3, '30-8': 4, '31-8': 5, '1-9': 1, '2-9': 0, '3-9': 0, '4-9': 2, '5-9': 3, '6-9': 4, '7-9': 5, '8-9': 1, '9-9': 0, '10-9': 0, '11-9': 2, '12-9': 3, '13-9': 4, '14-9': 5, '15-9': 1, '16-9': 0, '17-9': 0, '18-9': 0, '19-9': 2, '20-9': 3, '21-9': 4, '22-9': 5, '23-9': 0, '24-9': 0, '25-9': 1, '26-9': 2, '27-9': 3, '28-9': 0, '29-9': 0, '30-9': 0, '1-10': 0, '2-10': 0, '3-10': 0, '4-10': 4, '5-10': 5, '6-10': 1, '7-10': 2, '8-10': 0, '9-10': 3, '10-10': 4, '11-10': 5, '12-10': 1, '13-10': 2, '14-10': 0, '15-10': 0, '16-10': 3, '17-10': 4, '18-10': 5, '19-10': 1, '20-10': 2, '21-10': 0, '22-10': 0, '23-10': 0, '24-10': 0, '25-10': 3, '26-10': 4, '27-10': 5, '28-10': 0, '29-10': 0, '30-10': 1, '31-10': 2, '1-11': 3, '2-11': 4, '3-11': 5, '4-11': 0, '5-11': 0, '6-11': 1, '7-11': 2, '8-11': 3, '9-11': 4, '10-11': 5, '11-11': 0, '12-11': 0, '13-11': 1, '14-11': 2, '15-11': 3, '16-11': 4, '17-11': 5, '18-11': 0, '19-11': 0, '20-11': 1, '21-11': 2, '22-11': 3, '23-11': 4, '24-11': 5, '25-11': 0, '26-11': 0, '27-11': 1, '28-11': 2, '29-11': 3, '30-11': 4}
final_day_orders = []
print_list_final = []
headers = ["Course Code","Course Title","Old Attendance","New Percentage After OD"]


def login(email,password):
  iframe = wait.until(EC.presence_of_element_located((By.XPATH,"//iframe[@name='zohoiam']")))
  driver.switch_to.frame(iframe)
  login = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_id')))
  login.click()
  login.clear()
  login.send_keys(email)
  click_next_1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nextbtn"]')))
  click_next_1.click()
  driver.implicitly_wait(3)
  pass1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
  pass1.click()
  pass1.clear()
  pass1.send_keys(password)
  click_next_2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nextbtn"]')))
  click_next_2.click()

def get_Attendance():
  tt(2)
  driver.get('https://academia.srmist.edu.in/#Page:My_Attendance')
  driver.implicitly_wait(15)
  table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="zc-viewcontainer_My_Attendance"]/div/div[4]/div/table[3]')))
  rows = table.find_elements_by_tag_name("tr")
  for row in rows:
      columns = row.find_elements_by_tag_name("td")
      Course_Code.append(columns[0].text)
      Course_Title.append(columns[1].text)
      Slot.append(columns[4].text)
      Hours_Conducted.append(columns[5].text)
      Hours_Absent.append(columns[6].text)
      Attendance_Percentage.append(columns[7].text)

def get_time_table():
  driver.get('https://academia.srmist.edu.in/#Page:Unified_Time_Table_2023_Batch_1')
  driver.implicitly_wait(15)

  table_time_table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="zc-viewcontainer_Unified_Time_Table_2023_Batch_1"]/div/table[1]')))
  rows = table_time_table.find_elements_by_tag_name("tr")
  # Day_1.append(rows[3].text)
  # Day_2.append(rows[4].text)
  # Day_3.append(rows[5].text)
  # Day_4.append(rows[6].text)
  # Day_5.append(rows[7].text)


def get_Academic():
  driver.get("https://academia.srmist.edu.in/#Academic_Reports")
  page_source = driver.page_source
  soup = BeautifulSoup(page_source, 'html.parser')
  element = soup.select_one('#html_snippet > div > div.zc-pb-tile-container > div > div > div > div > table:nth-child(3)')

  if element:
    # Do something with the found element, e.g., extract its text
    print(element.text)
  # table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="html_snippet"]/div/div[2]/div/div/div/div/table[1]')))
  # rows = table.find_elements_by_tag_name("tr")
  # for row in rows:
  #     columns = row.find_elements_by_tag_name("td")
  #     row_data = [column.text for column in columns]
  #     table_data.append(row_data)

def map_date_dayorder(dates):
  for i in dates:
      if "-" in i:
        date,month = i.split("-")
        final_day_orders.append(table_date[f"{date}-{month}"])
          
          
          

def cal_OD(Day_order):
    for j in Day_order:
        for i in range(len(Day_orders[j][0])):
          if Day_orders[j][0][i] in Slot:
            Hours_Absent[Alphabetical_order[Day_orders[j][0][i]]]-= Day_orders[j][1][i]
            # Hours_Conducted[Alphabetical_order[Day_orders[Day_order][0][i]]]+= Day_orders[Day_order][1][i]    
    for i in range(0,len(Hours_Conducted)):
        new_percentage.append(((Hours_Conducted[i]-Hours_Absent[i])/Hours_Conducted[i]).__round__(4))

  
def err(reason,num):
  place = {0:"captcha can't be located",1:"pytesseract gave error",2:"work being handled"}
  print(f"error encountered- {num}")
  message = f'''following block is the possible reason for the raised exception {num},
  reason - {place[num]}, 
  exception raised - {reason}'''
  inter_msg = message.split(",")
  final_message = f'''{inter_msg[0]},
  {inter_msg[1]},
  {inter_msg[2].split("Stacktrace:")[0]}'''
  logger.error(final_message)
  

###########################################  Start of code  #################################################################################
flag = False
while flag==False:
  try:
    captchaaa = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[4]/div[2]/img')))
    login(captchaaa)
    try:
      grades= wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="listId8"]')))
      flag=True
    except:
      flag=False
  except Exception as error1:
    err(error1,1)


if flag==True:
  try:
    print(cal_grades())
  except Exception as error2:
    err(error2,2)

user_id = "nn4489"
# pasword_input= getpass.getpass("ENTER THE PASSWORD: ")
login(f"{user_id}@srmist.edu.in",keyring.get_password("srmsp",f"{user_id}"))
# user_id = input("Enter the user id: ")
# login(f"{user_id}@srmist.edu.in",pasword_input)
get_Attendance()
print(Hours_Absent)
print(Hours_Conducted)

Hours_Absent = list(map(int,Hours_Absent[1:]))
Hours_Conducted = list(map(int,Hours_Conducted[1:])) 
map_date_dayorder(['17-8','21-8','22-8','14-8','16-8','4-8','5-9','11-9','13-9','15-9'])
map_date_dayorder([])




cal_OD(final_day_orders)
Attendance_Percentage = list(map(float,Attendance_Percentage[1:])) 
Course_Title = list(map(str,Course_Title[1:])) 
Course_Code = list(map(str,Course_Code[1:])) 
new_percentage = list(map(lambda x:x*100,new_percentage))
for i in range(0,len(Course_Title)):
  print_list_final.append([Course_Code[i],Course_Title[i],Attendance_Percentage[i],new_percentage[i]])
os.system("clear")
print('''                                         Attendance details                         ''')
print(tabulate(print_list_final, headers=headers,tablefmt='github'))
driver.close()



# # make detention portal if u leave classes will u be detained or not



        

data ={
  "Hours_absent": [
    "0",
    "0",
    "0",
    "2",
    "0",
    "0",
    "0",
    "0",
    "0"
  ],
  "Hours_conducted": [
    "Hours Conducted",
    "2",
    "3",
    "3",
    "3",
    "2",
    "0",
    "2",
    "0",
    "0"
  ],
  "Course_code": [
    "Course Code",
    "21MAB204T\nRegular",
    "21CSC204J\nRegular",
    "21CSE251T\nRegular",
    "21CSC205P\nRegular",
    "21PDH201T\nRegular",
    "21CSC206T\nRegular",
    "21LEM202T\nRegular",
    "21CSC204J\nRegular",
    "21PDM202L\nRegular"
  ],
  "Course_Title": [
    "Course Title",
    "Probability and Queueing Theory",
    "Design and Analysis of Algorithms",
    "Digital Image Processing",
    "Database Management Systems",
    "Social Engineering",
    "Artificial Intelligence",
    "UHV-II: Universal Human Values – Understanding Harmony and Ethical Human Conduct",
    "Design and Analysis of Algorithms",
    "Critical and Creative Thinking Skills"
  ],
  "slot": [
    "Slot",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "LAB",
    "LAB"
  ],
  "Attendance_Percentage": [
    "Attn %",
    "100.00",
    "100.00",
    "100.00",
    "33.33",
    "100.00",
    "0.00",
    "100.00",
    "0.00",
    "0.00"
  ]
}
 
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
            print(obj['Hours_absent'][Alphabetical_order[Day_orders[j][0][i]]])
            intermediate = int(obj['Hours_absent'][Alphabetical_order[Day_orders[j][0][i]]])
            intermediate -= Day_orders[j][1][i]  
    for i in range(0,len(obj['Hours_conducted'])):
        new_percentage.append(((obj['Hours_conducted'][i]-obj["Hours_absent"][i])/obj['Hours_conducted'][i]).__round__(4))
    return new_percentage


map_date_dayorder(['18-1'],data)
    