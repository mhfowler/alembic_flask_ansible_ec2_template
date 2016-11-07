# Ansible Flask Template

With this template I can quickly deploy a new webapp to the amazon cloud which logs error messages to slack, has database connectivity, and is configured by Ansible (allowing for idempotent server configuration &mdash; no need to remember server state). 

I find this very useful for getting small applications up and running quickly. It is also useful for starting a new project to know from the onset that 'deployment' is already taken care of so I can focus on the actual project.

In the past without Ansible I would sometimes end up creating monolithic apps which share infrastructure  to perform multiple functions &mdash; I used to do this  because "solving deployment again" was an intimidating task and so I would tack more functionality onto existing infrastructure to save time. 
Because this template allows me to quickly start projects with deployment already taken care of, it encourages me to make new projects completely independent with their own github repository and deployment server, leading to fully independent micro services that are more robust.

In a sense this template is like my own Heroku, but in addition to the convenience of quickly bringing up new machines I can extend and customize it, as well as save money by bringing up AWS micro instances for free. 



## Steps To Deploy

### 1. Edit devops/vars.yaml

This file contains the parameters which control Ansible. 

- **app_name**: unimportant, but is used for naming of some files (probably should just keep it as hello_webapp)
- **repo_url**: change this to the url of your github repository (e.g. git@github.com:mhfowler/alembic_flask_ansible_ec2_template.git)
- **repo_remote**: git remote to use on server (e.g. origin)
- **repo_branch**: git branch to use on server (e.g. master)
- **src_dir**: the path to where the webapp will be stored on server (probably shouldn't change)
- **log_dir**: the path to where logs will be written on the server (probably shouldn't change)
- **aws_key_name**: the name of the AWS ssh key which Ansible will use for authentication (must already exist in amazon)
- **aws_security_group**: the security group which the spawned server will belong to (security group must already exist)
- **aws_instance_name**: the tag which the spawned server will be given &mdash; this is important for identifying your new server in the AWS console (e.g. aws_default)
- **aws_key_location**: the path on your local computer to the SSH private key associated with aws_key_name listed above &mdash; this file must already exist on your computer
- **aws_subnet**: the aws subnet which the spawned server will belong to (this subnet must already exist in your amazon)
- **prod_url**: this attribute is not used. I included it because when I add cron jobs via ansible I often make use of this (e.g. http://test.com/)


### 2. Create devops/secret_files/secret.json

All the files contained within devops/secret_files are ignored from git because they contain passwords and other secret information.

The Ansible recipe copies the files in secret_files to the server (to the same relative location) during the deploy task, so that these files can be referenced relatively and expected to exist both locally and on the server.

devops/secret_files/secret.json must contain valid json with a number of keys which are used throughout the application. 

My secret.json looks something like this:
```_
{
    "SLACKBOT_TOKEN": "XXXX",
    "SLACK_CHANNEL_ID": "XXXXXX"
    "AWS_ACCESS_KEY_ID": "XXXX",
    "AWS_SECRET_ACCESS_KEY": "XXXXX",
    "TEST_DB_CONNECTION": "XXXXX",
}
```
SLACKBOT_TOKEN is for authenticating with slack (see hello_utilities/slack_helper.py https://api.slack.com/)
SLACK_CHANNEL_ID is the slack channel id which slack_helper logs to by default.
AWS_ACCESS_KEY_ID and AWS_SECRET_ACESS_KEY are your AWS authentication credentials.
TEST_DB_CONNECTION is a string for authenticating with the database. See get_db_url() in _hello_settings.py for how to configure this to be different for different environments.


### 3. Generate SSH Deploy Keys 

Run `devops/generate_deploy_ssh_keys.sh` 

As a location for the key to be written, choose, secret_files/deploy_rsa &mdash; this will create two files, one in devops/secret_files/deploy_rsa and one in devops/secret_files/deploy_rsa.pub

In the Deploy Keys tab of the settings page of your github repository, copy and paste deploy_rsa.pub as your deploy key.

These deploy keys will be copied to the server as part of the Ansible deployment and will be used to pull the github repository.


### 4. Initialize Alembic

Whatever database you have configured to connect to via the string TEST_DB_CONNECTION in secret.json must already exist.

This project uses alembic to manage schema migrations.

To initialize your database with the correct tables run: `alembic upgrade head`

In the future to auto-generate new migrations run: `alembic revision --autogenerate -m "initial tables"`
Then inspect the migration in alembic/versions/ and then run: `alembic upgrade head` to run the migration.


### 5. Spawn A Server 

`./spawn_server.sh`
https://open.spotify.com/track/1S8FBwS475qrBhJhWtqeiP

If everything is correct, Ansible will spawn a new micro instance in the amazon cloud and then will deploy your repository to the created instance and configure it to have a live nginx server sering your flask web app.

After the spawn_server.yml stage of spawn_server.sh a new line will be added to devops/hosts which contains the IP address of your new server. devops/hosts should look something like 
```
[webservers]
52.87.226.172 ansible_ssh_user=ubuntu ansible_ssh_private_key_file=<local__path_to_your_aws_private_ssh_key>
```

This IP address will also be printed out on the last line of the Ansible log to std.out.


### 6. Test 

In your web browser visit the IP address of your newly created instance &mdash; it should say 'hello hello'.

Visit /slack/ you should receive a slack message.

Visit /error/ this test page will force a 500 error which should log a message to slack with the error (to test that error logging is working).

Visit /test_db/ everytime you refresh this page a new random value should appear (as a new value is logged to the database)


## Deploying New Code

Whenever you want to deploy new code:
```
git push origin master
./deploy.sh; 
```
deploy.sh will deploy your new code to the server as well as do some configuration steps which often need to happen again after changes (e.g. copy secret.json, install python requirements etc.)

Conventionally setup_server.sh contains configurations tasks which only need to be run once (for the server intialization) and spawn_server.sh is only run when you want to bring up a new machine.


## Troubleshooting 

The first step of spawn_server.sh is to spawn a new server. If that succeeds, then there will be a new line in devops/hosts (you can also confirm this machine's existence in the AWS EC2 console).

To troubleshot spawn_server.sh confirm that a new machine has been created, and then you can try individually running setup_server.sh and deploy.sh to isolate problems (these steps are also attempted when you run spawn_server.sh).



## Design Ideas 

#### bash scripts as buttons 
I think of bash scripts in my repository as buttons which I am adding to my IDE. Right click and then click Run to use them.


#### secret.json 
Any keys and passwords which can't be saved in Git should be stored in devops/secret_files/secret.json.

Ansible will make sure this file is in the same relative location on the server as it is locally, and every run of deploy.sh will copy this file over to the server. Throughout your code you can access the contents of secret.json by importing SECRETS_DICT from hello_settings.py_


#### hello_settings.py
hello_settings.py is the genesis point from which all else flows. hello_settings.py should not import from any other files.


#### hello_utilities
I try to isolate functionality into small files which can function independently. Each of these files goes in hello_utilities. I use the \__main\__ method at the bottom of these files to write 'tests' which can be verified by running the files.


####  idempotent server configuration
ansible has been revolutionary for my personal projects because it allows me to say what my code is as well as what environment my code requires.

Because ansible playbooks are idempotent, if your recipes are written well, you no longer need to remember server state, you just need to know that when you re-run ansible it will make your server what it is supposed to be.
