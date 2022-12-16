import cv2

def VideoReader(video_path, show=False):
    cap = cv2.VideoCapture(video_path)
    if (cap.isOpened() == False): 
        print("Error opening video stream or file")

    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            if show:
                # Display the resulting frame
                cv2.imshow('Frame',frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                yield frame

        # Break the loop
        else:
            yield False
            break

    # When everything done, release the video capture object
    cap.release()

if __name__ == '__main__':
    vid_path = 'test.avi'
    video_reader = VideoReader(vid_path)
    frame = next(video_reader)
    count = 0
    while frame is not False:
        print(f"Count: {count} | Shape: {frame.shape}")
        count += 1
        frame = next(video_reader)
