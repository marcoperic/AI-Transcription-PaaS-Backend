const express = require('express')
const fs = require('fs/promises')
const app = express()

app.get('/', (req, res) => {
    res.send('' + Math.random());
});

app.get('/goomba', (req, res) => {
    res.send('GOOMBA');
});

app.get('/upload_media', (req, res) => {

    fs.readFile('../../testing/sample_instructions_package.json', 'utf8').then((data) =>
    {
        res.json(JSON.parse(data))
    }).catch((err) => {
        console.log(err)
    });
})

app.listen(3000, () => console.log("Server is listening on port 3000."))

// start master.py as well. may be ncessary to allow for routing to multiple masters?