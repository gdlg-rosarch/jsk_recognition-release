Name:           ros-jade-imagesift
Version:        0.3.13
Release:        16%{?dist}
Summary:        ROS imagesift package

Group:          Development/Libraries
License:        LGPL
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jade-cv-bridge
Requires:       ros-jade-image-transport
Requires:       ros-jade-jsk-perception
Requires:       ros-jade-libsiftfast
Requires:       ros-jade-nodelet
Requires:       ros-jade-posedetection-msgs
Requires:       ros-jade-roscpp
Requires:       ros-jade-sensor-msgs
BuildRequires:  ros-jade-catkin
BuildRequires:  ros-jade-cmake-modules
BuildRequires:  ros-jade-cv-bridge
BuildRequires:  ros-jade-image-transport
BuildRequires:  ros-jade-jsk-perception
BuildRequires:  ros-jade-libsiftfast
BuildRequires:  ros-jade-nodelet
BuildRequires:  ros-jade-posedetection-msgs
BuildRequires:  ros-jade-roscpp
BuildRequires:  ros-jade-sensor-msgs

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
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/jade" \
        -DCMAKE_PREFIX_PATH="/opt/ros/jade" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/jade

%changelog
* Sun Jan 31 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-16
- Autogenerated by Bloom

* Sat Jan 30 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-15
- Autogenerated by Bloom

* Fri Jan 29 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-14
- Autogenerated by Bloom

* Thu Jan 28 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-13
- Autogenerated by Bloom

* Wed Jan 27 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-12
- Autogenerated by Bloom

* Tue Jan 26 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-11
- Autogenerated by Bloom

* Mon Jan 25 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-10
- Autogenerated by Bloom

* Sun Jan 24 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-9
- Autogenerated by Bloom

* Sun Jan 24 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-8
- Autogenerated by Bloom

* Mon Jan 18 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-7
- Autogenerated by Bloom

* Mon Jan 11 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-6
- Autogenerated by Bloom

* Mon Jan 04 2016 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-5
- Autogenerated by Bloom

* Mon Dec 28 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-4
- Autogenerated by Bloom

* Mon Dec 21 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-3
- Autogenerated by Bloom

* Sun Dec 20 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-2
- Autogenerated by Bloom

* Sun Dec 20 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.13-1
- Autogenerated by Bloom

* Fri Dec 18 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.11-0
- Autogenerated by Bloom

* Fri Dec 11 2015 Kei Okada <k-okada@jsk.t.u-tokyo.ac.jp> - 0.3.8-1
- Autogenerated by Bloom

