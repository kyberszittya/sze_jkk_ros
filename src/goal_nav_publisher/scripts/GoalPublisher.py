import argparse

import rospy
import actionlib
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult

def main():
    parser = argparse.ArgumentParser(description='Give the goal file')
    parser.add_argument('--filename')
    args = parser.parse_args()



    file = open(args.filename,'r')
    rospy.init_node('goalpublisher_node', anonymous=True)

    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    client.wait_for_server()
    rate = rospy.Rate(10)
    rate.sleep()
    msgs = 0
    for line in file:
        rospy.loginfo("Published new goal")
        msg = MoveBaseGoal()
        print(line)
        attrs = line.split(';')
        msg.target_pose.header.frame_id = attrs[0]
        msg.target_pose.pose.position.x = float(attrs[1])
        msg.target_pose.pose.position.y = float(attrs[2])
        msg.target_pose.pose.position.z = float(attrs[3])
        msg.target_pose.pose.orientation.x = float(attrs[4])
        msg.target_pose.pose.orientation.y = float(attrs[5])
        msg.target_pose.pose.orientation.z = float(attrs[6])
        msg.target_pose.pose.orientation.w = float(attrs[7])
        msg.target_pose.header.seq = msgs
        c_now = rospy.Time.now()
        msg.target_pose.header.stamp.secs = c_now.secs
        msg.target_pose.header.stamp.nsecs = c_now.nsecs
        client.send_goal(msg)

        res = client.wait_for_result()
        print res
        rospy.loginfo("Executed goal")
        rate.sleep()
        msgs += 1
        
    while not rospy.is_shutdown():
        rate.sleep()

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass