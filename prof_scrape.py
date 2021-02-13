import requests
from bs4 import BeautifulSoup

# params for prof = %20Name1%20Name2
MY_PROF_QUERRY_URL = "https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName=Simon" \
                     "%20Fraser%20University&schoolID=1482&query="
MY_PROF_URL = "https://www.ratemyprofessors.com"


def scrape_rating(name):
    prof_review = {'name': name}

    name_split = name.split(' ')
    suffix = ''
    for elem in name_split:
        suffix += '%20' + elem
    query_url = MY_PROF_QUERRY_URL + suffix

    # user agent spoof
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.80 Safari/537.36'}

    session = requests.Session()
    session.headers.update(headers)
    root = session.get(query_url)
    root_soup = BeautifulSoup(root.content, "html.parser")
    prof_infos = []
    for list in root_soup.findAll('li', attrs={'class': 'listing PROFESSOR'}):
        if len(list) != 0:
            prof_infos.append(list.a['href'])
    if len(prof_infos) != 0:
        # basic logic: obtain the first link
        prof_rating_url = MY_PROF_URL + prof_infos[0]
        review = session.get(prof_rating_url)
        review_soup = BeautifulSoup(review.content, "html.parser")
        prof_review['score'] = review_soup.find("div", {"class": "RatingValue__Numerator-qw8sqy-2 liyUjw"}).text
        feedback_num = []
        # other feedback number
        for elem in review_soup.findAll("div", {"class": "FeedbackItem__FeedbackNumber-uof32n-1 kkESWs"}):
            feedback_num.append(elem.text)
        prof_review['take_again'] = feedback_num[0]
        prof_review['difficulty'] = feedback_num[1]
        # look for all tags
        feedback_tag = []
        div_tags = review_soup.find("div", {"class": "TeacherTags__TagsContainer-sc-16vmh1y-0 dbxJaW"})
        for elem in div_tags.findAll("span", {"class": "Tag-bs9vf4-0 hHOVKF"}):
            feedback_tag.append(elem.text)
        prof_review['tags'] = feedback_tag
    else:
        prof_review['error'] = 'The professor does not exist or not available'
    print(prof_review)


scrape_rating("Liam O'Flaherty")
