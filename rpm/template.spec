Name:           ros-kinetic-jsk-perception
Version:        1.1.3
Release:        0%{?dist}
Summary:        ROS jsk_perception package

Group:          Development/Libraries
License:        BSD
URL:            http://jsk-docs.readthedocs.io/en/latest/jsk_recognition/doc/jsk_perception
Source0:        %{name}-%{version}.tar.gz

Requires:       eigen3-devel
Requires:       h5py
Requires:       libleveldb-devel
Requires:       python-scikit-learn
Requires:       ros-kinetic-angles
Requires:       ros-kinetic-cv-bridge
Requires:       ros-kinetic-dynamic-reconfigure
Requires:       ros-kinetic-geometry-msgs
Requires:       ros-kinetic-image-geometry
Requires:       ros-kinetic-image-transport
Requires:       ros-kinetic-image-view
Requires:       ros-kinetic-image-view2
Requires:       ros-kinetic-imagesift
Requires:       ros-kinetic-jsk-data
Requires:       ros-kinetic-jsk-gui-msgs
Requires:       ros-kinetic-jsk-recognition-msgs
Requires:       ros-kinetic-jsk-recognition-utils
Requires:       ros-kinetic-jsk-topic-tools
Requires:       ros-kinetic-libcmt
Requires:       ros-kinetic-message-runtime
Requires:       ros-kinetic-mk
Requires:       ros-kinetic-nodelet
Requires:       ros-kinetic-opencv-apps
Requires:       ros-kinetic-openni2-launch
Requires:       ros-kinetic-pcl-ros
Requires:       ros-kinetic-posedetection-msgs
Requires:       ros-kinetic-robot-self-filter
Requires:       ros-kinetic-rosbag
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-roseus
Requires:       ros-kinetic-rospack
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rostopic
Requires:       ros-kinetic-rqt-gui
Requires:       ros-kinetic-sensor-msgs
Requires:       ros-kinetic-sound-play
Requires:       ros-kinetic-std-msgs
Requires:       ros-kinetic-tf
Requires:       yaml-cpp-devel
BuildRequires:  eigen3-devel
BuildRequires:  git
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-cmake-modules
BuildRequires:  ros-kinetic-cv-bridge
BuildRequires:  ros-kinetic-dynamic-reconfigure
BuildRequires:  ros-kinetic-geometry-msgs
BuildRequires:  ros-kinetic-image-geometry
BuildRequires:  ros-kinetic-image-transport
BuildRequires:  ros-kinetic-image-view2
BuildRequires:  ros-kinetic-jsk-data
BuildRequires:  ros-kinetic-jsk-recognition-msgs
BuildRequires:  ros-kinetic-jsk-recognition-utils
BuildRequires:  ros-kinetic-jsk-tools
BuildRequires:  ros-kinetic-jsk-topic-tools
BuildRequires:  ros-kinetic-libcmt
BuildRequires:  ros-kinetic-message-generation
BuildRequires:  ros-kinetic-mk
BuildRequires:  ros-kinetic-nodelet
BuildRequires:  ros-kinetic-opencv-apps
BuildRequires:  ros-kinetic-pcl-ros
BuildRequires:  ros-kinetic-posedetection-msgs
BuildRequires:  ros-kinetic-robot-self-filter
BuildRequires:  ros-kinetic-roscpp
BuildRequires:  ros-kinetic-roseus
BuildRequires:  ros-kinetic-roslaunch
BuildRequires:  ros-kinetic-roslint
BuildRequires:  ros-kinetic-rospack
BuildRequires:  ros-kinetic-rostest
BuildRequires:  ros-kinetic-sensor-msgs
BuildRequires:  ros-kinetic-std-msgs
BuildRequires:  ros-kinetic-tf
BuildRequires:  yaml-cpp-devel

%description
ROS nodes and nodelets for 2-D image perception.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Fri Jul 14 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.3-0
- Autogenerated by Bloom

* Sat Mar 04 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.1-0
- Autogenerated by Bloom

* Sun Feb 12 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.0-2
- Autogenerated by Bloom

