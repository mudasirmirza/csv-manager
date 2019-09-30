<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Bottle CSV Project">
    <meta name="author" content="MudasirMirza">
    <link rel="icon" href="/static/favicon.ico">
    <title>Bottle CSV Project</title>
    <link rel="stylesheet" type="text/css" href="/static/bootstrap.min.css">
    <script type="text/javascript" src="/static/jquery.min.js"></script>
    <script type="text/javascript" src="/static/bootstrap.min.js"></script>
</head>
<body>
<nav class="navbar navbar-default navbar-static-top">
    <div class="container">
        <div class="row">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Home</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
            </div>
        </div>
    </div>
</nav>
<div class="container">
    <div class="row">
        <div class="jumbotron">
            <h4>{{s3_message}}</h4>
        </div>
    </div>
    <!--./row-->
    <div class="row">
        <hr>
        <ul>
            %for item in items:
            <li>{{item}}</li>
            %end
        </ul>
        <hr>
        <footer>
            <p>&copy; 2019 {{data["developer_project"]}}.</p>
        </footer>
    </div>
</div>
</html>