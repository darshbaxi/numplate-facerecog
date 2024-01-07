import cv2


def process_video(video_path, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get frames per second (fps)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create the output directory if it doesn't exist
    import os
    os.makedirs(output_path, exist_ok=True)

    # Loop through each frame
    frame_index = 0
    while True:
        # Read the frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            break

        if frame_index % int(fps) == 0:
            output_filename = f"processed_frame_{frame_index // int(fps)}.png"
            cv2.imwrite(output_path + '/' + output_filename, frame)
            return frame
    
        # Process the frame and save it at specified intervals
        # process_frame(frame, output_path, frame_index, fps)

        frame_index += 1

    # Release the video capture object
    cap.release()

# Replace 'your_video.mp4' with the path to your video file
# Replace 'output_frames' with the desired output directory
