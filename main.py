from requisições import getCalendarEvents
from sheets import adicionarAgendamento

try:
    eventos = getCalendarEvents()
except Exception as e:
    print(f"Erro ao obter eventos: {e}")
    eventos = []

for evento in eventos:
    try:
        dados = [
            evento.get("id", ""),
            evento.get("address", ""),
            evento.get("title", ""),
            evento.get("calendarId", ""),
            evento.get("locationId", ""),
            evento.get("contactId", ""),
            evento.get("groupId", ""),
            evento.get("appointmentStatus", ""),
            evento.get("assignedUserId", ""),
            evento.get("startTime", ""),
            evento.get("endTime", ""),
            evento.get("dateAdded", ""),
            evento.get("dateUpdated", ""),
            evento.get("createdBy", {}).get("userId", ""),
            evento.get("opportunityId", "")
        ]

        adicionarAgendamento(dados)
    except Exception as e:
        print(f"Erro ao adicionar agendamento: {e}")
