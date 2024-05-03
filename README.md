# DARTS-VOICE
[![Downloads](https://img.shields.io/github/downloads/lbormann/darts-voice/total.svg)](https://github.com/lbormann/darts-voice/releases/latest)

Darts-voice transcribes your voice in realtime (offline) to control an https://autodarts.io game. A running instance of https://github.com/lbormann/darts-caller is needed for processing commands.
Darts-voice uses vosk. check it out: https://alphacephei.com/vosk

On Linux you need to install PortAudio:

    sudo apt-get install portaudio19-dev



## INSTALL INSTRUCTION


### Desktop-OS:

- If you're running a desktop-driven OS it's recommended to use [darts-hub](https://github.com/lbormann/darts-hub) as it takes care of starting, updating, configurating and managing multiple apps.


### Headless-OS:

- Download the appropriate executable in the release section.


### By Source:

#### Setup python3

- Download and install python 3.x.x for your specific os.
- Download and install pip.


#### Get the project

    git clone https://github.com/lbormann/darts-voice.git

Go to download-directory and type:

    pip3 install -r requirements.txt

On MacOS:

    pip3 install -r requirements_mac.txt





## RUN IT

### Prerequisite

* You need to have a running caller - https://github.com/lbormann/darts-caller - (latest version)
* Download and extract a model from here: https://alphacephei.com/vosk/models (recommendable small ones, eg.: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
* Make sure your machine is strong enough to handle complexity of model (large models claim high memory usage and are slow).
* Make sure your microphone is configured as default in os.

### Run by executable

#### Example: Windows 

Create a shortcut of the executable; right click on the shortcut -> select properties -> add arguments in the target input at the end of the text field.

Example: C:\Downloads\darts-voice.exe -MP "C:\\vosk-models\\vosk-model-small-en-us-0.15"

Save changes.
Click on the shortcut to start the application.


### Run by source

#### Example: Linux

    python3 darts-voice.py -MP "C:\\vosk-models\\vosk-model-small-en-us-0.15"


### Usage

* Speak loud and clear to the microphone. 
* Verify recognized words in terminal.
* Adjust keywords for wrong recognized words.


Here are some examples that could work out of the box with model [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip):

#### Dart-correction

- first twenty
- second and last is miss
- first second third is twenty
- first is twenty
- second triple twelve
- second is perfect nineteen
- third one
- last is double ten
- second is big ten
- second is two
- last is number three
- second is twenty five
- first is fifty
- last is miss


#### Go next game

- next game

#### Go next

- next

#### Go back

- back
- undo

#### Ban current caller

- ban caller

#### Change current caller

- change caller

#### Control board

- start board
- stop board
- reset board
- calibrate board


 
### Arguments

- -MP / --model_path [REQUIRED] [Default: '']
- -L / --language [OPTIONAL] [Default: 1] [Possible values: 0 (no keyword-predefinitions) | 1 (english) | 2 (german)]
- -KNG / --keywords_next_game [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KN / --keywords_next [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KU / --keywords_undo [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KBC / --keywords_ban_caller [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KCC / --keywords_change_caller [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSB / --keywords_start_board [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KSPB / --keywords_stop_board [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KRB / --keywords_reset_board [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
- -KCB / --keywords_calibrate_board [OPTIONAL] [MULTIPLE ENTRIES POSSIBLE] [Default: []]
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

Host address to data-feeder (darts-caller). By Default this is '127.0.0.1:8079' (means your local ip-address)

*`-MP / --model_path`*

You need to set an absolute path to your model directory. Moreover make sure the given path doesn't reside inside main-directory (darts-voice).

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
    "BAN_CALLER": ["ban caller"],
    "CHANGE_CALLER": ["change caller"],
    "START_BOARD": ["start board"],
    "STOP_BOARD": ["stop board"],
    "RESET_BOARD": ["reset board"],
    "CALIBRATE_BOARD": ["calibrate board"],

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
    "BAN_CALLER": ["sprecher ausschließen"],
    "CHANGE_CALLER": ["sprecher wechseln"],
    "START_BOARD": ["starten"],
    "STOP_BOARD": ["stoppen"],
    "RESET_BOARD": ["zurücksetzen"],
    "CALIBRATE_BOARD": ["kalibrieren"],

    "FIRST_DART": ["erster", "erste", "erstens", "erst"],
    "SECOND_DART": ["zweiter", "zweite", "zweitens"],
    "THIRD_DART": ["dritter", "dritte", "drittens", "britta", "letzter"],

    "SINGLE": ["einfach", "normal", "normale"],
    "DOUBLE": ["doppel", "doppelt", "groß", "große"],
    "TRIPLE": ["dreifach", "perfekt", "perfekte"],
    
    "ZERO": ["null", "vorbei", "verhauen", "frauen"],
    "ONE": ["eins"],
    "TWO": ["zwei", "frei", "zwar"],
    "THREE": ["drei"],
    "FOUR": ["vier"],
    "FIVE": ["fünf"],
    "SIX": ["sechs"],
    "SEVEN": ["sieben"],
    "EIGHT": ["acht"],
    "NINE": ["neun", "neuen"],
    "TEN": ["zehn", "sehen"],
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

This application requires a running instance of darts-caller https://github.com/lbormann/darts-caller


## Resources

Icon by <a href="https://icon-icons.com/icon/microphone-musical-instrument/60191"></a> on <a href="https://icon-icons.com">icon-icons.com</a>
License <a href="https://creativecommons.org/licenses/by/4.0/">Attribution 4.0 International (CC BY 4.0)</a>                         
   

