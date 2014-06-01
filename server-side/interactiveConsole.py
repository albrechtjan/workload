# get interactive console redady
from workloadApp.models import Student, WorkingHoursEntry, Lecture

s = Student.objects.get()
s.getCalendarWeeks()