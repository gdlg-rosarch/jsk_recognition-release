// -*- mode: c++; indent-tabs-mode: nil; c-basic-offset: 4; -*-
// Software License Agreement (BSD License)
// Copyright (c) 2008, Willow Garage, Inc.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//   * Redistributions of source code must retain the above copyright notice,
//     this list of conditions and the following disclaimer.
//   * Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//   * The name of the author may not be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//
// author: Rosen Diankov
#include <algorithm>

#include <cstdio>
#include <vector>
#include <sstream>
#include <algorithm>
#include <ros/ros.h>

#include <boost/thread/mutex.hpp>

#include "opencv2/opencv.hpp"
#include "cv_bridge/cv_bridge.h"
#include "sensor_msgs/image_encodings.h"
#include "sensor_msgs/CameraInfo.h"
#include "sensor_msgs/Image.h"
#include "image_geometry/pinhole_camera_model.h"
#include "posedetection_msgs/ObjectDetection.h"
#include "posedetection_msgs/Detect.h"
#include "geometry_msgs/PointStamped.h"
#include "geometry_msgs/PoseStamped.h"
#include "math.h"
#include "geometry_msgs/PolygonStamped.h"
#include "jsk_pcl_ros/PolygonArray.h"
#include "jsk_pcl_ros/pcl_conversion_util.h"
#include "eigen_conversions/eigen_msg.h"
#include <sys/timeb.h>    // ftime(), struct timeb
#include <sys/time.h>

using namespace std;
using namespace ros;

class CheckerboardDetector
{
    template <typename T>
    static vector<T> tokenizevector(const string& s)
    {
        stringstream ss(s);
        return vector<T>((istream_iterator<T>(ss)), istream_iterator<T>());
    }

public:
    struct CHECKERBOARD
    {
        CvSize griddims; ///< number of squares
        vector<cv::Point3f> grid3d;
        //vector<CvPoint2D32f> corners;
        //cv::Mat corners;
        vector<cv::Point2f> corners;
        TransformMatrix tlocaltrans;
        std::string board_type;
    };

    posedetection_msgs::ObjectDetection _objdetmsg;
    sensor_msgs::CameraInfo _camInfoMsg;

    ros::Subscriber camInfoSubscriber,camInfoSubscriber2;
    ros::Subscriber imageSubscriber,imageSubscriber2;
    ros::Publisher _pubDetection;
    ros::Publisher _pubPoseStamped;
    ros::Publisher _pubCornerPoint;
    ros::Publisher _pubPolygonArray;
    ros::ServiceServer _srvDetect;

    string frame_id; // tf frame id
    bool invert_color;
    int display, verbose, maxboard;
    vector<CHECKERBOARD> vcheckers; // grid points for every checkerboard
    vector< string > vstrtypes; // type names for every grid point
    map<string,int> maptypes;
    ros::Time lasttime;
    boost::mutex mutexcalib;
    ros::NodeHandle _node;
    int dimx, dimy;
    double fRectSize[2];

    //////////////////////////////////////////////////////////////////////////////
    // Constructor
    CheckerboardDetector()
    {
        _node.param("display", display, 0);
        _node.param("verbose", verbose, 1);
        _node.param("maxboard", maxboard, -1);
        _node.param("invert_color", invert_color, false);
        char str[32];
        int index = 0;

        while(1) {
            string type;

            sprintf(str,"grid%d_size_x",index);
            if( !_node.getParam(str,dimx) )
                break;
            if (dimx < 3) {
                ROS_ERROR("Param: %s must be greater than 2",str);
                return;
            }

            sprintf(str,"grid%d_size_y",index);
            if( !_node.getParam(str,dimy) )
                break;
            if (dimy < 3) {
                ROS_ERROR("Param: %s must be greater than 2",str);
                return;
            }

            sprintf(str,"rect%d_size_x",index);
            if( !_node.getParam(str,fRectSize[0]) )
                break;

            sprintf(str,"rect%d_size_y",index);
            if( !_node.getParam(str,fRectSize[1]) )
                break;

            sprintf(str,"type%d",index);
            if( !_node.getParam(str,type) ) {
                sprintf(str,"checker%dx%d", dimx, dimy);
                type = str;
            }

            std::string board_type;
            _node.param("board_type", board_type, std::string("chess"));
            
            
            string strtranslation,strrotation;
            sprintf(str,"translation%d",index);
            _node.param(str,strtranslation,string());

            vector<float> vtranslation = tokenizevector<float>(strtranslation);
            sprintf(str,"rotation%d",index);
            _node.param(str,strrotation,string());

            vector<float> vrotation = tokenizevector<float>(strrotation);

            CHECKERBOARD cb;
            cb.griddims = cvSize(dimx,dimy);
            cb.board_type = board_type;
            cb.grid3d.resize(dimx*dimy);
            int j=0;
            if (board_type == "chess" || board_type == "circle") {
              for(int y=0; y<dimy; ++y)
                for(int x=0; x<dimx; ++x)
                  cb.grid3d[j++] = cv::Point3f(x*fRectSize[0], y*fRectSize[1], 0);
            }
            else if (board_type == "acircle") {
              for(int ii=0; ii<dimy; ii++) {
                for(int jj=0; jj<dimx; jj++) {
                  cb.grid3d[j++] = cv::Point3f((2*jj + ii % 2)*fRectSize[0],
                                          ii*fRectSize[1],
                                          0);
                }
              }
            }

            if( vtranslation.size() == 3 )
                cb.tlocaltrans.trans = 
                    Vector(vtranslation[0],vtranslation[1],vtranslation[2]);

            if( vrotation.size() == 9 )  {
                for(int k = 0; k < 3; ++k) {
                    cb.tlocaltrans.m[4*k+0] = vrotation[3*k+0];
                    cb.tlocaltrans.m[4*k+1] = vrotation[3*k+1];
                    cb.tlocaltrans.m[4*k+2] = vrotation[3*k+2];
                }
            }

            vcheckers.push_back(cb);
            vstrtypes.push_back(type);
            maptypes[vstrtypes.back()] = index;
            index++;
        }

        _node.param("frame_id", frame_id,string(""));

        if( maptypes.size() == 0 ) {
            ROS_ERROR("no checkerboards to detect");
            return;
        }

        if( display ) {
          cv::namedWindow("Checkerboard Detector",
                          (display == 1? CV_WINDOW_AUTOSIZE : display));
        }

        lasttime = ros::Time::now();
        if (!display) {
            ros::SubscriberStatusCallback connect_cb = boost::bind( &CheckerboardDetector::connectCb, this);
            _pubDetection =
                _node.advertise<posedetection_msgs::ObjectDetection> ("ObjectDetection", 1,
                                                                      connect_cb, connect_cb);
            _pubPoseStamped =
                _node.advertise<geometry_msgs::PoseStamped> ("objectdetection_pose", 1,
                                                             connect_cb, connect_cb);
            _pubCornerPoint = _node.advertise<geometry_msgs::PointStamped>("corner_point", 1, connect_cb, connect_cb);
            _pubPolygonArray = _node.advertise<jsk_pcl_ros::PolygonArray>("polygons", 1, connect_cb, connect_cb);
        }
        else {
            _pubDetection =
                _node.advertise<posedetection_msgs::ObjectDetection> ("ObjectDetection", 1);
            _pubPoseStamped =
                _node.advertise<geometry_msgs::PoseStamped> ("objectdetection_pose", 1);
            _pubCornerPoint = _node.advertise<geometry_msgs::PointStamped>("corner_point", 1);
            _pubPolygonArray = _node.advertise<jsk_pcl_ros::PolygonArray>("polygons", 1);
            subscribe();
        }
        //this->camInfoSubscriber = _node.subscribe("camera_info", 1, &CheckerboardDetector::caminfo_cb, this);
        //this->imageSubscriber = _node.subscribe("image",1, &CheckerboardDetector::image_cb, this);
        //this->camInfoSubscriber2 = _node.subscribe("CameraInfo", 1, &CheckerboardDetector::caminfo_cb2, this);
        //this->imageSubscriber2 = _node.subscribe("Image",1, &CheckerboardDetector::image_cb2, this);
        _srvDetect = _node.advertiseService("Detect",&CheckerboardDetector::detect_cb,this);
    }

    //////////////////////////////////////////////////////////////////////////////
    // Destructor
    virtual ~CheckerboardDetector()
    {
    }

    //////////////////////////////////////////////////////////////////////////////
    // Camera info callback
    void caminfo_cb(const sensor_msgs::CameraInfoConstPtr &msg)
    {
        boost::mutex::scoped_lock lock(this->mutexcalib);

        this->_camInfoMsg = *msg;

        // only get the camera info once <- this is dumb
        //this->camInfoSubscriber.shutdown();
        //this->camInfoSubscriber2.shutdown();
    }
    void caminfo_cb2(const sensor_msgs::CameraInfoConstPtr &msg)
    {
        ROS_WARN("The topic CameraInfo has been deprecated.  Please change your launch file to use camera_info instead.");
        caminfo_cb(msg);
    }
    
    void publishPolygonArray(const posedetection_msgs::ObjectDetection& obj)
    {
        jsk_pcl_ros::PolygonArray polygon_array;
        polygon_array.header = obj.header;
        for (size_t i = 0; i < obj.objects.size(); i++) {
            geometry_msgs::Pose pose = obj.objects[i].pose;
            Eigen::Affine3d affine;
            tf::poseMsgToEigen(pose, affine);
            Eigen::Vector3d A_local(0, 0, 0);
            Eigen::Vector3d B_local((dimx - 1) * fRectSize[0], 0, 0);
            Eigen::Vector3d C_local((dimx - 1) * fRectSize[0], (dimy - 1) * fRectSize[1], 0);
            Eigen::Vector3d D_local(0, (dimy - 1) * fRectSize[1], 0);
            Eigen::Vector3d A_global = affine * A_local;
            Eigen::Vector3d B_global = affine * B_local;
            Eigen::Vector3d C_global = affine * C_local;
            Eigen::Vector3d D_global = affine * D_local;
            geometry_msgs::Point32 a, b, c, d;
            jsk_pcl_ros::pointFromVectorToXYZ<Eigen::Vector3d, geometry_msgs::Point32>(A_global, a);
            jsk_pcl_ros::pointFromVectorToXYZ<Eigen::Vector3d, geometry_msgs::Point32>(B_global, b);
            jsk_pcl_ros::pointFromVectorToXYZ<Eigen::Vector3d, geometry_msgs::Point32>(C_global, c);
            jsk_pcl_ros::pointFromVectorToXYZ<Eigen::Vector3d, geometry_msgs::Point32>(D_global, d);
            geometry_msgs::PolygonStamped polygon;
            polygon.header = obj.header;
            polygon.polygon.points.push_back(a);
            polygon.polygon.points.push_back(b);
            polygon.polygon.points.push_back(c);
            polygon.polygon.points.push_back(d);
            polygon_array.polygons.push_back(polygon);
        }
        _pubPolygonArray.publish(polygon_array);
    }

    void image_cb2(const sensor_msgs::ImageConstPtr &msg)
    {
        ROS_WARN("The topic Image has been deprecated.  Please change your launch file to use image instead.");
        boost::mutex::scoped_lock lock(this->mutexcalib);
        if( Detect(_objdetmsg,*msg,this->_camInfoMsg) ) {
            if (_objdetmsg.objects.size() > 0) {
                geometry_msgs::PoseStamped pose;
                pose.header = _objdetmsg.header;
                pose.pose = _objdetmsg.objects[0].pose;
                _pubPoseStamped.publish(pose);
            }
            _pubDetection.publish(_objdetmsg);
            publishPolygonArray(_objdetmsg);
        }
    }

    //////////////////////////////////////////////////////////////////////////////
    // Image data callback
    void image_cb(const sensor_msgs::ImageConstPtr &msg)
    {
        boost::mutex::scoped_lock lock(this->mutexcalib);
        if( Detect(_objdetmsg,*msg,this->_camInfoMsg) ) {
            if (_objdetmsg.objects.size() > 0) {
                geometry_msgs::PoseStamped pose;
                pose.header = _objdetmsg.header;
                pose.pose = _objdetmsg.objects[0].pose;
                _pubPoseStamped.publish(pose);
            }
            _pubDetection.publish(_objdetmsg);
            publishPolygonArray(_objdetmsg);
        }
    }

    bool detect_cb(posedetection_msgs::Detect::Request& req, posedetection_msgs::Detect::Response& res)
    {
        bool result = Detect(res.object_detection,req.image,req.camera_info);
        return result;
    }


    void subscribe( )
    {
        if ( camInfoSubscriber == NULL )
            camInfoSubscriber = _node.subscribe("camera_info", 1, &CheckerboardDetector::caminfo_cb, this);
        if ( imageSubscriber == NULL )
            imageSubscriber = _node.subscribe("image", 1, &CheckerboardDetector::image_cb, this);
        if ( camInfoSubscriber2 == NULL )
            camInfoSubscriber2 = _node.subscribe("CameraInfo", 1, &CheckerboardDetector::caminfo_cb2, this);
        if ( imageSubscriber2 == NULL )
            imageSubscriber2 = _node.subscribe("Image",1, &CheckerboardDetector::image_cb2, this);

    }

    void unsubscribe( )
    {
        camInfoSubscriber.shutdown();
        camInfoSubscriber2.shutdown();
        imageSubscriber.shutdown();
        imageSubscriber2.shutdown();
    }
    
    void connectCb( )
    {
      boost::mutex::scoped_lock lock(this->mutexcalib);
      if (_pubDetection.getNumSubscribers() == 0 && _pubCornerPoint.getNumSubscribers() == 0 &&
          _pubPoseStamped.getNumSubscribers() == 0 && _pubPolygonArray.getNumSubscribers() == 0)
        {
            unsubscribe();
        }
      else
        {
            subscribe();
        }
    }

    bool Detect(posedetection_msgs::ObjectDetection& objdetmsg,
                const sensor_msgs::Image& imagemsg,
                const sensor_msgs::CameraInfo& camInfoMsg)
    {
        image_geometry::PinholeCameraModel model;
        sensor_msgs::CameraInfo cam_info(camInfoMsg);
        if (cam_info.distortion_model.empty()) {
            cam_info.distortion_model = "plumb_bob";
            cam_info.D.resize(5, 0);
        }
        // check all the value of R is zero or not
        // if zero, normalzie it
        if (std::equal(cam_info.R.begin() + 1, cam_info.R.end(), cam_info.R.begin())) {
            cam_info.R[0] = 1.0;
            cam_info.R[4] = 1.0;
            cam_info.R[8] = 1.0;
        }
        // check all the value of K is zero or not
        // if zero, copy all the value from P
        if (std::equal(cam_info.K.begin() + 1, cam_info.K.end(), cam_info.K.begin())) {
            cam_info.K[0] = cam_info.P[0];
            cam_info.K[1] = cam_info.P[1];
            cam_info.K[2] = cam_info.P[2];
            cam_info.K[3] = cam_info.P[4];
            cam_info.K[4] = cam_info.P[5];
            cam_info.K[5] = cam_info.P[6];
            cam_info.K[6] = cam_info.P[8];
            cam_info.K[7] = cam_info.P[9];
            cam_info.K[8] = cam_info.P[10];
        }
        model.fromCameraInfo(cam_info);
        cv_bridge::CvImagePtr capture_ptr;
        try {
          if (imagemsg.encoding == "32FC1") {
            cv_bridge::CvImagePtr float_capture
              = cv_bridge::toCvCopy(imagemsg,
                                    sensor_msgs::image_encodings::TYPE_32FC1);
            cv::Mat float_image = float_capture->image;
            cv::Mat mono_image;
            float_image.convertTo(mono_image, CV_8UC1);
            capture_ptr.reset(new cv_bridge::CvImage());
            capture_ptr->image = mono_image;
          }
          else {
            capture_ptr = cv_bridge::toCvCopy(imagemsg, sensor_msgs::image_encodings::MONO8);
          }
        } catch (cv_bridge::Exception &e) {
            ROS_ERROR("failed to get image %s", e.what());
            return false;
        }
        cv::Mat capture = capture_ptr->image;
        if (invert_color) {
            capture = cv::Mat((capture + 0.0) * 1.0 / 1.0) * 1.0;
            //capture = 255 - capture;
            cv::Mat tmp;
            cv::bitwise_not(capture, tmp);
            capture = tmp;
        }

        cv::Mat frame;
        
        if( display ) {
            cv::cvtColor(capture, frame, CV_GRAY2BGR);
        }

        vector<posedetection_msgs::Object6DPose> vobjects;

#pragma omp parallel for schedule(dynamic,1)
        for(int i = 0; i < (int)vcheckers.size(); ++i) {
            CHECKERBOARD& cb = vcheckers[i];
            int ncorners, board=0;
            posedetection_msgs::Object6DPose objpose;

            // do until no more checkerboards detected
            while((maxboard==-1)?1:((++board)<=maxboard)) {
                bool allfound = false;
                if (cb.board_type == "chess") {
                    allfound = cv::findChessboardCorners(
                        capture, cb.griddims, cb.corners);
                }
                else if (cb.board_type == "circle" ||
                         cb.board_type == "circles") {
                    allfound =
                        cv::findCirclesGrid(capture, cb.griddims, cb.corners);
                }
                else if (cb.board_type == "acircle" ||
                         cb.board_type == "acircles") {
                    // sometime cv::findCirclesGrid hangs
                    allfound =
                        cv::findCirclesGrid(
                            capture, cb.griddims, cb.corners,
                            cv::CALIB_CB_ASYMMETRIC_GRID | cv::CALIB_CB_CLUSTERING);
                }

                if(!allfound || cb.corners.size() != cb.grid3d.size())
                    break;

                // remove any corners that are close to the border
                const int borderthresh = 30;

                for(int j = 0; j < ncorners; ++j) {
                    int x = cb.corners[j].x;
                    int y = cb.corners[j].y;
                    if( x < borderthresh || x > capture.cols - borderthresh ||
                        y < borderthresh || y > capture.rows - borderthresh )
                    {
                        allfound = false;
                        break;
                    }
                }

                // mark out the image
                cv::Point upperleft, lowerright;
                upperleft.x = lowerright.x = cb.corners[0].x;
                upperleft.y = lowerright.y = cb.corners[0].y;
                for(size_t j = 1; j < cb.corners.size(); ++j) {
                    if( upperleft.x > cb.corners[j].x ) upperleft.x = cb.corners[j].x;
                    if( upperleft.y > cb.corners[j].y ) upperleft.y = cb.corners[j].y;
                    if( lowerright.x < cb.corners[j].x ) lowerright.x = cb.corners[j].x;
                    if( lowerright.y < cb.corners[j].y ) lowerright.y = cb.corners[j].y;
                }

                float step_size =
                  (double)( ((upperleft.x - lowerright.x) * (upperleft.x - lowerright.x)) +
                            ((upperleft.y - lowerright.y) * (upperleft.y - lowerright.y)) )
                  /
                  ( ((cb.griddims.width - 1) * (cb.griddims.width - 1)) +
                    ((cb.griddims.height - 1) * (cb.griddims.height - 1)) );
#if 0
                ROS_INFO("(%d %d) - (%d %d) -> %f ",
                         upperleft.x, upperleft.y, lowerright.x, lowerright.y, sqrt(step_size));
#endif
                int size = (int)(0.5*sqrt(step_size) + 0.5);

                if( allfound ) {
                    if (cb.board_type == "chess") { // subpixel only for chessboard
                        cv::cornerSubPix(capture, cb.corners,
                                         cv::Size(size,size), cv::Size(-1,-1),
                                         cv::TermCriteria(CV_TERMCRIT_ITER, 50, 1e-2));
                    }
                    objpose.pose = FindTransformation(cb.corners, cb.grid3d, cb.tlocaltrans, model);
                }

#pragma omp critical
                {
                    if( allfound ) {
                        vobjects.push_back(objpose);
                        vobjects.back().type = vstrtypes[i];
                    }
                    cv::rectangle(capture, upperleft, lowerright,
                                  cv::Scalar(0,0,0), CV_FILLED);
                }
            }

            //cvSaveImage("temp.jpg", pimggray);
        }

        objdetmsg.objects = vobjects;
        objdetmsg.header.stamp = imagemsg.header.stamp;
        if( frame_id.size() > 0 )
            objdetmsg.header.frame_id = frame_id;
        else
            objdetmsg.header.frame_id = imagemsg.header.frame_id;

        if( verbose > 0 )
            ROS_INFO("checkerboard: image: %ux%u (size=%u), num: %u, total: %.3fs",
                     imagemsg.width, imagemsg.height,
                     (unsigned int)imagemsg.data.size(), (unsigned int)objdetmsg.objects.size(),
                     (float)(ros::Time::now() - lasttime).toSec());
        lasttime = ros::Time::now();

        if( display ) {
            // draw each found checkerboard
            for(size_t i = 0; i < vobjects.size(); ++i) {
                int itype = maptypes[vobjects[i].type];
                CHECKERBOARD& cb = vcheckers[itype];
                Transform tglobal;
                tglobal.trans = Vector(vobjects[i].pose.position.x,vobjects[i].pose.position.y,vobjects[i].pose.position.z);
                tglobal.rot = Vector(vobjects[i].pose.orientation.w,vobjects[i].pose.orientation.x,vobjects[i].pose.orientation.y, vobjects[i].pose.orientation.z);
                Transform tlocal = tglobal * cb.tlocaltrans.inverse();

                cv::Point X[4];

                Vector vaxes[4];
                vaxes[0] = Vector(0,0,0);
                vaxes[1] = Vector(0.05f,0,0);
                vaxes[2] = Vector(0,0.05f,0);
                vaxes[3] = Vector(0,0,0.05f);

                for(int i = 0; i < 4; ++i) {
                    Vector p = tglobal*vaxes[i];
                    dReal fx = p.x*camInfoMsg.P[0] + p.y*camInfoMsg.P[1] + p.z*camInfoMsg.P[2] + camInfoMsg.P[3];
                    dReal fy = p.x*camInfoMsg.P[4] + p.y*camInfoMsg.P[5] + p.z*camInfoMsg.P[6] + camInfoMsg.P[7];
                    dReal fz = p.x*camInfoMsg.P[8] + p.y*camInfoMsg.P[9] + p.z*camInfoMsg.P[10] + camInfoMsg.P[11];
                    X[i].x = (int)(fx/fz);
                    X[i].y = (int)(fy/fz);
                }

                // draw three lines
                cv::Scalar col0(255,0,(64*itype)%256);
                cv::Scalar col1(0,255,(64*itype)%256);
                cv::Scalar col2((64*itype)%256,(64*itype)%256,255);
                cv::line(frame, X[0], X[1], col0, 1);
                cv::line(frame, X[0], X[2], col1, 1);
                cv::line(frame, X[0], X[3], col2, 1);

                // draw all the points
                for(size_t i = 0; i < cb.grid3d.size(); ++i) {
                    Vector grid3d_vec(cb.grid3d[i].x, cb.grid3d[i].y, cb.grid3d[i].z);
                    Vector p = tlocal * grid3d_vec;
                    dReal fx = p.x*camInfoMsg.P[0] + p.y*camInfoMsg.P[1] + p.z*camInfoMsg.P[2] + camInfoMsg.P[3];
                    dReal fy = p.x*camInfoMsg.P[4] + p.y*camInfoMsg.P[5] + p.z*camInfoMsg.P[6] + camInfoMsg.P[7];
                    dReal fz = p.x*camInfoMsg.P[8] + p.y*camInfoMsg.P[9] + p.z*camInfoMsg.P[10] + camInfoMsg.P[11];
                    int x = (int)(fx/fz);
                    int y = (int)(fy/fz);
                    cv::circle(frame, cv::Point(x,y), 6, cv::Scalar(0,0,0), 2);
                    cv::circle(frame, cv::Point(x,y), 2, cv::Scalar(0,0,0), 2);
                    cv::circle(frame, cv::Point(x,y), 4, cv::Scalar(64*itype,128,128), 3);
                }

                cv::circle(frame, X[0], 3, cv::Scalar(255,255,128), 3);
                // publish X[0]
                geometry_msgs::PointStamped point_msg;
                point_msg.header = imagemsg.header;
                point_msg.point.x = X[0].x;
                point_msg.point.y = X[0].y;
                point_msg.point.z = vobjects[vobjects.size() - 1].pose.position.z;
                _pubCornerPoint.publish(point_msg);
                
            }

            cv::imshow("Checkerboard Detector",frame);
            cv::waitKey(1);
        }

        return true;
    }


    //////////////////////////////////////////////////////////////////////////////
    // FindTransformation
    geometry_msgs::Pose FindTransformation(
        const vector<cv::Point2f> &imgpts, const vector<cv::Point3f> &objpts,
        const Transform& tlocal,
        const image_geometry::PinholeCameraModel& model)
    {
        geometry_msgs::Pose pose;
        Transform tchecker;
        cv::Mat R3_mat, T3_mat;
        cv::solvePnP(objpts, imgpts,
                     model.intrinsicMatrix(),
                     model.distortionCoeffs(),
                     R3_mat, T3_mat, false);
        double fR3[3];
        for (size_t i = 0; i < 3; i++) {
          fR3[i] = R3_mat.at<double>(i);
        }
        tchecker.trans.x = T3_mat.at<double>(0);
        tchecker.trans.y = T3_mat.at<double>(1);
        tchecker.trans.z = T3_mat.at<double>(2);
        double fang = sqrt(fR3[0]*fR3[0] + fR3[1]*fR3[1] + fR3[2]*fR3[2]);
        if( fang >= 1e-6 ) {
            double fmult = sin(fang/2)/fang;
            tchecker.rot = Vector(cos(fang/2),fR3[0]*fmult, fR3[1]*fmult, fR3[2]*fmult);
        }

        Transform tglobal = tchecker*tlocal;
        pose.position.x = tglobal.trans.x;
        pose.position.y = tglobal.trans.y;
        pose.position.z = tglobal.trans.z;
        pose.orientation.x = tglobal.rot.y;
        pose.orientation.y = tglobal.rot.z;
        pose.orientation.z = tglobal.rot.w;
        pose.orientation.w = tglobal.rot.x;
        return pose;
    }
};

////////////////////////////////////////////////////////////////////////////////
// MAIN
int main(int argc, char **argv)
{
    ros::init(argc,argv,"checkerboard_detector");
    if( !ros::master::check() )
        return 1;
  
    CheckerboardDetector cd;
    ros::spin();

    return 0;
}
