#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
#
Summary:	Sphinx extension to reference issues in issue trackers
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do tworzenia odnośników do systemów śledzenia zgłoszeń
Name:		python-sphinxcontrib-issuetracker
Version:	0.11
Release:	7
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/s/sphinxcontrib-issuetracker/sphinxcontrib-issuetracker-%{version}.tar.gz
# Source0-md5:	69c2f0e5770c5d7bad73f60f8d764e28
Source1:	http://docs.python.org/objects.inv?/python-objects.inv
# Source1-md5:	173c3f7fb1ad2162f1f194a5267700db
Source2:	http://sphinx.pocoo.org/objects.inv?/sphinx-objects.inv
# Source2-md5:	5f30379fe116fbace2636d5284df8622
Patch0:		%{name}-offline.patch
URL:		http://pypi.python.org/pypi/sphinxcontrib-issuetracker
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
Requires:	python-requests >= 0.13
%if %{with doc}
BuildRequires:	python-requests >= 0.13
BuildRequires:	sphinx-pdg-2 >= 1.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
Requires:	python3-requests >= 0.13
%if %{with doc}
BuildRequires:	python3-requests >= 0.13
BuildRequires:	sphinx-pdg-3 >= 1.1
%endif
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

%prep
%setup -q -n sphinxcontrib-issuetracker-%{version}
%patch0 -p1

cp -p %{SOURCE1} %{SOURCE2} doc

%build
%if %{with python2}
%py_build

%if %{with doc}
PYTHONPATH=$(pwd)/build-2/lib \
%{__make} -C doc html SPHINXBUILD=sphinx-build-2
mv doc/_build doc/_build2
%endif
%endif

%if %{with python3}
%py3_build

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/lib \
%{__make} -C doc html SPHINXBUILD=sphinx-build-3
mv doc/_build doc/_build3
%endif
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
%doc CHANGES.rst CREDITS LICENSE README.rst %{?with_doc:doc/_build3/html}
# top dir should belong to python-Sphinx?
%dir %{py_sitescriptdir}/sphinxcontrib
%dir %{py_sitescriptdir}/sphinxcontrib/issuetracker
%{py_sitescriptdir}/sphinxcontrib/issuetracker/*.py[co]
%{py_sitescriptdir}/sphinxcontrib/issuetracker/issuetracker.css
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*.egg-info
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-sphinxcontrib-issuetracker
%defattr(644,root,root,755)
%doc CHANGES.rst CREDITS LICENSE README.rst %{?with_doc:doc/_build3/html}
# top dir should belong to python-Sphinx?
%dir %{py3_sitescriptdir}/sphinxcontrib
%{py3_sitescriptdir}/sphinxcontrib/issuetracker
%{py3_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*.egg-info
%{py3_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*-nspkg.pth
%endif
