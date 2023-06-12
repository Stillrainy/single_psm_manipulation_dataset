import rosbag
import os
import sys
import shutil
from tqdm import tqdm

def change_topic_name(input_bag_path):
    # Create a temporary file for storing modified data
    temp_bag_path = "/tmp/temp.bag"
    
    with rosbag.Bag(temp_bag_path, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(input_bag_path).read_messages():
            if topic == "camera/right/image_color/compressed":
                topic = "/camera/right/image_color/compressed"
            outbag.write(topic, msg, t)

    # Delete the original bag file
    os.remove(input_bag_path)
    # Move the modified temporary file to the original location
    shutil.move(temp_bag_path, input_bag_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python change_topic.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        
        # Collect all bag files
        bag_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # If the file is a .bag file
                if file.endswith(".bag"):
                    file_path = os.path.join(root, file)
                    bag_files.append(file_path)
        
        # Process all bag files with a progress bar
        for file_path in tqdm(bag_files, desc="Processing .bag files"):
            change_topic_name(file_path)
