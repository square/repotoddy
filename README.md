## Repotoddy

Repotoddy is a continuous deployment tool that works in conjunction with [Reposado](https://github.com/wdas/reposado). An open source tool that replicates the key functionality of macOS Server's Software Update Service.

#### How it Works.

Repotoddy works by automatically moving new updates from Apple's Software Update Release Branch up the list of any extra release branches you desire to create with Reposado. Lets say you have three release branches. Development, Testing, and Production. Each one of these branches representing a different group of Macs in your environment. When repotoddy runs it checks to see if there are any updates in Testing that are not in Production. If there are it will move these updates from Testing to Production. Next it will check to see if there are any updates in Development that are not in Testing. If there are it will move them from Development to Testing. Lastly it will pull down any new available updates from the Apple Release Branch and add them to Development Branch. It is designed to slowly roll out Apple Software Updates to groups of machines for proper testing in your environment, all without manual intervention.

#### Installation

The following instructions assume that you already have a reposado instance
setup and configured. Attempting to use repotoddy without doing so may lead to unexpected results. If you do not, [here](https://github.com/wdas/reposado/blob/master/docs/getting_started.md) is a good starting point.

1. Clone or download this repository and extract the files to a directory of
your choosing.
```sh
git clone https://github.com/square/repotoddy.git
```

2. Change directory into this location.
```sh
cd repotoddy
```

3. In order for repotoddy to work correctly it needs to know where reposado and some of its files are located. An easy way to do this is to create symlinks to reposado.
```sh
ln -s /path/to/reposado-git-clone/code/* .
```

4. You should now be ready to configure repotoddy.
```sh
./repotoddy --configure
```

5. Next you can run repotoddy for basic functionality.
```sh
./repotoddy --run
```

For other options and features of repotoddy run the following.
```sh
./repotoddy --help
```

### Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

```
Copyright 2017 Square, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
