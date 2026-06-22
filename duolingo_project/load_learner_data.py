from common import *
import csv

print("Loading Learner data from CSV...")

# Path to your CSV file
csv_file = '/Users/tatesuarez/Desktop/67-262/finalproject/data/Learner.csv'

# Read the CSV file
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Prepare the INSERT statement
        tmpl = '''
            INSERT INTO Learner (
                learner_id, name, username, last_login, languages_learned,
                total_xp, streak, user_type, current_hearts, ad_preference,
                subscription_date, card_number, streak_notification_preference
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (learner_id) DO UPDATE SET
                name = EXCLUDED.name,
                username = EXCLUDED.username,
                last_login = EXCLUDED.last_login,
                languages_learned = EXCLUDED.languages_learned,
                total_xp = EXCLUDED.total_xp,
                streak = EXCLUDED.streak,
                user_type = EXCLUDED.user_type,
                current_hearts = EXCLUDED.current_hearts,
                ad_preference = EXCLUDED.ad_preference,
                subscription_date = EXCLUDED.subscription_date,
                card_number = EXCLUDED.card_number,
                streak_notification_preference = EXCLUDED.streak_notification_preference;
        '''
        
        # Convert empty strings to None for nullable fields
        subscription_date = row['subscription_date'] if row['subscription_date'] else None
        card_number = row['card_number'] if row['card_number'] else None
        ad_preference = row['ad_preference'] if row['ad_preference'] else None
        current_hearts = int(row['current_hearts']) if row['current_hearts'] else None
        
        # Convert TRUE/FALSE strings to boolean
        streak_notif = True if row['streak_notification_preference'] == 'TRUE' else False
        
        values = (
            int(row['learner_id']),
            row['name'],
            row['username'],
            row['last_login'],
            row['languages_learned'],
            int(row['total_xp']),
            int(row['streak']),
            row['user_type'],
            current_hearts,
            ad_preference,
            subscription_date,
            card_number,
            streak_notif
        )
        
        cmd = cur.mogrify(tmpl, values)
        cur.execute(cmd)
        print(f"Inserted/Updated learner_id {row['learner_id']}: {row['name']}")

# Commit all changes
conn.commit()

print("\n✓ All learner data loaded successfully!")

# Verify the data
print("\nVerifying loaded data:")
cmd = cur.mogrify("SELECT learner_id, name, username, user_type, streak, streak_notification_preference FROM Learner ORDER BY learner_id;", ())
cur.execute(cmd)
rows = cur.fetchall()

print(f"\nTotal learners in database: {len(rows)}")
for row in rows:
    print(f"  {row}")
