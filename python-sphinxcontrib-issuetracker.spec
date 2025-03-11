#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_with	tests	# unit tests (not ready for pytest 4+)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
#
Summary:	Sphinx extension to reference issues in issue trackers
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do tworzenia odnośników do systemów śledzenia zgłoszeń
Name:		python-sphinxcontrib-issuetracker
Version:	0.11
Release:	13
License:	BSD
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/s/sphinxcontrib-issuetracker/sphinxcontrib-issuetracker-%{version}.tar.gz
# Source0-md5:	69c2f0e5770c5d7bad73f60f8d764e28
Source1:	http://docs.python.org/objects.inv?/python-objects.inv
# Source1-md5:	173c3f7fb1ad2162f1f194a5267700db
Source2:	http://sphinx.pocoo.org/objects.inv?/sphinx-objects.inv
# Source2-md5:	5f30379fe116fbace2636d5284df8622
Patch0:		%{name}-offline.patch
Patch1:		sphinxcontrib-issuetracker-sphinx1.7.patch
# TODO: unfinished updates for pytest 4+
Patch2:		sphinxcontrib-issuetracker-pytest.patch
URL:		https://pypi.org/project/sphinxcontrib-issuetracker/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Sphinx >= 1.7
BuildRequires:	python-mock >= 0.7
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-pytest < 4
BuildRequires:	python-requests >= 1.1
# launchpadlib, SOAPpy>=0.12.5, debianbts>=1.10
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 1.7
BuildRequires:	python3-pytest >= 3.0
BuildRequires:	python3-pytest < 4
BuildRequires:	python3-requests >= 1.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-requests >= 1.1
# already installed package
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-3 >= 1.1
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Sphinx extension to reference issues in issue trackers, either
explicitly with an "issue" role or optionally implicitly by issue ids
like "#10" in plaintext.

%description -l pl.UTF-8
Rozszerzenie Sphinksa do umieszczania odnośników do systemów śledzenia
zgłoszeń - wprost poprzez regułę "issue" lub opcjonalnie poprzez numer
zgłoszenia zapisany tekstowo (np. "#10").

%package -n python3-sphinxcontrib-issuetracker
Summary:	Sphinx extension to reference issues in issue trackers
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do tworzenia odnośników do systemów śledzenia zgłoszeń
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-sphinxcontrib-issuetracker
A Sphinx extension to reference issues in issue trackers, either
explicitly with an "issue" role or optionally implicitly by issue ids
like "#10" in plaintext.

%description -n python3-sphinxcontrib-issuetracker -l pl.UTF-8
Rozszerzenie Sphinksa do umieszczania odnośników do systemów śledzenia
zgłoszeń - wprost poprzez regułę "issue" lub opcjonalnie poprzez numer
zgłoszenia zapisany tekstowo (np. "#10").

%package apidocs
Summary:	API documentation for sphinxcontrib-issuetracker module
Summary(pl.UTF-8):	Dokumentacja API modułu sphinxcontrib-issuetracker
Group:		Documentation

%description apidocs
API documentation for sphinxcontrib-issuetracker module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu sphinxcontrib-issuetracker.

%prep
%setup -q -n sphinxcontrib-issuetracker-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

cp -p %{SOURCE1} %{SOURCE2} doc

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst CREDITS LICENSE README.rst
%{py_sitescriptdir}/sphinxcontrib/issuetracker
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*.egg-info
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-sphinxcontrib-issuetracker
%defattr(644,root,root,755)
%doc CHANGES.rst CREDITS LICENSE README.rst
%{py3_sitescriptdir}/sphinxcontrib/issuetracker
%{py3_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*.egg-info
%{py3_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
