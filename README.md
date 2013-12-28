# Sigma Pi Gamma Iota Chapter's website

This repository contains the files for Sigma Pi Gamma Iota Chaper's new website, which can be found at: https://sigmapigammaiota.org/

## To get started:

First of all, you'll need to clone the project:
* Run `git clone https://github.com/westleyrussell/SPGammaIota.git && cd SPGammaIota`

Dependencies are listed the SigmaPi/requirements.txt file. To automatically install all of the dependencies, you can use [Pip](http://www.pip-installer.org/en/latest/index.html)! I would also recommend using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to isolate this project from your desktop Python environment, but that is not strictly necessary.

* Run `pip install SigmaPi/requirements.txt` to install the dependencies.
* Run `python SigmaPi/manage.py runserver 0.0.0.0:8000` to start the app and host it locally.
* Connect to http://localhost:8000/ from a browser to see the site.

NOTE:
* If this is your first time starting the app, you may have to run `python SigmaPi/manage.py syncdb` and follow the prompts to create an admin account.

Alternatively, if you would like to use [Vagrant](http://www.vagrantup.com/), a handy tool for customizing and isolating development environments, you can simply run `vagrant up && vagrant ssh` from the root of the project and after some setup you will be connected to a virtual machine set up with this project's environment.

From here, you can see the project in the `/vagrant` folder. Run `python /vagrant/SigmaPi/manage.py runserver 0.0.0.0:8000` to start the app, but `python /vagrant/SigmaPi/manage.py syncdb` first to setup the database.
