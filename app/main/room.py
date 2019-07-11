def create_room(id, name, players_amount, room_type, db):
    players_amount = int(players_amount)

    if room_type == 'pub':
        room_type = 1 
    else:
        room_type = 0 
    db.execute(
        'INSERT INTO room (id, room_name, room_size, room_type, engaged_place, playing_status) VALUES (?, ?, ?, ?, ?, ?)', (str(id), str(name), int(players_amount), int(room_type), 0, 0))
    db.commit()
    
