var pg = require("pg");

var conString = "pg://root:pegazo13@104.236.0.177:5432/hidro_sysdb";
//var conString = "postgres://YOURUSER:YOURPASSWORD@localhost/dev";


var client = new pg.Client(conString);
client.connect();


var query = client.query("SELECT temperatura FROM hidro_core_equipomedicion");
query.on("row", function (row, result) {
    result.addRow(row);
});
query.on("end", function (result) {
    console.log(JSON.stringify(result.rows, null, "    "));
    client.end();
});