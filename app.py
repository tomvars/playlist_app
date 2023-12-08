from flask import Flask, request, jsonify
import sqlite3

app = Flask("Playlist API")

@app.route('/', methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route('/student_list', methods=["GET"])
def students():
    return app.send_static_file("students.html")


@app.route('/add_song_to_playlist', methods=['POST'])
def add_song_to_playlist():
    data = request.json
    # data = {"playlist_id": 5, "track_id": 3000}
    playlist_id = data['playlist_id']
    track_id = data['track_id']

    with sqlite3.connect('Chinook_Sqlite.sqlite') as conn:
        cursor = conn.cursor()
        # Check if playlist exists
        playlist = cursor.execute('SELECT * FROM Playlist WHERE PlaylistId = ?', (playlist_id,)).fetchone()
        if not playlist:
            cursor.close()
            return jsonify({'error': 'Playlist not found'}), 404

        # Check if track exists
        track = cursor.execute('SELECT * FROM Track WHERE TrackId = ?', (track_id,)).fetchone()
        if not track:
            cursor.close()
            return jsonify({'error': 'Track not found'}), 404

        # Add song to playlist
        cursor.execute('INSERT INTO PlaylistTrack (PlaylistId, TrackId) VALUES (?, ?)', (playlist_id, track_id))
        conn.commit()
    return jsonify({'message': 'Song added to playlist'}), 200

# app.route(add_song_to_playlist, '/add_song_to_playlist', methods=['POST'])

@app.route('/playlist/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    with sqlite3.connect('Chinook_Sqlite.sqlite') as conn:
        cursor = conn.cursor()
        # Check if playlist exists
        playlist = cursor.execute('SELECT * FROM Playlist WHERE PlaylistId = ?', (playlist_id,)).fetchone()
        if not playlist:
            return jsonify({'error': 'Playlist not found'}), 404

        # Fetch all tracks in the playlist
        cursor.execute('SELECT Track.TrackId, Track.Name, Track.Composer FROM PlaylistTrack INNER JOIN Track ON PlaylistTrack.TrackId = Track.TrackId WHERE PlaylistTrack.PlaylistId = ?', (playlist_id,))
        tracks = cursor.fetchall()

        # Format the result as a list of dictionaries
        track_list = [{'track_id': track[0], 'track_name': track[1], 'track_composer': track[2]} for track in tracks]
    
    return jsonify(track_list), 200



if __name__ == '__main__':
    app.run(debug=True)