# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :forwarded_port, guest:8000, host:8000,
    auto_correct: true

  config.vm.provision "shell",
    inline: "echo 'alias activate=\"sudo apt-get -y update; sudo apt-get install -y python-pip; sudo pip install virtualenv; sudo virtualenv --always-copy /vagrant/venv/; source /vagrant/venv/bin/activate; sudo pip install -r /vagrant/SigmaPi/requirements.txt; cd /vagrant/SigmaPi/;
\"' >> /home/vagrant/.bashrc"


end
