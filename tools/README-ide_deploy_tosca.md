Project deployment tool
=======================

Introduction
------------

The `ide_deploy_tosca.sh` is a helper script, which executes the following
steps:

* packages the blueprint and the resource files,
* submits the blueprint bundle to the deployment service,
* waits for the deployment to finish, and
* displays the outputs.

Its main purpose is to provide to IDEs a single point of execution, ideally
to be used as a build target of a data-intensive application build target.

The tool accepts a number of command line parameters. It also accepts a single
parameter containing a path to the DICE deployment project file containing all
the needed deployment parameters.

Installation
------------

First, obtain the DICE deployment tools as described in the
[Getting the DICE deployment service](AdminGuide.md#getting-the-dice-deployment-service).
Then make sure that the `ide_deploy_tosca.sh` and the `dice-deployment-cli` are
accessible in system paths. E.g.:

    $ cd /usr/bin
    $ sudo ln -s "${DICE_DEPLOYMENT_TOOLS_PATH}/tools/ide_deploy_tosca.sh" .
    $ sudo ln -s "${DICE_DEPLOYMENT_TOOLS_PATH}/tools/dice-deployment-cli" .

Usage
-----

### Project file

When used in the project file mode, the tool has the following usage:

    $ ./ide_deploy_tosca.sh project.dice-delivery

The `project.dice-delivery` is the path to the configuration file containing
configuration, which looks like the following sample:

```
BLUEPRINT_PATH=model/spark-openstack.yaml
RESOURCES_PATH=resources
DEPLOYER_URL=http://10.10.43.22/
USERNAME=admin
PASSWORD=passvv0rd
CONTAINER=6681034c-3419-4da0-91b3-aa4f481f29df
```

The configuration parameters have the following meaning:

* `BLUEPRINT_PATH`: path to the TOSCA yaml blueprint. This path is relative to
  the path of the `project.dice-delivery`.
* `RESOURCES_PATH`: path to the folder containing resources to be bundled with
  the blueprint. This path is relative to the path of the
  `project.dice-delivery`.
* `DEPLOYER_URL`: URL of the deployment service.
* `USERNAME`: user name part of the credentials to the deployment service.
* `PASSWORD`: password name part of the credentials to the deployment service.
* `CONTAINER`: UUID of the container to deploy into.

The script will create a bundle and save it as `bin/blueprint.tar.gz`, relative
to the path of th e`project.dice-delivery`.

**Warning:** *this file contains plaintext credentials. As a result, we
do not recommend committing this file to the repository.*

### Command line parameters

An alternative usage lets the user provide all the needed parameters at the
command line. The usage in this case is as follows:

    $ ./ide_deploy_tosca.sh BLUEPRINT_PATH RESOURCES_PATH DEPLOYER_URL \
       USERNAME PASSWORD CONTAINER [ BIN_PATH ]

The meaning of the parameters is similar to the [#Project file] mode:

* `BLUEPRINT_PATH`: path to the TOSCA yaml blueprint.
* `RESOURCES_PATH`: path to the folder containing resources to be bundled with
  the blueprint.
* `DEPLOYER_URL`: URL of the deployment service.
* `USERNAME`: user name part of the credentials to the deployment service.
* `PASSWORD`: password name part of the credentials to the deployment service.
* `CONTAINER`: UUID of the container to deploy into.
* `BIN_PATH`: output path to where the blueprint package will be created;
  default value: `bin`.

Using from IDEs
---------------

### Sublime Text

Sublime Text enables custom build targets. For Sublime Text 3, create a file,
e.g., `DICE-Deployment.sublime-build` in `~/.config/sublime-text-3/Packages/User/`
with the following contents:

```
{
	"shell_cmd": "ide_deploy_tosca.sh $folder/project.dice-delivery"
}
```

This should make a **DICE-Deployment** option appear in the Tools -> Build 
system. Selecting it and then runnung Tools -> Build will run the script.

### Eclipse

Eclipse enables configuration of external tools, which can be executed from the
user's workspace. Built-in variables contain values describing the user's
current project, file being edited or other information on the tool
execution's context. These can be passed to the external tool to make it
process files being edited in the Eclipse.

We assume that the user will be editing their DIA in a Java (or any other
language or environment) project. In the root directory of the project, they
need to place the `project.dice-delivery` file as detailed
[above](#project-file).

We add the DICE deployment service's tool to the list of external tools as
follows:

* Open Run -> External Tools Configuration
* On the left side of the dialog select **Program** and click on **New launch
  configuration** icon at the top
* Name the launch configuration, e.g. "DICE deploy TOSCA blueprint"
* Make sure the Main tab is active
* Enter the path to your installation of the script in the Location field. E.g.,
  `/usr/bin/ide_deploy_tosca.sh`
* In the Arguments field, provide the path to the `project.dice-delivery` file.
  This will be relative to the current project, located in the path stored in the
  `${project_loc}` variable, thus we input the following:
  `"${project_loc}/project.dice-delivery"`
* Click **Apply** to save the tool configuration

Now the user can select "DICE deploy TOSCA blueprint" from the Run external
tool drop down on the main toolbar. This will execute the tool in the background
with the output of the tool appearing in the Output Console of Eclipse.