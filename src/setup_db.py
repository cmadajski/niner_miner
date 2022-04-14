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
    # add new User to staging
    db.session.add(christian)
    db.session.add(oviya)
    db.session.add(hinal)
    # commit new Users to the DB
    db.session.commit()

if __name__ == '__main__':
    setup_db()