def setup_db():
    from main import db
    db.create_all()

if __name__ == '__main__':
    setup_db()