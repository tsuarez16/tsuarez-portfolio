\c project

\echo 'Showing contents of Course table, which represents the courses offered in Duolingo:'
SELECT * FROM Course ORDER BY course_id;

\echo 'Showing contents of Learner table, which represents the learners and their profile information:'
SELECT * FROM Learner ORDER BY learner_id;

\echo 'Showing contents of Lesson table, which represents the lessons within a course:'
SELECT * FROM Lesson ORDER BY lesson_id;

\echo 'Showing contents of LessonProgress table, which represents a learner''s progress on specific lessons:'
SELECT * FROM LessonProgress ORDER BY learner_id, lesson_id;

\echo 'Showing contents of Attempt table, which represents individual attempts made by learners on exercises:'
SELECT * FROM Attempt ORDER BY attempt_id;

\echo 'Showing contents of Exercise table, which represents the exercises within lessons:'
SELECT * FROM Exercise ORDER BY exercise_id;

\echo 'Showing contents of Enrollments table, which represents which learners are enrolled in which courses:'
SELECT * FROM Enrollments ORDER BY course_id, learner_id;

\echo 'Showing contents of Employee table, which represents Duolingo employees (e.g., content designers, instructors, analysts):'
SELECT * FROM Employee ORDER BY employee_id;

\echo 'Showing contents of CourseAssignment table, which represents which employees are assigned to which courses:'
SELECT * FROM CourseAssignment ORDER BY employee_id, course_id;
