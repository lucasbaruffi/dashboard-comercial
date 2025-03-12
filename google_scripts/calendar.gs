function getCalendarEvents() {
  var calendarId = 'primary'; // Substitua pelo ID do seu calendário
  var now = new Date();
  var events = CalendarApp.getCalendarById(calendarId).getEventsForDay(now);
  var eventos = [];
  for (var i = 0; i < events.length; i++) {
    var event = events[i];
    eventos.push({
      id: event.getId(),
      title: event.getTitle(),
      startTime: event.getStartTime(),
      endTime: event.getEndTime(),
      // Adicione outros campos conforme necessário
    });
  }
  return eventos;
} 