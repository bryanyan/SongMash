var express = require('express');
var app = express();


app.use('/', function(req, res) {
    res.sendFile(__dirname + '/views/index.html');
})

var server = app.listen(8000, function() {
  var addr = server.address();
  console.log('Listening @ port %d', addr.port);
});