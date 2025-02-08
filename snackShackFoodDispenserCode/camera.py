from flask import Response, Flask
import cv2

camera = cv2.VideoCapture(0)  # Capture vidéo depuis la webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def start_stream():
    app = Flask(__name__)

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host="0.0.0.0", port=5001)
