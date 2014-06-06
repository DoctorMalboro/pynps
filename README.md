pynps
=====

Library to work with NPS (payment gateway)

How to install
==============
Be sure to have installed the latest setuptools:
$: pip-3.3 install setuptools --upgrade

Then run:
$: python3 ./setup.py install

Finally, pynps will search for its config file 'pynps.yaml' at 
    1- If you are not root: ~/.config/pynps
    2- If you are root: /etc/pynps
Be sure to create that dir if its not exists and create the pynps.yaml inside.
In this package, at the examples/pynps/ you have a sample config file.

Thats all.
