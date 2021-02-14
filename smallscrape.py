import requests
import json
from requests.exceptions import HTTPError, Timeout
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

## params = year/term/dept/coursenum
## i.e 2019/spring/cmpt/300
MATCH_LIST = ["fall", "spring", "summer"]
OUTLINE_BASE_URL = "http://www.sfu.ca/outlines.html?"
##CHROME_PATH = "D:\chromedriver_win32\chromedriver.exe" # need install chrome driver for selenium to work https://chromedriver.chromium.org/downloads

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
            return [parse_in[0], parse_in[1].lower(), parse_in[2], parse_in[3]]


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
    ret_dict_ls = []

    driver = webdriver.Chrome()
    for suffix_val in suffix_list:
        if suffix_val:
            ret_dict = {
                "course-times": [],
                "exam-times": [],
                "instructors": [],
                "prereq": [],
                "calenderdesc": "",
                "coursedet": "",
                "topics": [],
                "grading": [],
                "notes": [],
                "materials": "",
                "requiredreading": ""
            }
            furl = OUTLINE_BASE_URL + suffix_val
            driver.get(furl)
            try:
                owelems = driver.find_element_by_class_name("overview-list").find_elements_by_tag_name("li")
                for owelem in owelems:
                    attrib = owelem.get_attribute("class")
                    if attrib == "course-times":
                        ret_dict["course-times"].append(owelem.text)
                    elif attrib == "exam-times":
                        ret_dict["exam-times"].append(owelem.text)
                    elif attrib == "instructor":
                        ret_dict["instructors"].append(owelem.text)
                    elif attrib == "prereq":
                        ret_dict["prereq"].append(owelem.text)
            except NoSuchElementException:
                print("cannot find overview-list items")

            try:
                caldescr = driver.find_element_by_xpath(
                    "//h4[contains(text(),'CALENDAR DESCRIPTION:')]/following-sibling::p")
                ret_dict["calenderdesc"] = caldescr.text
            except NoSuchElementException:
                print("cannot find calendar description")

            try:
                coursedet = driver.find_element_by_xpath(
                    "//h4[contains(text(),'COURSE DETAILS:')]/following-sibling::p")
                ret_dict["coursedet"] = coursedet.text
            except NoSuchElementException:
                print("cannot find course details")

            try:
                topics = driver.find_element_by_xpath("//h2[contains(text(), 'Topics')]/following-sibling::ul")
                topicsls = topics.find_elements_by_tag_name("li")
                for topicls in topicsls:
                    ret_dict["topics"].append(topicls.text)
            except NoSuchElementException:
                print("cannot find related course topics")

            try:
                grading = driver.find_element_by_class_name("grading")
                glists = grading.find_element_by_class_name("grading-items").find_elements_by_tag_name("li")
                for glist in glists:
                    one = glist.find_element_by_class_name("one")
                    two = glist.find_element_by_class_name("two")
                    ret_dict["grading"].append({"one" : one.text, "two": two.text})
                notes = grading.find_elements_by_tag_name("p")
                for note in notes:
                    ret_dict["notes"].append(note.text)
            except NoSuchElementException:
                print("cannot find grading distribution")

            try:
                material = driver.find_element_by_xpath(
                    "//h4[contains(text(),'MATERIALS + SUPPLIES:')]/following-sibling::p")
                ret_dict["materials"] = material.text
            except NoSuchElementException:
                print("cannot find materials and suplies for course")

            try:
                reqreading = driver.find_element_by_xpath(
                    "//h4[contains(text(),'REQUIRED READING:')]/following-sibling::div")
                ret_dict["requiredreading"] = reqreading.text
            except NoSuchElementException:
                print("cannot find required reading")
            ret_dict_ls.append(ret_dict)
    ret_json = json.dumps(ret_dict_ls, indent=4)
    print(ret_json)
    driver.quit()


out = getResp(parseInputParams())
print(out)
scrapeOutline(out)
