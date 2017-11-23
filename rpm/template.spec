Name:           ros-indigo-jsk-perception
Version:        1.2.3
Release:        0%{?dist}
Summary:        ROS jsk_perception package

Group:          Development/Libraries
License:        BSD
URL:            http://jsk-docs.readthedocs.io/en/latest/jsk_recognition/doc/jsk_perception
Source0:        %{name}-%{version}.tar.gz

Requires:       PyYAML
Requires:       eigen3-devel
Requires:       h5py
Requires:       libleveldb-devel
Requires:       python-scikit-learn
Requires:       ros-indigo-angles
Requires:       ros-indigo-cv-bridge
Requires:       ros-indigo-dynamic-reconfigure
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-image-geometry
Requires:       ros-indigo-image-transport
Requires:       ros-indigo-image-view
Requires:       ros-indigo-image-view2
Requires:       ros-indigo-imagesift
Requires:       ros-indigo-jsk-data
Requires:       ros-indigo-jsk-gui-msgs
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-recognition-utils
Requires:       ros-indigo-jsk-rqt-plugins
Requires:       ros-indigo-jsk-topic-tools
Requires:       ros-indigo-libcmt
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-mk
Requires:       ros-indigo-ml-classifiers
Requires:       ros-indigo-nodelet
Requires:       ros-indigo-opencv-apps
Requires:       ros-indigo-openni2-launch
Requires:       ros-indigo-pcl-ros
Requires:       ros-indigo-posedetection-msgs
Requires:       ros-indigo-robot-self-filter
Requires:       ros-indigo-rosbag
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-roseus
Requires:       ros-indigo-rospack
Requires:       ros-indigo-rospy
Requires:       ros-indigo-rostopic
Requires:       ros-indigo-rqt-gui
Requires:       ros-indigo-rviz
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-sound-play
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-tf
Requires:       yaml-cpp-devel
BuildRequires:  eigen3-devel
BuildRequires:  git
BuildRequires:  ros-indigo-angles
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cmake-modules
BuildRequires:  ros-indigo-cv-bridge
BuildRequires:  ros-indigo-dynamic-reconfigure
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-image-geometry
BuildRequires:  ros-indigo-image-transport
BuildRequires:  ros-indigo-image-view2
BuildRequires:  ros-indigo-jsk-data
BuildRequires:  ros-indigo-jsk-recognition-msgs
BuildRequires:  ros-indigo-jsk-recognition-utils
BuildRequires:  ros-indigo-jsk-tools
BuildRequires:  ros-indigo-jsk-topic-tools
BuildRequires:  ros-indigo-libcmt
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-mk
BuildRequires:  ros-indigo-nodelet
BuildRequires:  ros-indigo-opencv-apps
BuildRequires:  ros-indigo-pcl-ros
BuildRequires:  ros-indigo-posedetection-msgs
BuildRequires:  ros-indigo-robot-self-filter
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-roseus
BuildRequires:  ros-indigo-roslaunch
BuildRequires:  ros-indigo-roslint
BuildRequires:  ros-indigo-rospack
BuildRequires:  ros-indigo-rostest
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  yaml-cpp-devel

%description
ROS nodes and nodelets for 2-D image perception.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Thu Nov 23 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.2.3-0
- Autogenerated by Bloom

* Sun Jul 23 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.2.2-0
- Autogenerated by Bloom

* Sat Jul 15 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.2.1-0
- Autogenerated by Bloom

* Sat Jul 15 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.2.0-0
- Autogenerated by Bloom

* Fri Jul 07 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.3-0
- Autogenerated by Bloom

* Fri Jun 16 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.2-0
- Autogenerated by Bloom

* Thu Feb 09 2017 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.1.0-0
- Autogenerated by Bloom

* Tue Dec 13 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.0.1-0
- Autogenerated by Bloom

* Mon Dec 12 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 1.0.0-0
- Autogenerated by Bloom

* Sun Oct 30 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.29-0
- Autogenerated by Bloom

* Sat Oct 29 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.28-0
- Autogenerated by Bloom

* Fri Sep 16 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.25-0
- Autogenerated by Bloom

* Thu Sep 15 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.24-0
- Autogenerated by Bloom

* Wed Sep 14 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.23-0
- Autogenerated by Bloom

* Tue Sep 13 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.22-0
- Autogenerated by Bloom

* Fri Apr 15 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.21-0
- Autogenerated by Bloom

* Thu Apr 14 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.20-0
- Autogenerated by Bloom

* Tue Mar 22 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.19-0
- Autogenerated by Bloom

* Mon Mar 21 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.18-0
- Autogenerated by Bloom

* Sun Mar 20 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.17-0
- Autogenerated by Bloom

* Thu Feb 11 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.16-0
- Autogenerated by Bloom

* Tue Feb 09 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.15-0
- Autogenerated by Bloom

* Fri Feb 05 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.14-0
- Autogenerated by Bloom

* Sun Dec 20 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-1
- Autogenerated by Bloom

* Sun Dec 20 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-0
- Autogenerated by Bloom

* Fri Dec 18 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.11-0
- Autogenerated by Bloom

* Thu Dec 17 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.10-0
- Autogenerated by Bloom

* Wed Dec 16 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.9-0
- Autogenerated by Bloom

* Fri Dec 11 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.8-1
- Autogenerated by Bloom

* Fri Sep 11 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.6-0
- Autogenerated by Bloom

* Wed Sep 09 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.5-0
- Autogenerated by Bloom

* Mon Sep 07 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.4-0
- Autogenerated by Bloom

* Sun Sep 06 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.3-0
- Autogenerated by Bloom

* Sat Sep 05 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.2-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.1-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.0-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.18-0
- Autogenerated by Bloom

* Fri Aug 21 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.17-0
- Autogenerated by Bloom

* Wed Aug 19 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.16-0
- Autogenerated by Bloom

* Tue Aug 18 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.15-0
- Autogenerated by Bloom

* Fri Aug 14 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.14-0
- Autogenerated by Bloom

* Fri Jun 19 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.13-0
- Autogenerated by Bloom

* Mon May 04 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.12-0
- Autogenerated by Bloom

* Mon Apr 13 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.11-0
- Autogenerated by Bloom

* Thu Apr 09 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.10-0
- Autogenerated by Bloom

* Wed Apr 01 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.9-0
- Autogenerated by Bloom

* Thu Mar 26 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.7-0
- Autogenerated by Bloom

* Wed Mar 25 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.6-0
- Autogenerated by Bloom

* Tue Mar 17 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.5-0
- Autogenerated by Bloom

* Mon Mar 09 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.4-0
- Autogenerated by Bloom

* Mon Feb 02 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.3-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.2-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.1-0
- Autogenerated by Bloom

* Thu Jan 29 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.2.0-0
- Autogenerated by Bloom

