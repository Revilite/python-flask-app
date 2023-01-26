from website import create_app

#Create instance of app
app = create_app()

if __name__ == '__main__':
  app.run(debug=True)