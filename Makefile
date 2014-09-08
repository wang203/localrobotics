
BASENAME=$(shell basename $(PATHNAME))
GITREPO=cloudmesh

TAG=`cat VERSION.txt`
MANUALDIR=`pwd`


all:
	make -f Makefile sphinx

setup:
	make -f Makefile setupbuild_ubuntu

FILE=index

watchdog:
	watchmedo shell-command --patterns="*.rst" --recursive --command="make; open doc/build/html/$(FILE).html" . 

c:
	/usr/bin/google-chrome-stable doc/build/html/index.html

f: 
	firefox doc/build/html/index.html 

view:
	open doc/build/html/index.html

#############################################################################
# SETUP SPHINX BUILD ENVIRONMENT
###############################################################################

setupbuild_ubuntu:
	#essential system packages/libraries required
	sudo apt-get install g++ python-dev python-pip python-virtualenv git libfreetype6-dev libpng-dev mercurial make
	#manually install sphinxcontrib-autorun
	mkdir -p ~/hg
	cd ~/hg; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/; cd sphinx-contrib/autorun; python setup.py install
	#setting up essential building requirements
	cd $(MANUALDIR)
	pip install -r requirements_pre.txt
	easy_install -U distribute
	pip install -r requirements.txt
	pip uninstall PIL

#############################################################################
# SPHINX DOC
###############################################################################

sphinx:
	cd doc; make html



