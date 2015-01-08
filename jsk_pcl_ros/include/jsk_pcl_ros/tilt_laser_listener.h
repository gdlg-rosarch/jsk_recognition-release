// -*- mode: c++ -*-
/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2014, JSK Lab
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/o2r other materials provided
 *     with the distribution.
 *   * Neither the name of the Willow Garage nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 *  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 *  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 *********************************************************************/


#ifndef JSK_PCL_ROS_TILT_LASER_LISTENER_H_
#define JSK_PCL_ROS_TILT_LASER_LISTENER_H_

#include <jsk_topic_tools/diagnostic_nodelet.h>
#include <sensor_msgs/JointState.h>
#include <jsk_pcl_ros/TimeRange.h>
#include "jsk_pcl_ros/line_segment_collector.h"

namespace jsk_pcl_ros
{
  class StampedJointAngle
  {
  public:
    typedef boost::shared_ptr<StampedJointAngle> Ptr;
    StampedJointAngle(const std_msgs::Header& header_arg, const double& value);
    virtual ~StampedJointAngle() {}
    std_msgs::Header header;
    virtual double getValue() { return value_; }
  protected:
    double value_;
  private:
    
  };
  
  class TiltLaserListener: public jsk_topic_tools::DiagnosticNodelet
  {
  public:
    TiltLaserListener(): DiagnosticNodelet("TiltLaserListener") { };
    enum LaserType {
      INFINITE_SPINDLE, INFINITE_SPINDLE_HALF, TILT, TILT_HALF_UP, TILT_HALF_DOWN
    };
  protected:
    ////////////////////////////////////////////////////////
    // methods
    ////////////////////////////////////////////////////////
    virtual void onInit();
    virtual void subscribe();
    virtual void unsubscribe();
    virtual void jointCallback(const sensor_msgs::JointState::ConstPtr& msg);
    virtual void updateDiagnostic(
      diagnostic_updater::DiagnosticStatusWrapper &stat);
    virtual void processTiltHalfUp(const ros::Time& stamp, const double& value);
    virtual void processTiltHalfDown(const ros::Time& stamp, const double& value);
    virtual void processTilt(const ros::Time& stamp, const double& value);
    virtual void processInfiniteSpindle(
      const ros::Time& stamp, const double& joint_angle, const double& velocity,
      const double& threshold);
    virtual void publishTimeRange(const ros::Time& stamp,
                                  const ros::Time& start,
                                  const ros::Time& end);
    ////////////////////////////////////////////////////////
    // ROS variables
    ////////////////////////////////////////////////////////
    ros::Subscriber sub_;
    ros::Publisher trigger_pub_;
    ros::Publisher cloud_pub_;
    ros::ServiceClient assemble_cloud_srv_;
    ////////////////////////////////////////////////////////
    // parameters
    ////////////////////////////////////////////////////////
    LaserType laser_type_;
    std::string joint_name_;
    double prev_angle_;
    double prev_velocity_;
    ros::Time start_time_;
    bool use_laser_assembler_;
    
    TimeStampedVector<StampedJointAngle::Ptr> buffer_;
  private:
    
  };
}

#endif
