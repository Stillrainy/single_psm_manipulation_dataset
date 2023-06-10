import rosbag
import os
import sys
import shutil

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
        print("Usage: python change_topic.py <input_bag_path>")
    else:
        change_topic_name(sys.argv[1])
