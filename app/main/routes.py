from flask import session, redirect, url_for, render_template, request, abort, Response
from flask_socketio import join_room, leave_room
from . import main
import json
from .forms import NameForm, CreateRoomForm, RoomCodeEnterForm, RoomLeaveForm
import uuid
from .room import create_room
from app.db import get_db
from flask_socketio import leave_room 
@main.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    print(request)
    pub_rooms = db.execute('SELECT * FROM room where room_type=1').fetchall()
    name_form = NameForm(prefix='username')
    create_room_form = CreateRoomForm(prefix='create_room')
    room_code_enter_form = RoomCodeEnterForm(prefix='enter_code')
    if 'pers_id' not in session:
        session['pers_id'] = str(uuid.uuid4())
    if name_form.validate_on_submit() and name_form.submit.data:
        session['username'] = name_form.name.data
    if 'username' not in session:
        session['username'] = 'Undifiend'
    elif create_room_form.validate_on_submit() and create_room_form.submit.data:
        id = uuid.uuid4()
        create_room(id, create_room_form.name.data, create_room_form.players_amount.data, create_room_form.room_type.data, db)
        return redirect(url_for('main.room') + '?id=' + str(id))
    elif room_code_enter_form.validate_on_submit():
        return 'Hello World'
    return render_template('index.html', **{'name_form':name_form, 
                                            'create_room_form':create_room_form,
                                            'room_code_enter_form':room_code_enter_form,
                                            'public_rooms': pub_rooms,
                                            'kek': json.dumps(4)
                            }) 

@main.route('/room', methods=['GET', 'POST'])
def room():
    print("(ROUTE) OPEN ROOM")
    room_leave_form = RoomLeaveForm()
    db = get_db()
    id = request.args.get('id')
    #playing table probably not need anymore
    playing = db.execute('SELECT * from playing where id=?', (session['pers_id'], )).fetchall()
    #print(playing)
    print('(ROUTE) GET FROM DB IF PLAYER IS ALREADY PLAY')
    #next line should be in dissconect
    room = db.execute('SELECT engaged_place, room_size, playing_status from room where id=?', (id, )).fetchall()
    print('(ROUTE) GET THE ROOM INFO FROM DB')
    #change all checks 
    if playing != []:
        #player already plays
        if 'room_id' in session:
            if session['room_id'] == id:
                session['reload'] = 'yes'
                return render_template('room.html', room_id = json.dumps(request.args['id']), room_leave_form=room_leave_form) 
        return abort(404)
    if 'room_id' not in session:
        session['room_id'] = id
    if room == []:
        #room does not exist
        return abort(404, 'room does not exist')
    room = room[0]
    if room['playing_status'] == 1:
        #players alrady play
        return abort(404)
    if room['engaged_place'] == room['room_size']:
        #room is full
        return abort(404)
    print('(ROUTE) PASS ALL TESTS TO JOIN ROOM')
    if  True:
        print('(ROUTE) START UPDATE DB')
        num_of_players = int(db.execute('select engaged_place from room where id=?', (id, )).fetchone()[0])+1
        db.execute('update room set engaged_place = ? where id=?', (num_of_players, id, ))
        db.execute('INSERT INTO playing (id) VALUES (?)', (session['pers_id'], ))
        db.commit()
        print('(ROUTE) END UPDATE DB')
        session['room_id'] = id 
        return render_template('room.html', room_id = json.dumps(request.args['id']), room_leave_form=room_leave_form) 

