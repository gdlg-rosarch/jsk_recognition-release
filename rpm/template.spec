Name:           ros-indigo-jsk-perception
Version:        0.2.12
Release:        0%{?dist}
Summary:        ROS jsk_perception package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/jsk_perception
Source0:        %{name}-%{version}.tar.gz

Requires:       eigen3-devel
Requires:       ros-indigo-angles
Requires:       ros-indigo-cv-bridge
Requires:       ros-indigo-driver-base
Requires:       ros-indigo-dynamic-reconfigure
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-image-geometry
Requires:       ros-indigo-image-transport
Requires:       ros-indigo-image-view2
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-topic-tools
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-mk
Requires:       ros-indigo-nodelet
Requires:       ros-indigo-pcl-ros
Requires:       ros-indigo-posedetection-msgs
Requires:       ros-indigo-rosbuild
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-rospack
Requires:       ros-indigo-rospy
Requires:       ros-indigo-rostest
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-tf
BuildRequires:  eigen3-devel
BuildRequires:  git
BuildRequires:  ros-indigo-angles
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cmake-modules
BuildRequires:  ros-indigo-cv-bridge
BuildRequires:  ros-indigo-driver-base
BuildRequires:  ros-indigo-dynamic-reconfigure
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-image-geometry
BuildRequires:  ros-indigo-image-transport
BuildRequires:  ros-indigo-image-view2
BuildRequires:  ros-indigo-jsk-recognition-msgs
BuildRequires:  ros-indigo-jsk-topic-tools
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-mk
BuildRequires:  ros-indigo-nodelet
BuildRequires:  ros-indigo-pcl-ros
BuildRequires:  ros-indigo-posedetection-msgs
BuildRequires:  ros-indigo-rosbuild
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-rospack
BuildRequires:  ros-indigo-rospy
BuildRequires:  ros-indigo-rostest
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-tf

%description
jsk_perception

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

