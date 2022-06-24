#from calendar import c
#import re
#from urllib.request import HTTPBasicAuthHandler
from lib2to3.pgen2 import token
import re
from idna import valid_contextj
import jwt
from datetime import datetime,timedelta
from flask import Flask, jsonify, make_response, request 
import os
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
from dotenv import load_dotenv
import mysql.connector
import pytz
#from requests import session
#from flask_restful import Api,fields,Resource

app=Flask(__name__)

#auth= HTTPBasicAuth()

@app.route('/')
def dummy_api():
    return "Welcome To API"

load_dotenv('.env')
#print("Subject : ",os.environ.get('SUBJECT'))
#print("Subject : ",os.environ.get('NAME')) 
#print("Subject : ",os.environ.get('MSG')) 
#print("Subject : ",os.environ.get('PSWD'))     
#print("subject : ",os.environ.get('subject')) 
'''
@app.route('/createtoken', methods=['GET'])
def createtoken():
    #return("Subject : "+os.environ.get('SUBJECT'))    
    SECRET_KEY = os.environ.get('PSWD')
     
    json_data = {
         "iss": os.environ.get('NAME'),
         "sub": os.environ.get('SUBJECT'),
         "message": os.environ.get('MSG'),
         "date": str(datetime.datetime.now())
    }
    encode_data = jwt.encode(payload=json_data, key=SECRET_KEY, algorithm="HS256")
    return encode_data 

#createtoken()
'''
#print("TOKEN : ",os.environ.get('TID'))    
'''
@app.route('/decodetoken', methods=['GET'])
def decodetoken():
    SECRET_KEY = os.environ.get('PASSWORD')
    token = os.environ.get('TID')
    try:
        decode_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms="HS256")
        return decode_data
    except Exception as e:
        message = f"Token is invalid --> {e}"
        return ({"message": message})
#decodetoken()
'''    

@app.route('/showdata', methods=['GET'])
def showdata():
    #return(SqlConnection.showdata()) #ERROR
    try:
        #load_dotenv('.env')
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute('select * from users')
            record = cursor.fetchall() 
            #return "hello ",record
            a=[]
            for i in record:
                a.append(i)
            return jsonify((a))
    except Exception as e:
        return("Error while connecting to MySQL",e)
    

@app.route('/insert', methods=['POST'])
def insertdata():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                #cursor.execute('INSERT INTO customers (name, address) VALUES (%s, %s)')
                #sql = "INSERT INTO users (usersId, usersName, usersEmail, usersPassword) VALUES (%s, %s, %s, %s)"
                #val = ("1", "Himadri", "him@gmail.com", "123")
                #cursor.execute(sql, val)
                content_type = request.headers.get('Content-Type')
                if (content_type == 'application/json'):
                    data = request.get_json()
                    usersId=data['usersId'] 
                    usersName=data['usersName']
                    usersEmail=data['usersEmail'] 
                    usersPassword=data['usersPassword']
                    #print(usersId,usersName)
                    sql = "INSERT INTO users (usersId, usersName, usersEmail, usersPassword) VALUES (%s, %s, %s, %s)"
                    val=(usersId,usersName,usersEmail,usersPassword)
                    cursor.execute(sql, val)
                    connection.commit()
                return jsonify({'message' : 'New user created!'})   
        else:
            return 'Content-Type not supported!'
    except Exception as e:
        print("error",e)
        return '404'

@app.route('/showdataid', methods=['POST'])
def showdataid():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            content_type = request.headers.get('Content-Type')
            if(content_type == 'application/json'):
                data = request.get_json()
                usersId=data['usersId']        
                sql="select * from company.users where usersId={};".format(usersId)
                #sql="select * from users"
                cursor.execute(sql)
                row=cursor.fetchall()
                for i in row:
                    return jsonify(i)
                #return jsonify({'user' : {}})   
                
        else:
            return 'Content-Type not supported!'
    except Exception as e:
        print("error",e)
        return make_response('404')


@app.route('/updata', methods=['PUT'])
def updata():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            #cur_a = connection.cursor(buffered=True)
            content_type = request.headers.get('Content-Type')
            if(content_type == 'application/json'):
                data = request.get_json()
                usersId=data['usersId']        
                sql="select * from company.users where usersId={};".format(usersId)
                #return sql
                cursor.execute(sql)
                usersName=data['usersName']
                usersEmail=data['usersEmail']
                usersPassword=data['usersPassword']
                sql_2="update company.users set usersName={}, usersEmail={}, usersPassword={} where usersId={};".format("'"+usersName+"'","'"+usersEmail+"'","'"+usersPassword+"'",usersId)
                #print(sql_2)
                cursor.execute(sql_2)
                connection.commit()
                return jsonify({'message' : 'Successfully updated'})
                #return jsonify({'user' : {}})   
        else:
            return 'Content-Type not supported!'
    except Exception as e:
        print("error: ",e)
        return make_response('404')


@app.route('/deldata', methods=['DELETE'])
def deldata():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            content_type = request.headers.get('Content-Type')
            if(content_type == 'application/json'):
                data = request.get_json()
                usersId=data['usersId']        
                sql="select * from company.users where usersId={};".format(usersId)
                #return sql
                cursor.execute(sql)
                #usersName=data['usersName']
                #usersEmail=data['usersEmail']
                #usersPassword=data['usersPassword']
                #print ("name: ",usersName)
                sql_2="delete from company.users where usersId={};".format(usersId)
                print(sql_2)
                cursor.execute(sql_2)
                connection.commit()
                return jsonify({'message' : 'Successfully Deleted'})
                #return jsonify({'user' : {}})   
        else:
            return 'Content-Type not supported!'
    except Exception as e:
        print("error: ",e)
        return make_response('404 id not found')

@app.route('/tokcre', methods=['GET'])
def tokcre():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            content_type = request.headers.get('Content-Type')
            if(content_type == 'application/json'):
                data = request.get_json()
                usersId=data['usersId']
                usersPassword=data['usersPassword']
                SECRET_KEY = usersPassword
                sql="select * from company.users where usersId={} and usersPassword={};".format(usersId,"'"+usersPassword+"'")
                cursor.execute(sql)
                json_data = {
                    "id": usersId,
                    "pass":usersPassword,
                    "date": str(datetime.datetime.now())
                }
                encode_data = jwt.encode(payload=json_data, key=SECRET_KEY, algorithm="HS256")
                return encode_data

            token =encode_data
            SECRET_KEY = usersPassword
            decode_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms="HS256")
            #return decode_data
        
                #return("Subject : "+os.environ.get('SUBJECT'))    
    except Exception as e:
        print("Error: ",e)
        return make_response('Un-Successful')

@app.route('/tokdeco', methods=['GET'])
def tokdeco():
    try:
        #connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        #if connection.is_connected():
        #    db_Info = connection.get_server_info()
        #    print("Connected to MySQL Server version ", db_Info)
        #    cursor = connection.cursor()
        #    content_type = request.headers.get('Content-Type')
        #    if(content_type == 'application/json'):
        #        data = request.get_json()
        #        usersId=data['usersId']
        #        usersPassword=data['usersPassword']
        #        SECRET_KEY = usersPassword
        #        sql="select * from company.users where usersId={} and usersPassword={};".format(usersId,"'"+usersPassword+"'")
        #        cursor.execute(sql)
        #        json_data = {
        #            "id": usersId,
        #            "pass":usersPassword,
        #            "date": str(datetime.datetime.now())
        #        }
        
        token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjMiLCJwYXNzIjoiYWJjMTIiLCJkYXRlIjoiMjAyMi0wNi0wNiAxNjoyNjo1MS45MTgwNTkifQ.8FG44FI7QMd7zOAEyn3-Vz1B1mwxuAXqm2qitkht6t4"
        SECRET_KEY = "abc12"
        decode_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms="HS256")
        return decode_data
                    #return("Subject : "+os.environ.get('SUBJECT'))    
    except Exception as e:
        message = f"Token is invalid --> {e}"
        return ({"message": message})
        

@app.route('/login', methods =['POST'])
def login():
    try:
        auth = request.authorization
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            try:
                #db_Info = connection.get_server_info()
                #print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()                
                sql="select usersId,usersPassword from company.users where usersId={} and usersPassword={};".format(auth.username,"'"+auth.password+"'")
                cursor.execute(sql)
                record = cursor.fetchone()
                if record:
                    SECRET_KEY="akash"
                    now=datetime.now() 
                    print("now: ",now)
                    d_utc = now.astimezone(pytz.UTC)
                    print('Current time in UTC Time-zone: ', d_utc)
                    delta=datetime.now()+timedelta(minutes=20)
                    dt_utc = delta.astimezone(pytz.UTC)
                    print('Current time in UTC Time-zone: ', dt_utc)
                    json_data = {
                        "id": auth.username,
                        "pass":auth.password,
                        "iat":d_utc,
                        "exp": dt_utc
                    }
                    encode_data = jwt.encode(json_data, key=SECRET_KEY, algorithm="HS256")
                    return jsonify({'msg': encode_data})                    
                else:
                    return jsonify({"msg": "Check id and password carefully"})    
            except Exception as e:
                print("Error: ",e)
                return jsonify({"msg": "Check again"})
    except Exception as e:
        print("Error: ",e)
        return make_response("Error")

 
@app.route('/decode', methods =['GET'])
def decode():
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEiLCJwYXNzIjoiMTIzIiwiZGF0ZSI6IjIwMjItMDYtMDggMTc6MjY6MTguMTYwNTA2In0.qkSXOlULUgQUZnUqOxVCFRPtQqVHxilKrDRjMq7ZOL8"
    SECRET_KEY = os.environ.get('SCKY')    
    try:    
        decode_data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        return jsonify(decode_data)
        
    except Exception as e:
        print("Error: ",e)
        return jsonify({"msg": "check again"})


@app.route('/authen', methods =['GET'])
def authen():
    headers = request.headers
    bearer = headers.get('Authorization')
    token_bearer = bearer.split()[1]
    SECRET_KEY = os.environ.get('SCKY')    
    try:
        if token_bearer:    
            decode_data = jwt.decode(token_bearer,SECRET_KEY,algorithms=['HS256'])
            print(decode_data)
            first_value = list(decode_data.items())[0][1]
            #print(first_value)
            now_time=list(decode_data.items())[2][1]
            print("current: ",now_time)
            dt_now_obj = datetime.fromtimestamp(now_time)
            print("cure time:",dt_now_obj)
            dtt_utc = dt_now_obj.astimezone(pytz.UTC)
            print('Current time in UTC Time-zone: ', dtt_utc)
            ch_ti=dtt_utc+timedelta(seconds=30)
            #print("chek add time: ",ch_ti)        
            #print("ex: ",exp_time)
            #dt_obj = datetime.fromtimestamp(exp_time)
            #print("exp time:",dt_obj)
            #exp_utc = dt_obj.astimezone(pytz.UTC)
            #print('Exp time in UTC Time-zone: ', exp_utc)        
            #min=exp_utc-dtt_utc
            #print("min: ",min)
            if str(datetime.now().astimezone(pytz.UTC))>str(ch_ti):
                return "Token Expired"  
            else:
                connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
                if connection.is_connected():
                    try:
                        cursor = connection.cursor()                
                        sql="select * from company.users where usersId={}".format(first_value)
                        #print(sql)
                        cursor.execute(sql)
                        record = cursor.fetchone()
                        if record:
                            return jsonify({"msg": "Token is valid"},{"user": decode_data}) 
                    except Exception as e:
                        print("Error: ",e)
                        return jsonify({"msg": "Invalid Token"})            
    except Exception as e:
        print("Error: ",e)
        return jsonify({"msg": "Check Again"})





if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0", port="5001")




























'''
@app.route('/login', methods=['POST'])
def login():
    try:
        connection = mysql.connector.connect(host=os.environ.get('HOS'), database=os.environ.get('DBS'), user=os.environ.get('ADM'), password=os.environ.get('PWOD'))
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)                
            sql="select usersId,usersPassword from company.users;"
            cursor.execute(sql)
            record = cursor.fetchall()
            a=[]
            for i in record:
                a.append(i)
            #print(a)
            auth = request.authorization
            #print("check1: ",auth.username)
            #print("check2",auth.password)
            for i in a:
                a=i[0]
                b=i[1]
                print("check3: ",a)
                print("check4",b)
                
            #try:
            
                #    print("hello")
                #    return "hi"
                #return "hii"
            if(auth.username==a):
                print("hello", auth.username)
                #    return "hi"
            #except Exception as e:
                #print("Error: ",e)
                #return make_response("Wrong")                   
    except Exception as e:
        print("Error: ",e)
        return make_response("Error")


'''

#@app.route('/')