from common import *

us = '''
US4 (Complex, Analytical): Shows the average accuracy score for each lesson in a course


As an Employee,
I want to see the average learner accuracy by lesson within a course
So that I can identify which lessons are too difficult for users.
'''

print(us)


def show_lesson_difficulty(course_id):
    
    """
    Implements US4:
    For a given course, show each lesson and the average learner accuracy
    on that lesson, so an employee can identify which lessons are harder.
    """

    # Show tables before running the US4 query
    print("\nBEFORE: Relevant tables ===")

    # Course table
    print("\nCourse table:")
    cmd = cur.mogrify("SELECT * FROM Course ORDER BY course_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'course_id name language_taught_in language_learning')

    # Lesson table
    print("\nLesson table:")
    cmd = cur.mogrify("SELECT * FROM Lesson ORDER BY lesson_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'lesson_id course_id title difficulty_level accuracy_score')

    # LessonProgress table
    print("\nLessonProgress table:")
    cmd = cur.mogrify("SELECT * FROM LessonProgress ORDER BY learner_id, lesson_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id lesson_id start_time completion_time best_accuracy xp_earned')

    
    tmpl = '''
        SELECT 
            C.course_id,
            C.name AS course_name,
            C.language_taught_in,
            C.language_learning,
            L.lesson_id,
            L.title AS lesson_title,
            L.difficulty_level,
            ROUND(AVG(LP.best_accuracy), 3) AS avg_learner_accuracy 
        FROM Course C
        JOIN Lesson L ON C.course_id = L.course_id
        LEFT JOIN LessonProgress LP ON L.lesson_id = LP.lesson_id
        WHERE C.course_id = %s
        GROUP BY C.course_id, C.name, C.language_taught_in, C.language_learning, L.lesson_id, L.title, L.difficulty_level
        ORDER BY avg_learner_accuracy ASC;

    '''
    
    cmd = cur.mogrify(tmpl, (course_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()

    print(f"\nRESULT: Average learner accuracy per lesson for course_id = {course_id}")
    cols = ('course_id course_name language_taught_in language_learning lesson_id lesson_title '
            'difficulty_level avg_learner_accuracy')
    show_table(rows, cols)

show_lesson_difficulty(9038)