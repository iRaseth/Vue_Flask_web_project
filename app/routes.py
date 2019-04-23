from app import app
from app import db
from app.database_models import User, Post, PrivateChat, PrivateMessage, PostSchema, SimpleNeuronModel, SimpleNeuronSchema
from app.app_methods import HTTP_Methods, DB_Methods, ANN_Single_Methods
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, session, abort, jsonify
import json
import numpy as np
from snn.algr import SimpleNeuron

HTTP_Validator = HTTP_Methods('http_validator')
DB_Set = DB_Methods('db_methods')
SNN_Single_Validator = ANN_Single_Methods('snn_validator')

@app.route('/')
@app.route('/index')
def index_route():
    return render_template('index.html', title='Index')
    #return render_template('unindex.html', title='Index')

@app.route('/register', methods=['GET', 'POST'])
def parse_request():
    if request.method != 'POST':
        return abort(405)
    
    request_json = request.get_json()
    if request_json['username'] and request_json['password']:
        if HTTP_Validator.is_username_unique(username=request_json['username']):
            newUser = User(username=request_json['username'])
            newUser.set_password(request_json['password'])
            db.session.add(newUser)
            db.session.commit()
            return 'user has been created successfuly'
        else:
            return 'user with this nickname already exist'
    else:
        return 'please input login and password for registration'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'user already logged in'
    if request.method == 'POST':
        user = HTTP_Validator.check_login_data(request)
        if user:
            login_user(user)
            #return redirect(url_for('default'))
            return 'login success'
        else:
            return 'wrong input data'
    else:
        return 'method err'

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return 'Uve been logged out'

@app.route('/get_id')
@login_required
def get_id():
    if current_user.is_authenticated:
        return current_user.username
    else:
        abort(401)

@app.route('/send_msg', methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'POST':
        if current_user.is_authenticated:
            request_json = request.get_json()
            post_body = request_json['message']
            if post_body:
                post_user = current_user.username
                new_post = Post(body=post_body,author=post_user)
                db.session.add(new_post)
                db.session.commit()
                return 'u have added post'
            else:
                return 'u cant send empty msg'
        #HTTP_Validator.parse_post_msg(request)
    elif request.method == 'GET':
        if current_user:
            return 'you cant send new message with GET method'

@app.route('/delete_post/<id>', methods=["DELETE"])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if current_user.username == post.author:
        db.session.delete(post)
        db.session.commit()
    else:
        return abort(401)
    return 'Note has been removed.'

@app.route('/get_posts')
@login_required
def get_posts():
    posts = Post.query.all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(posts)
    return jsonify(result.data)

@app.route('/set_single_neuron', methods=['GET', 'POST'])
@login_required
def send_ann_input():
    if request.method != 'POST':
        return abort(405)
    # Getting the necessary data for the neuron
    input_array = SNN_Single_Validator.single_neuron_input(request)
    for x in input_array:
        if x == 'err':
            return 'Error with data input.'
    #Creating the neuron
    neuron = SimpleNeuron(input_array)
    neuron.train(input_array[2])
    return jsonify(success=True,
                input=str(neuron.input),
                weights=str(neuron.weights),
                output=str(neuron.u))

@app.route('/default_neuron')
@login_required
def get_default_neuron():
    if current_user.is_authenticated:
        defaultNeuron = SimpleNeuronModel.query.filter_by(id=1).first()
        neuron_schema = SimpleNeuronSchema()
        result = neuron_schema.dump(defaultNeuron)
        return jsonify(result.data)
    else:
        return abort(401)

@app.route('/default')
@login_required
def default():
    return render_template('index.html', title='Index')

"""TESTING DB CONNECTION"""

@app.route('/show-db')
@login_required
def show_database():
    users = User.query.all()
    posts = Post.query.all()
    privatemessage = PrivateMessage.query.all()
    neurons = SimpleNeuronModel.query.all()
    print(users)
    print(posts)
    print(neurons)
    #print(type(posts))
    #print(privatemessage)
    return 'fetched'

@app.route('/delete-users')
@login_required
def delete_users():
    User.query.delete()
    Post.query.delete()
    db.session.commit()
    return 'deleted'
