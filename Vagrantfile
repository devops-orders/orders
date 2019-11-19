# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://atlas.hashicorp.com/search.
    config.vm.box = "ubuntu/bionic64"
    config.vm.hostname = "flask"

    # accessing "localhost:8080" will access port 80 on the guest machine.
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
    # config.vm.network "forwarded_port", guest: 3306, host: 3306, host_ip: "127.0.0.1"

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    config.vm.network "private_network", ip: "192.168.33.10"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    config.vm.provider "virtualbox" do |vb|
      # Customize the amount of memory on the VM:
      vb.memory = "512"
      vb.cpus = 1
      # Fixes some DNS issues on some networks
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end

    # Copy your .gitconfig file so that your git credentials are correct
    if File.exists?(File.expand_path("~/.gitconfig"))
      config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
    end

    # Copy the ssh keys into the vm for git access
    if File.exists?(File.expand_path("~/.ssh/id_rsa"))
      config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
    end

    if File.exists?(File.expand_path("~/.ssh/id_rsa.pub"))
      config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
    end

    # Copy your .vimrc file so that your vi looks like you expect
    if File.exists?(File.expand_path("~/.vimrc"))
      config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
    end

    # Copy your IBM Clouid API Key if you have one
    if File.exists?(File.expand_path("~/.bluemix/apikey.json"))
      config.vm.provision "file", source: "~/.bluemix/apikey.json", destination: "~/.bluemix/apikey.json"
    end

    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
    config.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y git python3 python3-pip python3-venv
      apt-get -y autoremove
      # Install app dependencies
      cd /vagrant
       pip3 install -r requirements.txt
    SHELL

    ######################################################################
    # Add MySQL docker container
    ######################################################################
    # docker run -d --name postgres -p 5432:5432 -v psql_data:/var/lib/postgresql/data postgres
    config.vm.provision :docker do |d|
      d.pull_images "mysql:5.5.62"
      d.run "mysql:5.5.62",
         args: "-d --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_ROOT_HOST='%' -p 3306:3306"
    end

    config.vm.provision "shell", inline: <<-SHELL
      echo "waiting for 10 seconds"  
      sleep 10
      echo "waiting 10 more"
      sleep 10
      cd /vagrant
      docker exec mysql mysql -uroot -proot -e "CREATE DATABASE test;"
    SHELL

    ######################################################################
    # Setup a Bluemix and Kubernetes environment
    ######################################################################
    config.vm.provision "shell", inline: <<-SHELL
    echo "\n************************************"
    echo " Installing IBM Cloud CLI..."
    echo "************************************\n"
    # Install IBM Cloud CLI as Vagrant user
    # curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
    sudo -H -u vagrant sh -c 'curl -sL http://ibm.biz/idt-installer | bash'
    sudo -H -u vagrant sh -c 'ibmcloud config --usage-stats-collect false'
    sudo -H -u vagrant sh -c "echo 'source <(kubectl completion bash)' >> ~/.bashrc"
    sudo -H -u vagrant sh -c "echo alias ic=/usr/local/bin/ibmcloud >> ~/.bash_aliases"
    echo "\n"
    echo "If you have an IBM Cloud API key in ~/.bluemix/apiKey.json"
    echo "You can login with the following command:"
    echo "\n"
    echo "ibmcloud login -a https://cloud.ibm.com --apikey @~/.bluemix/apiKey.json -r us-south"
    echo "\n"
    echo "\n************************************"
    echo " For the Kubernetes Dashboard use:"
    echo " kubectl proxy --address='0.0.0.0'"
    echo "************************************\n"
  SHELL

  end
