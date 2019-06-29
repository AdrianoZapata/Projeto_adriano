from app import app
from app.models.tables import User
from bottle import template, static_file, request, redirect

#static routes
@app.get('/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='app/static/css')

@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='app/static/js')

@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='app/static/img')

@app.get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
	return static_file(filename, root='app/static/fonts')

@app.route('/') # @get('/')
def login():
	return template('login', sucesso=True)

@app.route('/cadastro')
def cadastro():
	return template('cadastro', existe_username=False)

@app.route('/cadastro', method='POST')
def acao_cadastro(db):
	username = request.forms.get('username')
	password = request.forms.get('password')
	try:
		db.query(User).filter(User.username == username).one()
		existe_username = True
	except:
		existe_username = False
	if not existe_username:
		new_user = User(username, password)
		db.add(new_user)
		return redirect('/usuarios')
	return template('cadastro', existe_username=True)
	    
@app.route('/', method='POST') #@post('/')
def acao_login(db, session):
	username = request.forms.get('username')
	password = request.forms.get('password')
	result = db.query(User).filter((User.username == username) & (User.password == password)).all()
	sucesso = False if not result else True 
	if result:
		session['name'] = username
		return redirect('/usuarios')    
	return template('login', sucesso=False)

@app.route('/usuarios')
def usuarios(db, session):
	if session.get('name'):
		acesso = True
	else:
		acesso = False
	usuarios = db.query(User).all()
	return template('lista_usuarios', usuarios=usuarios, acesso=acesso)

@app.error(404)
def error404(error):
	return template('pagina404')
