from app.main import app

if __name__ == '__main__':
    # run app normally
    app.run(debug=True)
    # allow phone access by running over a local network
    # app.run(debug=True, host='192.168.0.6')