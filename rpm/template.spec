Name:           ros-indigo-imagesift
Version:        0.2.10
Release:        0%{?dist}
Summary:        ROS imagesift package

Group:          Development/Libraries
License:        LGPL
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-cv-bridge
Requires:       ros-indigo-image-transport
Requires:       ros-indigo-jsk-perception
Requires:       ros-indigo-libsiftfast
Requires:       ros-indigo-posedetection-msgs
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cv-bridge
BuildRequires:  ros-indigo-image-transport
BuildRequires:  ros-indigo-jsk-perception
BuildRequires:  ros-indigo-libsiftfast
BuildRequires:  ros-indigo-posedetection-msgs
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-sensor-msgs

%description
For every image, computes its sift features and send a new message with the
image, its intrinsic parameters, and the features. Parameters include: display -
shows the image on the local computer

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

