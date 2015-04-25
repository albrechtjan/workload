from django.contrib.auth.decorators import login_required, user_passes_test
from workloadApp.models import privacy_agreement
from workloadApp.models import WorkingHoursEntry, Lecture, Student


from datetime import date, timedelta
from objects import Week, Semester




@login_required
def weeks():
    pass

@login_required
@user_passes_test(privacy_agreement)
def weeks_lectures(request, year=None, week=None, lecture_id=None):
    if request.method == "GET":
        if lecture_id:
            pass
        else:
            pass
    if request.method == "POST":
        pass

@login_required
def menu_lectures_all(request):
    if request.method == "GET":
        pass
    else:
        pass

@login_required
@user_passes_test(privacy_agreement)
def menu_lectures_active(request, lecture_id=None):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    elif request.method == "DELTE":
        if lecture_id:
            pass
        else:
            raise
    else:
        pass

@login_required
def menu_statistics(request):
    pass

@login_required
def menu_privacy(request):
    pass

@login_required
def menu_privacy_agree(request):
    pass

@login_required
def menu_settings(request):
    pass

@login_required
def menu_settings_deletableLectures(request):
    pass
