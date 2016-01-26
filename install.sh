virtualenv $HOME/venv
. $HOME/venv/bin/activate
pip install -U pip
pip install -Ur requirements.txt
cd $HOME; git clone https://github.com/CitrineInformatics/pypif.git ; cd pypif ; python setup.py install ; cd -
export PYTHONPATH=$HOME/pypif

