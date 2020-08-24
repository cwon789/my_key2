#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

import sys, select, termios, tty

ROSCAR_MAX_ACCELL_VEL = 180
ROSCAR_MAX_STEERING_VEL = 180
BALLSCREW_MAX_VEL = 180

ROSCAR_MIN_ACCELL_VEL = 0
ROSCAR_MIN_STEERING_VEL = 0
BALLSCREW_MIN_VEL = 180

msg = """
Control Your ROSCAR!
---------------------------
Moving around:

        w        t

   a    s    d   g

        x        b
w/x : increase/decrease accell velocity
a/d : increase/decrease steering velocity
t/b : ballscrew control
g   : ballscrew stop
space key, s : force stop
CTRL-C to quit
"""

e = """
Communications Failed
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
         key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(target_accell_vel, target_angular_vel, target_ballscrew_vel):
    return "currently: \n accell vel    %s\n steering vel  %s\n ballscrew vel %s " % (target_accell_vel,target_steering_vel,target_ballscrew_vel)





if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)


    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('roscar_teleop',anonymous=True)


    status = 0
    target_accell_vel = 0
    target_steering_vel = 0
    target_ballscrew_vel = 0

    try:
        print (msg)
        while(1):
            key = getKey()
            if key == 'w' :
                target_accell_vel =0.1
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'x' :
                target_accell_vel =-0.1
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'a' :
                target_steering_vel =0.6
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 'd' :
                target_steering_vel =-0.6
                status = status + 1
                print (vels(target_accell_vel,target_steering_vel,target_ballscrew_vel))
            elif key == 's'  :
                target_accell_vel   = 0
                target_steering_vel  = 0
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 't':
                target_ballscrew_vel =0.3
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 'b' :
                target_ballscrew_vel =-0.3
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            elif key == 'g' :
                target_ballscrew_vel =0
                status +=1
                print (vels(target_accell_vel, target_steering_vel,target_ballscrew_vel))
            else:
                if (key == '\x03'):
                    break
            if status == 20 :
                print (msg)
                status = 0

            twist = Twist()
            twist.linear.x = target_accell_vel; twist.linear.y = target_ballscrew_vel; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = target_steering_vel
            pub.publish(twist)






    except rospy.ROSInterruptException:
        pass

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
