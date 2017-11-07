RPMBUILD for etcd
=========================

etcd rpm

How to Build
=========
    git clone https://github.com/allanhung/rpm_etcd
    cd rpm_etcd
    docker run --name=etcd_build --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS/x86_64 -v $(pwd)/rpms:/root/rpmbuild/RPMS/noarch -v $(pwd)/scripts:/usr/local/src/build centos /bin/bash -c "/usr/local/src/build/build_etcd.sh 1.7.2"

# check
    docker run --name=etcd_check --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS centos /bin/bash -c "yum localinstall -y /root/rpmbuild/RPMS/etcd-*.rpm"
