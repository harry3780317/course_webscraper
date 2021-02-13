from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/your-course', methods=['GET', 'POST'])
def your_course():
    if request.method == 'POST':
        return render_template('your_course.html', course=request.form['course'])
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
