# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :forwarded_port, guest:8000, host:8000,
    auto_correct: true

  # These commands, executed in order, will be aliased to "activate" on the VM.
  bootstrap_commands = ["sudo apt-get -y update;",
  						"sudo apt-get install -y python-pip;",
  						"sudo pip install virtualenv;",
  						"sudo virtualenv --always-copy /vagrant/venv/;",
  						"source /vagrant/venv/bin/activate;",
  						"sudo pip install -r /vagrant/SigmaPi/requirements.txt;",
  						"cd /vagrant/SigmaPi;"]

  coverage_commands = ["export PROJECT_PATH=/vagrant/SigmaPi/SPGammaIota/;",
                       "coverage run --source=$PROJECT_PATH manage.py test;",
                       "coverage report;"]

  config.vm.provision "shell",
    inline: "echo 'alias activate=\"#{bootstrap_commands.join()}\"' >> /home/vagrant/.bashrc;"+
            "echo 'alias cover=\"#{coverage_commands.join()}\"' >> /home/vagrant/.bashrc"

end
