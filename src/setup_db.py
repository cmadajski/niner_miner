def setup_db():
    from main import db, User
    db.create_all()
    # add default accounts for developers
    # create User object with developer info
    christian = User(name='Christian Madajski', id=1234, email=
    'cmadajsk@uncc.edu', password='password2', validation_code='123456', active=True)
    oviya = User(name='Oviya Monoharan', id=704, email=
    'omanohar@uncc.edu', password='oviya123', validation_code='123456', active=True)
    hinal = User(name='Hinal Makadiya', id=111, email=
    'hmakadi1@uncc.edu', password='Niner@123', validation_code='123456', active=True)
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
    db.session.add(professor)
    print('User "Professor" added to database.')
    db.session.add(praveen)
    print('User "Praveen" added to database.')
    # commit new Users to the DB
    db.session.commit()

if __name__ == '__main__':
    setup_db()