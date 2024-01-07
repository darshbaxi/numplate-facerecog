from frameIdea import process_video


frame = process_video('backend/TestVid.mp4', 'backend/output_images')

output_filename = f"processed_frame_{frame_index // int(fps)}.png"
cv2.imwrite(output_path + '/' + output_filename, frame)
            