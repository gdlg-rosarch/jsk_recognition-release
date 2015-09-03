Name:           ros-indigo-jsk-recognition
Version:        0.2.18
Release:        0%{?dist}
Summary:        ROS jsk_recognition package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/jsk_recognition
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ros-indigo-checkerboard-detector
Requires:       ros-indigo-imagesift
Requires:       ros-indigo-jsk-pcl-ros
Requires:       ros-indigo-jsk-perception
Requires:       ros-indigo-jsk-recognition-msgs
Requires:       ros-indigo-jsk-recognition-utils
Requires:       ros-indigo-resized-image-transport
BuildRequires:  ros-indigo-catkin

%description
Metapackage that contains recognition package for jsk-ros-pkg

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
* Fri Sep 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.18-0
- Autogenerated by Bloom

* Fri Aug 21 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.17-0
- Autogenerated by Bloom

* Wed Aug 19 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.16-0
- Autogenerated by Bloom

* Tue Aug 18 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.15-0
- Autogenerated by Bloom

* Fri Aug 14 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.14-0
- Autogenerated by Bloom

* Fri Jun 19 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.13-0
- Autogenerated by Bloom

* Mon May 04 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.12-0
- Autogenerated by Bloom

* Mon Apr 13 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.11-0
- Autogenerated by Bloom

* Thu Apr 09 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.10-0
- Autogenerated by Bloom

* Wed Apr 01 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.9-0
- Autogenerated by Bloom

* Thu Mar 26 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.7-0
- Autogenerated by Bloom

* Wed Mar 25 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.6-0
- Autogenerated by Bloom

* Tue Mar 17 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.5-0
- Autogenerated by Bloom

* Mon Mar 09 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.4-0
- Autogenerated by Bloom

* Mon Feb 02 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.3-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.2-0
- Autogenerated by Bloom

* Fri Jan 30 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.1-0
- Autogenerated by Bloom

* Thu Jan 29 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.2.0-0
- Autogenerated by Bloom

