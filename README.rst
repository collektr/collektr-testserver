Collektr test server
====================

This is a stand-alone test server with a dummy data set to develop client
applications against.

Installation
------------

It is assumed that you are trying to run this software under Ubuntu. ::

    sudo apt-get install python-pip python-virtualenv virtualenvwrapper
    mkvirtualenv collektr

Note that the prompt should have changed now and show ``(collektr)$``. ::

    git clone https://github.com/collektr/test-server.git
    cd test-server
    setvirtualenvproject
    pip install -r requirements.txt

Running the test server
-----------------------

::

    workon collektr
    python -m testserver


