import rospy
from geometry_msgs.msg import PoseStamped

import datetime

class GoalWriter():
    def __init__(self):
        c_now = datetime.datetime.now()
        self.f = open(str(c_now.year)
            +str(c_now.month)+str(c_now.day)
            +str(c_now.hour)+str(c_now.minute)
            +str(c_now.second)+".goals",'w')
    def callback_goal(self, data):
        line = str(data.header.frame_id)+";"
        line += str(data.pose.position.x)+";"
        line += str(data.pose.position.y)+";"
        line += str(data.pose.position.z)+";"
        line += str(data.pose.orientation.x)+";"
        line += str(data.pose.orientation.y)+";"
        line += str(data.pose.orientation.z)+";"
        line += str(data.pose.orientation.w)+";"
        line += '\n'
        print(line)
        self.f.write(line)

def main():
    rospy.init_node('goal_receiver')
    rospy.loginfo("Receiving goals")
    gw = GoalWriter()
    rospy.Subscriber("move_base_simple/goal", 
        PoseStamped, gw.callback_goal)    
    rospy.spin()
    

if __name__=='__main__':
    main()
    