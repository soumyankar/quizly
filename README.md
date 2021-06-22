# GetSetQuiz
Home of the core build of the quizly web application.


## Installation

* Clone the repo and change directory:  

```bash
git clone https://github.com/soumyankar/quizly.git
cd quizly/
```

* [**IMPORTANT**] Initialize a `virtualenv` and activate.  
As an additional check make sure that your console reads the `virtualenv` label as _Sherlock2.0_ after activating.

```bash
virtualenv -p python3 ./
source bin/activate
```  

* Install necessary packages for the flask application

```bash
pip install -r requirements.txt
```

* Test run the application!

```bash
python main.py
```  

Head over to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) on your favourite browser.

## Contributing  

* Fork the repo first.

* Clone the repo and change directory:  

```bash
git clone https://github.com/soumyankar/quizly.git
cd quizly/
```

* Make changes to the code and submit a PR!

```bash
git add -A
git commit -m "Super cool feature added"
git push origin master
```

Now you can submit a PR!
Remember to change the `requirements.txt` file in case you make any changes to the package managers. You can do this by:

```bash
pip-chill --no-version > requirements.txt
```

## Troubleshooting

In case you do not have `virtualenv` installed have a look down below.  

### Linux  
```bash
# Debian, Ubuntu
$ sudo apt-get install python-virtualenv

# CentOS, Fedora
$ sudo yum install python-virtualenv

# Arch
$ sudo pacman -S python-virtualenv
```

### Mac OS X or Windows  
```bash
$ sudo python2 Downloads/get-pip.py
$ sudo python2 -m pip install virtualenv
```

### On windows as administrator
```bash
> \Python27\python.exe Downloads\get-pip.py
> \Python27\python.exe -m pip install virtualenv
```

Now you can return to the Installation Notes to continue.