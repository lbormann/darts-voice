# coding: utf-8

import os
from pathlib import Path
import platform
import argparse
import websocket
import threading
import logging
import time
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import json

SetLogLevel(0)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)

main_directory = os.path.dirname(os.path.realpath(__file__))






VERSION = '1.0.1'




LANGUAGE_KEYWORDS = {

    # english
    1: {
        "LANGUAGE": "english",

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
    },

    # german
    2: {
        "LANGUAGE": "german",

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
    },
}




def ppi(message, info_object = None, prefix = '\r\n'):
    logger.info(prefix + str(message))
    if info_object != None:
        logger.info(str(info_object))
    
def ppe(message, error_object):
    ppi(message)
    if DEBUG:
        logger.exception("\r\n" + str(error_object))

    

def text2dart_score(text):
    try:
        throw_number = None
        field_name = None

        words = text.split(" ")
        # Überprüfung und Zuordnung der throw-number
        if words[0] in THROW_NUMBER_MAP:
            throw_number = THROW_NUMBER_MAP[words[0]]
        
        # Überprüfung und Zuordnung der field-name
        # Beginnen bei der gesamten Wortliste und sukzessive das erste Wort entfernen
        for i in range(len(words)):
            possible_field = " ".join(words[i:])
            if possible_field in FIELD_NAME_MAP:
                field_name = FIELD_NAME_MAP[possible_field]
                break

        return (throw_number, field_name)

    except Exception as e:
        ppe("Text2dart failed: ", e)
        return (None, None)

def text2nextgame(text):
    return text in NEXT_GAME_MAP

def text2next(text):
    return text in NEXT_MAP

def text2undo(text):
    return text in UNDO_MAP

def init_keywords():
    global NEXT_MAP
    global NEXT_GAME_MAP
    global UNDO_MAP
    global THROW_NUMBER_MAP
    global FIELD_NAME_MAP


    if LANGUAGE != 0:
        pre_def = LANGUAGE_KEYWORDS[LANGUAGE]

        NEXT_MAP = list(set(pre_def["NEXT"] + [s.lower() for s in KEYWORDS_NEXT]))
        NEXT_GAME_MAP = list(set(pre_def["NEXT_GAME"] + [s.lower() for s in KEYWORDS_NEXT_GAME]))
        UNDO_MAP = list(set(pre_def["UNDO"] + [s.lower() for s in KEYWORDS_UNDO]))

        dart_word_map = {
            1: list(set(pre_def["FIRST_DART"] + [s.lower() for s in KEYWORDS_FIRST_DART])),
            2: list(set(pre_def["SECOND_DART"] + [s.lower() for s in KEYWORDS_SECOND_DART])),
            3: list(set(pre_def["THIRD_DART"] + [s.lower() for s in KEYWORDS_THIRD_DART]))
        }

        area_single_word_map = list(set(pre_def["SINGLE"] + [s.lower() for s in KEYWORDS_SINGLE]))
        area_double_word_map = list(set(pre_def["DOUBLE"] + [s.lower() for s in KEYWORDS_DOUBLE]))
        area_triple_word_map = list(set(pre_def["TRIPLE"] + [s.lower() for s in KEYWORDS_TRIPLE]))

        number_word_map = {
            tuple(set(pre_def["ZERO"] + [s.lower() for s in KEYWORDS_ZERO])): "0",
            tuple(set(pre_def["ONE"] + [s.lower() for s in KEYWORDS_ONE])): "1",
            tuple(set(pre_def["TWO"] + [s.lower() for s in KEYWORDS_TWO])): "2",
            tuple(set(pre_def["THREE"] + [s.lower() for s in KEYWORDS_THREE])): "3",
            tuple(set(pre_def["FOUR"] + [s.lower() for s in KEYWORDS_FOUR])): "4",
            tuple(set(pre_def["FIVE"] + [s.lower() for s in KEYWORDS_FIVE])): "5",
            tuple(set(pre_def["SIX"] + [s.lower() for s in KEYWORDS_SIX])): "6",
            tuple(set(pre_def["SEVEN"] + [s.lower() for s in KEYWORDS_SEVEN])): "7",
            tuple(set(pre_def["EIGHT"] + [s.lower() for s in KEYWORDS_EIGHT])): "8",
            tuple(set(pre_def["NINE"] + [s.lower() for s in KEYWORDS_NINE])): "9",
            tuple(set(pre_def["TEN"] + [s.lower() for s in KEYWORDS_TEN])): "10",
            tuple(set(pre_def["ELEVEN"] + [s.lower() for s in KEYWORDS_ELEVEN])): "11",
            tuple(set(pre_def["TWELVE"] + [s.lower() for s in KEYWORDS_TWELVE])): "12",
            tuple(set(pre_def["THIRTEEN"] + [s.lower() for s in KEYWORDS_THIRTEEN])): "13",
            tuple(set(pre_def["FOURTEEN"] + [s.lower() for s in KEYWORDS_FOURTEEN])): "14",
            tuple(set(pre_def["FIFTEEN"] + [s.lower() for s in KEYWORDS_FIFTEEN])): "15",
            tuple(set(pre_def["SIXTEEN"] + [s.lower() for s in KEYWORDS_SIXTEEN])): "16",
            tuple(set(pre_def["SEVENTEEN"] + [s.lower() for s in KEYWORDS_SEVENTEEN])): "17",
            tuple(set(pre_def["EIGHTEEN"] + [s.lower() for s in KEYWORDS_EIGHTEEN])): "18",
            tuple(set(pre_def["NINETEEN"] + [s.lower() for s in KEYWORDS_NINETEEN])): "19",
            tuple(set(pre_def["TWENTY"] + [s.lower() for s in KEYWORDS_TWENTY])): "20",
            tuple(set(pre_def["TWENTY_FIVE"] + [s.lower() for s in KEYWORDS_TWENTY_FIVE])): "25",
            tuple(set(pre_def["FIFTY"] + [s.lower() for s in KEYWORDS_FIFTY])): "50",
        }
      
    else:

        NEXT_MAP = list(set([s.lower() for s in KEYWORDS_NEXT]))
        NEXT_GAME_MAP = list(set([s.lower() for s in KEYWORDS_NEXT_GAME]))
        UNDO_MAP = list(set([s.lower() for s in KEYWORDS_UNDO]))

        dart_word_map = {
            1: list(set([s.lower() for s in KEYWORDS_FIRST_DART])),
            2: list(set([s.lower() for s in KEYWORDS_SECOND_DART])),
            3: list(set([s.lower() for s in KEYWORDS_THIRD_DART]))
        }

        area_single_word_map = list(set([s.lower() for s in KEYWORDS_SINGLE]))
        area_double_word_map = list(set([s.lower() for s in KEYWORDS_DOUBLE]))
        area_triple_word_map = list(set([s.lower() for s in KEYWORDS_TRIPLE]))

        number_word_map = {
            tuple(set([s.lower() for s in KEYWORDS_ZERO])): "0",
            tuple(set([s.lower() for s in KEYWORDS_ONE])): "1",
            tuple(set([s.lower() for s in KEYWORDS_TWO])): "2",
            tuple(set([s.lower() for s in KEYWORDS_THREE])): "3",
            tuple(set([s.lower() for s in KEYWORDS_FOUR])): "4",
            tuple(set([s.lower() for s in KEYWORDS_FIVE])): "5",
            tuple(set([s.lower() for s in KEYWORDS_SIX])): "6",
            tuple(set([s.lower() for s in KEYWORDS_SEVEN])): "7",
            tuple(set([s.lower() for s in KEYWORDS_EIGHT])): "8",
            tuple(set([s.lower() for s in KEYWORDS_NINE])): "9",
            tuple(set([s.lower() for s in KEYWORDS_TEN])): "10",
            tuple(set([s.lower() for s in KEYWORDS_ELEVEN])): "11",
            tuple(set([s.lower() for s in KEYWORDS_TWELVE])): "12",
            tuple(set([s.lower() for s in KEYWORDS_THIRTEEN])): "13",
            tuple(set([s.lower() for s in KEYWORDS_FOURTEEN])): "14",
            tuple(set([s.lower() for s in KEYWORDS_FIFTEEN])): "15",
            tuple(set([s.lower() for s in KEYWORDS_SIXTEEN])): "16",
            tuple(set([s.lower() for s in KEYWORDS_SEVENTEEN])): "17",
            tuple(set([s.lower() for s in KEYWORDS_EIGHTEEN])): "18",
            tuple(set([s.lower() for s in KEYWORDS_NINETEEN])): "19",
            tuple(set([s.lower() for s in KEYWORDS_TWENTY])): "20",
            tuple(set([s.lower() for s in KEYWORDS_TWENTY_FIVE])): "25",
            tuple(set([s.lower() for s in KEYWORDS_FIFTY])): "50",
        }


    for k, values in dart_word_map.items():
        for v in values:
            THROW_NUMBER_MAP[v] = k
    # ppi(f'THROW_NUMBER_MAP: {THROW_NUMBER_MAP}')
 
    for words, number in number_word_map.items():
        for word in words:
            if number not in ["0", "25", "50"]:
                for kd in area_double_word_map:
                    FIELD_NAME_MAP[kd + " " + word] = "D" + number
                for kt in area_triple_word_map:
                    FIELD_NAME_MAP[kt + " " + word] = "T" + number
                for ks in area_single_word_map: 
                    FIELD_NAME_MAP[ks + " " + word] = "S" + number
                FIELD_NAME_MAP[word] = "S" + number
            else:
                FIELD_NAME_MAP[word] = number
    # ppi(f'FIELD_NAME_MAP: {FIELD_NAME_MAP}')

def start_voice_recognition():
    def process(*args):
        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))

        samplerate = None
        try:
            device_info = sd.query_devices(None, "input")
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info["default_samplerate"])
        except Exception as e:
            ppe("Microphone initialization failed: ", e)
            return

        try:
            init_keywords()
        except Exception as e:
            ppe("Keyword initialization failed: ", e)
            return


        try:
            q = queue.Queue()
            global WS_DATA_FEEDER

            # lang="en-us"
            # model_name="vosk-model-en-us-daanzu-20200905"
            model = Model(model_path=str(MODEL_PATH))
            rec = KaldiRecognizer(model, samplerate)
        
            with sd.RawInputStream(samplerate = samplerate, 
                                    blocksize = 8000, 
                                    device = None,
                                    dtype = "int16", 
                                    channels = 1, 
                                    callback = callback):
                while True:
                    try:
                        data = q.get()
                        if rec.AcceptWaveform(data):
                            stt_result = rec.Result()
                            stt_result = json.loads(stt_result)
                            stt_result = stt_result['text']
                            if stt_result != '':
                                stt_result = stt_result.lower()

                                if text2nextgame(stt_result):
                                    ppi(f"Command 'NEXT-GAME'")
                                    if WS_DATA_FEEDER is not None:
                                        WS_DATA_FEEDER.send('next-game')
                                    continue

                                if text2next(stt_result):
                                    ppi(f"Command 'NEXT'")
                                    if WS_DATA_FEEDER is not None:
                                        WS_DATA_FEEDER.send('next')
                                    continue

                                if text2undo(stt_result):
                                    ppi(f"Command 'UNDO'")
                                    if WS_DATA_FEEDER is not None:
                                        WS_DATA_FEEDER.send('undo')
                                    continue
                                
                                (dart_number, dart_field) = text2dart_score(stt_result)
                                # ppi(f"Command 't2d-debug': Dart {dart_number} = {dart_field}")
                                if dart_number != None and dart_field != None:
                                    ppi(f"Command 'CORRECT': Dart {dart_number} = {dart_field}")
                                    if WS_DATA_FEEDER is not None:
                                        WS_DATA_FEEDER.send(f'correct:{(dart_number - 1)}:{dart_field}')
                                    continue
                                
                                ppi(f"Unrecognized-Command: {stt_result}")
        
                        # else:
                            # stt_result = rec.PartialResult()
                            # stt_result = json.loads(stt_result)
                            # stt_result = stt_result['transcription']
                            # ppi(f"Voice-Recognition: (Partial): {stt_result}")
                            
                    except Exception as e:
                        ppe("Recognition-step failed: ", e)


        except Exception as e:
            ppe("KaldiRecognizer initialization failed: ", e)

    threading.Thread(target=process).start()



def connect_data_feeder():
    def process(*args):
        global WS_DATA_FEEDER
        websocket.enableTrace(False)
        data_feeder_host = CON
        if CON.startswith('ws://') == False:
            data_feeder_host = 'ws://' + CON
        WS_DATA_FEEDER = websocket.WebSocketApp(data_feeder_host,
                                on_open = on_open_data_feeder,
                                on_error = on_error_data_feeder,
                                on_close = on_close_data_feeder)

        WS_DATA_FEEDER.run_forever()
    threading.Thread(target=process).start()

def on_open_data_feeder(ws):
    ppi('CONNECTED TO DATA-FEEDER ' + str(ws.url))
    
def on_close_data_feeder(ws, close_status_code, close_msg):
    try:
        ppi("Websocket [" + str(ws.url) + "] closed! " + str(close_msg) + " - " + str(close_status_code))
        ppi("Retry : %s" % time.ctime())
        time.sleep(3)
        connect_data_feeder()
    except Exception as e:
        ppe('WS-Close failed: ', e)
    
def on_error_data_feeder(ws, error):
    ppe('WS-Error ' + str(ws.url) + ' failed: ', error)

    



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-CON", "--connection", default="127.0.0.1:8079", required=False, help="Connection to data feeder")
    ap.add_argument("-MP", "--model_path", required=True, help="Absolute path to your model folder")
    ap.add_argument("-L", "--language", required=False, default=1, type=int, choices=range(0, len(LANGUAGE_KEYWORDS) + 1), help="Predefined language keywords")
    ap.add_argument("-KNG", "--keywords_next_game", required=False, default=[], nargs='+', help="Keywords for command 'next-game'")
    ap.add_argument("-KN", "--keywords_next", required=False, default=[], nargs='+', help="Keywords for command 'next'")
    ap.add_argument("-KU", "--keywords_undo", required=False, default=[], nargs='+', help="Keywords for command 'undo'")       
    ap.add_argument("-KFD", "--keywords_first_dart", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")  
    ap.add_argument("-KSD", "--keywords_second_dart", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTD", "--keywords_third_dart", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KS", "--keywords_single", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KD", "--keywords_double", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KT", "--keywords_triple", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KZERO", "--keywords_zero", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KONE", "--keywords_one", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTWO", "--keywords_two", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTHREE", "--keywords_three", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KFOUR", "--keywords_four", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KFIVE", "--keywords_five", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KSIX", "--keywords_six", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KSEVEN", "--keywords_seven", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KEIGHT", "--keywords_eight", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KNINE", "--keywords_nine", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTEN", "--keywords_ten", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KELEVEN", "--keywords_eleven", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTWELVE", "--keywords_twelve", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTHIRTEEN", "--keywords_thirteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KFOURTEEN", "--keywords_fourteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KFIFTEEN", "--keywords_fifteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KSIXTEEN", "--keywords_sixteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KSEVENTEEN", "--keywords_seventeen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KEIGHTEEN", "--keywords_eighteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KNINETEEN", "--keywords_nineteen", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTWENTY", "--keywords_twenty", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KTWENTYFIVE", "--keywords_twenty_five", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-KFIFTY", "--keywords_fifty", required=False, default=[], nargs='+', help="Keywords for command 'dart-correction'")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=False, required=False, help="If '1', the application will output additional information")

    args = vars(ap.parse_args())


    DEBUG = args['debug']
    CON = args['connection']
    MODEL_PATH = Path(args['model_path'])
    LANGUAGE = args['language']
    KEYWORDS_NEXT_GAME = args['keywords_next_game']
    KEYWORDS_NEXT = args['keywords_next']
    KEYWORDS_UNDO = args['keywords_undo']
    KEYWORDS_FIRST_DART = args['keywords_first_dart']
    KEYWORDS_SECOND_DART = args['keywords_second_dart']
    KEYWORDS_THIRD_DART = args['keywords_third_dart']
    KEYWORDS_SINGLE = args['keywords_single']
    KEYWORDS_DOUBLE = args['keywords_double']
    KEYWORDS_TRIPLE = args['keywords_triple']
    KEYWORDS_ZERO = args["keywords_zero"]
    KEYWORDS_ONE = args["keywords_one"]
    KEYWORDS_TWO = args["keywords_two"]
    KEYWORDS_THREE = args["keywords_three"]
    KEYWORDS_FOUR = args["keywords_four"]
    KEYWORDS_FIVE = args["keywords_five"]
    KEYWORDS_SIX = args["keywords_six"]
    KEYWORDS_SEVEN = args["keywords_seven"]
    KEYWORDS_EIGHT = args["keywords_eight"]
    KEYWORDS_NINE = args["keywords_nine"]
    KEYWORDS_TEN = args["keywords_ten"]
    KEYWORDS_ELEVEN = args["keywords_eleven"]
    KEYWORDS_TWELVE = args["keywords_twelve"]
    KEYWORDS_THIRTEEN = args["keywords_thirteen"]
    KEYWORDS_FOURTEEN = args["keywords_fourteen"]
    KEYWORDS_FIFTEEN = args["keywords_fifteen"]
    KEYWORDS_SIXTEEN = args["keywords_sixteen"]
    KEYWORDS_SEVENTEEN = args["keywords_seventeen"]
    KEYWORDS_EIGHTEEN = args["keywords_eighteen"]
    KEYWORDS_NINETEEN = args["keywords_nineteen"]
    KEYWORDS_TWENTY = args["keywords_twenty"]
    KEYWORDS_TWENTY_FIVE = args["keywords_twenty_five"]
    KEYWORDS_FIFTY = args["keywords_fifty"]


    if DEBUG:
        ppi('Started with following arguments:')
        ppi(json.dumps(args, indent=4))
    
    args_post_check = None
    try:
        if os.path.commonpath([MODEL_PATH, main_directory]) == main_directory:
            args_post_check = 'MODEL_PATH resides inside MAIN-DIRECTORY! It is not allowed!'
    except:
        pass



    global WS_DATA_FEEDER
    WS_DATA_FEEDER = None

    global NEXT_MAP
    NEXT_MAP = []

    global NEXT_GAME_MAP
    NEXT_GAME_MAP = []

    global UNDO_MAP
    UNDO_MAP = []

    global THROW_NUMBER_MAP
    THROW_NUMBER_MAP = {}

    global FIELD_NAME_MAP
    FIELD_NAME_MAP = {}






    osType = platform.system()
    osName = os.name
    osRelease = platform.release()
    ppi('\r\n', None, '')
    ppi('##########################################', None, '')
    ppi('       WELCOME TO AUTODARTS-VOICE', None, '')
    ppi('##########################################', None, '')
    ppi('VERSION: ' + VERSION, None, '')
    ppi('RUNNING OS: ' + osType + ' | ' + osName + ' | ' + osRelease, None, '')
    ppi('\r\n', None, '')


    if args_post_check is not None: 
        ppi('Please check your arguments: ' + args_post_check)
    else:

        try:
            connect_data_feeder()
        except Exception as e:
            ppe("Connect failed: ", e)

        try:
            start_voice_recognition()
        except Exception as e:
            ppe("Initializing voice recognition failed: ", e)


time.sleep(30)
    



   
