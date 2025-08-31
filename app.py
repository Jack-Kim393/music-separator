import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from celery import Celery
import subprocess

from werkzeug.utils import secure_filename

# Flask 앱 초기화
app = Flask(__name__, template_folder='templates', static_folder='static')

# Celery 설정
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_ACCEPT_CONTENT'] = ['json']

# Celery 인스턴스 생성
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 업로드된 파일 및 분리된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
SEPARATED_FOLDER = 'separated_music'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SEPARATED_FOLDER, exist_ok=True)

@celery.task(bind=True)
def run_separation(self, input_path, output_dir):
    """
    Celery 작업으로 Spleeter 음원 분리를 실행합니다.
    """
    try:
        self.update_state(state='PROCESSING')
        
        # Spleeter 실행 명령어
        command = [
            'spleeter', 
            'separate',
            '-p', 'spleeter:2stems', 
            '-o', output_dir,
            input_path
        ]
        
        # subprocess를 실행하고 완료될 때까지 기다립니다.
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        
        return {'status': 'SUCCESS', 'stdout': process.stdout}

    except subprocess.CalledProcessError as e:
        return {'status': 'FAILURE', 'error': e.stderr}
    except Exception as e:
        return {'status': 'FAILURE', 'error': str(e)}

@app.route('/')
def index():
    """
    메인 UI 페이지를 렌더링합니다.
    """
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    오디오 파일을 업로드하고 음원 분리 작업을 시작합니다.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Celery 작업 시작
        task = run_separation.delay(input_path, SEPARATED_FOLDER)

        return jsonify({"task_id": task.id})

@app.route('/api/status/<task_id>')
def task_status(task_id):
    """
    특정 작업의 진행 상태를 반환합니다.
    """
    task = run_separation.AsyncResult(task_id)
    response = {
        'status': task.state,
    }
    if task.state == 'SUCCESS':
        result = task.get()
        response['status'] = result.get('status')
        if response['status'] == 'FAILURE':
            response['message'] = result.get('error')
        else:
            response['result'] = result
    elif task.state == 'FAILURE':
        # This should not happen anymore, but as a fallback
        response['message'] = str(task.info)
    
    return jsonify(response)

@app.route('/api/tracks')
def get_tracks():
    """
    분리 완료된 모든 트랙의 목록을 반환합니다.
    """
    track_list = []
    if os.path.exists(SEPARATED_FOLDER):
        for song_folder in os.listdir(SEPARATED_FOLDER):
            song_path = os.path.join(SEPARATED_FOLDER, song_folder)
            if os.path.isdir(song_path):
                tracks = {
                    "original_title": song_folder,
                    "tracks": []
                }
                for file in os.listdir(song_path):
                    if file.endswith('.wav'):
                        track_name = os.path.splitext(file)[0]
                        tracks['tracks'].append({
                            "name": track_name,
                            "url": f"/separated_music/{song_folder}/{file}"
                        })
                track_list.append(tracks)
    return jsonify(track_list)

@app.route('/separated_music/<path:filename>')
def serve_separated_file(filename):
    """
    분리된 오디오 파일을 서빙합니다.
    """
    return send_from_directory(SEPARATED_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)