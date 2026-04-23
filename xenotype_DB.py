from app import create_app, db
from app.models import Scenario

app = create_app()

with app.app_context():
    db.create_all()

    if Scenario.query.count() == 0:
        scenarios = [
            Scenario(
                title="Distress Signal",
                genre="Sci-Fi",
                difficulty="Easy",
                intro_text="A damaged spacecraft is sending a distress call.",
                passage="SOS... Hull breach detected... oxygen failing...",
                outcome_high="You decoded the signal perfectly and saved the crew.",
                outcome_mid="You decoded most of the signal, but valuable time was lost.",
                outcome_low="The transmission was too corrupted to interpret in time.",
                is_official=True
            ),
            Scenario(
                title="Alien Archive",
                genre="Sci-Fi",
                difficulty="Medium",
                intro_text="An ancient alien archive has been discovered.",
                passage="The archive pulses with strange encoded symbols...",
                outcome_high="You translated the archive with remarkable precision.",
                outcome_mid="You recovered parts of the archive, but some meaning was lost.",
                outcome_low="The archive remained mostly unreadable."
            )
        ]

        db.session.add_all(scenarios)
        db.session.commit()
        print("Starter scenarios added.")

    print("Database ready.")
