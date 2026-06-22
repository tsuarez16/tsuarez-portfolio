from common import *

us = '''
US1 (Simple, Operational): Turns streak-reminder notifications on or off


As an Freemium user, I want to be able to turn streak-reminder notifications on or off,
so I can build good habits and consistently keep up with learning the language, and
not be disturbed by notifications when I don't want them.
'''

print(us)


def toggle_streak_notifications(learner_id):
    
    """
    Implements US1:
    As a Freemium user, I want to be able to turn streak-reminder notifications on or off,
    so I can build good habits and consistently keep up with learning the language, and
    not be disturbed by notifications when I don't want them.
    """

    # Show tables before running the US1 query
    print("\nBEFORE: Relevant tables ===")

    # Learner table
    print("\nLearner table:")
    cmd = cur.mogrify("SELECT * FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id name username last_login languages_learned total_xp streak user_type current_hearts ad_preference subscription_date card_number streak_notification_preference')

    # Toggle the streak notification preference for the specific learner
    print(f"\n\nTOGGLING streak notification preference for learner_id = {learner_id}")
    
    tmpl = '''
        UPDATE Learner
        SET streak_notification_preference = NOT streak_notification_preference
        WHERE learner_id = %s;
    '''
    
    cmd = cur.mogrify(tmpl, (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    conn.commit()

    # Show the updated state
    print("\n\nAFTER: Learner table ===")
    cmd = cur.mogrify("SELECT learner_id, name, username, user_type, streak, streak_notification_preference FROM Learner WHERE learner_id = %s;", (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    
    print(f"\nDEBUG: Number of rows returned: {len(rows)}")
    if rows:
        print(f"DEBUG: Row data: {rows[0]}")
    
    print(f"\nRESULT: Streak notification preference updated for learner_id = {learner_id}")
    show_table(rows, 'learner_id name username user_type streak streak_notification_preference')

# Test with a freemium user (learner_id 101 - Sarah Chen)
# This will toggle Sarah's notifications from TRUE to FALSE, or FALSE to TRUE
toggle_streak_notifications(101)