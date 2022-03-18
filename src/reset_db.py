def reset_db():
    from main import db
    # remove db
    db.drop_all()
    # create db
    db.create_all()

if __name__ == '__main__':
    reset_db()
    print("Database tables have been reset.")