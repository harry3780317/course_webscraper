import requests
from requests.exceptions import HTTPError, Timeout
from selenium import webdriver
##from selenium.webdriver.chrome.options import Options
## params = year/term/dept/coursenum
## i.e 2019/spring/cmpt/300
MATCH_LIST = ["fall", "spring", "summer"]
OUTLINE_BASE_URL = "http://www.sfu.ca/outlines.html?"
##CHROME_PATH = "D:\chromedriver_win32\chromedriver.exe" # need install chrome driver for selenium to work https://chromedriver.chromium.org/downloads

##input("list out courses format: year/<fall|spring|summer> \n or search course format: year/<fall|spring|summer>/dept/coursenumber")

def parseInputParams():

    while True:
        input_params = input("search for class in format of year/term/dept/coursenum: ")
        if input_params:
            parse_in = input_params.split("/")
            if len(parse_in) < 4:
                print("need exactly four arguments i.e in the format of year/term/dept/coursenum")
                continue
            if not parse_in[0].isnumeric():
                print("year should be numeric i.e 2019")
                continue
            if parse_in[1].lower() not in MATCH_LIST:
                print("terms must be exactly one of fall|spring|summer")
                continue
            if any(i.isdigit() for i in parse_in[2]):
                print("dept cannot contain numbers")
                continue
            if not parse_in[3].isnumeric():
                print("coursenumber should be numeric i.e 300")
                continue
            return [parse_in[0], parse_in[1].lower(),parse_in[2],parse_in[3]]

def getResp(query_list):

    query_str = "http://www.sfu.ca/bin/wcm/course-outlines?year={}&term={}&search={}%20{}".format(query_list[0],
                                                                                                  query_list[1],
                                                                                                  query_list[2],
                                                                                                  query_list[3])
    print("related results: \n")
    suffix_list = []
    try:
        res = requests.get(query_str, timeout=5)
        res.raise_for_status()
        jsonRes = res.json()
        for value in jsonRes:
            suffix_str = value["value"]
            ls = suffix_str.split("/")
            if len(ls) < 5:
                continue
            if ls[3] != query_list[3]:
                continue
            suffix_list.append(suffix_str)

    except HTTPError as httperror:
        print(f"http error raised: code: {httperror}")
    except Timeout as timeout:
        print(f"http error timed out: code: {timeout}")
    except Exception as excep:
        print(f"exception raised: code: {excep}")
    return suffix_list

def scrapeOutline(suffix_list):

    driver = webdriver.Chrome()
    for suffix_val in suffix_list:
        if suffix_val:
            furl = OUTLINE_BASE_URL + suffix_val
            driver.get(furl)
            owelems = driver.find_element_by_class_name("overview-list").find_elements_by_tag_name("li")
            for owelem in owelems:
                attrib = owelem.get_attribute("class")
                if attrib == "course-times" or attrib == "exam-times":
                    p = owelem.text
                    print(p)
                elif attrib == "instructor":
                    instr = owelem.text
                    print(instr)
                elif attrib == "prereq":
                    prereq = owelem.text
                    print(prereq)
            caldescr = driver.find_element_by_xpath("//h4[contains(text(),'CALENDAR DESCRIPTION:')]/following-sibling::p")
            print(caldescr.text)
            coursedet = driver.find_element_by_xpath("//h4[contains(text(),'COURSE DETAILS:')]/following-sibling::p")
            print(coursedet.text)
            glists = driver.find_element_by_class_name("grading-items").find_elements_by_tag_name("li")
            for glist in glists:
                one = glist.find_element_by_class_name("one")
                two = glist.find_element_by_class_name("two")
                print(one.text)
                print(two.text)
            material = driver.find_element_by_xpath("//h4[contains(text(),'MATERIALS + SUPPLIES:')]/following-sibling::p")
            print(material.text)
            reqreading = driver.find_element_by_xpath("//h4[contains(text(),'REQUIRED READING:')]/following-sibling::div")
            print(reqreading.text)
    driver.close()

out = getResp(parseInputParams())
print(out)
#scrapeOutline(out)
