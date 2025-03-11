from requisições import getCalendarEvents

eventos = getCalendarEvents()

for evento in eventos:
    print(evento["title"])