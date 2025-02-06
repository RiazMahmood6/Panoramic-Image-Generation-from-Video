import cv2
import numpy as np

def extract_frames(video_path, interval=30):
    """
    Extract frames from a video at a specified interval.
    Args:
        video_path (str): Path to the video file.
        interval (int): Number of frames to skip between extractions.
    Returns:
        list: List of extracted frames.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            frames.append(frame)
        frame_count += 1

    cap.release()
    return frames

def stitch_frames(frames):
    """
    Stitch a list of frames into a panoramic image.
    Args:
        frames (list): List of frames to stitch.
    Returns:
        np.ndarray: The resulting panoramic image.
    """
    # Use OpenCV's Stitcher to create a panorama
    stitcher = cv2.Stitcher_create()  # For OpenCV >= 4.0
    status, pano = stitcher.stitch(frames)

    if status != cv2.Stitcher_OK:
        raise Exception(f"Error during stitching: {status}")
    return pano

def main(video_path, output_path, interval=30):
    """
    Main function to generate a panoramic image from a video.
    Args:
        video_path (str): Path to the video file.
        output_path (str): Path to save the resulting panoramic image.
        interval (int): Number of frames to skip between extractions.
    """
    print("Extracting frames from video...")
    frames = extract_frames(video_path, interval=interval)
    print(f"Extracted {len(frames)} frames.")

    if len(frames) < 2:
        print("Not enough frames to create a panorama. Try reducing the interval.")
        return

    print("Stitching frames into a panoramic image...")
    try:
        panorama = stitch_frames(frames)
        cv2.imwrite(output_path, panorama)
        print(f"Panoramic image saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Path to the input video
    video_path = "video.mp4"  # Replace with your video file path

    # Path to save the output panoramic image
    output_path = "panorama.jpg"  # Replace with your desired output path

    # Interval for frame extraction (adjust based on video FPS and overlap requirements)
    frame_interval = 10  # Use a lower interval for shorter videos

    main(video_path, output_path, frame_interval)






