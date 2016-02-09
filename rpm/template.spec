Name:           ros-jade-jsk-recognition-msgs
Version:        0.3.15
Release:        0%{?dist}
Summary:        ROS jsk_recognition_msgs package

Group:          Development/Libraries
License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jade-geometry-msgs
Requires:       ros-jade-message-generation
Requires:       ros-jade-pcl-msgs
Requires:       ros-jade-sensor-msgs
Requires:       ros-jade-std-msgs
BuildRequires:  ros-jade-catkin
BuildRequires:  ros-jade-geometry-msgs
BuildRequires:  ros-jade-message-generation
BuildRequires:  ros-jade-pcl-msgs
BuildRequires:  ros-jade-sensor-msgs
BuildRequires:  ros-jade-std-msgs

%description
The jsk_recognition_msgs package

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
* Tue Feb 09 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.15-0
- Autogenerated by Bloom

* Sat Feb 06 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.14-1
- Autogenerated by Bloom

* Thu Feb 04 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.14-0
- Autogenerated by Bloom

* Wed Feb 03 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-20
- Autogenerated by Bloom

* Wed Feb 03 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-19
- Autogenerated by Bloom

* Tue Feb 02 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-18
- Autogenerated by Bloom

* Mon Feb 01 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-17
- Autogenerated by Bloom

* Sun Jan 31 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-16
- Autogenerated by Bloom

* Sat Jan 30 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-15
- Autogenerated by Bloom

* Fri Jan 29 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-14
- Autogenerated by Bloom

* Thu Jan 28 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-13
- Autogenerated by Bloom

* Wed Jan 27 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-12
- Autogenerated by Bloom

* Tue Jan 26 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-11
- Autogenerated by Bloom

* Mon Jan 25 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-10
- Autogenerated by Bloom

* Sun Jan 24 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-9
- Autogenerated by Bloom

* Sun Jan 24 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-8
- Autogenerated by Bloom

* Mon Jan 18 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-7
- Autogenerated by Bloom

* Mon Jan 11 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-6
- Autogenerated by Bloom

* Mon Jan 04 2016 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-5
- Autogenerated by Bloom

* Mon Dec 28 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-4
- Autogenerated by Bloom

* Mon Dec 21 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-3
- Autogenerated by Bloom

* Sun Dec 20 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-2
- Autogenerated by Bloom

* Sun Dec 20 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.13-1
- Autogenerated by Bloom

* Fri Dec 18 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.11-0
- Autogenerated by Bloom

* Fri Dec 11 2015 Ryohei Ueda <ueda@jsk.t.u-tokyo.ac.jp> - 0.3.8-1
- Autogenerated by Bloom

