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

#ifndef JSK_PCL_ROS_ENVIRONMENT_PLANE_MODELING_H_
#define JSK_PCL_ROS_ENVIRONMENT_PLANE_MODELING_H_

#include <pcl_ros/pcl_nodelet.h>

#include <pcl/kdtree/kdtree_flann.h>
#include <message_filters/subscriber.h>
#include <message_filters/time_synchronizer.h>
#include <message_filters/synchronizer.h>
#include <dynamic_reconfigure/server.h>

#include <jsk_recognition_msgs/PolygonArray.h>
#include <jsk_recognition_msgs/ModelCoefficientsArray.h>
#include <jsk_recognition_msgs/ClusterPointIndices.h>
#include <sensor_msgs/PointCloud2.h>
#include <jsk_pcl_ros/EnvironmentLock.h>
#include <jsk_pcl_ros/PolygonOnEnvironment.h>

#include <jsk_pcl_ros/pcl_conversion_util.h>
#include <jsk_pcl_ros/EnvironmentPlaneModelingConfig.h>

#include <diagnostic_updater/diagnostic_updater.h>
#include <diagnostic_updater/publisher.h>

#include <std_srvs/Empty.h>

#include <jsk_topic_tools/time_accumulator.h>

#include "jsk_pcl_ros/grid_map.h"
#include "jsk_pcl_ros/pcl_util.h"

#include <jsk_recognition_msgs/SparseOccupancyGridArray.h>

namespace jsk_pcl_ros
{
  class EnvironmentPlaneModeling: public pcl_ros::PCLNodelet
  {
  public:
    typedef pcl::PointXYZRGB PointT;
    typedef EnvironmentPlaneModelingConfig Config;
    typedef message_filters::sync_policies::ExactTime<
      sensor_msgs::PointCloud2,
      jsk_recognition_msgs::ClusterPointIndices,
      jsk_recognition_msgs::PolygonArray,
      jsk_recognition_msgs::ModelCoefficientsArray,
      jsk_recognition_msgs::PolygonArray,
      jsk_recognition_msgs::ModelCoefficientsArray> SyncPolicy;
    typedef message_filters::sync_policies::ExactTime<
      sensor_msgs::PointCloud2,
      jsk_recognition_msgs::ClusterPointIndices,
      jsk_recognition_msgs::PolygonArray,
      jsk_recognition_msgs::ModelCoefficientsArray
      > SyncPolicyWithoutStaticPolygon;
    typedef message_filters::sync_policies::ExactTime<
      jsk_recognition_msgs::PolygonArray,
      jsk_recognition_msgs::ModelCoefficientsArray
      > PolygonSyncPolicy;
  protected:
    virtual void onInit();
    virtual void estimateOcclusion(
      const pcl::PointCloud<pcl::PointXYZRGB>::Ptr input,
      const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& input_indices,
      const std::vector<pcl::PointCloud<PointT>::Ptr>& segmented_cloud,
      std::vector<GridMap::Ptr>& grid_maps,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& static_polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& static_coefficients,
      jsk_recognition_msgs::PolygonArray::Ptr result_polygons,
      jsk_recognition_msgs::ModelCoefficientsArray::Ptr result_coefficients,
      pcl::PointCloud<PointT>::Ptr result_pointcloud,
      jsk_recognition_msgs::ClusterPointIndices::Ptr result_indices);
    
    template <class A, class B>
    bool isValidHeaders(
      const std::vector<A>& as, const std::vector<B>& bs);
    bool isValidInput();
    virtual void inputCallback(
      const sensor_msgs::PointCloud2::ConstPtr& input,
      const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& input_indices,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& static_polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& static_coefficients);
    virtual void configCallback(Config &config, uint32_t level);
    virtual bool lockCallback();
    virtual bool startBuildEnvironmentCallback(
      std_srvs::Empty::Request& req,
      std_srvs::Empty::Response& res);
    virtual bool stopBuildEnvironmentCallback(
      std_srvs::Empty::Request& req,
      std_srvs::Empty::Response& res);

    virtual bool dummyLockCallback(EnvironmentLock::Request& req,
                                   EnvironmentLock::Response& res);
    virtual bool polygonOnEnvironmentCallback(PolygonOnEnvironment::Request& req,
                                              PolygonOnEnvironment::Response& res);
    virtual bool primitiveLockCallback(std_srvs::Empty::Request& req,
                                       std_srvs::Empty::Response& res);
    virtual bool primitiveUnlockCallback(std_srvs::Empty::Request& req,
                                         std_srvs::Empty::Response& res);
    virtual bool clearMapCallback(std_srvs::Empty::Request& req,
                                  std_srvs::Empty::Response& res);
    virtual bool registerToHistoryCallback(std_srvs::Empty::Request& req,
                                           std_srvs::Empty::Response& res);
    virtual bool registerCompletionToHistoryCallback(
      std_srvs::Empty::Request& req,
      std_srvs::Empty::Response& res);
    virtual void appendGridMaps(std::vector<GridMap::Ptr>& old_maps,
                                std::vector<GridMap::Ptr>& new_maps);
    virtual bool polygonNearEnoughToPointCloud(
      const size_t plane_i,
      const pcl::PointCloud<PointT>::Ptr sampled_point_cloud);
    virtual void samplePolygonToPointCloud(
      const geometry_msgs::PolygonStamped sample_polygon,
      pcl::PointCloud<PointT>::Ptr output,
      double sampling_param);
    
    virtual void decomposePointCloud(
      const pcl::PointCloud<PointT>::Ptr& input,
      const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& input_indices,
      std::vector<pcl::PointCloud<PointT>::Ptr>& output);
    virtual void internalPointDivide(const PointT& A, const PointT& B,
                                     const double ratio,
                                     PointT& output);

    virtual void downsizeGridMaps(std::vector<GridMap::Ptr>& maps);
    
    virtual void extendConvexPolygon(
      const geometry_msgs::PolygonStamped& static_polygon,
      const PCLModelCoefficientMsg& coefficients,
      const geometry_msgs::PolygonStamped& nearest_polygon,
      geometry_msgs::PolygonStamped& output_polygon);
    virtual void updateAppendingInfo(const int env_plane_index,
                                     const size_t static_plane_index,
                                     std::map<int, std::set<size_t> >& result);
    virtual void buildGridMap(
      const std::vector<pcl::PointCloud<PointT>::Ptr>& segmented_clouds,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
      std::vector<GridMap::Ptr>& grid_maps);
    virtual void publishGridMap(
      ros::Publisher& pub,
      const std_msgs::Header& header,
      const std::vector<GridMap::Ptr> grid_maps);
    virtual void publishGridMapPolygon(
      ros::Publisher& pub_polygons,
      ros::Publisher& pub_coefficients,
      const std_msgs::Header& header,
      const std::vector<GridMap::Ptr> grid_maps);
    // find the nearest plane to static_polygon and static_coefficient
    // from polygons and coefficients
    virtual int findNearestPolygon(
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
      const geometry_msgs::PolygonStamped& static_polygon,
      const PCLModelCoefficientMsg& static_coefficient);

    virtual void fillEstimatedRegionByPointCloud
    (const std_msgs::Header& header,
     const pcl::PointCloud<pcl::PointXYZRGB>::Ptr input,
     const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& indices,
     const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
     const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
     const jsk_recognition_msgs::PolygonArray::ConstPtr& static_polygons,
     const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& static_coefficients,
     const jsk_recognition_msgs::PolygonArray& result_polygons,
     const std::map<int, std::set<size_t> >& estimation_summary,
     pcl::PointCloud<PointT>::Ptr all_cloud,
     jsk_recognition_msgs::ClusterPointIndices& all_indices,
     std::vector<GridMap::Ptr> grid_maps);

    virtual void inputCallback(
      const sensor_msgs::PointCloud2::ConstPtr& input,
      const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& input_indices,
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients);
    
    virtual void copyClusterPointIndices
    (const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& indices,
     jsk_recognition_msgs::ClusterPointIndices& output);
    virtual void computePolygonCentroid(
      const geometry_msgs::PolygonStamped msg,
      pcl::PointXYZRGB& output);
    virtual void addIndices(const size_t start, const size_t end,
                            PCLIndicesMsg& output);
    virtual void updateDiagnostic(
      diagnostic_updater::DiagnosticStatusWrapper &stat);
    // for historical_accumulation_
    virtual int findCorrespondGridMap(
      const std::vector<float>& coefficients,
      const geometry_msgs::Polygon& polygon);
    virtual int findNearGridMapFromCoefficients(
      const std::vector<GridMap::Ptr>& maps, GridMap::Ptr map);
    virtual void registerGridMap(const GridMap::Ptr new_grid_map);
    virtual void selectionGridMaps();
    virtual pcl::PointCloud<EnvironmentPlaneModeling::PointT>::Ptr
    projectCloud(
    const pcl::PointCloud<PointT>::Ptr input_cloud,
    const std::vector<float> input_coefficient);

    virtual void staticPolygonCallback(
      const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
      const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr samplePointCloudOnPolygon(
      const geometry_msgs::PolygonStamped& candidate_polygon,
      const PCLModelCoefficientMsg& candidate_polygon_coefficients);
    virtual void completeGridMap(
    const pcl::PointCloud<pcl::PointXYZRGB>::Ptr input,
    const jsk_recognition_msgs::ClusterPointIndices::ConstPtr& input_indices,
    const std::vector<pcl::PointCloud<PointT>::Ptr>& segmented_cloud,
    const jsk_recognition_msgs::PolygonArray::ConstPtr& polygons,
    const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& coefficients,
    const jsk_recognition_msgs::PolygonArray::ConstPtr& static_polygons,
    const jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr& static_coefficients,
    std::vector<GridMap::Ptr>& output_grid_maps);
        
    ////////////////////////////////////////////////////////
    // ROS variables
    ////////////////////////////////////////////////////////
    boost::mutex mutex_;
    boost::shared_ptr <dynamic_reconfigure::Server<Config> > srv_;
    
    // synchronized subscription
    boost::shared_ptr<message_filters::Synchronizer<SyncPolicy> > sync_;
    boost::shared_ptr<
      message_filters::Synchronizer<SyncPolicyWithoutStaticPolygon> >
    sync_without_static_;
    boost::shared_ptr<
      message_filters::Synchronizer<PolygonSyncPolicy> > sync_static_polygon_;
    message_filters::Subscriber<sensor_msgs::PointCloud2> sub_input_;
    message_filters::Subscriber<jsk_recognition_msgs::ClusterPointIndices> sub_indices_;
    message_filters::Subscriber<jsk_recognition_msgs::PolygonArray> sub_polygons_;
    message_filters::Subscriber<jsk_recognition_msgs::ModelCoefficientsArray> sub_coefficients_;
    message_filters::Subscriber<jsk_recognition_msgs::PolygonArray> sub_static_polygons_;
    message_filters::Subscriber<jsk_recognition_msgs::ModelCoefficientsArray> sub_static_coefficients_;
    ros::ServiceServer lock_service_;
    ros::ServiceServer polygon_on_environment_service_;
    ros::ServiceServer primitive_lock_service_;
    ros::ServiceServer primitive_unlock_service_;
    ros::ServiceServer clear_map_service_;
    ros::ServiceServer register_to_history_service_;
    ros::ServiceServer register_completion_to_history_service_;
    ros::ServiceServer start_build_environment_service_;
    ros::ServiceServer stop_build_environment_service_;
    ros::Publisher debug_polygon_pub_;
    ros::Publisher debug_env_polygon_pub_;
    ros::Publisher debug_pointcloud_pub_;
    ros::Publisher debug_env_pointcloud_pub_;
    ros::Publisher debug_grid_map_completion_pub_;
    ros::Publisher old_map_polygon_pub_;
    ros::Publisher old_map_polygon_coefficients_pub_;
    ros::Publisher occlusion_result_polygons_pub_;
    ros::Publisher occlusion_result_coefficients_pub_;
    ros::Publisher occlusion_result_pointcloud_pub_;
    ros::Publisher occlusion_result_indices_pub_;
    ros::Publisher grid_map_array_pub_;
    ros::Publisher old_map_pub_;
    // member variables to store the latest messages
    sensor_msgs::PointCloud2::ConstPtr latest_input_;
    jsk_recognition_msgs::ClusterPointIndices::ConstPtr latest_input_indices_;
    jsk_recognition_msgs::PolygonArray::ConstPtr latest_input_polygons_;
    jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr latest_input_coefficients_;
    jsk_recognition_msgs::PolygonArray::ConstPtr latest_static_polygons_;
    jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr latest_static_coefficients_;
    
    // member variables to keep the messasge which we process
    sensor_msgs::PointCloud2::ConstPtr processing_input_;
    jsk_recognition_msgs::ClusterPointIndices::ConstPtr processing_input_indices_;
    jsk_recognition_msgs::PolygonArray::ConstPtr processing_input_polygons_;
    jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr processing_input_coefficients_;
    jsk_recognition_msgs::PolygonArray::ConstPtr processing_static_polygons_;
    jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr processing_static_coefficients_;
    jsk_recognition_msgs::PolygonArray::ConstPtr completion_static_polygons_;
    jsk_recognition_msgs::ModelCoefficientsArray::ConstPtr completion_static_coefficients_;
    
    std::vector<pcl::KdTreeFLANN<pcl::PointXYZ>::Ptr> kdtrees_;
    uint32_t environment_id_;
    double distance_thr_;
    double sampling_d_;
    double resolution_size_;
    // parameters for occlusion
    double plane_distance_threshold_;
    double plane_angle_threshold_;
    // grid map
    double grid_map_distance_threshold_;
    double grid_map_angle_threshold_;
    bool continuous_estimation_;
    bool history_accumulation_;
    bool history_statical_rejection_;
    bool estimate_occlusion_;
    bool use_static_polygons_;
    int static_generation_;
    int required_vote_;
    int decrease_grid_map_;
    bool register_next_map_;
    bool register_completion_next_map_;
    std::vector<GridMap::Ptr> grid_maps_;
    std::vector<GridMap::Ptr> old_grid_maps_;
    jsk_topic_tools::TimeAccumulator occlusion_estimate_time_acc_;
    jsk_topic_tools::TimeAccumulator grid_building_time_acc_;
    jsk_topic_tools::TimeAccumulator kdtree_building_time_acc_;
    jsk_topic_tools::TimeAccumulator polygon_collision_check_time_acc_;
    boost::shared_ptr<diagnostic_updater::Updater> diagnostic_updater_;
    int generation_;
  private:
  };
}

#endif
