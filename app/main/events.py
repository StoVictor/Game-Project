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
    print('(DISCONNECT) PLAYER HAD EXIT ROOM')
    print(session['reload'])
    id = session['room_id']
    db = get_db()
    print('(DISCONNECT) DELETE PLAYER ID FROM PLAYING TABLE')
    db.execute('DELETE FROM playing WHERE id=?', (session['pers_id'], )) 
    num_of_players = db.execute('select engaged_place from room where id=?', (id, )).fetchone()[0]
    print('(DISCONNECT) DECIDE WHAT TO DO UPON NUM OF PLAYERS')
    if num_of_players == 1:
        print('(DISCONNECT) DELETE ROOM')
        db.execute('DELETE FROM room WHERE id=?', (session['room_id'], ))
    else:
        print('(DISCONNECT) DECREASE AMOUNT OF PLAYERS')
        db.execute('update room set engaged_place = ? where id=?', (num_of_players-1, id, ))
    db.commit()
    db.close()
    print('(DISCONNECT) END UP DEAL WITH DB')
    print('(DISCONNECT) SEND user_leave EVENT')
    emit('user_leave', str(session['username']) + ' has leaved the room', room=id)
    print('(DISCONNECT) USE leave_room')
    leave_room(id)

@socketio.on('connect')
def hanle_connect_event():
    print('(CONNECT) PLAYER HAD CONNECTED TO ROOM')

@socketio.on('join')
def handle_join_event(id):
        print('(JOIN) PLAYER HAD JOINED ROOM')
        join_room(id) 
        emit('user_enter', str(session['username']) + ' has entered the room', room=id)
