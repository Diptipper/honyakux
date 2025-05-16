# honyakux
bite-sized translation practice

A very simple python script that fetches a random sentence from syosetu (you can pick any novels you like). You then try to translate this sentence yourself. When ready, press enter and an LLM will give a translation for you.

Designed to run on Linux systems. Windows system might also work.

Requirements: python (+ the package "requests"), ollama (+ model you want to use such as llama3)

To modify the novel database, add another file <novel_id>.dat in novel_data folder. Inside the file, enter the number of chapters. You don't have to come back and update the number of chapters every time. The program try to check if there's more chapter automatically.
