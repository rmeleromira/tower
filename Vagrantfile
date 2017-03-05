# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.hostname = "tower"
  config.vm.network "public_network",
    :dev => "br0",
    :mode => "bridge",
    :type => "bridge"
    

  config.vm.provider :libvirt do |lv|
    lv.memory = "8192"
    lv.cpus = "4"
    lv.graphics_ip = "192.168.1.96"
    
  end
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provision.yml"
  end
end
