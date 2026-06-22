from common import *

us = '''
US5 (Simple, Operational): View current payment method for Duolingo Max users


As a Max user,
I want to view my current payment method on file,
So that I can verify my subscription payment information
'''

print(us)


def view_payment_method(learner_id):
    
    """
    Implements US5:
    As a Max user, view the current payment method (card number) and subscription details.
    """

    # Show tables before running the US5 query
    print("\nBEFORE: Relevant tables ===")

    # Learner table
    print("\nLearner table:")
    cmd = cur.mogrify("SELECT * FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id name username last_login languages_learned total_xp streak user_type current_hearts ad_preference subscription_date card_number streak_notification_preference')

    print(f"\nVIEWING payment method for learner_id = {learner_id}")
    
    tmpl = '''
        SELECT name, card_number, subscription_date, ad_preference
        FROM Learner
        WHERE learner_id = %s AND user_type = 'max';
    '''
    
    cmd = cur.mogrify(tmpl, (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    
    print(f"\nRESULT: Payment method for learner_id = {learner_id}")
    cols = 'name card_number subscription_date ad_preference'
    show_table(rows, cols)

# Test with learner_id 103 (Rebecca Sucgang) - a max user
view_payment_method(103)