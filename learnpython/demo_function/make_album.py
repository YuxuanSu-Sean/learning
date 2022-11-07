def make_album(singer_name, album_name, song_num = ''):
    if song_num:
        f_name = {'singer_name': singer_name, 'album_name': album_name, 'song_number': song_num}
    else:
        f_name = {'singer_name': singer_name, 'album_name': album_name}

    return f_name

print(make_album('jay', 'qilixiang'))
