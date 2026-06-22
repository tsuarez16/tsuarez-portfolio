from common import *

us = '''
US8 (Complex, Analytical): See how many learners are enrolled in each course

As an Employee,
I want to see how many learners are enrolled in each course
So that I can report on the popularity of each language course.
'''

print(us)


def show_course_enrollment_counts():
    """
    Implements US8:
    Show all courses and the number of learners enrolled in each one.
    """

    print("\nBEFORE: Relevant tables ===")

    # Course table
    print("\nCourse table:")
    cmd = cur.mogrify("SELECT * FROM Course ORDER BY course_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'course_id name language_taught_in language_learning')

    # Enrollments table
    print("\nEnrollments table:")
    cmd = cur.mogrify("SELECT * FROM Enrollments ORDER BY course_id, learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'course_id learner_id')

    tmpl = '''
        SELECT 
            c.course_id,
            c.name AS course_name,
            c.language_learning,
            c.language_taught_in,
            COUNT(e.learner_id) AS total_enrolled_learners
        FROM Course AS c
        LEFT JOIN Enrollments AS e ON c.course_id = e.course_id
        GROUP BY c.course_id, c.name, c.language_learning, c.language_taught_in
        ORDER BY total_enrolled_learners DESC;
    '''

    cmd = cur.mogrify(tmpl, ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()

    print("\nRESULT: Enrollment count per course")
    cols = ('course_id course_name language_learning language_taught_in total_enrolled_learners')
    show_table(rows, cols)

show_course_enrollment_counts()
