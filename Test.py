from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
#from sqlalchemy.orm import joinedload
#from sqlalchemy.orm import sessionmaker

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/alchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
load_dotenv('.env')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adminname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

@app.route('/')
def dummy_api():
    return "Welcome To Flask-SqlAlchemy"

@app.route('/input', methods=['GET'])
def insert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        user_name=data['username']
        print(user_name)
        user_email=data['email']
        print(user_email)
        user=User(username=user_name, email=user_email)
        #print(user)
        db.session.add(user)
        db.session.commit()         
    return "insert data"


@app.route('/fetch', methods=['GET'])
def fetch():
    #return "hi"
    val=[]
    #value={}
    users=User.query.all()
    for user in users:
        dic={}
        id=user.id
        name=user.username
        mail=user.email
        #print(id," ",name," ",mail)
        dic=id,name,mail
        #print("ss",dic)
        val.append(dic)
    print("\n")
        #print(val)
    return jsonify(val)
    #for i in val:        
    #return "ok  "

@app.route('/update', methods=['PUT'])
def update():
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        data = request.get_json()
        u_id=data['id']
        u_name=data['username']
        u_mail=data['email']
        print(u_id)
        user = User.query.get(u_id)
        user.username = u_name
        user.email= u_mail
        db.session.commit() 
        return "update Sucessful"

@app.route('/delt', methods=['DELETE'])
def delt():
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        data = request.get_json()
        u_id=data['id']
        print(u_id)
        user=User.query.get(u_id)
        db.session.delete(user)
        db.session.commit()
        return "delete successful"


@app.route('/admininput', methods=['POST'])
def admin():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        admin_name=data['adminname']
        print(admin_name)
        admin_email=data['email']
        print(admin_email)
        admin=Admin(adminname=admin_name, email=admin_email)
        #print(user)
        db.session.add(admin)
        db.session.commit()         
    return "admin data successfully inserted"

'''
@app.route('/injoin', methods=['GET'])
def injoin():
    Session = sessionmaker()
    session = Session()
    query = session.query(User).join(Admin, User.id==Admin.id)    
    print("My Join Query: ",str(query))
    for a in query.all():
        print (a.id, a.username, a.email)
    return "ok"

'''

if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port="5001")
