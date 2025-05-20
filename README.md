# honyakux
bite-sized translation practice

A very simple python script that fetches a random sentence from syosetu (you can pick any novels you like). You then try to translate this sentence yourself. When ready, press enter and an LLM will give a translation for you.

Designed to run on Linux systems. Windows system might also work.

## Installation
1. install the following requirements:
* Python
	* "requests" package
 	* "googletrans==4.0.0-rc1" package 
 	* "pykakasi" package [If you are going to use `translate`]
 	* "MeCab" package [If you are going to use `translate`]
* ollama (+ model you want to use such as llama3)
* MeCab (not the package!) [If you are going to use `translate`]
* Git
  
2. Clone this repo to your local folder: `git clone github.com/Diptipper/honyakux`
3. Go to the folder `honyaku` and run the following commands (replace ... by your global path to the folder):

 	chmod +x ./honyakux.sh
	chmod +x ./translate.sh
	sudo ln -s /Users/.../honyakux/honyakux.sh /usr/local/bin/honyakux
	sudo ln -s /Users/.../honyakux/translate.sh /usr/local/bin/translate

You have to add the permission to use the shell script first (go to the folder and run `chmod +x ./honyakux.sh` and `chmod +x ./translate.sh`).

Also, make sure you install MeCab and add the correct path to the system. To find the path, enter this in the terminal

	% find /opt/homebrew -name mecabrc
 	<some paths should appear>
  
add the following command to beginning of `translate.sh`

	export MECABRC=<path without quotation>



To modify the novel database, add another file <novel_id>.dat in novel_data folder. Inside the file, enter the number of chapters. You don't have to come back and update the number of chapters every time. The program try to check if there's more chapter automatically.
