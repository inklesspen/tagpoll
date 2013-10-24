<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Tag Poll</title>

    <!-- Bootstrap core CSS -->
    <link href="${request.static_path('tagpoll:static/css/bootstrap.css')}" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="${request.static_path('tagpoll:static/css/site.css')}" rel="stylesheet">

  </head>

  <body>

    <div class="container" ng-app="tagpoll">

      ${next.body()}

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="${request.static_path('tagpoll:static/js/jquery-2.0.3.js')}"></script>
    <script src="${request.static_path('tagpoll:static/js/lodash.js')}"></script>
    <script src="${request.static_path('tagpoll:static/js/bootstrap.js')}"></script>
    <script src="${request.static_path('tagpoll:static/js/angular.js')}"></script>
    <script src="${request.static_path('tagpoll:static/js/site.js')}"></script>
  </body>
</html>
