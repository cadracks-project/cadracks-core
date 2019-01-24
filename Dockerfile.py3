FROM guillaumeflorent/miniconda-pythonocc:3-0.18.3

MAINTAINER Guillaume Florent <guillaume.florent@tutanota.com>

# For wx : libgtk2.0-0 libxxf86vm1
# Funily, installing libgtk2.0-0 seems to solve the XCB plugin not found issue for Qt !!
# For pyqt : libgl1-mesa-dev libx11-xcb1
RUN apt-get update && apt-get install -y --no-install-recommends libgtk2.0-0 libxxf86vm1 libgl1-mesa-dev libx11-xcb1 && rm -rf /var/lib/apt/lists/*

# Other conda packages
RUN conda install -y numpy matplotlib wxpython pyqt networkx jinja2 pytest
RUN conda install -y -c gflorent corelib aocxchange aocutils>=18.2 ccad party

# cadracks_core
WORKDIR /opt
# ADD https://api.github.com/repos/cadracks/cadracks-core/git/refs/heads/master version.json
RUN git clone --depth=1 https://github.com/cadracks/cadracks-core
WORKDIR /opt/cadracks-core
RUN python setup.py install
