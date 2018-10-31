%{?_javapackages_macros:%_javapackages_macros}
Name:          simple-jndi
Version:       0.11.4.1
Release:       6.3
Summary:       A JNDI implementation
Group:         Development/Java
License:       BSD
Url:           http://code.google.com/p/osjava/
Source0:       http://osjava.googlecode.com/svn/dist/releases/official/simple-jndi/simple-jndi-0.11.4.1-src.tar.gz
# wget -O simple-jndi-0.11.4.1.pom http://osjava.googlecode.com/svn/releases/simple-jndi-0.11.4.1/pom.xml
Source1:       simple-jndi-%{version}.pom
Patch0:        simple-jndi-0.11.4.1-jdk7.patch

BuildRequires: java-devel
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: apache-commons-dbcp
BuildRequires: apache-commons-pool
BuildRequires: junit

Requires:      apache-commons-dbcp
Requires:      apache-commons-pool

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
Simple-JNDI is intended to solve two problems. The first is
that of finding a container independent way of opening a
database connection, the second is to find a good way of
specifying application configurations.
1. Unit tests or prototype code often need to emulate the
  environment within which the code is expected to run.
  A very common one is to get an object of type
  javax.sql.DataSource from JNDI so a java.sql.Connection
  to your database of choice may be opened.
2. Applications need configuration; a JNDI implementation
  makes a handy location for configuration values. Either
  as a globally available system, or via IoC through the
  use of some kind of JNDI configuration facade (see gj-config).
A solution: simple implementation of JNDI. It is entirely
library based, so no server instances are started, and it
sits upon Java .properties files, XML files or Windows-style
.ini files, so it is easy to use and simple to understand.
The files may be either on the file system or in the classpath.

%package javadoc

Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n simple-jndi-%{version}
find . -name "*.class" -delete
find . -name "*.jar" -delete
%patch0 -p0

# this test at random fails
rm -r src/test/org/osjava/sj/memory/SharedMemoryTest.java

%build

%ant \
  -Dlibdir=lib \
  -Dcommons-pool.jar=file://$(build-classpath commons-pool) \
  -Dcommons-dbcp.jar=file://$(build-classpath commons-dbcp) \
  jar javadoc

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}/

%files -f .mfiles
%doc LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 06 2012 gil cattaneo <puntogil@libero.it> 0.11.4.1-1
- initial rpm
