#!/bin/bash -v
set -e
cp -r monstrWeb /opt/.
systemctl restart httpd
systemctl status httpd

