from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pandas as pd
import os


#pull each row's data out:
def Parser(): 
    #find current year:
    years = driver.find_element_by_xpath("/html/body/div[2]/div[2]")
    current_year = years.find_element_by_class_name("selected")
    
    #find current field:
    fields = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/span[2]")
    field = fields.find_element_by_class_name("selected-item")
    
    #find current sub-field:
    try:
        subfields = driver.find_element_by_class_name("sub-items")
        sub_field = subfields.find_element_by_class_name("selected-item")
    except:
        pass
    
    try:
        #finds data box
        first_box = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[1]/div[1]")
        #finds data rows within the box
        under = first_box.find_element_by_tag_name("ul")
        rows = under.find_elements_by_tag_name("li")
    except:
        pass
    try:
        rows_data = []
        for row in rows:
            row_data = []
            date = row.find_element_by_tag_name("b")
            price = row.find_element_by_tag_name("span")
            try:
                row_data.append(field.text)
            except:
                row_data.append('N/A')
            try:
                row_data.append(sub_field.text)
            except:
                row_data.append('N/A')
            try:
                row_data.append(re.findall('\d{1,4}',date.text)[0])
            except:
                row_data.append('N/A')
            try:
                row_data.append(re.findall('\d{1,4}',date.text)[1])
            except:
                row_data.append('N/A')
            try:
                row_data.append(re.findall('\d+',price.text)[0])
            except:
                row_data.append('N/A')
            rows_data.append(row_data)
            
        try:          
            df = pd.DataFrame(rows_data,columns=['Field', 'Subfield', 'Year', 'Month', 'Price'])
            
            if os.path.isfile('china.csv'):
                df.to_csv('china.csv', mode='a', header=False)
            else:
                df.to_csv('china.csv', mode='a', header=True)
        except:
            pass
    except:
        pass
    

def Refresh():
    elements = []
    regions = driver.find_element_by_class_name("elem-l")
    links = regions.find_elements_by_tag_name('a')
    for i in links:
        elements.append(i)
    return elements

def Refresh_subs():
    feelds = []
    try:
        subfields = driver.find_element_by_class_name("sub-items")
        s_field = subfields.find_elements_by_tag_name("a")
    except:
        pass
    for i in s_field:
        feelds.append(i)
    return feelds


driver = webdriver.Chrome('/Users/jackrickards/Documents/Python/Betting/Odds_Scrapers/Bet365/chromedriver')
driver.get('https://www.anjuke.com/fangjia/chengdu2017/')
driver.set_page_load_timeout(5)

for i in range (24):
    try:
        Parser()
        elements = Refresh()
        elements[i].click()
    except:
        pass
    for x in range(25):
        try:
            Parser()
            subs = Refresh_subs()  
            if 'SM' in subs[x].text:
                pass
            else:
                try:
                    subs[x].click()
                    Parser()
                except TimeoutException:
                    driver.execute_script("window.stop();")
        except:
            pass
    
    
    
    
    
    
    
    
    
    

