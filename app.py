from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Need, Resource, Service

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # required for session to work

@app.before_request
def before_request():
    if db.is_closed():
        db.connect()

@app.teardown_request
def teardown_request(exception):
    if not db.is_closed():
        db.close()

# --- HOME PAGE ---
@app.route('/')
def home():
    return render_template('home.html')

# --- PROFILE PAGE ---
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_user = User.create(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            street_address=request.form['street'],
            city=request.form['city'],
            state=request.form['state'],
            zip_code=request.form['zip'],
            volunteer=request.form.get('status') == 'Volunteer',
            admin=request.form.get('status') == 'Admin'
        )
        session['user_id'] = new_user.id
        session['status'] = 'Admin' if new_user.admin else 'Volunteer'
        return redirect(url_for('profile'))

    individuals = User.select()
    return render_template('profile.html', individuals=individuals)

# --- REQUESTS PAGE ---
@app.route('/requests', methods=['GET', 'POST'])
def requests_page():
    if request.method == 'POST':
        Need.create(
            type=request.form['type'],
            priority=request.form['priority'],
            requester=session['user_id']
        )
        return redirect(url_for('requests_page'))

    requests_data = Need.select()
    return render_template('requests.html', requests=requests_data)

# --- RESOURCES PAGE ---
@app.route('/resources')
def resources():
    resources_data = Resource.select()
    return render_template('resources.html', resources=resources_data)

# --- RUN APP ---
if __name__ == '__main__':
    app.run(debug=True)
