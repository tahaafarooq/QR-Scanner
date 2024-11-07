from flask import Flask, render_template, Response, request, url_for
from helpers import camera, gen_frames
from model import db, Invitees
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qr_invite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

detector = cv2.QRCodeDetector()

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_invitees', methods=['GET', 'POST'])
def add_invites():
    if request.method == 'GET':
        return render_template('add_invites.html')
    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        location = request.form.get('location')

        if first_name is not None and last_name is not None and location is not None:
            # first check if user exists
            check = Invitees.query.filter_by(first_name=first_name).first()
            if check is not None:
                if check.last_name == last_name:
                    return render_template('add_invites.html', output='User Exists!')
            else:
                # add the new invitees to the DB
                push = Invitees(first_name, last_name, location)
                db.session.add(push)
                db.session.commit()

                return render_template('add_invites.html', output='User Added')
        else:
            return render_template('add_invites.html', output='Try Again')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture', methods=['GET'])
def capture_qr():
    success, frame = camera.read()
    if success:
        # save the captured image
        cv2.imwrite('capture_image.jpeg', frame)
        # attempt to check if the image captured is a QR code
        data, points, _ = detector.detectAndDecode(frame)
        if points is not None:
            print(data)
            return render_template('index.html', output="QR Code Saved")
        else:
            return render_template('index.html', output="No QR Code Identified!")
    else:
        return render_template('index.html', output="Failed To Capture Image!")


if __name__ == '__main__':
    app.run(debug=True)

