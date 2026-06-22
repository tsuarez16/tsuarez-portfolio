from common import *

us = '''
US10 (Simple, Operational): Control Ad Load

As a Freemium User,
I want to toggle a setting that allows me to choose 
“fewer longer ads” or “more shorter ads”
So that the app fits my tolerance without hurting my learning.
'''

print(us)


def update_ad_load_preference(learner_id, new_preference):
    """
    Implements US10:
    Allows a freemium learner to update their ad load preference.
    """

    # Show tables before updating
    print("\nBEFORE UPDATE ===")
    cmd = cur.mogrify("SELECT learner_id, user_type, ad_preference FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id user_type ad_preference')

    if new_preference not in ('fewer longer ads', 'more shorter ads'):
        raise ValueError("Invalid preference. Must be 'fewer_longer' or 'more_shorter'.")

    tmpl = '''
        UPDATE Learner
        SET ad_preference = %s
        WHERE learner_id = %s
          AND user_type = 'freemium';
    '''

    cmd = cur.mogrify(tmpl, (new_preference, learner_id))
    print_cmd(cmd)
    cur.execute(cmd)

    print("\nAFTER UPDATE ===")
    cmd = cur.mogrify("SELECT learner_id, user_type, ad_preference FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id user_type ad_preference')

    print(f"\nRESULT: Updated ad load preference for learner_id = {learner_id} to '{new_preference}' (if freemium).")

update_ad_load_preference(105, 'more shorter ads')
