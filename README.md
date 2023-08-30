# AUTODARTS-VOICE
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-voice/total.svg)](https://github.com/lbormann/autodarts-voice/releases/latest)

Autodarts-voice transcribes voice in realtime (offline) to control an autodarts-game. A running instance of https://github.com/lbormann/autodarts-caller is needed for processing commands.
Autodarts-voice uses vsok. check it out: https://alphacephei.com/vosk


## INSTALL INSTRUCTION

### Desktop-OS:

- If you're running a desktop-driven OS it's recommended to use [autodarts-desktop](https://github.com/lbormann/autodarts-desktop) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source:

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/autodarts-voice.git

Go to download-directory and type:

    pip3 install -r requirements.txt





## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/autodarts-caller - (latest version)
* Download and extract a model from here: https://alphacephei.com/vosk/models
* Make sure your machine is strong enough to handle complexity of chosen model (large models claim high memory usage).
* Make sure your microphone is configured as default in os.

### Run by executable

#### Example: Windows 

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\autodarts-voice.exe -MP "C:\\vosk-models\\vosk-model-small-en-us-0.15"

Save changes.
Click on the shortcut to start the application.


### Run by source

#### Example: Linux

    python3 autodarts-voice.py -MP "C:\\vosk-models\\vosk-model-small-en-us-0.15"


### Usage

* Speak loud and clear to the microphone. 
* Verify recognized words in terminal.
* Adjust keywords for wrong recognized words.


Here are some examples that could work out of the box with model [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip):

#### Dart-correction

- First twenty
- First single twenty
- Second triple twelve
- Third one
- Last double ten
- Second is two
- Last is number three
- Second is twenty five
- First is fifty

#### Go next

- Next

#### Go back

- Back
- Undo


 
### Arguments

- -CON / --connection [OPTIONAL] [Default: "127.0.0.1:8079"] 
- -MP / --model_path [REQUIRED] [Default: '']
- -KN / --keywords_next [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: ["next"]]
- -KU / --keywords_undo [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: ["undo", "back", "bag"]]
- -KFD / --keywords_first_dart [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: ["first", "for", "prime", "up"]]
- -KSD / --keywords_second_dart [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: ["second", "middle"]]


*`-CON / --connection`*

Host address to data-feeder (autodarts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address / usually you do NOT need to change this)

*`-MP / --model_path`*

You need to set an absolute path to your model directory. Moreover make sure the given path doesn't reside inside main-directory (autodarts-voice).

*`-K* / --keywords_*`*

For every argument starting with 'keywords' you can set multiple values.
    


_ _ _ _ _ _ _ _ _ _





## !!! IMPORTANT !!!

This application requires a running instance of autodarts-caller https://github.com/lbormann/autodarts-caller


## BUGS

It may be buggy. I've just coded it for fast fun with https://autodarts.io. You can give me feedback in Discord > wusaaa


## TODOs


### Done

- init project


## Resources

Icon by <a href="https://icon-icons.com/icon/microphone-musical-instrument/60191"></a> on <a href="https://icon-icons.com">icon-icons.com</a>
License <a href="https://creativecommons.org/licenses/by/4.0/">Attribution 4.0 International (CC BY 4.0)</a>                         
   

