document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');
    const trackList = document.getElementById('track-list');

    // 초기 트랙 목록 로드
    loadTracks();

    // 드래그 앤 드롭 이벤트 처리
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
    });

    dropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFiles(files);
        }
    }, false);

    // 파일 선택 버튼 이벤트
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFiles(fileInput.files);
        }
    });

    function handleFiles(files) {
        const file = files[0];
        if (file && file.type.startsWith('audio/')) {
            uploadFile(file);
        } else {
            updateStatus('오디오 파일만 업로드할 수 있습니다.', true);
        }
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        updateStatus(`'${file.name}' 업로드 중...`);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.task_id) {
                updateStatus('파일 업로드 완료. 음원 분리를 시작합니다...');
                checkStatus(data.task_id);
            } else {
                throw new Error(data.error || '업로드에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Upload Error:', error);
            updateStatus(`업로드 오류: ${error.message}`, true);
        });
    }

    function checkStatus(taskId) {
        const interval = setInterval(() => {
            fetch(`/api/status/${taskId}`)
                .then(response => response.json())
                .then(data => {
                    switch (data.status) {
                        case 'processing':
                            updateStatus('음원 분리 중... 잠시만 기다려주세요.');
                            break;
                        case 'complete':
                            clearInterval(interval);
                            updateStatus('🎉 음원 분리 완료!', false, 5000);
                            loadTracks();
                            break;
                        case 'error':
                            clearInterval(interval);
                            updateStatus(`오류 발생: ${data.message}`, true);
                            break;
                        case 'not_found':
                            clearInterval(interval);
                            updateStatus('작업을 찾을 수 없습니다.', true);
                            break;
                    }
                })
                .catch(error => {
                    clearInterval(interval);
                    console.error('Status Check Error:', error);
                    updateStatus('상태 확인 중 오류가 발생했습니다.', true);
                });
        }, 3000); // 3초마다 상태 확인
    }

    function loadTracks() {
        updateStatus('분리된 트랙 목록을 불러오는 중...');
        fetch('/api/tracks')
            .then(response => response.json())
            .then(data => {
                trackList.innerHTML = ''; // 목록 초기화
                if (data.length === 0) {
                    trackList.innerHTML = '<p class="loading-message">분리된 곡이 없습니다. 새 음원을 업로드 해보세요.</p>';
                } else {
                    data.reverse().forEach(song => {
                        const trackItem = document.createElement('div');
                        trackItem.className = 'track-item';

                        let tracksHtml = `<h3>${song.original_title}</h3>`;
                        song.tracks.sort((a, b) => a.name.localeCompare(b.name)); // 이름순 정렬 (accompaniment, vocals)

                        song.tracks.forEach(track => {
                            tracksHtml += `
                                <div class="audio-player">
                                    <p>${track.name.charAt(0).toUpperCase() + track.name.slice(1)}</p>
                                    <audio controls src="${track.url}"></audio>
                                    <a href="${track.url}" download class="download-link">↓ ${track.name}.wav 다운로드</a>
                                </div>
                            `;
                        });

                        trackItem.innerHTML = tracksHtml;
                        trackList.appendChild(trackItem);
                    });
                }
                updateStatus(''); // 상태 메시지 클리어
            })
            .catch(error => {
                console.error('Load Tracks Error:', error);
                trackList.innerHTML = '<p class="loading-message">트랙 목록을 불러오는 데 실패했습니다.</p>';
                updateStatus('');
            });
    }

    function updateStatus(message, isError = false, clearAfter = 0) {
        uploadStatus.textContent = message;
        uploadStatus.style.color = isError ? '#e74c3c' : '#2c3e50';

        if (clearAfter > 0) {
            setTimeout(() => {
                uploadStatus.textContent = '';
            }, clearAfter);
        }
    }
});
