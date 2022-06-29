from requests import request


def check_new_email(errors, user_info, requested_user):
    # is the email field empty?
    if user_info['email'] == "":
        errors['email'] = True
        errors['email_str'] = 'Email address is required!'
    # is the email a UNCC address?
    elif 'uncc.edu' not in user_info['email']:
        errors['email'] = True
        errors['email_str'] = 'Not a UNCC email address!'
    # does the email already exist in the database?
    elif requested_user != None:
        errors['email'] = True
        errors['email_str'] = 'Email address is already associated with an account!'
    
    return errors

def check_new_password(errors, user_info):
    # is password at least 8 characters long?
    if len(user_info['password']) < 8:
        errors['password'] = True
        errors['password_str'].append('Password not 8+ characters long!')
    # do both passwords equal each other?
    if user_info['password'] != user_info['password_repeat']:
        errors['password'] = True
        errors['password_str'].append('Passwords do not match!')

    return errors

def check_login_email(errors, login_attempt, requested_user):
    if requested_user == None:
        errors['email'] = True
        errors['email_str'] = 'Account does not exist for the given email!'
    # is the requested user activated?
    elif requested_user.is_active() == False:
        errors['email'] = True
        errors['email_str'] = 'Account has not been validated yet!'
    
    return errors

def check_login_password(errors, login_attempt, requested_user):
    # check if password field is empty
    if len(login_attempt['password']) == 0:
        errors['password'] = True
        errors['password_str'] = 'Password required!'

    # check if the attempted password matches the actual password
    elif requested_user.password != login_attempt['password']:
        errors['password'] = True
        errors['password_str'] = 'Password not valid for given email!'

    return errors