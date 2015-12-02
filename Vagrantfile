Vagrant.configure("2") do |config|

  # Tell Vagrant where would you like to start your VMs (you can also have a
  # specific per-VM configuration. Do not put this section in case you want to
  # start your VMs on the same host)
  config.vm.provider :libvirt do |libvirt|
    libvirt.driver = 'kvm'
  end

  # Let's provision it by running a script. You can also run
  # puppet, chef, ansible, and others. Check the Vagrant website for
  # details.
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbooks/vmx.yml"
    ansible.groups = {
      "routers" => ["vRX1"]
    }
  end

  # Here's our VM confguration
  config.vm.define :vRX1 do |machine|

    # It should be an Ubuntu 14.04 box
    machine.vm.box = "ubuntu/trusty64"

    # With a public IP (it's optional)
    # machine.vm.network :public_network, ip: '192.168.48.193', :dev => "br0", :mode => 'bridge'
    # With so much RAM and CPUs
    machine.vm.provider :libvirt do |domain|
      domain.memory = 2048
      domain.cpus = 2
    end

  end
end

