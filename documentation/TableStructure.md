Database Tables
-------------

[Read here](ReadoutDatabase.md) how to open and download the database.


Among the tables in the database, only those who's name starts with `workloadAdpp_` are interesting for evaluation.


`workloadApp_student`	
----------------

This table contains a row for each user. 


 * `id` : primary key
 * `user_id`  : integer ID of the user
 * `semesterOfStudy` : This column should be ignored in favour of the column with the same name in the `workloadApp_workinghoursentry` table.
 * `ignoreData` : **This is important. Users with this column value set to `1` have indicated that the data they entered is not correct and should be ignored.** For example it might be a developer account for testing purposes.




`workloadApp_lecture`
---------------

This table contains a row for each lecture. The list of lectures can be edited via the admin panel.

 * `id` : primary key
 * `semester` : semester in which the lecture is held. (Lectures with the same name but in different semesters are different lectures for the purpose of this software.)
 * `name` : name of the lecture
 * `startDay` : Day in the first week the lecture is held.
 * `endDay` : Day in the last week the lecture is held.



`workloadApp_workinghoursentry`
-----------------
Most important table for evaluation.
This table contains a row for each week and lecture each student has made an entry for.
If a student makes an entry about how many hours he spent on a certain lecture in certain week, this information goes here.

 * `id` : primary key
 * `lecture_id` : primary key of the lecture for which the entry was made
 * `student_id` : primary key of the student who made the entry
 * `week` : Date of the Monday of the week for which the entry was made
 * `semesterOfStudy` : semester of study of the student who made the entry at the time of making the entry. This is not 100% reliable I think, especially in the beginning of a semester. A value 0 indicates that the semester of study is unknonw.
 * `hoursInLecture` : Hours the student stated to have spent visiting the lecture itself.
 * `hoursForHomework` : Hours the student stated to have spent on homework for the lecture.
 * `hoursStudying` : Hours the student stated to have spent studying for the lecture.
 


`workloadApp_student_lectures`
-----------------

This table contains a row for each active lecture of each student. It defines which lectures are active for which students.
A lecture is active if the student has selected it for data entry. This is usually if the student is currently visiting this lecture.
An entry in this table is not a necessary or sufficient condition to determine if a student has entered data for a certain lecture.
It is recommended to ignore this table.

 * `id` : primary key
 * `student_id` : primary key of the student in the `workloaApp_student` table.
 * `lecture_id` : primary key of the lecture in the `workloaApp_lecture` table.