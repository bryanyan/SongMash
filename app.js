var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');
var path = require('path');
var PythonShell = require('python-shell');
var app = express();


app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: false }))


app.post('/submit_text', function(req, res) {
	fs.writeFile('body.txt', req.body.texter, function(err) {
		if(err) {
			return console.log(err);
		}
		console.log("Successfully wrote to file!");
	});
	var options = {
  		mode: 'text',
		pythonOptions: ['-u'],
		args: ['body.txt']
	};
	PythonShell.run('merge.py', options, function(err, results) {
		console.log('results: %j', results);
		var file = __dirname + 'output.mp4';
		res.download('output.mp4');
	});
});


var server = app.listen(8080, function() {
	var addr = server.address();
	console.log('Listening @ port %d', addr.port);
});
