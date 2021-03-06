# Instructions for adding tools to Galaxy via the commandline.

This set of instructions show how to:

  * Copy the manage_bootstrap_user.py file
  * Setup a admin user for the Galaxy server via the command line.
  * Get the user's api key
  * Add tools via the commandline
  * Delete the admin user from the database


## 1. Copy the bootstrap user script

  1. ssh to the server as ubuntu user.
  2. Clone this repo.
  ```
  git clone https://github.com/gvlproject/gvl.utilities.git
  ```
  3. Copy the `manage_bootstrap_user.py` script to the correct place.
  ```
  sudo su galaxy
  cp gvl.utilities/add_tools_to_Galaxy/manage_bootstrap_user.py /mnt/galaxy/galaxy-app/scripts/api/
  ```

## 2. Setup an admin user

  1. Make sure that postgres is running:

  ```
  sudo su postgres
  pg_ctl status -D /mnt/galaxy/db
  ```
  If this returns:

  ```
  pg_ctl: server is running (PID: 4258)
  /usr/lib/postgresql/9.3/bin/postgres "-D" "/mnt/galaxy/db"
  ```

  it's running. If not then do the following to start it up:

  ```
  pg_ctl -D /mnt/galaxy/db start
  exit
  ```

  2. Make sure Galaxy is running.

  You can do this by checking out the main.pid file or tailing the main.log file. If it is not running start it up:

  ```
  sudo su galaxy
  sh /mnt/galaxy/galaxy-app/run.sh --log_file main.log --pid_file main.pid --daemon
  ```

  To restart Galaxy at anytime use:

  ```
  sh /mnt/galaxy/galaxy-app/run.sh --log_file main.log --pid_file main.pid --stop-daemon
  sh /mnt/galaxy/galaxy-app/run.sh --log_file main.log --pid_file main.pid --daemon
  ```

  2. Now, create the admin user.

  ```
  sudo su galaxy
  cd /mnt/galaxy/galaxy-app
  source .venv/bin/activate
  python scripts/api/manage_bootstrap_user.py \
    -c /mnt/galaxy/galaxy-app/config/galaxy.ini \
    create \
    -e <email> \
    -u <username> \
    -p <password>
  ```
  where you've substituted appropriate username, email and password fields.
  This script will return the users api key. Cut and paste the key somewhere you can get to it as you'll need it for the rest of the process...

## 3. Add tools via the command line

You'll need to use the `install_tool_shed_tools.py` script for this. For each tool, you'll need to know its name, owner and the toolshed url.

Example command:
  ```
  python scripts/api/install_tool_shed_tools.py \
    -l http://127.0.0.1:8080 \
    -a 63bef48cbcf13ca9fe56c1f0a6558def \
    --name package_r_3_1_2 \
    --owner iuc \
    -u https://toolshed.g2.bx.psu.edu \
    --panel-section-id textutil \
    --repository-deps \
    --tool-deps
    -r changeset_revision
  ```

  where `-a` is the api key we recorded earlier and `--section` is the section in the tool menu you want this tool to appear in.

**Installation doesn't always work!** Sometimes you need to repair the repository... The script for this is located at `/mnt/galaxy/galaxy-app/scripts/api/repair_tool_shed_repository.py`

Example command:

  ```
  python scripts/api/repair_tool_shed_repository.py \
  -u "https://toolshed.g2.bx.psu.edu/" \
  -a bac0a28cefc2f002b378d5b41f0c0daa \
  -l 127.0.0.1:8080 \
  -n package_libxml2_2_9_1 \
  -o iuc \
  -r 45b16a3ab504
  ```

where `-a` is the api key, `-n` is the package name, `-o` is the owner and `-r` is the changeset revision number of the tool that needs repairing.

## 4. Delete the admin user

Once you have finished installing and repairing tools and you no longer require the admin user, it can be deleted via the following commands.

  ```
  sudo su galaxy
  cd /mnt/galaxy/galaxy-app
  source .venv/bin/activate
  python scripts/api/manage_bootstrap_user.py \
    -c /mnt/galaxy/galaxy-app/config/galaxy.ini \
    delete \
    --username <username>
  ```

  All done.

  Simon Gladman - 31-5-2016
