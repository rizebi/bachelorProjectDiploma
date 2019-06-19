body = ""
body += "<style> \ntable, th, td { \nborder: 1px solid black; \nborder-collapse: collapse; \n} \n th, td { \npadding: 5px; \ntext-align: left; \n" +
" white-space:pre \n} \n</style>";

if(product.frequency.toLowerCase() === 'monthly')
  body += '<b>Report type: </b>Monthly<br>\n';
if(product.frequency.toLowerCase() === 'weekly')
  body += '<b>Report type: </b>Weekly<br>\n';
if(product.frequency.toLowerCase() === 'daily')
  body += '<b>Report type: </b>Daily<br>\n';

body += '<b>Product name: </b>' + product.name + ' <br>\n';
body += '<b>Data source: </b>Katastif MacDumps <br>\n';
body += '<b>Data interval: </b>' +  start_date.toUTCString() + "----" + end_date.toUTCString() + ' <br>\n';

totalDumpsCurrent = 0;
totalDumpsPrev = 0;
Object.keys(dumps).forEach(function(key) {
  totalDumpsCurrent += dumps[key]["nrCrashes"];
  logger("Current = " + key + " " + dumps[key]["nrCrashes"])
}, this);
Object.keys(prevDumps).forEach(function(key) {
  totalDumpsPrev += prevDumps[key]["nrCrashes"];
  logger("Prev = " + key + " " + prevDumps[key]["nrCrashes"])
}, this);

logger("Current total = " + totalDumpsCurrent);
logger("Prev total = " + totalDumpsPrev);

var avgTotal7DaysCrashes = Math.ceil(intToFloat(totalDumpsPrev / 7, 2))
var totalDumpsVariationColor = totalDumpsCurrent > avgTotal7DaysCrashes ? 'red': 'green';
body += '<b>No of dumps for current interval: </b><b style="color: ' + totalDumpsVariationColor + '">' + totalDumpsCurrent  + ` (${add_variation(totalDumpsCurrent, avgTotal7DaysCrashes)})` + '</b><br>\n';
body += '<b>Previous 7 days Average no of crashes: </b>' + avgTotal7DaysCrashes + '<br>\n';

// ####################### END OF HEADER #######################
if(Object.keys(dumps).length === 0) {
  body += '<p style="color: green"> No crash events submitted for the selected product. </p>';
  return body;
}
// Daca nu am iesit, inseamna ca avem ce pune in tabel:
body += "<br>"
body += "\n\n<table style=\"border: 1px solid black\">";
body += "\n<tr>";
body += "<th>Module Name</th>";
body += "<th>No Of Crashes</th>";
body += "<th>No Of Unique IP</th>";
body += "<th>Previous 7 days Average no of crashes</th>";
body += "<th>No of crashes by module version</th>";
body += "<th>Crashes by Offset</th>";

// Aici trebuie sa scoatem o lista de key de module, ordonata descrescator dupa nr de crashuri pe fiecare modul
keysModulesSorted = Object.keys(dumps).sort(function(a, b){return dumps[b].nrCrashes - dumps[a].nrCrashes})
//logger("keysModulesSorted = " + keysModulesSorted)

keysModulesSorted.forEach(function(keyModule) {
  //logger("For keyModule = " + keyModule)
  // Aici trebuie sa scoatem o lista de key de versiuni, ordonata descrescator dupa nr de crashuri pe fiecare versiune

  keysVersion = Object.keys(dumps[keyModule])
  // Trebuie sa scoate nrCrashes deoarece nu e versiune
  keysVersion = arrayRemove(keysVersion, "nrCrashes")
  keysVersion = arrayRemove(keysVersion, "ipAddresses")
  //logger("keysVersion = " + keysVersion)
  if(prevDumps[keyModule] != undefined)
    average7DaysCrashes = Math.ceil(intToFloat(prevDumps[keyModule]["nrCrashes"] / 7, 2));
  else
    average7DaysCrashes = 0;
  var dumpsVariationColor = dumps[keyModule]["nrCrashes"] > average7DaysCrashes ? 'red': 'green';
  keysVersionSorted = keysVersion.sort(function(a, b){return dumps[keyModule][b].nrCrashes - dumps[keyModule][a].nrCrashes})
  //logger("keysVersionSorted = " + keysVersionSorted)

  body += "<tr>";
  var rowspan_MAX = Object.keys(dumps[keyModule]).length - 2;
  if (rowspan_MAX >= 3) {
    rowspan_MAX = 2;
  }
  //logger("rowspan_MAX = " + rowspan_MAX)
  body += "<td rowspan=\"" + rowspan_MAX + "\">" + keyModule + "</td>";
  body += "<td rowspan=\"" + rowspan_MAX + "\" style=\"color: " + dumpsVariationColor + "\">" + dumps[keyModule]["nrCrashes"] + "</td>";
  body += "<td rowspan=\"" + rowspan_MAX + "\">" + Object.keys(dumps[keyModule].ipAddresses).length + "</td>";
  body += "<td rowspan=\"" + rowspan_MAX + "\">" + average7DaysCrashes + "</td>";

  // O sa afisam maxim 2 versiuni per modul. Asa ca le ignoram pe celelalte
  keysVersionSorted = keysVersionSorted.slice(0, 2)
  keysVersionSorted.forEach(function(keyVersion) {
    //logger("For keyVersion = " + keyVersion)
    // Aici trebuie sa scoatem o lista de key de offseturi, ordonata descrescator dupa nr de crash-uri pe fiecare offset
    keysOffsetSorted = Object.keys(dumps[keyModule][keyVersion]["dumpOffsets"]).sort(function(a, b){return dumps[keyModule][keyVersion]["dumpOffsets"][b] - dumps[keyModule][keyVersion]["dumpOffsets"][a]})
    //logger("keysOffsetSorted = " + keysOffsetSorted)

    body += "<td>" + keyVersion + " = " + dumps[keyModule][keyVersion].nrCrashes + "</td>"
    body += "<td>" + keysOffsetSorted[0] + " = " + dumps[keyModule][keyVersion].dumpOffsets[keysOffsetSorted[0]] + "</td>"
    body += "</tr>"
  }, this);
}, this);
body += "</table>\n";
