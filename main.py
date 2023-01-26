from website import create_app
import os

#Create instance of app
app = create_app()

if __name__ == '__main__':
  app.run(debug=True, port=os.getenv("PORT", default=3001))