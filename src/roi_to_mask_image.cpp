// -*- mode: c++ -*-
/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2015, JSK Lab
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
 *   * Neither the name of the JSK Lab nor the names of its
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

#include "jsk_perception/roi_to_mask_image.h"
#include <boost/assign.hpp>
#include <jsk_topic_tools/log_utils.h>

namespace jsk_perception
{
  void ROIToMaskImage::onInit()
  {
    DiagnosticNodelet::onInit();
    pub_ = advertise<sensor_msgs::Image>(
      *pnh_, "output", 1);
    onInitPostProcess();
  }

  void ROIToMaskImage::subscribe()
  {
    sub_ = pnh_->subscribe("input", 1, &ROIToMaskImage::convert, this);
    ros::V_string names = boost::assign::list_of("~input");
    jsk_topic_tools::warnNoRemap(names);
  }

  void ROIToMaskImage::unsubscribe()
  {
    sub_.shutdown();
  }

  void ROIToMaskImage::convert(
    const sensor_msgs::CameraInfo::ConstPtr& info_msg)
  {
    cv::Mat mask_image = cv::Mat::zeros(info_msg->height,
                                        info_msg->width,
                                        CV_8UC1);
    cv::Rect rect(info_msg->roi.x_offset,
                  info_msg->roi.y_offset,
                  info_msg->roi.width,
                  info_msg->roi.height);
    cv::rectangle(mask_image, rect, cv::Scalar(255), CV_FILLED);
    pub_.publish(cv_bridge::CvImage(
                   info_msg->header,
                   sensor_msgs::image_encodings::MONO8,
                   mask_image).toImageMsg());
  }
}

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS (jsk_perception::ROIToMaskImage, nodelet::Nodelet);
