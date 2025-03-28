from app import app, db
from models import Machine, User
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Invalid username or password', 'error')
        elif not check_password_hash(user.password, password):
            flash('Invalid username or password', 'error')
        else:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/machines')
@login_required
def machines():
    all_machines = Machine.query.order_by(Machine.status, Machine.name).all()
    return render_template('machines.html', machines=all_machines)

@app.route('/')
@login_required
def dashboard():
    machines_count = Machine.query.count()
    active_machines = Machine.query.filter_by(status='active').count()
    maintenance_needed = Machine.query.filter(Machine.status != 'active').count()
    
    # Get machines needing maintenance soon (within 30 days)
    maintenance_soon = Machine.query.filter(
        Machine.last_maintenance < datetime.utcnow() - timedelta(days=330)  # ~11 months
    ).count()
    
    return render_template('dashboard.html',
        machines_count=machines_count,
        active_machines=active_machines,
        maintenance_needed=maintenance_needed,
        maintenance_soon=maintenance_soon,
        recent_activity=[]
    )

@app.route('/add-machine', methods=['GET', 'POST'])
@login_required
def add_machine():
    if request.method == 'POST':
        new_machine = Machine(
            name=request.form['name'],
            ip_address=request.form['ip_address'],
            cpu_specs=request.form['cpu_specs'],
            ram_gb=request.form['ram_gb'],
            storage_gb=request.form['storage_gb'],
            os_version=request.form['os_version'],
            last_maintenance=datetime.strptime(request.form['last_maintenance'], '%Y-%m-%d'),
            status=request.form['status']
        )
        db.session.add(new_machine)
        db.session.commit()
        return redirect(url_for('machines'))
    return render_template('add_machine.html')

@app.route('/api/machines')
@login_required
def api_machines():
    machines = Machine.query.all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'status': m.status
    } for m in machines])