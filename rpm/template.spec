Name:           ros-indigo-jsk-pcl-ros
Version:        0.3.17
Release:        0%{?dist}
Summary:        ROS jsk_pcl_ros package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/jsk_pcl_ros
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       python-scikit-learn
Requires:       ros-indigo-cv-bridge
Requires:       ros-indigo-diagnostic-msgs
Requires:       ros-indigo-diagnostic-updater
Requires:       ros-indigo-dynamic-reconfigure
Requires:       ros-indigo-eigen-conversions
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-image-geometry
Requires:       ros-indigo-image-transport
Requires:       ros-indigo-image-view2
Requires:       ros-indigo-interactive-markers
Requires:       ros-indigo-jsk-footstep-msgs
Requires:       ros-indigo-jsk-pcl-ros-utils
Requires:       ros-indigo-jsk-perception
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-recognition-utils
Requires:       ros-indigo-jsk-topic-tools
Requires:       ros-indigo-kdl-conversions
Requires:       ros-indigo-kdl-parser
Requires:       ros-indigo-laser-assembler
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-ml-classifiers
Requires:       ros-indigo-moveit-core
Requires:       ros-indigo-moveit-ros-perception
Requires:       ros-indigo-nav-msgs
Requires:       ros-indigo-nodelet
Requires:       ros-indigo-octomap
Requires:       ros-indigo-octomap-msgs
Requires:       ros-indigo-octomap-ros
Requires:       ros-indigo-octomap-server
Requires:       ros-indigo-pcl-conversions
Requires:       ros-indigo-pcl-msgs
Requires:       ros-indigo-pcl-ros
Requires:       ros-indigo-robot-self-filter
Requires:       ros-indigo-rosboost-cfg
Requires:       ros-indigo-roscpp-tutorials
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-std-srvs
Requires:       ros-indigo-stereo-msgs
Requires:       ros-indigo-tf
Requires:       ros-indigo-tf-conversions
Requires:       ros-indigo-tf2-ros
Requires:       ros-indigo-visualization-msgs
Requires:       yaml-cpp-devel
BuildRequires:  boost-devel
BuildRequires:  python-scikit-learn
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cv-bridge
BuildRequires:  ros-indigo-diagnostic-msgs
BuildRequires:  ros-indigo-diagnostic-updater
BuildRequires:  ros-indigo-dynamic-reconfigure
BuildRequires:  ros-indigo-eigen-conversions
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-image-geometry
BuildRequires:  ros-indigo-image-transport
BuildRequires:  ros-indigo-image-view2
BuildRequires:  ros-indigo-interactive-markers
BuildRequires:  ros-indigo-jsk-footstep-msgs
BuildRequires:  ros-indigo-jsk-pcl-ros-utils
BuildRequires:  ros-indigo-jsk-recognition-msgs
BuildRequires:  ros-indigo-jsk-recognition-utils
BuildRequires:  ros-indigo-jsk-tools
BuildRequires:  ros-indigo-jsk-topic-tools
BuildRequires:  ros-indigo-kdl-conversions
BuildRequires:  ros-indigo-kdl-parser
BuildRequires:  ros-indigo-laser-assembler
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-ml-classifiers
BuildRequires:  ros-indigo-moveit-core
BuildRequires:  ros-indigo-moveit-ros-perception
BuildRequires:  ros-indigo-nav-msgs
BuildRequires:  ros-indigo-nodelet
BuildRequires:  ros-indigo-octomap
BuildRequires:  ros-indigo-octomap-msgs
BuildRequires:  ros-indigo-octomap-ros
BuildRequires:  ros-indigo-octomap-server
BuildRequires:  ros-indigo-pcl-conversions
BuildRequires:  ros-indigo-pcl-msgs
BuildRequires:  ros-indigo-pcl-ros
BuildRequires:  ros-indigo-robot-self-filter
BuildRequires:  ros-indigo-rosboost-cfg
BuildRequires:  ros-indigo-roscpp-tutorials
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-std-srvs
BuildRequires:  ros-indigo-stereo-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-tf-conversions
BuildRequires:  ros-indigo-tf2-ros
BuildRequires:  ros-indigo-visualization-msgs
BuildRequires:  yaml-cpp-devel

%description
jsk_pcl_ros

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
* Sun Mar 20 2016 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.17-0
- Autogenerated by Bloom

* Thu Feb 11 2016 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.16-0
- Autogenerated by Bloom

* Tue Feb 09 2016 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.15-0
- Autogenerated by Bloom

* Fri Feb 05 2016 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.14-0
- Autogenerated by Bloom

* Sun Dec 20 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.13-1
- Autogenerated by Bloom

* Sun Dec 20 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.13-0
- Autogenerated by Bloom

* Fri Dec 18 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.11-0
- Autogenerated by Bloom

* Thu Dec 17 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.10-0
- Autogenerated by Bloom

* Wed Dec 16 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.9-0
- Autogenerated by Bloom

* Fri Dec 11 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.8-1
- Autogenerated by Bloom

* Fri Sep 11 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.6-0
- Autogenerated by Bloom

* Wed Sep 09 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.5-0
- Autogenerated by Bloom

* Mon Sep 07 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.4-0
- Autogenerated by Bloom

* Sun Sep 06 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.3-0
- Autogenerated by Bloom

* Sat Sep 05 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.2-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.1-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.3.0-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.18-0
- Autogenerated by Bloom

* Fri Aug 21 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.17-0
- Autogenerated by Bloom

* Wed Aug 19 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.16-0
- Autogenerated by Bloom

* Tue Aug 18 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.15-0
- Autogenerated by Bloom

* Fri Aug 14 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.14-0
- Autogenerated by Bloom

* Fri Jun 19 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.13-0
- Autogenerated by Bloom

* Mon May 04 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.12-0
- Autogenerated by Bloom

* Mon Apr 13 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.11-0
- Autogenerated by Bloom

* Thu Apr 09 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.10-0
- Autogenerated by Bloom

* Wed Apr 01 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.9-0
- Autogenerated by Bloom

* Thu Mar 26 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.7-0
- Autogenerated by Bloom

* Wed Mar 25 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.6-0
- Autogenerated by Bloom

* Tue Mar 17 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.5-0
- Autogenerated by Bloom

* Mon Mar 09 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.4-0
- Autogenerated by Bloom

* Mon Feb 02 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.3-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.2-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.1-0
- Autogenerated by Bloom

* Thu Jan 29 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.0-0
- Autogenerated by Bloom

