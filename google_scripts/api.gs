function getCalendarEventsFromAPI() {
  var url = 'https://services.leadconnectorhq.com/calendars/events';
  var authorization = 'Bearer ' + 'SEU_TOKEN_DE_AUTORIZACAO'; // Substitua pelo seu token de autorização
  var locationId = 'SEU_LOCATION_ID'; // Substitua pelo seu locationId
  var calendarId = 'SEU_CALENDAR_ID'; // Substitua pelo seu calendarId
  var query = {
    'locationId': locationId,
    'calendarId': calendarId,
    'startTime': '1741489200000',
    'endTime': '1741662000000'
  };
  var options = {
    'method': 'get',
    'headers': {
      'Authorization': authorization,
      'Version': '2021-04-15'
    },
    'muteHttpExceptions': true
  };
  var response = UrlFetchApp.fetch(url + '?' + new URLSearchParams(query).toString(), options);
  if (response.getResponseCode() === 200) {
    var json = JSON.parse(response.getContentText());
    return json.events;
  } else {
    Logger.log('Erro ao obter eventos: ' + response.getContentText());
    return [];
  }
} 