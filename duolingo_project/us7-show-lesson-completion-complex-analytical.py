from common import *

us = '''
US7 (Complex, Analytical): Analyze completion rates across all lessons

As an Employee,
I want to analyze completion rates for each lesson in the courses I oversee
So that I can identify which lessons have low completion and may need improvement.
'''

print(us)


def show_lesson_completion(employee_id):
    """
    Implements US7:
    For all courses overseen by a given employee, show each lesson and the
    learner completion rate, so the employee can identify lessons that may
    need improvement.
    """

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
            c.name AS course_name,
            l.title AS lesson_title,
            l.difficulty_level,
            COUNT(*) AS total_attempts,
            COUNT(CASE WHEN lp.completion_time IS NOT NULL THEN 1 END) AS completed_count,
            ROUND(
                COUNT(CASE WHEN lp.completion_time IS NOT NULL THEN 1 END) * 100.0 
                / COUNT(*), 2
            ) AS completion_rate_percent

        FROM Employee AS e
        JOIN CourseAssignment AS ca ON e.employee_id = ca.employee_id
        JOIN Course AS c ON ca.course_id = c.course_id
        JOIN Lesson AS l ON c.course_id = l.course_id
        JOIN LessonProgress AS lp ON l.lesson_id = lp.lesson_id
        WHERE e.employee_id = %s

        GROUP BY c.name, l.title, l.difficulty_level, l.lesson_id
        ORDER BY completion_rate_percent ASC;
    '''

    cmd = cur.mogrify(tmpl, (employee_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()

    print(f"\nRESULT: Lesson completion analysis under employee_id = {employee_id}")
    cols = ('course_name lesson_title difficulty_level total_attempts '
            'completed_count completion_rate_percent')
    show_table(rows, cols)


show_lesson_completion(301)
