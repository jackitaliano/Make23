var express = require('express');

var bodyParser = require("body-parser");

var app = express();

const firebaseAdmin = require('firebase-admin');

const request = require('request');

firebaseAdmin.initializeApp({
    credential: firebaseAdmin.credential.cert({
        projectId: 'makeohio2023',
        privateKey: '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDIgKNqcBoQze2F\nsjaoeL9J+EAPGv+NEvaOu6chQZpTRqYHk0AUdMxUKcBVYi1y/hFPYnuikRmfC9PH\nFT5IstP3prpfzSskFlzr5UIeimXdINZrprDD+LwugVqmZrak26073/3pEAyRF3zC\nZhyEhSoFC+3aDTQ6LBq9aq8maauDiLIxQGGqFPIlzp6MOEKhmKI1kpaWCzUwbVci\nqqTDa7uGf47bmMe/tK4eL8QE6z3z0GI3tKKSz3x5YcC5xO1Xix9STpSoYAjs6Qt5\nuYbL1hDKC9hNa59YBu3LqlOKlEpf1txqMGPjzv3TSjqfdRQHxX3jxwvVy3CUgv6h\neZKbL00XAgMBAAECggEAGdKbeVNbwAtNinkD2hnHBSdQVMG05P3qvEJFyZ4x2oTQ\nUExyJdBPGo3QBA8jbFp1b0RvSOYoJxg2W78MKP/DFfOmsDzzz++DYyxBIj7P1LVs\neCvdOzgXQGQPgTvcTQov2vTDtlcHT053lm/hP14JJeI97WXi8pUIkpmhWjCk0sk3\nTDePFqMepMzsI2qY+EJFBRrPmp0wVG7REB2OISPiaq4kTRKKSmGmK2eZi1uBotbI\nJ6+zXdUfidjErMHQzEcTYexro0aRUC4Ex1HlZV73Cfhy0HDQS9z9z+Ic4Bk1GQdw\nJH8mlNF9l5bA1kKv7/fCl7/HxkroB88dHLCxiyWoBQKBgQDpI8+V261+LBgdjx8H\nTKuZzEKf1HqWEPB+blBCz+FYfXk2KXAnam+yO7qxWWVrFPYtqkAVJI6BpceXu5Ad\njkGKDNQfTiz0A7oflzTWR7A4ApOnJznOngdnfCzofKlrR2/9NCx/sMdL8N3QUy2P\nBY2/PAaoN3SBDQ01nh4nndTKlQKBgQDcKZN0OPouS3cduT5Ig7PeGtqYhfFI6+wc\nsO/2aRlcTM966rLUMx6pFQodqnmOMWm6EOT/ye0qt+6VOYROCCpO3EULpYCpu4Lv\nyYGHVc7RVcsPWY3zV8QOtUePO0nfxUQvNU8IEMFJXXJNLkhFlYJax0iKIqYGwV7r\nN1F2bcu5+wKBgHj3D7odpUMV9d1AaUUMTu0ZwmfTg1dhqqau7g38dlvHnqCvl3Wc\nECBWRWPHkoug8Kp4748IzLgQICNmOjxblz3dsiIcGc7yMBw8BDo6MACftaTBAYln\nDUhwcYyfQfhbtIuYCo6mVoHck/qHbdgLdaSHrJyTSWu8LeJoDBVaGxKRAoGAVpSv\nHVyu3nflDzZjTQcmPClZX/QE0IWfJCVdKQ1p4MeALLmRvCuiWiIhCUuaZBYAmyC7\nve/+KfeNhvfIlRtW8A5lxM/ASn+oXX5kRwGyxNY1dgLk9RbFznbx/lz1j1+3kc0o\nGGbmbGCoa7vQxjSmv+ZxG4nGuw9esafejHFfVfMCgYBOeckVOgpmv3/usm7tfQUs\nq2BJ3g1PVWHw64821IlToZW6xVPeuyR/ZjTdYQMcWAdexLgGd9OPGwvSUNO9T+w9\n6b9a/ORZgoJegsc3VXyvgm0AHq402bsFLWy9BcyZPqjb4ITLuo6hjFWT48RT9Agi\nNcC9nKBpoOnrXPA2olQ7Gg==\n-----END PRIVATE KEY-----\n',
        clientEmail: 'firebase-adminsdk-iyviq@makeohio2023.iam.gserviceaccount.com'
    }),
    databaseURL: 'https://makeohio2023-default-rtdb.firebaseio.com'
})

const db = firebaseAdmin.database();

const ref = db.ref('NewSentence');
ref.on('value', (snapshot) => {
    console.log('Data Changed: ', snapshot.val());
    const data = snapshot.val();

    db.ref('data').set(data);
});


app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

var handlebars = require('express-handlebars').create({defaultLayout: 'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars')

app.get('/', function(req,res) {
    res.render(__dirname + '/public/index.html');
});

app.listen(3000, function(){
    console.log('Listening on port 3000...');
})
