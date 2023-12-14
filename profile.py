from flask import Flask, render_template, request, flash,redirect
from werkzeug.security import generate_password_hash, check_password_hash
import binascii
import base64
app = Flask(__name__)


def update_pp(db,profile_picture,current_user):
    
    if profile_picture:
        image_data = profile_picture.read()
        cursor = db.cursor()
        cursor.execute('UPDATE users SET profile_picture=%s WHERE id=%s', (image_data, current_user.id))
        db.commit()

        flash('Profile picture updated successfully', 'success')

       

def update_password(db,old_password,new_password,confirm_password,current_user):
           
    if check_password_hash(current_user.password, old_password):
        if new_password == confirm_password:
            new_hash = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
            cursor = db.cursor()
            cursor.execute('UPDATE users SET password_hash=%s WHERE id=%s', (new_hash, current_user.id))
            db.commit()
            flash('Password updated successfully', 'success')
        else:
            flash('New password and confirm password do not match', 'error')
    else:
        flash('Invalid old password', 'error')
    

@app.route('/profile', methods=['GET', 'POST'])
def profile_page(db, current_user):
    cursor = db.cursor()
    cursor.execute("select profile_picture from users where id=%s;",(current_user.id,))
    byte_pic=cursor.fetchall()
    blob_data=byte_pic[0][0]
    base64_image = base64.encodebytes(blob_data)
    
    if request.method == 'POST':
        operation =request.form['operation']
        if operation=="1":
            old_password = request.form['oldPassword']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']  
            update_password(db,old_password,new_password,confirm_password,current_user)
        else:
            profile_picture = request.files['profile_picture']
            update_pp(db,profile_picture,current_user)
        
    return render_template("profile.html",base64_image=base64_image)

if __name__ == '__main__':
    app.run(debug=True)
