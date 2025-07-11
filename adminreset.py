from app import app, db, User
from werkzeug.security import generate_password_hash

def update_user(email, new_email=None, new_password=None):
    with app.app_context():   # <-- application context starts here
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found!")
            return
        if new_email:
            user.email = new_email
        if new_password:
            user.password = generate_password_hash(new_password)
        db.session.commit()
        print("User updated!")

if __name__ == "__main__":
    update_user("filipowskimark@gmail.com", new_email="new@example.com", new_password="newpassword123")
