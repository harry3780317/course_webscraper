import json
import urllib.request

from flask import Flask, render_template, request, redirect, url_for

from prof_scrape import scrape_rating
from smallscrape import scrapeOutlineForApp

app = Flask(__name__)
prefix = ('')


@app.route('/')
def home():
    with urllib.request.urlopen("http://www.sfu.ca/bin/wcm/course-outlines/?year=2021&term=summer&search=CMPT") as url:
        courses = json.loads(url.read().decode())
    return render_template('home.html', courses=courses)


@app.route('/your-course', methods=['GET', 'POST'])
def your_course():
    if request.method == 'POST':
        url_suffix = request.form['course']
        outline = scrapeOutlineForApp(url_suffix)
        if 'instructor' in outline:
            name = generated_name(outline['instructor'])
            rating = scrape_rating(name)
            return render_template('your_course.html', outline=outline, rating=rating)
        return render_template('your_course.html', outline=outline)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()


def generated_name(name):
    final_name = ''
    for word in name.split('\n'):
        if word[0].isupper() and word != 'INSTRUCTOR:':
            final_name += word + ' '
    return final_name
