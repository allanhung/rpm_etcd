ETCDVER=${1:-'3.2.9'}
RPMVER="${ETCDVER/-/_}"
MAJOR_VERION=${ETCDVER:0:1}
export RPMBUILDROOT=/root/rpmbuild
export GOPATH=/usr/share/gocode
export PATH=$GOPATH/bin:$PATH

# go repo
rpm --import https://mirror.go-repo.io/centos/RPM-GPG-KEY-GO-REPO
curl -s https://mirror.go-repo.io/centos/go-repo.repo | tee /etc/yum.repos.d/go-repo.repo
# epel
yum install -y epel-release
yum -y install golang git bzip2 rpm-build
mkdir -p $RPMBUILDROOT/SOURCES && mkdir -p $RPMBUILDROOT/SPECS && mkdir -p $RPMBUILDROOT/SRPMS
# fix rpm marcos
sed -i -e "s#.centos##g" /etc/rpm/macros.dist

# get etcd
mkdir -p $GOPATH/src/github.com/coreos
cd $GOPATH/src/github.com/coreos
git clone --depth=10 -b v$ETCDVER https://github.com/coreos/etcd.git

# build etcd
cd $GOPATH/src/github.com/coreos/etcd
./build

# build rpm
sed -e "s/^Version:.*/Version: $RPMVER/g" /usr/local/src/build/etcd.spec > $RPMBUILDROOT/SPECS/etcd.spec
/bin/cp -f /usr/local/src/build/etcd.service $RPMBUILDROOT/SOURCES/
/bin/cp -f /usr/local/src/build/etcd.conf $RPMBUILDROOT/SOURCES/
rpmbuild -bb $RPMBUILDROOT/SPECS/etcd.spec
