Presentation
------------
This project implements the 15118-20 norm for the use case DC BPT Dynamic using *Python*.


Installation and configuration
------------------------------
To install the tool, it is fairly straightforward:

1. Download the git repository <https://gitlab.pleiade.edf.fr/R43/15118-20-v2g> and Miniconda <https://docs.conda.io/en/latest/miniconda.html>

.. code-block:: bash

    git clone https://gitlab.pleiade.edf.fr/R43/15118-20-v2g
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

2. Setup a virtual environment

.. code-block:: bash

    conda create -n edf15118-20 python=3.8

3. Install dependencies

.. code-block:: bash

    pip install -r requirements.txt // using pip
    conda install -f environment.yml // using conda

4. Configure the tool by modifying the *.ini* files.


Usage
-----

Launching protocol
==================
1. Set up the network settings (ports, interfaces, ChargeController,...)
2. Connect to serial terminals using *screen*
3. On the EVCC Charge Controller card, run to launch the driver:

.. code-block:: bash

    sh start_server.sh // to have the logging on scree
    systemctl start tcpserver.service // to have it on background
4. Start the EVSE, then the EV
5. Plug the cables

GUI
===

.. code-block:: bash

    python secc/evse_gui.py // run evse
    python secc/ev_gui.py   // run ev

To stop running, use the **stop** button on the EV side.

Log-based
=========

.. code-block:: bash

    python secc/start_evse.py // run evse
    python secc/start_ev.py   // run ev

To stop running, press **ENTER** on the EV side in the terminal.

Extras
------

Generating documentation
========================
To generate the documentation, go to *doc* and run:

.. code-block:: bash

    make html


Updating XSD files and associated XML classes
=============================================
To update the *XSD* files and the associated *XML* classes:

1. Make a backup of the old *XSD* files in *shared/xsd_files/previous_version*
2. Make a backup of the old *EXIG* files as well in *shared/exig_files/previous_version*
3. Copy the new *XSD* files in *shared/xsd_files/latest_version*
4. Generate the new *EXIG* files using **OpenEXI_Example4/OpenEXI_Example4.jar**
5. Copy the new *EXIG* files in *shared/exig_files/latest_version*
6. Delete *shared/xml_classes* package
7. Generate the new *XML* classes:

.. code-block:: bash

    xsdata shared/xsd_files/latest_version/V2G_CI_AppProtocol.xsd --package shared.xml_classes.app_protocol
    xsdata shared/xsd_files/latest_version/V2G_CI_CommonMessages.xsd --package shared.xml_classes.common_messages
    xsdata shared/xsd_files/latest_version/V2G_CI_DC.xsd --package shared.xml_classes.dc




Generating new certificates
===========================
To generate new certificates, go to *shared/certificates/* and run:

.. code-block:: bash

    ./generateCertificates.sh

Updating packages
=================
To update all **pip** packages, run:

.. code-block:: bash

    pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

Exporting dependencies
======================
To export dependencies, run:

.. code-block:: bash

    pip freeze > requirements.txt // using pip
    conda env export > environment.yml // using conda


Generating python file from QtDesigner
======================================
After generating *.ui* file, run:

.. code-block:: bash

    pyuic5 <name>.ui > <name>.py
