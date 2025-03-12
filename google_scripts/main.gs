function main() {
  var eventos = getCalendarEvents();
  for (var i = 0; i < eventos.length; i++) {
    var evento = eventos[i];
    var dados = [
      evento.id || '',
      evento.address || '',
      evento.title || '',
      evento.calendarId || '',
      evento.locationId || '',
      evento.contactId || '',
      evento.groupId || '',
      evento.appointmentStatus || '',
      evento.assignedUserId || '',
      evento.startTime || '',
      evento.endTime || '',
      evento.dateAdded || '',
      evento.dateUpdated || '',
      (evento.createdBy && evento.createdBy.userId) || '',
      evento.opportunityId || ''
    ];
    adicionarAgendamento(dados);
  }
} 