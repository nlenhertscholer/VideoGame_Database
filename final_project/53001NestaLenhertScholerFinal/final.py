from bottle import template, route, run, error, post, get, request
from datetime import datetime, timedelta
import psycopg2
from connection import *


# ---------------------- Helper Functions ----------------------------


# Quick function to validate form input
def check_input(value, comparator):
    if value != comparator:
        return value
    else:
        return ""


def connect():
    conn = psycopg2.connect(dbname=database, user=user,
                            password=password, host=url)
    return conn


# Function to get all of the available genres
def search_genres():
    sql = "SELECT DISTINCT genre FROM genre;"
    conn = None
    try:
        conn = connect()
        with conn.cursor() as cur:
            cur.execute(sql)
            genres = cur.fetchall()
    finally:
        if conn:
            conn.close()

    return genres


def get_genres():
    genres_raw = search_genres()
    genres = []
    for data in genres_raw:
        genres.append(data[0])

    return genres


# Function to build sql string
def create_query(name, date, genre):
    use_genre = False
    if genre != "":
        sql = "SELECT game_id, name, rating, convert_date(first_rel_date), genre FROM game NATURAL JOIN genre "
        use_genre = True
    else:
        sql = "SELECT game_id, name, rating, convert_date(first_rel_date) FROM game "

    # Get correct search parameters
    if name != "" or date != "" or genre != "":
        if name != "":
            name = '%' + name + '%'
        full_check = "name iLIKE %s AND convert_date(first_rel_date) = %s AND genre = %s"
        full_check = full_check.split(' AND ')
        pairing = {name: full_check[0], date: full_check[1], genre: full_check[2]}
        valid_pairs = {key: value for key, value in pairing.items() if key != ""}
        params = [key for key in pairing.keys() if key != ""]

        # build back string
        sql += "WHERE "
        for key, value in valid_pairs.items():
            sql += value + " AND "

        # Remove trailing AND
        if 'AND' in sql:
            sql = sql[:-4]
    else:
        params = ()

    sql += "ORDER BY game_id ASC LIMIT 50;"

    return sql, params


# Function to get game results from database
def search_game(gid=None, name="", date="", genre=""):
    if gid is None:
        query, params = create_query(name, date, genre)
    else:
        query = "SELECT * FROM game LEFT OUTER JOIN genre USING(game_id) where game_id = %s"
        params = (gid,)

    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            game_list = cur.fetchall()
    finally:
        conn.close()

    return game_list


# Function to grab the list of games from the
def get_game_names(game_tuples):
    names = {}
    for data in game_tuples:
        game_id = data[0]
        game_name = data[1]
        if game_name not in names.values():
            names[game_id] = game_name

    return names


# Function to update the database after View/Edit of a game
def update_db(game_name, date, genre, gid):
    game = search_game(gid)[0]
    old_name = game[1]
    old_date_ts = game[3]
    if old_date_ts:
        old_date = datetime.utcfromtimestamp(old_date_ts)
        old_date = old_date.strftime('%Y-%m-%d')
    else:
        old_date = None
    old_genre = game[4]

    if game_name == old_name and date == old_date and genre == old_genre:
        # nothing was changed
        return False

    conn = None
    date_ts = int(datetime.strptime(date, "%Y-%m-%d").timestamp())

    updated = False
    try:
        conn = connect()
        cur = conn.cursor()

        if game_name != old_name or date != old_date:
            # Game Table update
            query = '''UPDATE game SET name = %s, first_rel_date = %s
                       WHERE game_id = %s;'''
            params = (game_name, date_ts, gid,)
            cur.execute(query, params)
        if genre is not None:
            # Genre Table update
            # First see if it's already in the database since multiple genres do exist
            query = '''SELECT * FROM genre WHERE game_id = %s;'''
            params = (gid,)
            cur.execute(query, params)
            pairings = cur.fetchall()
            new_pair = (genre, gid)

            if new_pair not in pairings:
                query = "INSERT INTO genre VALUES (%s, %s);"
                cur.execute(query, new_pair)
        conn.commit()
        updated = True
    except:
        if conn:
            conn.rollback()
        updated = None
    finally:
        if conn:
            conn.close()

    return updated


def get_platforms(gid):
    query = '''SELECT platform.name, abbreviation, generation, convert_date(first_rel_date)
               FROM platform NATURAL JOIN game_platform JOIN game USING(game_id)
               WHERE game_id = %s'''
    params = (gid,)
    platform_data = None

    conn = connect()
    try:
        curr = conn.cursor()
        curr.execute(query, params)
        platform_data = curr.fetchall()
    except:
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

    return platform_data


def get_all_platforms():
    query = "SELECT name FROM platform;"
    conn = connect()
    platforms = None
    try:
        curr = conn.cursor()
        curr.execute(query)
        platforms = curr.fetchall()
    except:
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    return platforms


def add_platform_to_db(platform, game_id):
    # Get the platform id
    updated = False
    query = "SELECT platform_id FROM platform WHERE name = %s"
    conn = connect()
    plat_id = None
    try:
        curr = conn.cursor()
        curr.execute(query, (platform,))
        plat_id = curr.fetchone()[0]
    except:
        if conn:
            conn.rollback()
        updated = None
    finally:
        if conn:
            conn.close()

    if plat_id and updated is not None:
        query = "INSERT INTO game_platform VALUES (%s, %s);"
        params = (plat_id, game_id)
        conn = connect()
        try:
            curr = conn.cursor()
            curr.execute(query, params)
            conn.commit()
            updated = True
        except:
            if conn:
                conn.rollback()
            updated = None
        finally:
            if conn:
                conn.close()
    return updated


def add_new_game(game_name, date, genre):
    query = '''SELECT MAX(game_id) FROM game;'''
    conn = connect()
    updated = False
    gid = None
    try:
        curr = conn.cursor()
        curr.execute(query)
        gid = curr.fetchone()[0] + 1
    except:
        if conn:
            conn.rollback()
        updated = None
    finally:
        if conn:
            conn.close()

    if gid:
        if date:
            date_ts = datetime.strptime(date, '%Y-%m-%d')
            date_ts = int(date_ts.timestamp())
        else:
            date_ts = None
        query = '''INSERT INTO game (game_id, name, first_rel_date) VALUES (%s, %s, %s)'''
        params = (gid, game_name, date_ts)

        conn = connect()
        try:
            curr = conn.cursor()
            curr.execute(query, params)
            conn.commit()
            updated = True
        except:
            if conn:
                conn.rollback()
            updated = None
        finally:
            if conn:
                conn.close()

        if updated is not None and genre is not None:
            # add genre
            query = "INSERT INTO genre VALUES (%s, %s)"
            params = (genre, gid)

            conn = connect()
            try:
                curr = conn.cursor()
                curr.execute(query, params)
                conn.commit()
                updated = True
            except:
                if conn:
                    conn.rollback()
                updated = None
            finally:
                if conn:
                    conn.close()

    return updated


# -------------------------- Bottle Webpage Functions -------------------


@get('/')
@get('/home')
def homepage(deleted=False):
    # Get game genres to display in list
    genres = get_genres()

    return template("home", genres=genres, deleted=deleted)


@post('/results')
def results():
    # Obtain search fields
    searchname = request.forms.get('game_name')
    date_string = request.forms.get('release_date')
    genre = request.forms.get('game_genre')

    # Validate searches
    game_name = check_input(searchname, "")
    genre = check_input(genre, "N/A")
    date = date_string
    if date != "":
        # Something is wrong with datetime so need to subtract a day to get the right search
        date = datetime.strptime(date_string, '%Y-%m-%d') - timedelta(days=1)

    # Get database results
    game_data = search_game(name=game_name, date=date, genre=genre)
    game_names = get_game_names(game_data)      # Get the game names along with primary keys
    sorted_data = sorted(game_names.items(), key=lambda val: val[1])

    return template("results", games=sorted_data, game_results=True)


@route('/newgame')
def add_game(empty=False, updated=False):
    genres = get_genres()
    return template("new_game", alter=False, genres=genres, empty=empty, updated=updated)


@post('/newgame')
def add_game_db():
    game_name = request.forms.get('new_game_name')

    if game_name == "":
        return add_game(empty=True)

    all_games = search_game(name=game_name)
    all_games_names = get_game_names(all_games)

    if game_name in all_games_names.values():
        return add_game(empty=False, updated=None)

    date = request.forms.get('init_release_date')
    genre = request.forms.get('new_game_genre')
    if genre == 'N/A':
        genre = None
    if date == '':
        date = None

    updated = add_new_game(game_name, date, genre)

    return add_game(empty=False, updated=updated)


@route('/game/<game_id:int>')
def alter_game(game_id, updated=False):
    game = search_game(game_id)[0]
    genres = get_genres()
    name = game[1]

    date_ts = game[3]    # In timestamp format, need to convert to YYYY-MM-DD
    if date_ts:
        date = datetime.utcfromtimestamp(date_ts)
        date = date.strftime('%Y-%m-%d')
    else:
        date = None

    main_genre = game[4]

    return template('new_game', alter=True, new_update=updated, genres=genres,
                    main_genre=main_genre, game_name=name, release_date=date, game_id=game_id)


@post('/game/<game_id:int>')
def alter_game_post(game_id):
    # Updated page after game has been updated
    new_name = request.forms.get("game_name")
    new_date = request.forms.get("init_rel_date")
    new_genre = request.forms.get("game_genre")

    # Process changes
    if new_genre == "N/A":
        new_genre = None
    updated = update_db(new_name, new_date, new_genre, game_id)

    return alter_game(game_id, updated)


@route('/delete/<game_id:int>')
def delete_game(game_id):
    query = '''DELETE FROM game WHERE game_id = %s;'''
    conn = connect()
    deleted = False
    try:
        cur = conn.cursor()
        cur.execute(query, (game_id,))
        conn.commit()
        deleted = True
    except:
        if conn:
            conn.rollback()
        deleted = None
    finally:
        if conn:
            conn.close()

    return homepage(deleted)


@route('/game/<game_id:int>/platforms')
def show_platforms(game_id):
    platforms = get_platforms(game_id)

    return template("results", platforms=platforms, game_results=False)


@route('/game/<game_id:int>/newplatform')
def add_platform(game_id, updated=False):
    game = search_game(game_id)[0]
    game_name = game[1]
    game_platforms_raw = get_platforms(game_id)     # Get the game's platforms so they do not show up in the list
    all_platforms_raw = get_all_platforms()

    game_platforms = [plat[0] for plat in game_platforms_raw]
    all_platforms = [platform[0] for platform in all_platforms_raw if platform[0] not in game_platforms]
    all_platforms.sort()

    return template('add_platform', game=game_name, platforms=all_platforms, game_id=game_id, updated=updated)


@post('/game/<game_id:int>/newplatform')
def add_platform_db(game_id):
    new_platform = request.forms.get('new_platform')
    updated = add_platform_to_db(new_platform, game_id)
    return add_platform(game_id, updated)


@error(404)
def error404(error):
    return template('error_page')


# Start the server
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=False, reloader=True)
