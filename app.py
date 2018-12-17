from flask import Flask, flash, render_template, request, session,jsonify,Blueprint
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from models.Todo import Todo
from models.users import users

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)

app.register_blueprint(blueprint)

ns = api.namespace('todo', description='TODO operations')


@app.route('/')
def home():
    list  = [task for task in todo]
    if  session.get('logged_in') in [user.login,user.login_as_admin]:
        return render_template('index.html', todo_list=list,user=session.get("logged_in"))
    else:
        return login()

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        if 'login_type' not in request.form:
            return render_template('login.html' ,error={"msg":"Enter one option"})
        if int(request.form['login_type']) == user.login_as_admin :
            session['logged_in'] = user.login_as_admin
        else:
            session['logged_in'] = user.login
        return home()
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return login()


@app.route("/add",methods=["POST"])
def add():
    task = request.form['task']
    due_by = request.form['due_by']
    status = request.form['status']

    print(request.form['id'])

    if request.form['id'] != "#":
        id = request.form['id']
        print(status)
        todo.update(id,task, due_by,status)
        return home()
    else:
        todo.insert(task,due_by,status)
        return home()

@ns.route('/due_date')
@ns.response(404, 'Opps! page not found')
@ns.param('due_date', 'The task date')
class due_date(Resource):
    @ns.doc('due_date')
    def get(self):
        '''Fetch a given resource'''
        print(request.args)
        if "due_date" in request.args:
            due_date = request.args.get('due_date')
            return jsonify(todo.api(todo.due_date, date=due_date))
        else:
            return jsonify({"error":"param due_date not provided"})


@ns.route('/over_due')
@ns.response(404, 'Opps! page not found')
class over_due(Resource):
    @ns.doc('over_due')
    def get(self):
        '''Fetch a given resource'''
        return jsonify(todo.api(todo.overdue))


@ns.route('/finished')
@ns.response(404, 'Opps! page not found')
class finished(Resource):
    @ns.doc('finished')
    def get(self):
        '''Fetch a given resource'''
        return jsonify(todo.api(todo.finished))


if __name__ == "__main__":
    todo = Todo()
    user = users()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)

