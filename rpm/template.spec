Name:           ros-indigo-jsk-recognition-utils
Version:        0.3.14
Release:        0%{?dist}
Summary:        ROS jsk_recognition_utils package

Group:          Development/Libraries
License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-eigen-conversions
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-image-geometry
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-topic-tools
Requires:       ros-indigo-pcl-msgs
Requires:       ros-indigo-pcl-ros
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-tf
Requires:       ros-indigo-tf-conversions
Requires:       ros-indigo-tf2-ros
Requires:       ros-indigo-visualization-msgs
Requires:       yaml-cpp-devel
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-eigen-conversions
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-image-geometry
BuildRequires:  ros-indigo-jsk-recognition-msgs
BuildRequires:  ros-indigo-jsk-topic-tools
BuildRequires:  ros-indigo-pcl-msgs
BuildRequires:  ros-indigo-pcl-ros
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-tf-conversions
BuildRequires:  ros-indigo-tf2-ros
BuildRequires:  ros-indigo-visualization-msgs
BuildRequires:  yaml-cpp-devel

%description
The jsk_recognition_utils package

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
* Fri Feb 05 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.14-0
- Autogenerated by Bloom

* Sun Dec 20 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-1
- Autogenerated by Bloom

* Sun Dec 20 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-0
- Autogenerated by Bloom

* Fri Dec 18 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.11-0
- Autogenerated by Bloom

* Thu Dec 17 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.10-0
- Autogenerated by Bloom

* Wed Dec 16 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.9-0
- Autogenerated by Bloom

* Fri Dec 11 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.8-1
- Autogenerated by Bloom

* Fri Sep 11 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.6-0
- Autogenerated by Bloom

* Wed Sep 09 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.5-0
- Autogenerated by Bloom

* Mon Sep 07 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.4-0
- Autogenerated by Bloom

* Sun Sep 06 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.3-0
- Autogenerated by Bloom

* Sat Sep 05 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.2-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.1-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.0-0
- Autogenerated by Bloom

* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.18-0
- Autogenerated by Bloom

