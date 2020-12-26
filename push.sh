#!/bin/bash -ex

echo '''
#!/bin/bash -ex

cd ~/repos/bunkerbowl
git fetch --all
git reset --hard origin/master
git pull
pip3 install -r requirements.txt
''' >> command.sh

chmod a+x command.sh
ssh pi@tardis 'bash -s' < command.sh
rm command.sh
