from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from MoistureReadingsFrontEnd.database.models import MoistureReading
    db.drop_all()
    db.create_all()
