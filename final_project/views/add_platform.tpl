<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Add Platform</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
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

    <div class="container">
        <div class="starter-template">
            <h1>New Platform For {{game}}</h1>
            <br>
            <form action="/game/{{game_id}}/newplatform" method="post">
                <div class="input-group">
                    <label for="new_platform">Platform Name</label>
                    <select class="form-control" name="new_platform" id="new_platform">
                        % for platform in platforms:
                            <option value="{{platform}}">{{platform}}</option>
                        % end
                    </select>
                </div><br>
                <div class="input-group">
                    <button class="btn btn-primary btn-block" type="submit">Add Platform</button>
                </div>
            </form>
        </div><br>
        % if updated:
            <div class="alert alert-success" role="alert">
                Change was succesful!
            </div>
        % elif updated is None:
            <div class="alert alert-danger" role="alert">
                Database Error: Unable to update record.
            </div>
        % end
    </div>
</body>