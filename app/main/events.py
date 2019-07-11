from flask import request, session, redirect
from flask_socketio import emit, join_room, leave_room, rooms, disconnect
from .. import socketio
from app.db import get_db

@socketio.on('message')
def handle_my_event(arg):
    print('Hi: ' + str(request.sid))
    return request.sid 

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    id = session['room_id']
    db = get_db()
    db.execute('DELETE FROM playing WHERE id=?', (session['pers_id'], )) 
    num_of_players = int(db.execute('select engaged_place from room where id=?', (id, )).fetchone()[0])
    if num_of_players == 1:
        db.execute('DELETE FROM room WHERE id=?', (session['room_id'], ))
    else:
        db.execute('update room set engaged_place = ? where id=?', (num_of_players-1, id, ))
    db.commit()
    db.close()
    emit('user_leave', str(session['username']) + ' has leaved the room', room=id)
    leave_room(id)

@socketio.on('connect')
def hanle_connect_event():
    print(str(request.sid))

@socketio.on('join')
def handle_join_event(id):
        print('Join')
        join_room(id) 
        emit('user_enter', str(session['username']) + ' has entered the room', room=id)


