function adicionarAgendamento(dados) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('agendamentos');
  var data = sheet.getDataRange().getValues();
  var found = false;
  for (var i = 0; i < data.length; i++) {
    if (data[i][0] === dados[0]) { // Compara pelo ID do evento
      sheet.getRange(i + 1, 1, 1, dados.length).setValues([dados]);
      Logger.log('Atualizado na linha ' + (i + 1));
      found = true;
      break;
    }
  }
  if (!found) {
    sheet.appendRow(dados);
    Logger.log('Linha adicionada com sucesso');
  }
} 