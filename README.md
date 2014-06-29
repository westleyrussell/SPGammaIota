# Sigma Pi Gamma Iota Chapter's website

This repository contains the files for Sigma Pi Gamma Iota Chaper's new website, which can be found at: https://sigmapigammaiota.org/

## Set up your environment:

First of all, you'll need to clone the project:
* `git clone https://github.com/westleyrussell/SPGammaIota.git && cd SPGammaIota`

Then, you need to build this projects environment using [Vagrant](http://www.vagrantup.com/). If you have never used Vagrant before, you are strongly encouraged to read a little about it before proceeding. And if you haven't installed it, you will need to. Once vagrant is installed, here are the steps (to be run in the SPGammaIota directory):
* `vagrant up`
* `vagrant ssh`
* `activate`

Now the following has happened:
* You've started up an Ubunutu VM, and SSHed into it.
* The /vagrant folder within the VM is sychronized with your local SPGammaIota folder.
* The `activate` command installed all of the projects dependencies with Pip, and then left you off inside the /vagrant folder in the VM.

From here, you run the webserver (from within the VM) with:
* `python manage.py runserver 0.0.0.0:8000` (see the note below if this is your first time)
* This will run the Gunicorn server, and start it listening on port 8000.
* Port 8000 within the VM is forwarded to port 8000 on your host machine (thanks, Vagrant!), so you can now open up your web browser and visit http://localhost:8000/ to see the site.

NOTE:
* If this is your first time starting the app, you may have to run `python SigmaPi/manage.py syncdb` and follow the prompts to create an admin account to use locally.

## Start developing:
You may now edit the code in the SPGammaIota folder on your host machine, in any old editor like usual, and the changes you make will automatically be sychronized to the folder in the VM. Plus, since Django is running in DEBUG mode for development, you don't need to restart the server or anything to see your changes reflected in the browser.

## Stuck?
Get in contact with @austintrose however you can: he is responsible for helping you get the project running so you can just develop without worrying about the details.
