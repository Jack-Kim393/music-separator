
import os
import uuid
import threading
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory

# Flask 앱 초기화
app = Flask(__name__, template_folder='templates', static_folder='static')

# 업로드된 파일 및 분리된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
SEPARATED_FOLDER = 'separated_music'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SEPARATED_FOLDER, exist_ok=True)

# 작업 상태를 저장할 딕셔너리
tasks = {}

def run_separation(task_id, input_path, output_dir):
    """
    별도의 스레드에서 Spleeter 음원 분리 스크립트를 실행합니다.
    """
    try:
        tasks[task_id]['status'] = 'processing'
        
        # music_separator.py 스크립트 실행
        # 가상환경의 python을 사용하도록 경로를 지정할 수 있습니다.
        # 가상환경의 python 실행 파일을 직접 지정합니다.
        python_executable = os.path.join('.venv', 'Scripts', 'python.exe')
        command = [
            python_executable, 
            '.venv/music_separator.py', 
            '-i', input_path, 
            '-o', output_dir
        ]
        
        # subprocess를 실행하고 완료될 때까지 기다립니다.
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        
        tasks[task_id]['status'] = 'complete'
        print(f"Task {task_id} completed successfully.")
        print("Stdout:", process.stdout)

    except subprocess.CalledProcessError as e:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['message'] = e.stderr
        print(f"Error processing task {task_id}: {e.stderr}")
    except Exception as e:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['message'] = str(e)
        print(f"An unexpected error occurred in task {task_id}: {e}")


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
        # 입력 파일을 저장할 경로
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # 새 작업을 생성
        task_id = str(uuid.uuid4())
        tasks[task_id] = {'status': 'pending'}

        # 백그라운드에서 음원 분리 작업 시작
        thread = threading.Thread(target=run_separation, args=(task_id, input_path, SEPARATED_FOLDER))
        thread.start()

        return jsonify({"task_id": task_id})

@app.route('/api/status/<task_id>')
def task_status(task_id):
    """
    특정 작업의 진행 상태를 반환합니다.
    """
    task = tasks.get(task_id, {})
    return jsonify({"status": task.get('status', 'not_found'), "message": task.get('message', '')})

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
                            "url": f"/{SEPARATED_FOLDER}/{song_folder}/{file}"
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
    # host='0.0.0.0'으로 설정하여 외부에서도 접속 가능하게 합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)
