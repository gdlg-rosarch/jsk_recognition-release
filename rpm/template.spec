Name:           ros-hydro-checkerboard-detector
Version:        0.1.25
Release:        0%{?dist}
Summary:        ROS checkerboard_detector package

Group:          Development/Libraries
License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-cv-bridge
Requires:       ros-hydro-dynamic-tf-publisher
Requires:       ros-hydro-eigen-conversions
Requires:       ros-hydro-jsk-pcl-ros
Requires:       ros-hydro-message-filters
Requires:       ros-hydro-posedetection-msgs
Requires:       ros-hydro-rosconsole
Requires:       ros-hydro-roscpp
Requires:       ros-hydro-sensor-msgs
Requires:       ros-hydro-tf
Requires:       ros-hydro-tf2
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-cv-bridge
BuildRequires:  ros-hydro-dynamic-tf-publisher
BuildRequires:  ros-hydro-eigen-conversions
BuildRequires:  ros-hydro-jsk-pcl-ros
BuildRequires:  ros-hydro-message-filters
BuildRequires:  ros-hydro-posedetection-msgs
BuildRequires:  ros-hydro-rosconsole
BuildRequires:  ros-hydro-roscpp
BuildRequires:  ros-hydro-sensor-msgs
BuildRequires:  ros-hydro-tf
BuildRequires:  ros-hydro-tf2

%description
Uses opencv to find checkboards and compute their 6D poses with respect to the
image. Requires the image to be calibrated. Parameters: display - show the
checkerboard detection rect%d_size_x - size of checker in x direction
rect%d_size_y - size of checker in y direction grid%d_size_x - number of
checkers in x direction grid%d_size_y - number of checkers in y direction There
can be more than one grid%d declared, the numbers should grow consecutively
starting at 0.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p build && cd build
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/hydro" \
        -DCMAKE_PREFIX_PATH="/opt/ros/hydro" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
cd build
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Sat Nov 22 2014 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.1.25-0
- Autogenerated by Bloom

