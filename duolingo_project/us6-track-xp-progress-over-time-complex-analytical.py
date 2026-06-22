from common import *

us = '''
US6 (Complex, Analytical): Track XP Progress Over Time

As a Learner,
I want to see how my XP grows over time
So that I can visualize my progress and stay motivated.
'''

print(us)


def show_xp_progress_over_time(learner_id):
    """
    Implements US6:
    Uses a window function to show daily and cumulative XP progression for a given learner.
    """

    print("\nBEFORE: Relevant tables ===")

    # Learner table
    print("\nLearner table:")
    cmd = cur.mogrify(
        "SELECT learner_id, name, total_xp, streak "
        "FROM Learner ORDER BY learner_id;", ()
    )
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, "learner_id name total_xp streak")

    # LessonProgress table
    print("\nLessonProgress table:")
    cmd = cur.mogrify(
        "SELECT learner_id, lesson_id, start_time, xp_earned "
        "FROM LessonProgress ORDER BY learner_id, start_time;", ()
    )
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, "learner_id lesson_id start_time xp_earned")

    tmpl = '''
        SELECT
            d.learner_id,
            d.xp_date,
            d.daily_xp,
            SUM(d.daily_xp) OVER (
                PARTITION BY d.learner_id
                ORDER BY d.xp_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cumulative_xp
        FROM (
            SELECT
                lp.learner_id,
                DATE(lp.start_time) AS xp_date,
                SUM(lp.xp_earned) AS daily_xp
            FROM LessonProgress lp
            WHERE lp.learner_id = %s
            GROUP BY lp.learner_id, DATE(lp.start_time)
        ) AS d
        ORDER BY d.xp_date;
    '''

    cmd = cur.mogrify(tmpl, (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()

    print(f"\nRESULT: XP Progress Over Time for learner_id = {learner_id}")
    cols = "learner_id xp_date daily_xp cumulative_xp"
    show_table(rows, cols)

show_xp_progress_over_time(101)
