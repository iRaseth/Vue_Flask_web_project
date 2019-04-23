from app import db
from app.database_models import User, Post, SimpleNeuronModel
from app import app
import numpy as np
import json

class HTTP_Methods():
    def __init__(self, name):
        self.name = name

    def check_login_data(self, request):
        request_json = request.get_json()
        username = request_json['username']
        password = request_json['password']
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            if db_user.check_password(password):
                return db_user
            else:
                return False
        else:
            return False

    def is_username_unique(self, username):
        db_user = User.query.filter_by(username = username).first()
        if db_user is not None:
            return False
        else:
            return True

    def parse_post_msg(self, request):
        return True


class DB_Methods():
    def __init__(self, name):
        self.name = name

    def return_post_JSON(self, posts):
        dictionary = {}
        dictionary_index = 0
        for post in posts:
            tmp_dictionary = {
                'author' : post.author,
                'post' : post.body
            }
            dictionary[dictionary_index] = tmp_dictionary
            dictionary_index += 1
        post_json = json.dumps(dictionary, indent=4)
        return(post_json)

class ANN_Single_Methods():
    def __init__(self, name):
        self.name = name

    def get_x(self, request, input_name):
        x_json = request.get_json()
        x = str(x_json[input_name])
        x_len = ''
        for i in x:
            if i == '.':
                x_len = x.replace('.','')
        if len(x_len) > 5:
            return 'err'
        try:
            x_float = float(x)
        except ValueError:
            return 'err'
        return x_float

    def get_iterator(self, request):
        iterator_json = request.get_json()
        iterator = str(iterator_json['iterator'])
        if len(iterator) > 3:
            return 'err'
        try:
            iterator = int(iterator)
        except ValueError:
            return 'err'
        if iterator > 100:
            return 100
        elif iterator < 5:
            return 5
        return iterator

    def get_learning_parameter(self, request):
        learning_parameter_json = request.get_json()
        learning_parameter = str(learning_parameter_json['learningParameter'])
        if len(learning_parameter) > 3:
            return 'err'
        try:
            learning_parameter = float(learning_parameter)
        except ValueError:
            return 'err'
        if learning_parameter > 0.9:
            return 0.9
        elif learning_parameter < 0.1:
            return 0.1
        return learning_parameter

    def single_neuron_input(self, request):
        x1 = self.get_x(request, 'x1')
        x2 = self.get_x(request, 'x2')
        iterator = self.get_iterator(request)
        learning_parameter = self.get_learning_parameter(request)
        desired_output = self.get_x(request, 'output')
        input_array = [x1, x2, iterator, learning_parameter, desired_output]
        return input_array

class DataInitializer():
    def __init__(self, name):
        self.name = name

    def createNeuron(self):
        defaultNeuron = SimpleNeuronModel(x1=1.5, x2=2.0, iterator=50, learning_parameter=0.1, expected_output=4)
        neuron = SimpleNeuronModel.query.filter_by(x1=1.5).first()
        if neuron is None:
            db.session.add(defaultNeuron)
            db.session.commit()
            print defaultNeuron

dataInit = DataInitializer('myInitializer')
dataInit.createNeuron()
