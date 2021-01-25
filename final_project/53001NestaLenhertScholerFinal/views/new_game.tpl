<!DOCTYPE html>
<!--suppress XmlDuplicatedId -->
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    % if alter:
        <title>Edit {{game_name}}</title>
    % else:
        <title>Add New Game</title>
    % end
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
<body>
    <!--navbar-->
    <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="inactive">
                <a href="/">Search</a>
            </li>
            % if alter:
                <li class="inactive">
                    <a href="/newgame">Add New Game</a>
                </li>
            % else:
                <li class="active">
                    <a href="/newgame">Add New Game</a>
                </li>
            % end
        </ul>
    </div>
        <!--search form-->
    <div class="container">
        <div class="starter-template">
            % if alter:
                <h1>Change {{game_name}}</h1>
            % else:
                <h1>Add a game</h1>
            % end
            <br>

            % if alter:
                <form action="/game/{{game_id}}" method="post">
                    <div class="input-group">
                        <label for="game_name">Change Game Name</label>
                        <input type="text" class="form-control" value="{{game_name}}" name="game_name" id="game_name">
                    </div><br>
                    <div class="input-group">
                        <label for="init_rel_date">Change Initial Release Date</label>
                        % if release_date:
                            <input type="date" class="form-control" value="{{release_date}}" name="init_rel_date" id="init_rel_date">
                        % else:
                            <!--suppress XmlDuplicatedId -->
                        <input type="date" class="form-control" name="init_rel_date" id="init_rel_date">
                        % end
                    </div><br>
                    <div class="input-group">
                        <label for="game_genre">Change Genre</label>
                        <select class="form-control" name="game_genre" id="game_genre">
                            % if main_genre:
                                <option>{{main_genre}}</option>
                                % for genre in genres:
                                    % if genre != main_genre:
                                        <option>{{genre}}</option>
                                    % end
                                % end
                            % else:
                                <option>N/A</option>
                                % for genre in genres:
                                    <option>{{genre}}</option>
                                % end
                            % end
                        </select>
                    </div><br>
                <div class="input-group">
                    <button class="btn btn-primary btn-block" type="submit">Submit Changes</button>
                </div>
                </form><br>
                <!-- Alert the user that a change was made -->
                % if new_update:
                    <div class="alert alert-success" role="alert">
                        Change was succesful!
                    </div>
                % elif new_update is None:
                    <div class="alert alert-danger" role="alert">
                        Database Error: Unable to update record.
                    </div>
                % end

            % else:
                <form action="/newgame" method="post">
                    <div class="input-group">
                        <label for="new_game_name">Game Name</label>
                        <input type="text" class="form-control" placeholder="Insert New Game Name" name="new_game_name" id="new_game_name">
                    </div><br>
                    % if empty:
                    <div class="alert alert-danger" role="alert">
                        Game name cannot be empty
                    </div><br>
                    % end
                    <div class="input-group">
                        <label for="init_rel_date">Initial Release Date</label>
                        <input type="date" class="form-control" name="init_release_date" id="init_rel_date">
                    </div><br>
                    <div class="input-group">
                        <label for="new_game_genre">Choose The Main Genre Of The Game</label>
                        <select class="form-control" name="new_game_genre" id="new_game_genre">
                            <!--Default value to not depend on it-->
                            <option value="N/A">N/A</option>

                            <!--Add from database here-->
                            % for genre in genres:
                                <option>{{genre}}</option>
                            % end
                        </select>
                    </div><br>
                <div class="input-group">
                    <button class="btn btn-primary btn-block" type="submit">Add Game</button>
                </div>
                </form><br>
                % if updated:
                    <div class="alert alert-success" role="alert">
                        Game was added successfully!
                    </div>
                % elif updated is None:
                    <div class="alert alert-danger" role="alert">
                        Database Error: Unable to update record.
                    </div>
                % end
            % end


        </div>
    </div>
</body>