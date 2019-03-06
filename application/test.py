from app import app
from db_setup import init_db
 
init_db()
 
 
@app.route('/')
def test():
    return "welcome to this group!"
 
if __name__ == '__main__':
    app.run()
