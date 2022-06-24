from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
#from sqlalchemy.orm import joinedload
#from sqlalchemy.orm import sessionmaker

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
load_dotenv('.env')

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    adminName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

@app.route('/')
def dummy_api():
    return "Welcome To Flask-SqlAlchemy"

@app.route('/input', methods=['POST'])
def insert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        user_name=data['userName']
        print(user_name)
        user_email=data['email']
        print(user_email)
        user=User(userName=user_name, email=user_email)
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
        id=user.uid
        name=user.userName
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
        u_id=data['uid']
        u_name=data['userName']
        u_mail=data['email']
        print(u_id)
        user = User.query.get(u_id)
        user.userName = u_name
        user.email= u_mail
        db.session.commit() 
        return "update Sucessful"

@app.route('/delt', methods=['DELETE'])
def delt():
    content_type = request.headers.get('Content-Type')
    if(content_type == 'application/json'):
        data = request.get_json()
        u_id=data['uid']
        print(u_id)
        user=User.query.get(u_id)
        db.session.delete(user)
        db.session.commit()
        return "delete successful"


@app.route('/adin', methods=['POST'])
def admin():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        u_id=data['uid']
        admin_name=data['adminName']
        print(admin_name)
        admin_email=data['email']
        print(admin_email)
        try:
            if User.query.filter_by(uid=u_id).first():                    
                admin=Admin(uid=u_id, adminName=admin_name, email=admin_email)
            #print(user)
                db.session.add(admin)
                db.session.commit()         
                return "admin data successfully inserted"
            return "user not exits"
        except Exception as e:
            print("error",e)
            return make_response('Check Again')

@app.route('/lejo', methods=['GET'])
def lejo():
    qu=db.session.query(User.uid,User.userName,User.email,Admin.email).join(Admin,Admin.aid==User.uid,isouter=True).all()
    #print(qu)
    val=[]
    for ans in qu:
        #print(ans)
        dic={}
        id=ans.uid
        name=ans.userName
        mail=ans.email
        #print(id," ",name," ",mail)
        dic=id,name,mail
        val.append(dic) 
    return jsonify(val)


@app.route('/rijo', methods=['GET'])
def rijo():
    qu=db.session.query(User.uid,User.userName,User.email,Admin.email).join(Admin,Admin.aid==User.uid,isouter=False).all()
    #print(qu)
    val=[]
    for ans in qu:
        #print(ans)
        dic={}
        id=ans.uid
        name=ans.userName
        mail=ans.email
        #print(id," ",name," ",mail)
        dic=id,name,mail
        val.append(dic) 
    return jsonify(val)


@app.route('/outjo', methods=['GET'])
def outjo():
    qu=db.session.query(User.userName, Admin.email).outerjoin(Admin, User.userName == Admin.adminName).all()
    print(qu)
    val=[]
    #return "kk"
    for ans in qu:
        print(ans)
        dic={}
        name=ans.userName
        mail=ans.email    
        dic=name,mail
        val.append(dic) 
    return jsonify(val)
    
@app.route('/jo', methods=['GET'])
def jo():
    qu=db.session.query(Admin).filter(User.userName == Admin.adminName)
    #qu=db.session.query(Admin).filter(User.uid == Admin.aid)
    #print(qu)
    val=[]
    #return "kk"
    for ans in qu:
        print(ans)
        dic={}
        a_id="aid: "+str(ans.aid)
        u_id="uid: "+str(ans.uid)
        name="admin name: "+ans.adminName
        mail="admin email: "+ans.email    
        dic=a_id,u_id,name,mail
        val.append(dic) 
    return jsonify(val)
    #return "ok"

if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port="5001")
