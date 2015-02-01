Name:           ros-indigo-jsk-pcl-ros
Version:        0.2.3
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
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-topic-tools
Requires:       ros-indigo-laser-assembler
Requires:       ros-indigo-message-runtime
Requires:       ros-indigo-ml-classifiers
Requires:       ros-indigo-moveit-core
Requires:       ros-indigo-moveit-ros-perception
Requires:       ros-indigo-nodelet
Requires:       ros-indigo-pcl-conversions
Requires:       ros-indigo-pcl-msgs
Requires:       ros-indigo-pcl-ros
Requires:       ros-indigo-rosboost-cfg
Requires:       ros-indigo-roscpp-tutorials
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-sklearn
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
BuildRequires:  ros-indigo-jsk-recognition-msgs
BuildRequires:  ros-indigo-jsk-topic-tools
BuildRequires:  ros-indigo-laser-assembler
BuildRequires:  ros-indigo-message-generation
BuildRequires:  ros-indigo-ml-classifiers
BuildRequires:  ros-indigo-moveit-core
BuildRequires:  ros-indigo-moveit-ros-perception
BuildRequires:  ros-indigo-nodelet
BuildRequires:  ros-indigo-pcl-conversions
BuildRequires:  ros-indigo-pcl-msgs
BuildRequires:  ros-indigo-pcl-ros
BuildRequires:  ros-indigo-rosboost-cfg
BuildRequires:  ros-indigo-roscpp-tutorials
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-sklearn
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
mkdir -p build && cd build
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
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Mon Feb 02 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.3-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.2-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.1-0
- Autogenerated by Bloom

* Thu Jan 29 2015 Youhei Kakiuchi <youhei@jsk.t.u-tokyo.ac.jp> - 0.2.0-0
- Autogenerated by Bloom

