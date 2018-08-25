import os

from flask import request, Flask
from keras.models import Sequential
from keras.layers import Dense

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        experiments = db.query_db('select * from experiment')
        print('experiments: ', experiments)

        return 'hi ople.ai' # TODO: return list of experiments

    # create an experiment
    @app.route('/experiment', methods=['POST'])
    def create_experiment():
        experiment = request.get_json()
        name, type, result, test_data, train_data = experiment

        db.query_db('insert into experiment (name, type, result, test_data, train_data) values (?, ?, ?, ?, ?)', \
            [name, type, result, test_data, train_data])

        return 'ok' # TODO: return id

    # retrieve an experiment
    @app.route('/experiment/<int:id>')
    def read_experiment(id):
        experiment = db.query_db('select from experiment where id = ? ', \
            [id] one=True)
        
        return experiment # TODO: to json

    # modify an experiment
    @app.route('/experiment/<int:id>', methods=['PUT'])
    def update_experiment(id):
        experiment = request.get_json()
        name, type, result, test_data, train_data, id = experiment

        db.query_db('update experiment set name = ?, type = ?, result = ?, test_data = ?, train_data = ?) where id = ?', \
            [name, type, result, test_data, train_data, id])

        return 'ok' # TODO: return id

    # delete an experiment
    @app.route('/experiment/<int:id>', methods=['DELETE'])
    def delete_experiment(id):
        db.query_db('delete from experiment where id = ?', \
            [id])

        return 'ok' # TODO: return id

    # train
    @app.route('/train/<int:id>')
    def train(id):
        train_data = db.query_db('select train_data from experiment where id = ? ', \
            [id] one=True)
        x_train, y_train = get_x_y_split(train_data)

        model = Sequential()
        model.add(Dense(units=64, activation='relu', input_dim=100))
        model.add(Dense(units=10, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=5, batch_size=32)
        model.save('some/path/to/experiment/id/models/model_id')

        return 'model id'

    # test
    @app.route('/test/<int:id>/<int:model_id>')
    def test(id, model_id):
        model = keras.models.load_model('some/path/to/experiment/id/models/model_id')
        test_data = db.query_db('select test_data from experiment where id = ? ', \
            [id] one=True)
        x_test, y_test = get_x_y_split(train_data)

        loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

        return 'statistics'

    # predit
    @app.route('/predict/<int:id>/<int:model_id>')
    def predict(id, model_id):
        model = keras.models.load_model('some/path/to/experiment/id/models/model_id')
        x_test = request.get_json()

        classes = model.predict(x_test, batch_size=128)

        return 'prediction'

    from . import db
    db.init_app(app)

    return app