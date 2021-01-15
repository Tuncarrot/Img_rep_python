from imgRepFlask import create_app

app = create_app() # using config file as default

if __name__ == '__main__':
    app.run(debug=True)