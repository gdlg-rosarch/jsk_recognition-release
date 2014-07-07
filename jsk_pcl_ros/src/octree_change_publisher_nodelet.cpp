/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2013, Yuto Inagaki and JSK Lab
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


#include "jsk_pcl_ros/octree_change_publisher.h"
#include <pluginlib/class_list_macros.h>

namespace jsk_pcl_ros
{
  void OctreeChangePublisher::onInit(void)
  {
    PCLNodelet::onInit();
    counter_ = 0;

    pnh_->param("resolution", resolution_, 0.02);
    pnh_->param("noise_filter", noise_filter_, 2);

    octree_ = new pcl::octree::OctreePointCloudChangeDetector<pcl::PointXYZRGB>(resolution_);

    filtered_cloud.reset(new pcl::PointCloud<pcl::PointXYZRGB>);

    //Set subscribe setting
    sub_ = pnh_->subscribe("input", 1, &OctreeChangePublisher::cloud_cb,this);
    diff_pub_ = pnh_->advertise<sensor_msgs::PointCloud2>("octree_change_result", 1);

  }

  void OctreeChangePublisher::cloud_cb(const sensor_msgs::PointCloud2 &pc)
  {
    if(pc.fields.size() <= 0){
      return;
    }

    pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZRGB>());
    std::vector<int> indices;
    pcl::fromROSMsg(pc, *cloud);
    octree_->setInputCloud (cloud);
    octree_->addPointsFromInputCloud ();

    if (counter_ != 0){
      boost::shared_ptr<std::vector<int> > newPointIdxVector (new std::vector<int>);

      octree_->getPointIndicesFromNewVoxels (*newPointIdxVector, noise_filter_);

      filtered_cloud.reset (new pcl::PointCloud<pcl::PointXYZRGB>);
      filtered_cloud->points.reserve(newPointIdxVector->size());

      for (std::vector<int>::iterator it = newPointIdxVector->begin (); it != newPointIdxVector->end (); it++)
        filtered_cloud->points.push_back(cloud->points[*it]);

      sensor_msgs::PointCloud2 octree_change_pointcloud2;
      pcl::toROSMsg(*filtered_cloud, octree_change_pointcloud2);
      octree_change_pointcloud2.header = pc.header;
      octree_change_pointcloud2.is_dense = false;
      diff_pub_.publish(octree_change_pointcloud2);
    }

    octree_->switchBuffers ();
    counter_++;
  }
}

typedef jsk_pcl_ros::OctreeChangePublisher OctreeChangePublisher;
PLUGINLIB_DECLARE_CLASS (jsk_pcl, OctreeChangePublisher, OctreeChangePublisher, nodelet::Nodelet);
