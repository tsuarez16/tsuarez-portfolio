from common import *

us = '''
US3 (Complex, Operational): Hearts decrease when getting something wrong


As a Learner,
I want to see my hearts decrease when I get something wrong,
So that I understand how many more chances I get until my hearts are over
'''

print(us)


def decrease_hearts_on_mistake(learner_id, exercise_id):
    
    """
    Implements US3:
    Demonstrates the trigger that decreases hearts when a learner gets something wrong.
    When an incorrect attempt (is_correct = FALSE) is inserted into Attempt table,
    the trigger automatically decreases the learner's current_hearts.
    """

    # Show tables before running the US3 query
    print("\nBEFORE: Relevant tables ===")

    # Learner table
    print("\nLearner table:")
    cmd = cur.mogrify("SELECT * FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id name username last_login languages_learned total_xp streak streak_notification_preference user_type current_hearts ad_preference subscription_date card_number')

    # Attempt table
    print("\nAttempt table:")
    cmd = cur.mogrify("SELECT * FROM Attempt ORDER BY attempt_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'attempt_id attempted_at is_correct learner_id')

    print(f"\nINSERTING incorrect attempt for learner_id = {learner_id} (trigger will decrease hearts)")
    
    # Get the next attempt_id
    cur.execute("SELECT COALESCE(MAX(attempt_id), 0) + 1 FROM Attempt;")
    next_attempt_id = cur.fetchone()[0]
    
    # Insert an incorrect attempt - the trigger will automatically decrease hearts
    tmpl = '''
        INSERT INTO Attempt (attempt_id, attempted_at, is_correct, learner_id)
        VALUES (%s, NOW(), FALSE, %s);
    '''
    
    cmd = cur.mogrify(tmpl, (next_attempt_id, learner_id))
    print_cmd(cmd)
    cur.execute(cmd)
    conn.commit()

    # Show the updated state
    print("\nAFTER: Updated tables ===")
    
    # Show updated Learner hearts
    print("\nLearner table (showing hearts decrease):")
    cmd = cur.mogrify("SELECT learner_id, name, current_hearts, user_type FROM Learner WHERE learner_id = %s;", (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    
    print(f"\nRESULT: Hearts decreased for learner_id = {learner_id}")
    cols = 'learner_id name current_hearts user_type'
    show_table(rows, cols)

# Test with learner_id 101 (Sarah Chen) - a freemium user getting something wrong
decrease_hearts_on_mistake(101, 5001)