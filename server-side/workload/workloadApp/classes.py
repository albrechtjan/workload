from datetime import date

class StudentWeek:
	def __init__(self, mondaydate, hasdata=False):
		self.hasData = hasdata
		self.mondayDate = mondaydate
	def getWeekNumber(self):
		return self.mondayDate.isocalendar()[1]

	def getYear(self):
		# returns the year in which the week happens
		return self.mondayDate.isocalendar()[0]


