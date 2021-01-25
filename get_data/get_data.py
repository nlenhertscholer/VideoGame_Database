# TODO: Add comments

import requests
import csv
import datetime
from datetime import timezone

DEBUG = False
GENERATE_CSV = True
DELIM = ';'

api_key = {'user-key': 'edf32f70e1ce7aedca3746ff47475e33'}
url = 'https://api-v3.igdb.com/'


def send_request(end, query):
    global api_key
    global url
    req = requests.post(url+end, headers=api_key, data=query)
    return req.json()


def write_csv(filename, full_data, keys):
    assert type(filename) is str
    assert type(full_data) is list
    assert type(keys) is list

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=DELIM)
        csvwriter.writerow(keys)    # Column identifiers
        csv_row = []
        for data in full_data:
            new_row = []
            for key in keys:
                if key in data.keys():
                    new_row += [data[key]]
                else:
                    new_row += [""]
            csv_row.append(new_row)
        csvwriter.writerows(csv_row)
    return


def get_data_pairings(search_key, data, heading_id, comp):
    assert len(heading_id) == 2
    pairing_data = []
    for entity in data:
        if search_key in entity.keys():
            if type(entity[search_key]) is not list:
                entity[search_key] = [entity[search_key]]

            for id1 in entity[search_key]:
                if not next((pair for pair in pairing_data if (pair[heading_id[0]] == id1
                                                               and pair[heading_id[1]] == entity[comp])), False):
                    # No pairing was found so add it to pairing_data
                    pair = {heading_id[0]: id1, heading_id[1]: entity[comp]}
                    pairing_data.append(pair)
    return pairing_data


# games
print("\n----------------------------------- Getting the Games -----------------------------------\n")
num_games = 50000
endpoint = 'games'
popularity = 0
limit = 500
date = datetime.datetime(1993, 12, 30, tzinfo=timezone.utc)
earliest_year = int(date.replace(tzinfo=timezone.utc).timestamp())
print("Calling games from iteration:", 0)
body = f'fields name, aggregated_rating, first_release_date, game_engines, genres, game_modes, platforms;' \
       f' where popularity > {popularity} & first_release_date > {earliest_year} & category = 0; ' \
       f'limit {limit}; sort id asc;'

game_data = send_request(endpoint, body)
game_ids = []
for game in game_data:
    game_ids.append(game['id'])
    # if 'game_engines' in game.keys():
    #     for engine in game['game_engines']:
    #         if engine not in game_engine_ids:
    #             game_engine_ids.append(engine)

iters = int(num_games/limit)

# Get more games
if iters > 1:
    max_id = max(game_ids)
    for i in range(iters-1):
        print("Calling games from iteration:", i+1)
        body = f'fields name, aggregated_rating, first_release_date, game_engines, genres, game_modes, platforms; ' \
               f'where popularity > {popularity} & first_release_date > {earliest_year} & id > {max_id} & category = 0; ' \
               f'limit {limit}; sort id asc;'
        new_data = send_request(endpoint, body)
        for game in new_data:
            game_ids.append(game['id'])
        game_data += new_data
        max_id = max(game_ids)

# Get game_engine ids for following queries
game_engine_ids = []
for game in game_data:
    if 'game_engines' in game.keys():
        for engine in game['game_engines']:
            if engine not in game_engine_ids:
                game_engine_ids.append(engine)


# Get engines
print("\n----------------------------------- Getting the Engines -----------------------------------\n")
endpoint = 'game_engines'
limit = 500
body = f'fields name, platforms; sort id asc; limit {limit};'
engine_data = send_request(endpoint, body)
body = f"fields name, platforms; " \
       f"where id > {engine_data[-1]['id']}; sort id asc; limit {limit};"

engine_data += send_request(endpoint, body)
engine_ids = []
for engine in engine_data:
    engine_ids.append(engine['id'])
game_engine_ids = [idx for idx in game_engine_ids if idx in engine_ids]

print("\n----------------------------------- Getting the Genres -----------------------------------\n")
# Get game genres
endpoint = 'genres'
limit = 500     # only 21 in database
body = f'fields name; limit {limit}; sort id asc;'
genre_data = send_request(endpoint, body)

print("\n----------------------------------- Getting the Modes -----------------------------------\n")
# Get game modes
endpoint = 'game_modes'
limit = 500   # Only 5 in database, this will cover all of them
body = f'fields name; limit {limit}; sort id asc;'
mode_data = send_request(endpoint, body)    # body is same as in genres

print("\n----------------------------------- Getting the Companies -----------------------------------\n")
# Get game companies that worked with
endpoint = 'companies'
limit = 500
startidx = 0
lastidx = 500
company_data = []
max_companies = 10000   # Just get 10000 random companies
company_ids = []
while len(company_data) < max_companies:
    print("Calling companies from iteration:", int(len(company_data)/500))
    idx = 0 if len(company_ids) == 0 else max(company_ids)
    body = f'fields name, country, developed, published, start_date; ' \
           f'where id > {idx}; limit {limit}; sort id asc;'

    # for j in game_ids[startidx + 1:lastidx]:
    #     body += f' | (published=[{j}] | developed=[{j}])'

    body += f"; limit {limit};"
    new_comp_data = send_request(endpoint, body)
    for comp in new_comp_data:
        company_ids.append(comp['id'])
    company_data += new_comp_data


# Get release dates for consoles
print("\n----------------------------------- Getting the Release Dates -----------------------------------\n")
endpoint = 'release_dates'
first = True
limit = 500
final_game_id = game_ids[-1]
first_idx = 0
final_idx = 499
release_date_data = []
while final_idx < num_games:
    print(f"Getting the release dates for games between idx = {first_idx} and idx={final_idx}")
    body = f'fields date, game, platform, category, updated_at; where (game={game_ids[first_idx]}'
    for i in game_ids[first_idx + 1:final_idx]:
        body += f' | game={i}'
    # Get only release dates for world-wide release - not tracking regional sales
    body += f') & region=8; limit {limit};'
    date_data = send_request(endpoint, body)
    release_date_data += date_data
    first_idx = final_idx
    final_idx += 500


# Get all of the platforms
# PLATFORM_CATEGORY = ['console', 'arcade', 'platform',
#                      'operating_system', 'portable_console', 'computer']
print("\n----------------------------------- Getting the Platforms -----------------------------------\n")
endpoint = 'platforms'
limit = 500
body = f'fields name, abbreviation, category, generation; limit {limit};'
platform_data = send_request(endpoint, body)
# Subtract the values of the category by 1
# for platform in platform_data:
#     if 'category' in platform.keys():
#         platform['category'] = PLATFORM_CATEGORY[platform['category']-1]

if DEBUG:
    print("---------- GAME DATA --------------")
    print(game_data[0], '\n')
    print("---------- ENGINE DATA --------------")
    print(engine_data[0], '\n')
    print("---------- GENRE DATA --------------")
    print(genre_data[0], '\n')
    print("---------- MODE DATA --------------")
    print(mode_data[0], '\n')
    print("---------- COMPANY DATA --------------")
    print(company_data[0], '\n')
    print("---------- RELEASE DATE DATA --------------")
    print(release_date_data[0], '\n')
    print("---------- PLATFORM DATA --------------")
    print(platform_data[0], '\n')

if GENERATE_CSV:

    # Engine Table Data
    print("\n----------------------------------- Writing to engine.csv -----------------------------------\n")
    engine_file = 'engine.csv'
    engine_headers = ['id', 'name']
    write_csv(engine_file, engine_data, engine_headers)

    # Game Table Data
    print("\n----------------------------------- Writing to game.csv -----------------------------------\n")

    game_file = 'game.csv'
    game_headers = ['id', 'name', 'aggregated_rating', 'first_release_date']
    write_csv(game_file, game_data, game_headers)

    # Game Engine Table Data
    print("\n----------------------------------- Writing to game_engine.csv -----------------------------------\n")
    game_engine_file = 'game_engine.csv'
    game_engine_headers = ['engine_id', 'game_id']
    accessing_key = 'game_engines'
    comparating_key = 'id'
    game_engine_data = get_data_pairings(accessing_key, game_data, game_engine_headers, comparating_key)
    game_engine_data = [engine for engine in game_engine_data if engine['engine_id'] in game_engine_ids]
    write_csv(game_engine_file, game_engine_data, game_engine_headers)

    # Game Genre Table Data
    print("\n----------------------------------- Writing to game_genre.csv -----------------------------------\n")
    game_genre_file = "game_genre.csv"
    game_genre_headers = ['genre', 'game_id']
    accessing_key = 'genres'
    comparating_key = 'id'
    game_genre_data = get_data_pairings(accessing_key, game_data, game_genre_headers, comparating_key)
    i = 0
    for i in range(len(game_genre_data)):
        game_genre_data[i][game_genre_headers[0]] = \
            next(item['name'] for item in genre_data if item['id'] == game_genre_data[i][game_genre_headers[0]])
    write_csv(game_genre_file, game_genre_data, game_genre_headers)

    # Game Mode Table Data
    print("\n----------------------------------- Writing to game_mode.csv -----------------------------------\n")
    game_mode_file = "game_mode.csv"
    game_mode_headers = ['mode', 'game_id']
    accessing_key = 'game_modes'
    comparating_key = 'id'
    game_mode_data = get_data_pairings(accessing_key, game_data, game_mode_headers, comparating_key)
    i = 0
    for i in range(len(game_mode_data)):
        game_mode_data[i][game_mode_headers[0]] = \
            next(item['name'] for item in mode_data if item['id'] == game_mode_data[i][game_mode_headers[0]])
    write_csv(game_mode_file, game_mode_data, game_mode_headers)

    # Company Table Data
    print("\n----------------------------------- Writing to company.csv -----------------------------------\n")
    company_file = 'company.csv'
    company_headers = ['id', 'name', 'country', 'start_date']
    write_csv(company_file, company_data, company_headers)

    # Published Table
    print("\n----------------------------------- Writing to published.csv -----------------------------------\n")
    published_file = "published.csv"
    published_headers = ['game_id', 'company_id']
    accessing_key = 'published'
    comparating_key = 'id'
    published_data = get_data_pairings(accessing_key, company_data, published_headers, comparating_key)
    published_data = [item for item in published_data if item['game_id'] in game_ids]
    write_csv(published_file, published_data, published_headers)

    # Developed Table
    print("\n----------------------------------- Writing to developed.csv -----------------------------------\n")
    developed_file = "developed.csv"
    developed_headers = ['game_id', 'company_id']
    accessing_key = 'developed'
    comparating_key = 'id'
    developed_data = get_data_pairings(accessing_key, company_data, developed_headers, comparating_key)
    developed_data = [dev for dev in developed_data if dev['game_id'] in game_ids]
    write_csv(developed_file, developed_data, developed_headers)

    # Platform Data Table
    print("\n----------------------------------- Writing to platform.csv -----------------------------------\n")
    platform_file = "platform.csv"
    platform_headers = ['id', 'name', 'abbreviation', 'category', 'generation']
    write_csv(platform_file, platform_data, platform_headers)

    # Platforms release on
    print("\n----------------------------------- Writing to game_platform.csv -----------------------------------\n")
    game_plat_file = "game_plat.csv"
    game_plat_headers = ['platform_id', 'game_id']
    accessing_key = 'platforms'
    comparating_key = 'id'
    game_plat_data = get_data_pairings(accessing_key, game_data, game_plat_headers, comparating_key)
    write_csv(game_plat_file, game_plat_data, game_plat_headers)

    # Release Date table data
    print("\n----------------------------------- Writing to release_dates.csv -----------------------------------\n")
    rel_dates_file = "release_dates.csv"
    rel_dates_headers = ['platform', 'game', 'date', 'category']
    # Check for duplicate primary keys. If there is one, get the most resent update
    dupes = []
    for date in release_date_data:
        dupes.append((date['platform'], date['game']))
    cleaned_dates_data = []
    seen = {}
    for i in range(len(release_date_data)):
        if dupes[i][0]+dupes[i][1] in seen.keys():
            continue
        cnt = dupes.count(dupes[i])
        seen[dupes[i][0]+dupes[i][1]] = 1
        if cnt > 1:
            dup_dicts = [data for data in release_date_data
                         if data['platform'] == dupes[i][0] and data['game'] == dupes[i][1]]
            max_dict = dup_dicts[0]
            for j in range(1, len(dup_dicts)):
                if dup_dicts[j]['updated_at'] > max_dict['updated_at']:
                    max_dict = dup_dicts[j]
            cleaned_dates_data.append(max_dict)
        else:
            cleaned_dates_data.append(release_date_data[i])

    write_csv(rel_dates_file, cleaned_dates_data, rel_dates_headers)

    # Engine Platforms data
    print("\n----------------------------------- Writing to engine_platforms.csv -----------------------------------\n")
    engine_platforms_file = "engine_platforms.csv"
    engine_platforms_headers = ['platform_id', 'engine_id']
    accessing_key = 'platforms'
    comparating_key = 'id'
    engine_platforms_data = get_data_pairings(accessing_key, engine_data, engine_platforms_headers, comparating_key)
    write_csv(engine_platforms_file, engine_platforms_data, engine_platforms_headers)
