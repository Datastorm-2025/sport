import os
import sys
import csv

# Thêm src vào path để import example_perdictor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from src.example_perdictor import predictor

# Sử dụng environment variables hoặc đường dẫn mặc định
INPUT_PATH = os.environ.get('INPUT_PATH', os.path.join(BASE_DIR, 'example', 'input'))
OUTPUT_PATH = os.environ.get('OUTPUT_PATH', os.path.join(BASE_DIR, 'example', 'output'))
OUTPUT_FILENAME = 'submission.csv'

# Các band score hợp lệ
VALID_BANDS = ['band_1_2', 'band_2_4', 'band_4_6', 'band_6_8', 'band_8_10']

# Extensions video được hỗ trợ
VIDEO_EXTENSIONS = ['.mov', '.mp4', '.avi', '.mkv', '.wmv', '.flv']

def validate_paths():
    """Validate input/output paths exist and create output directory if needed."""
    if not os.path.exists(INPUT_PATH):
        print(f"ERROR: Input directory not found: {INPUT_PATH}")
        sys.exit(1)
    
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    print(f"Input path: {INPUT_PATH}")
    print(f"Output path: {OUTPUT_PATH}")


def get_video_files():
    """Get list of video files to process from INPUT_PATH."""
    files = []
    for f in os.listdir(INPUT_PATH):
        ext = os.path.splitext(f)[1].lower()
        if ext in VIDEO_EXTENSIONS:
            files.append(f)
    
    if not files:
        print(f"WARNING: No video files found in {INPUT_PATH}")
        print("Supported formats:", VIDEO_EXTENSIONS)
    
    return sorted(files)


def predict_video(video_path):
    
    # Your code here ...
    score = predictor(video_path)
    
    if score not in VALID_BANDS:
        raise ValueError(f"Invalid score '{score}'. Must be one of {VALID_BANDS}")
    
    return score


def save_predictions(results, output_filename=OUTPUT_FILENAME):
    """
    Save predictions to CSV file.
    
    Format output (CỐ ĐỊNH - KHÔNG THAY ĐỔI):
        file_name,score
        video1.mov,band_1_2
        video2.mov,band_4_6
    
    Args:
        results: List of tuples (file_name, score)
        output_filename: Tên file output (mặc định: submission.csv - CỐ ĐỊNH)
    """
    output_file = os.path.join(OUTPUT_PATH, output_filename)
    
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['file_name', 'score'])
            for file_name, score in results:
                writer.writerow([file_name, score])
        
        return True
    except Exception as e:
        print(f"\nERROR: Failed to save predictions: {e}")
        sys.exit(1)


def run_inference():

    # Validate paths
    validate_paths()
    
    # Get video files
    video_files = get_video_files()
    if not video_files:
        print("\n⚠ WARNING: No video files found to process!")
        print("Creating empty submission file...")
        save_predictions([])
        return
    
    print(f"\n📁 Found {len(video_files)} video file(s) to process")
    print("=" * 60)
    
    # Process each video
    results = []
    errors = []
    
    for i, filename in enumerate(video_files, 1):
        video_path = os.path.join(INPUT_PATH, filename)
        print(f"\n[{i}/{len(video_files)}] Processing: {filename}")
        
        try:
            score = predict_video(video_path)
            results.append((filename, score))
            print(f"  ✓ Predicted: {score}")
        except Exception as e:
            error_msg = f"Failed to predict {filename}: {e}"
            print(f"  ✗ ERROR: {e}")
            errors.append(error_msg)
            # Default fallback score
            results.append((filename, 'band_1_2'))
            print(f"  ⚠ Using default: band_1_2")
    
    # Save results
    print("\n" + "=" * 60)
    print("SAVING RESULTS...")
    print("=" * 60)
    save_predictions(results)
    
    # Summary
    print("\n" + "=" * 60)
    print("INFERENCE SUMMARY")
    print("=" * 60)
    print(f"✓ Total videos processed: {len(video_files)}")
    print(f"✓ Successful predictions: {len(video_files) - len(errors)}")
    if errors:
        print(f"⚠ Errors encountered: {len(errors)}")
        for err in errors:
            print(f"  - {err}")
    print("=" * 60)
    print("✓ INFERENCE COMPLETED SUCCESSFULLY!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_inference()
