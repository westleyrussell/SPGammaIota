# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise64"

  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :forwarded_port, guest:8000, host:8000,
    auto_correct: true

  # Update so I'm getting latest pip
  config.vm.provision :shell,
    :inline => "sudo apt-get update"

  # Install pip
  config.vm.provision :shell,
    :inline => "sudo apt-get install -y python-pip"

  # Clear old osx/linux virtualenv
  config.vm.provision :shell,
    :inline => "sudo pip install -r /vagrant/SigmaPi/requirements.txt"

end
