<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Results</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <script>
        $(document).ready(function() {
            $('#results').DataTable();
        } );
</script>
</head>
<body>
    <!--navbar-->
    <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="inactive">
                <a href="/">Search</a>
            </li>
            <li class="inactive">
                <a href="/newgame">Add New Game</a>
            </li>
        </ul>
    </div>

    <!--search results-->
    % if game_results:
        <div class="container">
            <div class="starter-template">
                % if len(games) != 0:
                    <h1>Video Games</h1>
                        <table class="table", id="results">
                            <tbody>
                                <tr>
                                    <td colspan="5"><b>Game Name</b></td>
                                </tr>
                                % for game in games:
                                <tr>
                                    <td>{{game[1]}}</td>
                                    <td><a class="btn btn-primary" href="/game/{{game[0]}}">View/Edit</a></td>
                                    <td><a class="btn btn-primary" href="/delete/{{game[0]}}">Delete</a></td>
                                    <td><a class="btn btn-primary" href="/game/{{game[0]}}/platforms">Show Available Platforms</a></td>
                                    <td><a class="btn btn-primary" href="/game/{{game[0]}}/newplatform">Add Platform</a></td>
                                </tr>
                                % end
                            </tbody>
                        </table>
                % else:
                    <h1>No games match your search results.</h1>
                % end
            </div>
    % else:
        <div class="container">
            <div class="starter-template">
                % if len(platforms) != 0:
                    <h1>Platforms</h1>
                        <table class="table", id="results">
                            <thead>
                                <th>Platform Name</th>
                                <th>Abbreviated Name</th>
                                <th>Console Generation</th>
                                <th>Release Date</th>
                            </thead>
                            <tbody>
                                % for platform in platforms:
                                <tr>
                                    <td>{{platform[0]}}</td>
                                    <td>{{platform[1]}}</td>
                                    <td>{{platform[2]}}</td>
                                    <td>{{platform[3]}}</td>
                                </tr>
                                % end
                            </tbody>
                        </table>
                % else:
                    <h1>No platform data for this game.</h1>
                % end
            </div>
        </div>

</body>