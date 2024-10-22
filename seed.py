import csv
from datetime import datetime
from app import app, db
from models import Episode, Guest, Appearance

def seed_data_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year = row['YEAR']
            occupation = row['GoogleKnowlege_Occupation']
            show_date = row['Show']
            group = row['Group']
            guest_list = row['Raw_Guest_List']

            # Convert the show_date string to a Python date object
            try:
                air_date = datetime.strptime(show_date, '%m/%d/%y').date()
            except ValueError:
                print(f"Error parsing date: {show_date}")
                continue

            # Query the Episode model using the air_date
            episode = Episode.query.filter_by(air_date=air_date).first()

            if not episode:
                episode = Episode(
                    title=group,
                    year=year,
                    air_date=air_date  # Now this is a proper date object
                )
                db.session.add(episode)
                db.session.commit()

            for guest_name in guest_list.split(','):
                guest = Guest.query.filter_by(name=guest_name.strip()).first()

                if not guest:
                    guest = Guest(name=guest_name.strip(), occupation=occupation)
                    db.session.add(guest)
                    db.session.commit()

                appearance = Appearance.query.filter_by(guest_id=guest.id, episode_id=episode.id).first()

                if not appearance:
                    appearance = Appearance(
                        guest_id=guest.id,
                        episode_id=episode.id,
                        role=None  # Add any necessary role if applicable
                    )
                    db.session.add(appearance)
                    db.session.commit()

# Set up Flask application context
with app.app_context():
    seed_data_from_csv('seed.csv')
