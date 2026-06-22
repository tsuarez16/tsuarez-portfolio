from common import *

us = '''
US2 (Simple, Analytical): View current hearts count and maximum hearts limit


As a Freemium user, I want to view my current hearts count and maximum hearts limit,
so I know how many mistakes I can make before losing access to lessons.
'''

print(us)


def view_hearts_info(learner_id):
    
    """
    Implements US2:
    As a Freemium user, I want to view my current hearts count and maximum hearts limit,
    so I know how many mistakes I can make before losing access to lessons.
    """

    # Show tables before running the US2 query
    print("\nBEFORE: Relevant tables ===")

    # Learner table
    print("\nLearner table:")
    cmd = cur.mogrify("SELECT * FROM Learner ORDER BY learner_id;", ())
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    show_table(rows, 'learner_id name username last_login languages_learned total_xp streak user_type current_hearts ad_preference subscription_date card_number streak_notification_preference')

    # View hearts information for the specific freemium learner
    print(f"\nVIEWING hearts information for learner_id = {learner_id}")
    
    # Maximum hearts for freemium users is 5 (this is a business rule)
    max_hearts = 5
    
    tmpl = '''
        SELECT name, current_hearts, user_type
        FROM Learner
        WHERE learner_id = %s AND user_type = 'freemium';
    '''
    
    cmd = cur.mogrify(tmpl, (learner_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    
    # Display the results in table form
    if rows:
        # Add max_hearts to each row for display
        display_rows = [(rows[0][0], rows[0][1], max_hearts, rows[0][2])]
        
        print(f"\nRESULT: Hearts information for learner_id = {learner_id}")
        cols = 'name current_hearts maximum_hearts user_type'
        show_table(display_rows, cols)
    else:
        print(f"\nNo freemium user found with learner_id = {learner_id}")
        print("This user story is only available for freemium users.")

# Test with a freemium user (learner_id 101 - Sarah Chen)
view_hearts_info(101)

#Test with a premium user (learner_id 103 - Rebecca Sucgang)
view_hearts_info(103)