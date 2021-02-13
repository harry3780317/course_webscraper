import requests
from requests.exceptions import HTTPError, Timeout
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
##from selenium.webdriver.chrome.options import Options
## params = year/term/dept/search_param

MATCH_LIST = ["fall", "spring", "summer"]
OUTLINE_BASE_URL = "http://www.sfu.ca/outlines.html?"
##CHROME_PATH = "D:\chromedriver_win32\chromedriver.exe" # need install chrome driver for selenium to work https://chromedriver.chromium.org/downloads
CHROME_PATH = "/home/muvda/Study/Proj/mountain madness/chromedriver.exe"

##input("list out courses format: year/<fall|spring|summer> \n or search course format: year/<fall|spring|summer>/search_wildcard")
def checkInputParams():
    while True:
        input_params = "2019/fall/eng"  ## for testing purpose, please change to user input
        if input_params:
            parse_in = input_params.split("/")
            if len(parse_in) < 2:
                continue

            if not parse_in[0].isnumeric or parse_in[1].lower() not in MATCH_LIST:
                continue
            query_str = "http://www.sfu.ca/bin/wcm/course-outlines?year={}&term={}".format(parse_in[0],
                                                                                           parse_in[1].lower())
            if len(parse_in) == 3:
                query_str += "&search={}".format(parse_in[2])
            getResp(query_str)
            break

def getResp(query_str):
    try:
        res = requests.get(query_str, timeout=5)
        res.raise_for_status()
        jsonRes = res.json()
        print("FULL RESPONSE\n\n")
        print(jsonRes)
        print("\n\nONLY GET VALUE\n\n")
        for value in jsonRes:
            print(value["value"])

    except HTTPError as httperror:
        print(f"http error raised: code: {httperror}")
    except Timeout as timeout:
        print(f"http error timed out: code: {timeout}")
    except Exception as excep:
        print(f"exception raised: code: {excep}")

def scrapeOutline(suffix_val):
    furl = OUTLINE_BASE_URL + suffix_val
    driver = webdriver.Chrome(ChromeDriverManager().install())
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

scrapeOutline("2020/spring/math/100/d200")
