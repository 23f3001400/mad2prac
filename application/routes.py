from flask import current_app as app, jsonify
from flask_security import auth_required,roles_required, current_user,roles_accepted
@app.route('/api/admin')
@auth_required('token') #Authentication
@roles_required('admin') #RBAC
def admin_home():
    return '<h1>Admin Home</h1>'

@app.route('/api/home')
@auth_required('token') #Authentication
@roles_accepted('user','admin') #RBAC
def user_home():
    user = current_user
    return jsonify({
        'username': user.username,
        "email": user.email,
        "password": user.password
    })