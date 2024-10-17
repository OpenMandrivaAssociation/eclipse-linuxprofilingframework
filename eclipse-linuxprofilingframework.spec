%define src_repo_tag   R0_6_1
%define eclipse_base   %{_libdir}/eclipse
%define install_loc    %{_libdir}/eclipse/dropins/linuxprofilingframework
%define qualifier      201010081321

# Package in %%{_libdir} but no native code so no debuginfo
%global debug_package %{nil}

Name:           eclipse-linuxprofilingframework
Version:        0.6.1
Release:        4
Summary:        Eclipse Linux Tools Profiling Framework

Group:          Development/Java
License:        EPL
URL:            https://eclipse.org/linuxtools
# sh -x ./eclipse-linuxprofilingframework-fetch-src.sh %{src_repo_tag}
Source0:        %{name}-fetched-src-%{src_repo_tag}.tar.bz2
Source1:        %{name}-fetch-src.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# No CDT on ppc64
ExcludeArch: ppc64

BuildRequires: eclipse-pde >= 0:3.6.0
Requires: eclipse-platform >= 0:3.6.0
BuildRequires: eclipse-cdt >= 0:7.0.0
Requires: eclipse-cdt >= 0:7.0.0

%description
Plugins common to Eclipse Linux Tools profiling tools.

%prep
%setup -q -n %{name}-fetched-src-%{src_repo_tag}

%build
%{eclipse_base}/buildscripts/pdebuild -d cdt -f org.eclipse.linuxtools.profiling \
 -a "-DjavacSource=1.5 -DjavacTarget=1.5 -DforceContextQualifier=%{qualifier}" \
 -j -DJ2SE-1.5=%{_jvmdir}/java/jre/lib/rt.jar \

%install
rm -rf %{buildroot}
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}

unzip -q -d $RPM_BUILD_ROOT%{install_loc} \
     build/rpmBuild/org.eclipse.linuxtools.profiling.zip

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc org.eclipse.linuxtools.profiling-feature/epl-v10.html
%{install_loc}

