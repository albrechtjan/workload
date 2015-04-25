Documentation of the main functions of the REST API. This is not necessarliy exhaustive, there might be more undocumented urls and returns


GET /api  //this is the entry point


The responses to the REST- API are specific to the authenticated user. The user token is always transmitted as a parameter

GET /api/weeks/   returns: weeks
GET /api/weeks/<year>/<week>/lectures/   returns: lectures 
GET /api/weeks/<year>/<week>/lectures/<lecture_id>/ returns: lecture with attribute has_data
POST /api/weeks/<year>/<week>/lectures/ params: lecture-identifier, attending, homework, studying // this does not ADD a lecture, but it adds an entry


GET /api/menu/lectures/active/ returns list of lectures selected by user
GET /api/menu/lectures/all/  returns list of all available lectures
POST /api/menu/lecturs/active/ //adds a lecture
DELETE /api/menu/lecturs/active/<lecture_id>

GET /api/menu/statistics/
GET /api/menu/privacy/
POST /api/menu/privacy/agree
GET /api/menu/settings returns list of settings
GET /api/menu/settings/deletable_lectures  returns list of deletable lectures
DELETE /api/menu/settings/deletable_lectures/deletable_lecture 
