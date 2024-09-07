# MYCEGO Test App

Данное тестовое задание было реализовано в течении 6 дней.
Начало реализации: 02.09.2024 в 12:00
Конец реализации (включая инструкцию по сетапу): 07.09.2024 в 19:05

В проекте были реализованы все требования, кроме 1 дополнительного - одновременного скачивания нескольких файлов по причине того,
чтобы не увеличить сроки. 

Инструкции по сетапу проекта:
1. download python 3.12.5:
- For Windows Users: https://www.python.org/downloads/release/python-3125/
- For Linux Users:

	- For Arch, Manjaro, Artix users:
		 (if yay not installed: 
		 1. `sudo pacman -Syu`
		 2. `sudo pacman -S --needed git base-devel`
		 3. `git clone https://aur.archlinux.org/yay.git`
		 4.  `cd yay && mkpkg -si`)
		`yay -S python312`

	- For Ubuntu, Debian, Mint users: 
		1. `sudo apt update && sudo apt upgrade -y`
		2. `sudo apt install -y software-properties-common`
		3. `sudo add-apt-repository ppa:deadsnakes/ppa`
		4. `sudo apt update`
		5. `sudo apt install -y python3.12`
  
- For MacOS users:
		(if brew not installed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`)
		1. `brew update`
		2. `brew install python@3.12`
		3. `export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"`
		4.`source ~/.zshrc  # or source ~/.bash_profile or source ~/.bashrc`
download pip (if it's not automatically downloaded with python):

	for Windows users:
		`python -m ensurepip`

	for Linux users:

	for Arch, Manjaro, Artix users:

			`sudo pacman -S python-pip`
  
	for Ubuntu, Debian, Mint Users:

			`sudo apt install python3-pip`
  
	for MacOS users:

		`python3 -m ensurepip`
  
2. git clone https://github.com/slsforme/mycego_test.git (ensure, that you downloaded git before)
3. activate virtual enviroment:
	Windows:

		`python -m venv env`
	Activation:			
	for cmd:

		`env\Scripts\activate`

	for PowerShell:
		`.\env\Scripts\Activate.ps1`

	Linux:

		`python3 -m venv env`
   
	Activation:

		`source env/bin/activate`

	MacOS:

		`python3 -m venv env`
	Activation:

		`source env/bin/activate`
	(personally I used virtualenv: https://virtualenv.pypa.io/en/latest/)
1. Moving into project dir:
	`cd mycego_test`
5. Download packages and dependencies:
	`pip install -r requirements.txt`
6. Running migrations for main modules:
	`python manage.py migrate`
7. Running local server: 
    `python manage.py runserver`

	 




