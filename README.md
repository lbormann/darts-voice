# AUTODARTS-VOICE
[![Downloads](https://img.shields.io/github/downloads/lbormann/autodarts-voice/total.svg)](https://github.com/lbormann/autodarts-voice/releases/latest)

Autodarts-voice transcribes your voice in realtime (offline) to control an autodarts-game. A running instance of https://github.com/lbormann/autodarts-caller is needed for processing commands.
Autodarts-voice uses vosk. check it out: https://alphacephei.com/vosk


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

On MacOS:

    pip3 install -r requirements_mac.txt





## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/autodarts-caller - (latest version)
* Download and extract a model from here: https://alphacephei.com/vosk/models (recommendable small ones, eg.: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
* Make sure your machine is strong enough to handle complexity of model (large models claim high memory usage and are slow).
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

- first twenty
- first is twenty
- second triple twelve
- third one
- last double ten
- second is two
- last is number three
- second is twenty five
- first is fifty
- last is miss

#### Go next turn

- next

#### Go next game

- next game

#### Go back

- back
- undo


 
### Arguments

- -MP / --model_path [REQUIRED] [Default: '']
- -L / --language [OPTIONAL] [Default: 1] [Possible values: 0 (no keyword-predefinitions) | 1 (english) | 2 (german)]
- -KNG / --keywords_next_game [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KN / --keywords_next [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KU / --keywords_undo [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFD / --keywords_first_dart [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSD / --keywords_second_dart [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTD / --keywords_third_dart [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KS / --keywords_single [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KD / --keywords_double [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KT / --keywords_triple [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KZERO / --keywords_zero [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KONE / --keywords_one [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTWO / --keywords_two [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTHREE / --keywords_three [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFOUR / --keywords_four [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFIVE / --keywords_five [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSIX / --keywords_six [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSEVEN / --keywords_seven [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KEIGHT / --keywords_eight [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KNINE / --keywords_nine [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTEN / --keywords_ten [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KELEVEN / --keywords_eleven [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTWELVE / --keywords_twelve [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTHIRTEEN / --keywords_thirteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFOURTEEN / --keywords_fourteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFIFTEEN / --keywords_fifteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSIXTEEN / --keywords_sixteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSEVENTEEN / --keywords_seventeen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KEIGHTEEN / --keywords_eighteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KNINETEEN / --keywords_nineteen [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTWENTY / --keywords_twenty [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KTWENTY_FIVE / --keywords_twenty_five [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KFIFTY / --keywords_fifty [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -CON / --connection [OPTIONAL] [Default: "127.0.0.1:8079"] 

*`-CON / --connection`*

Host address to data-feeder (autodarts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address)

*`-MP / --model_path`*

You need to set an absolute path to your model directory. Moreover make sure the given path doesn't reside inside main-directory (autodarts-voice).

*`-L / --language`*

Language defines which [predefined keywords](#Languages) should be used.


*`-K* / --keywords_*`*

For every argument starting with 'K'/'keywords' you can set multiple values that merged with predefined keywords except you set -L to 0.
    


_ _ _ _ _ _ _ _ _ _


## Languages

(Predefined keywords)

### English

    "NEXT_GAME": ["next game"],
    "NEXT": ["next"],
    "UNDO": ["undo", "back", "bag"],

    "FIRST_DART": ["first", "for", "prime", "up"],
    "SECOND_DART": ["second", "middle"],
    "THIRD_DART": ["third", "thought", "last", "down"],

    "SINGLE": ["single", "singer", "simple"],
    "DOUBLE": ["double", "stubble", "great", "big"],
    "TRIPLE": ["triple", "perfect", "tribal", "couple", "templar", "tumbler", "stripper"],
    
    "ZERO": ["zero", "miss", "his", "myth", "missed"],
    "ONE": ["one"],
    "TWO": ["two", "to", "too"],
    "THREE": ["three", "free"],
    "FOUR": ["four", "for", "thor"],
    "FIVE": ["five", "size"],
    "SIX": ["six"],
    "SEVEN": ["seven"],
    "EIGHT": ["eight", "aid"],
    "NINE": ["nine"],
    "TEN": ["ten", "turn"],
    "ELEVEN": ["eleven", "level"],
    "TWELVE": ["twelve", "twelfth"],
    "THIRTEEN": ["thirteen", "thirty"],
    "FOURTEEN": ["fourteen", "fourty"],
    "FIFTEEN": ["fifteen"],
    "SIXTEEN": ["sixteen", "sixty"],
    "SEVENTEEN": ["seventeen", "seventy"],
    "EIGHTEEN": ["eighteen", "eighty"],
    "NINETEEN": ["nineteen", "ninety"],
    "TWENTY": ["twenty"],
    "TWENTY_FIVE": ["twenty five", "bull", "bullet", "boy"],
    "FIFTY": ["fifty", "bullseye"]

### German

    "NEXT_GAME": ["nächstes spiel", "nächste spiel"],
    "NEXT": ["weiter"],
    "UNDO": ["zurück"],

    "FIRST_DART": ["erster", "erste", "erstens"],
    "SECOND_DART": ["zweiter", "zweite", "zweitens"],
    "THIRD_DART": ["dritter", "dritte", "drittens", "britta", "letzter"],

    "SINGLE": ["einfach", "normal", "normale"],
    "DOUBLE": ["doppel", "doppelt", "groß", "große"],
    "TRIPLE": ["dreifach", "perfekt", "perfekte"],
    
    "ZERO": ["null", "vorbei", "verhauen", "frauen"],
    "ONE": ["eins"],
    "TWO": ["zwei"],
    "THREE": ["drei"],
    "FOUR": ["vier"],
    "FIVE": ["fünf"],
    "SIX": ["sechs"],
    "SEVEN": ["sieben"],
    "EIGHT": ["acht"],
    "NINE": ["neun", "neuen"],
    "TEN": ["zehn"],
    "ELEVEN": ["elf"],
    "TWELVE": ["zwölf"],
    "THIRTEEN": ["dreizehn"],
    "FOURTEEN": ["vierzehn"],
    "FIFTEEN": ["fünfzehn"],
    "SIXTEEN": ["sechzehn"],
    "SEVENTEEN": ["siebzehn"],
    "EIGHTEEN": ["achtzehn", "option"],
    "NINETEEN": ["neunzehn"],
    "TWENTY": ["zwanzig"],
    "TWENTY_FIVE": ["fünfundzwanzig"],
    "FIFTY": ["fünfzig"]


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
   

