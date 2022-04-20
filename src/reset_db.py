def reset_db():
    from main import db, User
    # remove db
    db.drop_all()
    print('Database deleted.')
    # create db
    db.create_all()
    print('Database created.')
    # add default accounts for developers
    # create User object with developer info
    christian = User(name='Christian Madajski', id=1234, email=
    'cmadajsk@uncc.edu', phone='980-290-0679', password='password2', validation_code='123456', active=True)
    oviya = User(name='Oviya Monoharan', id=704, email=
    'omanohar@uncc.edu', phone='111-222-3333', password='oviya123', validation_code='123456', active=True)
    hinal = User(name='Hinal Makadiya', id=111, email=
    'hmakadi1@uncc.edu', phone='1234567890', password='Niner@123', validation_code='123456', active=True)
    drew =  User(name='Drew Moore', id=696969, email=
    'dmoor121@uncc.edu', phone='336-880-4733', password='Drew1212!', validation_code='123456', active=True)
    professor = User(name='Dr. Rudd', id=1357, email=
    'jrudd@uncc.edu', password='bestprofessor1234', validation_code='123456', active=True)
    praveen = User(name='Praveen Kumar Gavara', id=2468, email=
    'pgavara@uncc.edu', password='awesometa1234', validation_code='123456', active=True)
    # add new Users to staging
    db.session.add(christian)
    print('User "Christian" added to database.')
    db.session.add(oviya)
    print('User "Oviya" added to database.')
    db.session.add(hinal)
    print('User "Hinal" added to database.')
    db.session.add(drew)
    print('User "Drew" added to database.')
    db.session.add(professor)
    print('User "Professor" added to database.')
    db.session.add(praveen)
    print('User "Praveen" added to database.')
    # commit new Users to the DB
    db.session.commit()

if __name__ == '__main__':
    reset_db()
    print("Database reset complete.")