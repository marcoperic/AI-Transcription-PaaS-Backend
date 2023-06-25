const express = require('express')
const app = express()

app.get('/', (req, res) => {
    res.send('Hello world!');
});

app.get('/goomba', (req, res) => {
    res.send('GOOMBA');
});

app.listen(3000, () => console.log("Server is listening on port 3000."))