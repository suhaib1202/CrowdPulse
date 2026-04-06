from flask import Flask, Response, render_template, jsonify
import cv2
import time
import threading
from detector import analyze_frame

app = Flask(__name__)

# Shared state
latest_score = 0
latest_total = 0
latest_engaged = 0
score_history = []
lock = threading.Lock()

camera = cv2.VideoCapture(0)

def generate_frames():
    global latest_score, latest_total, latest_engaged, score_history

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Mirror effect

        score, total, engaged, face_data = analyze_frame(frame)

        with lock:
            latest_score = score
            latest_total = total
            latest_engaged = engaged
            timestamp = time.strftime("%H:%M:%S")
            score_history.append({"time": timestamp, "score": score})
            if len(score_history) > 60:
                score_history.pop(0)

        # Draw coloured dots on faces
        for face in face_data:
            colour = (0, 255, 0) if face["engaged"] else (0, 0, 255)
            label = "Engaged" if face["engaged"] else "Zoned Out"
            cv2.circle(frame, face["position"], 12, colour, -1)
            cv2.putText(frame, label, 
                        (face["position"][0] - 30, face["position"][1] - 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, colour, 1)

        # Overlay score on video
        cv2.rectangle(frame, (0, 0), (300, 50), (0, 0, 0), -1)
        cv2.putText(frame, f"Engagement: {score}%  |  Faces: {total}",
                    (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        time.sleep(0.05)  # ~20 FPS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    with lock:
        return jsonify({
            "score": latest_score,
            "total": latest_total,
            "engaged": latest_engaged,
            "history": score_history[-20:]
        })

if __name__ == '__main__':
    app.run(debug=False, threaded=True)