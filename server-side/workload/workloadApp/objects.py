import isoweek


class Week(isoweek.Week):
    def isCurrentWeek(self):
        return self == isoweek.Week.thisweek()