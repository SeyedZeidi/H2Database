#PT2, web application.
#Authors: Seyed Saqlain Zeidi en Valentijn Stokkermans
#Date: 4-4-2021
#This is a chat application made with the Flask framework.
#draai onder python3.7.3

import os
import time
from flask import Flask, render_template, redirect, request, flash, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Lock
import json

async_mode = None

#app initialization
app = Flask(__name__)

app.config['SECRET_KEY'] = '1fcd0333d5a84f2bbbf2834461e653a2' #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #relative database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#socketio initialization
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()
db = SQLAlchemy(app)    #database intialization
login_manager = LoginManager(app)       
login_manager.init_app(app)

active_users = []   #variable for the active users list

#database class for users
class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        #username and password cant be empty
        #username has to be unique
        username = db.Column(db.String(20), unique=True, nullable=False)
        password = db.Column(db.String(60), nullable=False)

#database class for rooms
class Room(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        #room_name has to be unique and cant be empty
        #room_users cant be empty.
        room_name = db.Column(db.String(30), nullable=False)
        is_group = db.Column(db.Boolean, nullable=True)

#database class for chat history
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amessage = db.Column(db.String(1000), nullable=False)
    room = db.Column(db.Integer, db.ForeignKey(Room.id, ondelete = 'CASCADE'), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)


class Is_in(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)

#get id for user from database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#maak een room voor een op een chats
def make_room(username):
    partner = User.query.filter_by(username=username).first()
    user1 = db.session.query(Is_in).filter_by(user=partner.id).all()
    user2 = db.session.query(Is_in).filter_by(user=current_user.id).all()
    for room1 in user1:
        for room2 in user2:
            if( room1.room == room2.room ): #check of de room al bestaat
                room = Room.query.get(room1.room)
                if(room.is_group == False):
                    return room.id #als hij al bestaat return het id van deze room

    room_name = partner.username + current_user.username

    try:
        new_room = Room(room_name=room_name, is_group=False ) #crear nieuwe room
        db.session.add(new_room)
        db.session.commit()
        user5 = Is_in(user=partner.id, room=new_room.id) 
        #crear nieuwe connectie tussen user en nieuwe room
        db.session.add(user5)
        db.session.commit()
        user9 = Is_in(user=current_user.id, room=new_room.id) 
        #crear nieuwe connectie tussen andere user en nieuwe room
        db.session.add(user9)
        db.session.commit()
        
    except:
        print('komt het door try?')

        return 'error' #internal error
        
    return new_room.id

#maak een groep chat room
def make_group(members, room_name):
    if (len(members) >= 3): # check voor tenminste 3 members
        new_room = Room(room_name=rome_name, is_group=True )
        for member in members:
            add_member(member, new_room.id) #voeg user toe
        return new_room.id
    return 'error'

#voegt de members van een groeps chat toe aan de groep
def add_member(member, roomid):
        user = Is_in(user=member.id, room=new_room.id)
        #crear nieuwe connectie tussen user en nieuwe room
        db.session.add(user)
        db.session.commit()

#create a user (sign up)
def add_user(username, password):
    #check if the username exists in database
    user = User.query.filter_by(username=username).first()
    if user:
        return False #If a user already exists, return False.
    if len(password) < 8 or len(password) > 40:
        return False #If a user already exists, return False.
    try:
        #generate a new user in the database and hash the password
        newuser = User(username=username, password=generate_password_hash(password, method='sha256')) 
        db.session.add(newuser)
        db.session.commit()
    except:
        return False #internal error
    return True

#check the password for login
def check_password(username, password):
    #check if the username exists in database
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    #check if the password is correct    
    if not check_password_hash(user.password, password):
        return False
    return True

#generate list with active users
def actieve_lijst():
    lijst = '<ul>'
    for i in active_users:
        lijst += '<li>' + i + '</li>'
    lijst += '</ul>'
    socketio.emit('actieve_lijst', lijst)

#main page of the web application
@app.route('/')
def index():
    #Checks if the user is in a session.
    #Automatically log out if the session didn't
    #end by closing the browser.
    if "user" in session:
        user = session["user"]
        return redirect('/logout')
    #otherwise it will go to index.html
    else:
        return render_template('index.html')

#route to login page
@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html', title='Login in')

#checks if the login credentials are in the database
@app.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username = username).first()
    realPass = check_password(username, password)
    if not realPass:
        flash("Wrong credentials")
        return redirect('/login') #user gets redirected to login page
                                  #if the credentials are wrong

    #if the credentials are correct, the user gets a unique session
    session["user"] = username
    login_user(user)
    #user gets added into the list of active users
    active_users.append(current_user.username) 
    actieve_lijst()
    return redirect('/users') #redirects to the chat page

#route for sign up page
@app.route('/signup', methods=['GET'])
def get_signup():
    return render_template('signup.html', title='Sign up')
        
#users can create a new account        
@app.route('/signup', methods=['POST'])
def post_signup():
    #username has to be unique
    username = request.form['username']
    password = request.form['password']
    if not add_user(username, password):
        flash('Username already exists')
        return redirect('/signup')
    #if all requirements are met, the account is created
    flash('Account created successfully')
    return redirect('/login')

#user can log out at any time
@app.route('/logout')
def logout():
    logout_user()
    #session will expire if user logs out
    session.pop("user", None)
    #user gets redirected to the index.html page
    return redirect('/')

#route for the chat page
@app.route('/users', methods=['GET', 'POST'])
#user can't access page without being in a session
@login_required
def users():
    print(active_users)
    if not current_user.is_authenticated:
        return redirect('/login')
    #chat history is called
    amessages = History.query.all()
    return render_template('users.html', active_users=active_users ,username=current_user.username, sync_mode=socketio.async_mode, amessages = amessages) 

#rout to try and make a room between 2 persons
@app.route('/gme/<username>', methods=['GET'])
def gme(username):
    soos = make_room(username)
    if (soos == 'error'):
        return redirect ('/users')
    return redirect('/room/'+str(soos))

#route to the chat room 
@app.route('/room/<roomid>', methods=['GET'])
def room(roomid):
        user_rooms = db.session.query(Is_in).filter_by(user=current_user.id).all()
        
        for room in user_rooms:
            if (room.room == int(roomid)):
                amessages = db.session.query(History).filter_by(room=roomid).all()
                return render_template('chat.html', roomid=roomid, amessages=amessages)
        return redirect('/users')   

#route to create a room template
@app.route('/create_room', methods=['GET'])
def create_room():
    return render_template('create_room.html')

#route to create a room
@app.route('/create_room', methods=['POST'])
def create_room_post(members, room_name):
    roomid = make_group(members, room_name)
    return redirect('/room/'+str(roomid))

#socket for disconnection
@socketio.on('disconnect')
def disconnect_user():
    #user gets removed from the active users list
    active_users.remove(current_user.username)
    actieve_lijst()
    logout_user()
    #session expires
    session.pop('user', None)

#socket from incoming messages
@socketio.on('inkomend-bericht')
def on_message(data):
    message = data['message']
    username = data['username']
    room = data['room']
    time_stamp = time.strftime('%H:%M', time.localtime())   #finding the time
    bericht = {"username": username, "message": message, "time_stamp": time_stamp}
    #complete message (content, sender and time of message) is added to the database
    amessage = History(amessage = data['message'], room = data['room'], sender = data['username'], time = time_stamp)
    db.session.add(amessage)
    db.session.commit()
    data.append(timestamp: time_stamp)
    #message is sent to front end
    socketio.emit('receive_message', bericht, room = data['room'])

#socket for joining a room
@socketio.on('join_room')
def on_join(data):
    join_room(data['room'])

#run the app
if __name__ == "__main__":
        socketio.run(app, debug=True)
