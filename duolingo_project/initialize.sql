-- drop the project database if it exists
DROP database if EXISTS project;

-- create it afresh
CREATE database project;
\c project

\i create.sql

-- load the data

\copy Course(course_id, name, language_taught_in, language_learning) FROM data/Course.csv csv header;
\copy Learner(learner_id, name, username, last_login, languages_learned, total_xp, streak, streak_notification_preference, user_type, current_hearts, ad_preference, subscription_date, card_number) FROM data/Learner.csv csv header;
\copy Employee(employee_id, name, position, department) FROM data/Employee.csv csv header;
\copy Enrollments(course_id, learner_id) FROM data/Enrollments.csv csv header;
\copy Lesson(lesson_id, course_id, title, difficulty_level, accuracy_score) FROM data/Lesson.csv csv header;
\copy Attempt(attempt_id, attempted_at, is_correct, learner_id) FROM data/Attempt.csv csv header;
\copy Exercise(exercise_id, difficulty_level, question_type, question, accuracy_score, attempt_id, lesson_id) FROM data/Exercise.csv csv header;
\copy LessonProgress(learner_id, lesson_id, start_time, completion_time, best_accuracy, xp_earned) FROM data/LessonProgress.csv csv header;
\copy CourseAssignment(employee_id, course_id) FROM data/CourseAssignment.csv csv header;
