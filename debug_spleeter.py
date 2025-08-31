
import sys
from spleeter.separator import Separator
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python debug_spleeter.py <path_to_audio_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = "/app/separated_music/debug_output"
    
    print(f"--- DEBUG: STARTING SEPARATION FOR {input_file} ---")
    
    try:
        # Spleeter 분리기 초기화
        separator = Separator('spleeter:2stems')
        
        # 분리 실행
        separator.separate_to_file(input_file, output_dir)
        
        print(f"--- DEBUG: FINISHED SEPARATION ---")
        
    except Exception as e:
        print(f"--- DEBUG: ERROR ---")
        import traceback
        traceback.print_exc()

