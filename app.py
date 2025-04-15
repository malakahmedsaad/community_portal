from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # required for session to work

# --- HOME PAGE ---
@app.route('/')
def home():
    return render_template('home.html')

# --- PROFILE PAGE ---
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        session['status'] = request.form['status']  # <--- store status in session
        with open('static/individuals.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                request.form['first_name'],
                request.form['last_name'],
                request.form['phone'],
                request.form['street'],
                request.form['city'],
                request.form['state'],
                request.form['zip'],
                request.form['status']
            ])
        return redirect(url_for('profile'))

    individuals = []
    try:
        with open('static/individuals.csv', newline='') as f:
            reader = csv.reader(f)
            individuals = list(reader)
    except FileNotFoundError:
        individuals = []

    return render_template('profile.html', individuals=individuals)

# --- REQUESTS PAGE ---
@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    if request.method == 'POST':
        with open('static/requests.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                request.form['status'],
                request.form['type'],
                request.form['priority'],
                request.form['zip'],
                request.form['contact']
            ])
        return redirect(url_for('requests_page'))

    requests_data = []
    try:
        with open('static/requests.csv', newline='') as f:
            reader = csv.reader(f)
            requests_data = list(reader)
    except FileNotFoundError:
        requests_data = []

    return render_template('requests.html', requests=requests_data)

# --- RESOURCES PAGE ---
@app.route('/resources')
def resources():
    resources_data = []
    try:
        with open('static/resources.csv', newline='') as f:
            reader = csv.reader(f)
            resources_data = list(reader)
    except FileNotFoundError:
        resources_data = []

    return render_template('resources.html', resources=resources_data)

# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)
