<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Search Games</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
<body>
    <!--navbar-->
    <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active">
                <a href="/">Search</a>
            </li>
            <li class="inactive">
                <a href="/newgame">Add New Game</a>
            </li>
        </ul>
    </div>

    <!--search form-->
    <div class="container">
        <div class="starter-template">
            <h1>Search for a game</h1>
            <h4>Using any or all of the following fields</h4>
            <br>
            <form action="/results" method="post">
                <div class="input-group">
                    <label for="game_name">Game Name</label>
                    <input type="text" class="form-control" placeholder="Search by Name" name="game_name" id="game_name">
                </div>
                <br>
                <div class="input-group">
                    <label for="rel_date">Release Date</label>
                    <input type="date" class="form-control" name="release_date" id="rel_date">
                </div>
                <br>
                <div class="input-group">
                    <label for="game_genre">Game Genre</label>
                    <select class="form-control" name="game_genre" id="game_genre">
                        <!--Default value to not depend on it-->
                        <option value="N/A">N/A</option>

                        <!--Add from database here-->
                        % for genre in genres:
                            <option>{{genre}}</option>
                        % end
                    </select>
                </div>
                <br>
                <div class="input-group">
                    <button class="btn btn-primary btn-block" type="submit">Search</button>
                </div>
            </form><br>
            % if deleted:
                <div class="alert alert-success" role="alert">
                    Record successfully deleted.
                </div>
            % elif deleted is None:
                <div class="alert alert-danger" role="alert">
                  Error in deleting record.
                </div>
        </div>
    </div>

</body>