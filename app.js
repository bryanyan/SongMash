var express = require('express');
var bodyParser = require('body-parser');
var request = require('request');
var fs = require('fs');
var path = require('path');
var XML2JS = require('xml2js').parseString;
var PythonShell = require('python-shell');
var app = express();


app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: false }))


var mergeBodyText = function(res) {
    console.log("Beginning video merge...");
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
}

app.post('/submit_text', function(req, res) {
	var givenText = req.body.texter;
    fs.writeFile('body.txt', givenText, function(err) {
        if(err) {
            return console.log(err);
        }
        console.log("Wrote custom text to body.txt");
        mergeBodyText(res);
    });
});

app.post('/submit_song', function(req, res) {
	var givenText = '';
    var CHART_LYRIC_API = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={artistName}&song={songName}';
    var artist = req.body.artist;
    var song = req.body.song;
    CHART_LYRIC_API = CHART_LYRIC_API.replace('\{artistName\}', artist).replace('\{songName\}', song);
    request(CHART_LYRIC_API, function (err, res, body) {
        console.log("Searching up song lyrics on Chart Lyric...")
        console.log("  Artist: ", artist, " Song: ", song);
        if(err) {
            return console.log(err);
        }
        XML2JS(body, function (err, result) {
            if (err) {
                return console.log(err);
            }
            console.log("Received lyrics response...");
            var jsonResponse = JSON.parse(JSON.stringify(result));
            var lyrics = jsonResponse.GetLyricResult.Lyric;
            givenText = lyrics[0];
            fs.writeFile('body.txt', givenText, function(err) {
                if(err) {
                    return console.log(err);
                }
                console.log("Wrote custom text to body.txt");
                mergeBodyText(res);
            });
        });
    });
});

var server = app.listen(8080, function() {
	var addr = server.address();
	console.log('Listening @ port %d', addr.port);
});
