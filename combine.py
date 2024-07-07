from flask import Flask,render_template, request, jsonify, Response, redirect, url_for, render_template_string,  session 

import mysql.connector
from PIL import Image
import os
import datetime
import cv2
import face_recognition
import base64
import io
import numpy as np
fname=""
check_data = ""


  

def write_file(image_data, filename):
    try:
        print("entered file writing")
        print(filename)
        if not os.path.exists(filename):
            # Create the file if it doesn't exist
            open(filename, 'a').close()

        with open(filename, 'wb') as file:
            print("writing......", filename)
            file.write(image_data)
            print("Written")
    except Exception as e:
        print("Error writing file:", e)

def readBLOB(p_id, photo):
    print("Reading BLOB data from python_employee table")
    global f_name, t_name, arrival, source, l_name,mobile_no,airline
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='sentinel',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        
        sql_fetch_blob_query = """SELECT * from passport_holders where Passport_ID = %s"""

        cursor.execute(sql_fetch_blob_query, (p_id,))
        record = cursor.fetchall()
        print("Storing employee image and bio-data on disk \n")
        for row in record:
            f_name = row[1]
            l_name = row[2]
            t_name = f_name + " " + row[2]
            image = row[10]
            write_file(image, photo)
        
        sql_query_2 = """SELECT * FROM  passengers where Passport_ID = %s"""

        cursor.execute(sql_query_2,(p_id,))
        record = cursor.fetchall()
        for row in record:
            source=row[6]
            arrival=row[7]
            mobile_no=row[4]
            airline=row[5]




    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed") 
            return f_name


def readverification(p_id):
    global pexpiry, vexpiry, p_ex_result, vcheck, v_ex_result, w_check ,h_check, assistance
    h_check = "Y"

    print("Reading data from sentinel")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='sentinel',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        
        sql_query_1 = """SELECT * from passport_holders where Passport_ID = %s"""

        cursor.execute(sql_query_1, (p_id,))
        record = cursor.fetchall()
        print("Storing employee image and bio-data on disk \n")
        for row in record:
            pexpiry=row[7]
            today=datetime.date.today()
            if(pexpiry>today):
               p_ex_result = "Y"
               print("Passport Validity Successful:  ",p_ex_result)
            else:
               print("Invalid Passport")
               p_ex_result = "N"
        
        
        sql_query_3 = """SELECT * FROM visadetails where Passport_ID = %s"""

        cursor.execute(sql_query_3,(p_id,))
        record = cursor.fetchall()
        if record == []:
            vcheck = "N"
            v_ex_result = "N"
            print("No Valid Visa")
        else:
            for row in record:
                if row[1] == p_id:
                    vcheck = "Y"
                    vexpiry = row[2]
                    today=datetime.date.today()
                    if(vexpiry>today):
                        v_ex_result = "Y"
                        print("Visa Validity Successful:  ",v_ex_result)
                    else:
                        v_ex_result = "N"

        

        
        sql_query_4 = """ SELECT * FROM wanted_list where Passport_ID = %s"""
        cursor.execute(sql_query_4,(p_id,))
        record = cursor.fetchall()
        global w_check
        if record == []:
            w_check="N"
        else: 
            for row in record:
                print("Checking criminal activity")
                if row[1] == p_id:
                    print("Wanted")
                    if row[4] == "A" or row[4] == "B":
                        print("Highly Wanted")
                        w_check = "Y"
                    else:
                        w_check = "N"
                        print("No criminal activity found")
        

        sql_query_5 = """ SELECT * FROM healthdetails where Passport_ID = %s"""
        cursor.execute(sql_query_5,(p_id,))
        record = cursor.fetchall()
        for row in record:
            if row[2] == "Y":
                assistance = "Y"
                print("assistance needed")
            else:
                assistance = "N"
                print("no assistance")
            
            if row[3] == "N" and arrival == "Manchester":
                h_check = "N"
                print("no proper vaccine")
            elif row[5] == "N" and arrival == "Tanzania":
                h_check = "N"
                print("no proper vaccine")
            elif row[4] == "N" and arrival == 'China':
                h_check = "N"
                print("no proper vaccine")
            else:
                h_check = "Y"
                print("proper vaccine done")
                
        
        


    except mysql.connector.Error as error:
        print("Failed to read from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed") 
            




def facercg():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    # Load a sample picture and learn how to recognize it.
    path = 'C:/Users/adnan/Documents/Project/FinalProject/Faces'
    os.chdir(path)
    global face_image
    face_image = f'{datetime.date.today()}_{data}.jpg'
    x_image = face_recognition.load_image_file(f'{datetime.date.today()}_{data}.jpg')
    x_face_encoding = face_recognition.face_encodings(x_image)[0]
    # Create arrays of known face encodings and their names
    global known_face_encodings 
    known_face_encodings = [x_face_encoding]
    global known_face_names 
    known_face_names = [fname]
    # Initialize some variables
    global face_locations
    face_locations = []
    global face_encodings
    face_encodings = []
    global face_names
    face_names = []
    global process_this_frame
    process_this_frame = True

def login_check(username,password):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='sentinel',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        print("MYSQL ACTIVATED")
        sql_fetch_blob_query = """SELECT * from officers where username = %s and password = %s"""

        cursor.execute(sql_fetch_blob_query, (username,password))
        record = cursor.fetchall()
        print("RECORD FETCHED")

        if record:
            print("success")
            return "success"
        else:
            print("fail")
            return "fail"
        


    except mysql.connector.Error as error:
        print("Error: ".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




def gen_frames():


    facercg()
    global face_counter
    global check_data
    face_counter = 0
    global total_counter
    total_counter = 0
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            print("camera fail")
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations,)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_counter+=1
                    total_counter+=1
                    print("face = ",face_counter)
                    print("total = ",total_counter)
                    
                        
                    
                    
                        
                else:
                    total_counter+=1

                if face_counter>9:
                        print("success")
                        
                        check_data = "success"
                       
                        
                elif face_counter<4 and total_counter>9:
                        print("fail")
                        check_data = "fail"
                        

                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

def finalnotify():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='sentinel',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        print("MYSQL ACTIVATED")

        sql_fetch_blob_query_1 = """INSERT INTO %s values(%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(sql_fetch_blob_query_1,(arrival,data,f_name,l_name,mobile_no,airline,source,arrival))


        


    except mysql.connector.Error as error:
        print("Error: ".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

app = Flask(__name__,template_folder="templates") 
app.secret_key = os.urandom(24)  # Generate a random secret key for sessions

# Admin Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'admin_db'
}

# Create a connection to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/')
def main():
    return render_template('landing.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    datanew = request.get_json()
    username = datanew.get("username")
    print(username)
    password = datanew.get("password")
    print(password)
    global result

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    admin = cursor.fetchone()
    conn.close()
    print(admin)
    if admin:
        return jsonify({"status": "success"})
    elif not admin:
        return jsonify({"status": "fail"})
    """data=login_check(username,password)
    print('after check',data)
    if data == "success":
        return jsonify({"status": "success"})
    elif data == "fail":
        return jsonify({"status": "fail"})"""



@app.route('/qr')  
def qr(): 
    return render_template('qrscan.html') 
  
@app.route('/process', methods=['POST']) 
def process(): 
    global fname
    global data
    data = request.get_json()
    print('The catregno is: ', data)
    os.getcwd()
    global face_image
    face_image = f'{datetime.date.today()}_{data}.jpg'
    fname=readBLOB(data,os.path.join('Faces',f'{datetime.date.today()}_{data}.jpg'))
    return jsonify({'status':'success'})


@app.route('/face_recog')
           
def face_recog():
    return render_template('face.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/counter',methods=["POST"])
def counter():
    hello=request.get_json()
    i=hello.get("i")

    camera.release()
    if check_data == "success":
        print("SUCCESS SENT TO JS",check_data)
        return jsonify({"status": "success"})
    elif check_data == "fail":
        print("FAIL SENT TO JS",check_data)
        return jsonify({"status": "fail"})
    else:
        print("FAILED TO SEND AT ALL")






  
@app.route('/verification')
def verification():
    im = Image.open(face_image)
    im = im.convert('RGB')
    data = io.BytesIO()
    im.save(data,"JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("tester.html",img_data=encoded_img_data.decode('utf-8'))

@app.route('/details',methods=["POST"])
def details():
    requesting=request.get_json()
    i=requesting.get("i")
    print(fname,data,source,arrival)
    readverification(data)
    return jsonify({'name':t_name,'pid':data,'arrival':arrival})



@app.route('/finalcheck',methods=["POST"])
def finalcheck():
    print(data)
    requesting_new=request.get_json()
    i=requesting_new.get("i")
    print(p_ex_result, vcheck, v_ex_result,w_check,h_check,assistance)
    return jsonify({'passport':p_ex_result,'visacheck':vcheck,'visaresult':v_ex_result,
                    'wanted':w_check,'healthcheck':h_check,'assistance':assistance})





@app.route('/facefail')
def facefail():
    return render_template('qrscan.html')

@app.route('/verified')
def verified():
    return render_template('welcomenew.html')

@app.route('/rejected')
def rejected():
    return render_template('failnew.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')




@app.route('/adminlogincheck', methods=['POST'])
def adminlogincheck():
    datanew = request.get_json()
    username = datanew.get("username")
    print(username)
    password = datanew.get("password")
    print(password)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    admin = cursor.fetchone()
    conn.close()
    print(admin)
    if admin:
        return jsonify({"status": "success"})
    elif not admin:
        return jsonify({"status": "fail"})



@app.route('/adminhome')
def adminhome():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
    conn.close()
    return render_template('adminhome.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                       (name, username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('adminhome'))

    return render_template('add_user.html')


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        cursor.execute("UPDATE users SET name=%s, username=%s, password=%s WHERE id=%s",
                       (name, username, password, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('adminhome'))

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('adminhome'))

@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)

  