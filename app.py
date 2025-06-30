from flask import Flask, render_template, request, redirect, url_for, session
import db
import traffic_db 

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/')
def home():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])

            # Redirect based on role
            if session['is_admin']:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success = db.create_user(username, password)
        if success:
            return redirect(url_for('login'))
        else:
            return "Username already exists. <a href='/register'>Try again</a>"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session and session.get('is_admin'):
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'user_id' in session and not session.get('is_admin'):
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/manage_signals', methods=['GET', 'POST'])
def manage_signals():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form['location']
        status = request.form['status']
        traffic_db.add_signal(location, status)

    signals = traffic_db.get_all_signals()
    return render_template('manage_signals.html', signals=signals)
@app.route('/report_incidents', methods=['GET', 'POST'])
def report_incidents():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        location = request.form['location']
        incident_type = request.form['incident_type']
        description = request.form['description']
        traffic_db.add_incident(location, incident_type, description)

    incidents = traffic_db.get_all_incidents()
    return render_template('report_incidents.html', incidents=incidents)

@app.route('/delete_signal/<int:signal_id>')
def delete_signal(signal_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    traffic_db.delete_signal(signal_id)
    return redirect(url_for('manage_signals'))
@app.route('/delete_incident/<int:incident_id>')
def delete_incident(incident_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    traffic_db.delete_incident(incident_id)
    return redirect(url_for('report_incidents'))

@app.route('/view_reports')
def view_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    incidents = traffic_db.get_all_incidents()
    signals=traffic_db.get_all_signals()
    return render_template('view_reports.html', incidents=incidents,signals=signals)


if __name__ == '__main__':
    db.init_db()
    traffic_db.init_traffic_db()
    app.run(debug=True)
