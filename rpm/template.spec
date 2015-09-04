Name:           ros-hydro-jsk-recognition-utils
Version:        0.3.1
Release:        0%{?dist}
Summary:        ROS jsk_recognition_utils package

Group:          Development/Libraries
License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-hydro-eigen-conversions
Requires:       ros-hydro-geometry-msgs
Requires:       ros-hydro-image-geometry
Requires:       ros-hydro-jsk-recognition-msgs
Requires:       ros-hydro-jsk-topic-tools
Requires:       ros-hydro-pcl-msgs
Requires:       ros-hydro-pcl-ros
Requires:       ros-hydro-sensor-msgs
Requires:       ros-hydro-tf
Requires:       ros-hydro-tf-conversions
Requires:       ros-hydro-tf2-ros
BuildRequires:  ros-hydro-catkin
BuildRequires:  ros-hydro-eigen-conversions
BuildRequires:  ros-hydro-geometry-msgs
BuildRequires:  ros-hydro-image-geometry
BuildRequires:  ros-hydro-jsk-recognition-msgs
BuildRequires:  ros-hydro-jsk-topic-tools
BuildRequires:  ros-hydro-pcl-msgs
BuildRequires:  ros-hydro-pcl-ros
BuildRequires:  ros-hydro-sensor-msgs
BuildRequires:  ros-hydro-tf
BuildRequires:  ros-hydro-tf-conversions
BuildRequires:  ros-hydro-tf2-ros

%description
The jsk_recognition_utils package

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/hydro/setup.sh" ]; then . "/opt/ros/hydro/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
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
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/hydro

%changelog
* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.1-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.0-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.18-0
- Autogenerated by Bloom

