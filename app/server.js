const express = require('express');
const app = express();
const compression = require('compression');


const server = app.listen(process.env.PORT || 7777, listen);

function listen() {
    const port = server.address().port;
    // console.log(server.address());
    console.log('Server listening at http://0.0.0.0:' + port);
}

app.use(compression());
app.use(express.json());
app.use(express.urlencoded())

app.use(express.static(__dirname + "/dist"));
app.use(express.static(__dirname));