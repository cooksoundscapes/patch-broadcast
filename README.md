## Pure Data patch audio stream

Served in a HTTP endpoint.  
  
It works by serving a raw stream and a wav header, made with libpd and Flask.  
  
This repository is just a raw example of libpd + a micro web server, it's not ready to use. As it serves a wave file, it's not really a stream!

## Install & Usage

1. Create the virtual env:
```
python -m venv v_env
```
2. activate the environment:
```
source v_env/bin/activate
```
3. Install dependencies
```
pip install numpy flask
```
4. Install libpd for this virtual environment. After cloning and building libpd repo, cd to the python folder there and, with the virtual env activated, run:
```
make
sudo make install
```

For starting the server, the script requires a folder for the Pure Data project, and will attempt to read a main.pd file inside it, e.g:
```
./main.py analog-synth
```
