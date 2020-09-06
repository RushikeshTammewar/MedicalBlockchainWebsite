## MedicalBlockchainWebsite

### Installing developer environment for hyperledger fabric (Refer- https://hyperledger.github.io/composer/latest/installing/development-tools.html)
1) Essential CLI tools:
```
$ npm install -g composer-cli@0.19
```
2) Utility for running a REST Server on your machine to expose your business networks as RESTful APIs:
```
$ npm install -g composer-rest-server@0.19
```
3) Useful utility for generating application assets:
```
$ npm install -g generator-hyperledger-composer@0.19
```
4) Yeoman is a tool for generating applications, which utilises generator-hyperledger-composer:
```
$ npm install -g yo
```

### Install Playground: Browser app for simple editing and testing Business Networks
```
$ npm install -g composer-playground
```

### Install Hyperledger Fabric
This step gives you a local Hyperledger Fabric runtime to deploy your business networks to.<br>
In a directory of your choice (we will assume ~/fabric-dev-servers), get the .tar.gz file that contains the tools to install Hyperledger Fabric:
```
$ mkdir ~/fabric-dev-servers && cd ~/fabric-dev-servers
$ curl -O https://raw.githubusercontent.com/hyperledger/composer-tools/master/packages/fabric-dev-servers/fabric-dev-servers.tar.gz
$ tar -xvf fabric-dev-servers.tar.gz
```
A zip is also available if you prefer: just replace the .tar.gz file with fabric-dev-servers.zip and the tar -xvf command with a unzip command in the preceding snippet.<br>
Use the scripts you just downloaded and extracted to download a local Hyperledger Fabric v1.1 runtime:<br>
```
$ cd ~/fabric-dev-servers
$ export FABRIC_VERSION=hlfv11
$ ./downloadFabric.sh
```
### Install Python Packages for Recommendation System
```
$ pip3 install -r requirements.txt
```

### Starting and stopping Hyperledger Fabric
The first time you start up a new runtime, you'll need to run the start script, then generate a PeerAdmin card:
```
$ cd ~/fabric-dev-servers
$ export FABRIC_VERSION=hlfv11
$ ./startFabric.sh
$ ./createPeerAdminCard.sh
```
You can start and stop your runtime using ~/fabric-dev-servers/stopFabric.sh, and start it again with ~/fabric-dev-servers/startFabric.sh.<br>
At the end of your development session, you run ~/fabric-dev-servers/stopFabric.sh and then ~/fabric-dev-servers/teardownFabric.sh.<br> 

### Starting composer-playground
```
$ composer-playground
```
It will typically open your browser automatically, at the following address: http://localhost:8080/login<br>

### Running web application (Refer - https://hyperledger.github.io/composer/v0.19/applications/web)
1) First start hyperledger fabric runtime by above commands
```
$ cd ~/fabric-dev-servers<br>
$ ./startFabric.sh
$ ./createPeerAdminCard.sh
```
2) Install the Business Network Archive onto the Hyperledger Fabric network
```
$ composer network install --card PeerAdmin@hlfv1 --archiveFile healthcare_blockchain@0.0.1.bna
```
3) Start your Business Network on your Hyperledger Fabric
```
$ composer network start --networkName healthcare_blockchain --networkVersion 0.0.1 --networkAdmin admin --networkAdminEnrollSecret adminpw --card PeerAdmin@hlfv1 --file networkadmin.card
```
4) Install the 'admin' card ready for use
```
$ composer card import --file networkadmin.card
```
5) Deploy composer-rest-server
```
$ composer-rest-server -c admin@healthcare_blockchain -n never -u true -d Y
```
6) Running the node app locally
```
$ node app.js
```
7) Now open index.html, you will have to provide your id and userType (patient or doctor).<br>
8) Various html pages are provided corresponding to different transactions (inferred from fileName).<br>
