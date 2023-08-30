import os
import platform
import argparse
import websocket
import threading
import logging
import time
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger=logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(sh)



VERSION = '1.0.0'

DEFAULT_KEYWORDS_NEXT = ["next"]
DEFAULT_KEYWORDS_UNDO = ["undo", "back", "bag"]
DEFAULT_KEYWORDS_FIRST_DART = ["first", "for", "prime", "up"]
DEFAULT_KEYWORDS_SECOND_DART = ["second", "middle"]
DEFAULT_KEYWORDS_THIRD_DART = ["third", "thought", "last", "down"]
DEFAULT_KEYWORDS_SINGLE = ["single", "singer", "simple"]
DEFAULT_KEYWORDS_DOUBLE = ["double", "tablet", "number", "great", "big"]
DEFAULT_KEYWORDS_TRIPLE = ["triple", "perfect", "tribal", "couple", "templar", "tumbler"]
DEFAULT_KEYWORDS_ZERO = ["zero", "miss", "his", "myth"]
DEFAULT_KEYWORDS_ONE = ["one"]
DEFAULT_KEYWORDS_TWO = ["two", "to", "too"]
DEFAULT_KEYWORDS_THREE = ["three", "free"]
DEFAULT_KEYWORDS_FOUR = ["four", "for", "thor"]
DEFAULT_KEYWORDS_FIVE = ["five", "size"]
DEFAULT_KEYWORDS_SIX = ["six"]
DEFAULT_KEYWORDS_SEVEN = ["seven"]
DEFAULT_KEYWORDS_EIGHT = ["eight", "aid"]
DEFAULT_KEYWORDS_NINE = ["nine"]
DEFAULT_KEYWORDS_TEN = ["ten", "turn"]
DEFAULT_KEYWORDS_ELEVEN = ["eleven", "level"]
DEFAULT_KEYWORDS_TWELVE = ["twelve", "twelfth"]
DEFAULT_KEYWORDS_THIRTEEN = ["thirteen"]
DEFAULT_KEYWORDS_FOURTEEN = ["fourteen"]
DEFAULT_KEYWORDS_FIFTEEN = ["fifteen"]
DEFAULT_KEYWORDS_SIXTEEN = ["sixteen"]
DEFAULT_KEYWORDS_SEVENTEEN = ["seventeen"]
DEFAULT_KEYWORDS_EIGHTEEN = ["eighteen"]
DEFAULT_KEYWORDS_NINETEEN = ["nineteen", "ninety"]
DEFAULT_KEYWORDS_TWENTY = ["twenty"]
DEFAULT_KEYWORDS_TWENTY_FIVE = ["twenty five", "bull", "bullet", "boy"]
DEFAULT_KEYWORDS_FIFTY = ["fifty", "bullseye"]


FIELD_NAME_MAP = {}





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
        print(e)
        return (None, None)

def text2next(text):
    return text in KEYWORDS_NEXT

def text2undo(text):
    return text in KEYWORDS_UNDO

def init_keywords():
    global THROW_NUMBER_MAP

    dart_word_map = {
        1: KEYWORDS_FIRST_DART,
        2: KEYWORDS_SECOND_DART,
        3: KEYWORDS_THIRD_DART
    }

    reverse_mapping = {}
    for k, values in dart_word_map.items():
        for v in values:
            reverse_mapping[v] = k
    THROW_NUMBER_MAP = reverse_mapping
    # ppi(f'THROW_NUMBER_MAP: {THROW_NUMBER_MAP}')

    
    number_word_map = {
        tuple(KEYWORDS_ZERO): "0",
        tuple(KEYWORDS_ONE): "1",
        tuple(KEYWORDS_TWO): "2",
        tuple(KEYWORDS_THREE): "3",
        tuple(KEYWORDS_FOUR): "4",
        tuple(KEYWORDS_FIVE): "5",
        tuple(KEYWORDS_SIX): "6",
        tuple(KEYWORDS_SEVEN): "7",
        tuple(KEYWORDS_EIGHT): "8",
        tuple(KEYWORDS_NINE): "9",
        tuple(KEYWORDS_TEN): "10",
        tuple(KEYWORDS_ELEVEN): "11",
        tuple(KEYWORDS_TWELVE): "12",
        tuple(KEYWORDS_THIRTEEN): "13",
        tuple(KEYWORDS_FOURTEEN): "14",
        tuple(KEYWORDS_FIFTEEN): "15",
        tuple(KEYWORDS_SIXTEEN): "16",
        tuple(KEYWORDS_SEVENTEEN): "17",
        tuple(KEYWORDS_EIGHTEEN): "18",
        tuple(KEYWORDS_NINETEEN): "19",
        tuple(KEYWORDS_TWENTY): "20",
        tuple(KEYWORDS_TWENTY_FIVE): "25",
        tuple(KEYWORDS_FIFTY): "50",
    }

    for words, number in number_word_map.items():
        for word in words:
            if number not in ["0", "25", "50"]:
                for kd in KEYWORDS_DOUBLE:
                    FIELD_NAME_MAP[kd + " " + word] = "D" + number
                for kt in KEYWORDS_TRIPLE:
                    FIELD_NAME_MAP[kt + " " + word] = "T" + number
                for ks in KEYWORDS_SINGLE: 
                    FIELD_NAME_MAP[ks + " " + word] = "S" + number
                FIELD_NAME_MAP[word] = "S" + number
            else:
                FIELD_NAME_MAP[word] = number
    # # "zero": "0", "twenty five": "25", "fifty": "50"
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
            # vosk-model-en-us-daanzu-20200905
            model = Model(model_path=MODEL_PATH)
            rec = KaldiRecognizer(model, samplerate)
        
            with sd.RawInputStream(samplerate = samplerate, 
                                    blocksize = 8000, 
                                    device = None,
                                    dtype = "int16", 
                                    channels = 1, 
                                    callback = callback):
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        stt_result = rec.Result()
                        stt_result = json.loads(stt_result)
                        stt_result = stt_result['text']
                        if stt_result != '':
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
                                # continue
                            
                            ppi(f"Unrecognized-Command: {stt_result}")
     
                    # else:
                        # stt_result = rec.PartialResult()
                        # stt_result = json.loads(stt_result)
                        # stt_result = stt_result['transcription']
                        # ppi(f"Voice-Recognition: (Partial): {stt_result}")

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
    ap.add_argument("-KN", "--keywords_next", required=False, default=DEFAULT_KEYWORDS_NEXT, nargs='+', help="keywords for command 'next'")
    ap.add_argument("-KU", "--keywords_undo", required=False, default=DEFAULT_KEYWORDS_UNDO, nargs='+', help="keywords for command 'undo'")       
    ap.add_argument("-KFD", "--keywords_first_dart", required=False, default=DEFAULT_KEYWORDS_FIRST_DART, nargs='+', help="keywords for command 'dart-correction'")  
    ap.add_argument("-KSD", "--keywords_second_dart", required=False, default=DEFAULT_KEYWORDS_SECOND_DART, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTD", "--keywords_third_dart", required=False, default=DEFAULT_KEYWORDS_THIRD_DART, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KS", "--keywords_single", required=False, default=DEFAULT_KEYWORDS_SINGLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KD", "--keywords_double", required=False, default=DEFAULT_KEYWORDS_DOUBLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KT", "--keywords_triple", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KZERO", "--keywords_zero", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KONE", "--keywords_one", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTWO", "--keywords_two", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTHREE", "--keywords_three", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KFOUR", "--keywords_four", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KFIVE", "--keywords_five", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KSIX", "--keywords_six", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KSEVEN", "--keywords_seven", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KEIGHT", "--keywords_eight", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KNINE", "--keywords_nine", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTEN", "--keywords_ten", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KELEVEN", "--keywords_eleven", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTWELVE", "--keywords_twelve", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTHIRTEEN", "--keywords_thirteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KFOURTEEN", "--keywords_fourteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KFIFTEEN", "--keywords_fifteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KSIXTEEN", "--keywords_sixteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KSEVENTEEN", "--keywords_seventeen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KEIGHTEEN", "--keywords_eighteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KNINETEEN", "--keywords_nineteen", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTWENTY", "--keywords_twenty", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KTWENTYFIVE", "--keywords_twenty_five", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-KFIFTY", "--keywords_fifty", required=False, default=DEFAULT_KEYWORDS_TRIPLE, nargs='+', help="keywords for command 'dart-correction'")
    ap.add_argument("-DEB", "--debug", type=int, choices=range(0, 2), default=False, required=False, help="If '1', the application will output additional information")

    args = vars(ap.parse_args())

   

    global WS_DATA_FEEDER
    WS_DATA_FEEDER = None

    global THROW_NUMBER_MAP
    THROW_NUMBER_MAP = None


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

    DEBUG = args['debug']
    CON = args['connection']
    MODEL_PATH = args['model_path']
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



    try:
        connect_data_feeder()
    except Exception as e:
        ppe("Connect failed: ", e)

    try:
        start_voice_recognition()
    except Exception as e:
        ppe("Initializing voice recognition failed: ", e)


time.sleep(30)
    



   
