#
# Conditional build:
%bcond_without	doc	# HTML documentation build
#
Summary:	Sphinx extension to reference issues in issue trackers
Summary(pl.UTF-8):	Rozszerzenie Sphinksa do tworzenia odnośników do systemów śledzenia zgłoszeń
Name:		python-sphinxcontrib-issuetracker
Version:	0.11
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/s/sphinxcontrib-issuetracker/sphinxcontrib-issuetracker-%{version}.tar.gz
# Source0-md5:	69c2f0e5770c5d7bad73f60f8d764e28
Source1:	http://docs.python.org/objects.inv#/python-objects.inv
# Source1-md5:	9128e774ec21dcd62dc5bca61cdd91ee
Source2:	http://sphinx.pocoo.org/objects.inv#/sphinx-objects.inv
# Source2-md5:	4db0b6eb4e1f4635ad02669e5b1ba15e
Patch0:		%{name}-offline.patch
URL:		http://pypi.python.org/pypi/sphinxcontrib-issuetracker
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with doc}
BuildRequires:	python-requests >= 0.13
BuildRequires:	sphinx-pdg >= 1.1
%endif
Requires:	python-Sphinx >= 1.1
Requires:	python-requests >= 0.13
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

%prep
%setup -q -n sphinxcontrib-issuetracker-%{version}
%patch0 -p1

cp -p %{SOURCE1} %{SOURCE2} doc

%build
%{__python} setup.py build

%if %{with doc}
PYTHONPATH=$(pwd)/build/lib \
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CREDITS LICENSE README.rst %{?with_doc:doc/_build/html}
# top dir should belong to python-Sphinx?
%dir %{py_sitescriptdir}/sphinxcontrib
%dir %{py_sitescriptdir}/sphinxcontrib/issuetracker
%{py_sitescriptdir}/sphinxcontrib/issuetracker/*.py[co]
%{py_sitescriptdir}/sphinxcontrib/issuetracker/issuetracker.css
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*.egg-info
%{py_sitescriptdir}/sphinxcontrib_issuetracker-%{version}-py*-nspkg.pth
