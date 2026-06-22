from common import *

us = '''
US9 (Complex, Analytical): Identify Lessons with Low XP Gains

As an Employee,
I want to see which lessons give learners the lowest XP on average
So that I can rebalance XP gains and improve learner engagement.
'''

print(us)


def show_low_xp_lessons():
    """
    Implements US9:
    Shows lessons with the lowest average XP earned by learners.
    Helps employees identify lessons that may need reward adjustments.
    """

    print("\nBEFORE: Relevant tables ===")

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
            l.lesson_id,
            l.title AS lesson_title,
            l.difficulty_level,
            ROUND(AVG(lp.xp_earned), 2) AS avg_xp_earned,
            COUNT(lp.learner_id) AS total_attempts
        FROM LessonProgress AS lp
        JOIN Lesson AS l ON lp.lesson_id = l.lesson_id
        GROUP BY l.lesson_id, l.title, l.difficulty_level
        ORDER BY avg_xp_earned ASC;
    '''

    cmd = cur.mogrify(tmpl, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()

    print("\nRESULT: Lessons with Lowest Average XP Earned")
    cols = ('lesson_id lesson_title difficulty_level avg_xp_earned total_attempts')
    show_table(rows, cols)

show_low_xp_lessons()
