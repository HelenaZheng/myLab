#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
from easygui import *
import os
#egdemo()
import sys
from configobj import ConfigObj,ConfigObjError
import logging
from flowParser import flowParser
from samsungParser import samsungParser

#sys.path.append('./lib')
from lib.logConf import logConf
from lib.utils import utils

path = os.path.dirname(os.path.realpath(__file__))

#TODO:
#   packaging
#   1. add package scripts
#   ui
#   1. add silent mode
#   flowparser
#   1. add ike parsing
#   2. add service, adapter, imscm logic
#   2.1 start from imscm
#   3. error msg indication:
#   4.1 parse reason,cause
#   web page
#   1. how to display
#   2. overall results, use actdiag
#   3. possible error msg defined in config.ini



class loggergui():
    def __init__(self):
        try:
            configfile = path + '/config.ini'
            config = ConfigObj(configfile, file_error=True)
            self.config = config
            self.loglevel =  config['logging']['loglevel']
            print self.loglevel
            print logging.getLevelName(self.loglevel)
            self.logger = logConf(debuglevel=logging.getLevelName(self.loglevel))

            #one sip msg to render diagram's time
            self.estimatetime = config['utils']['estimate']

        except (ConfigObjError, IOError) as e:
             print 'Could not read "%s": %s' % (configfile, e)


    def run(self):
        # util will do the search
        # util will create result dir
        # flowParser only parse one file
        title = 'VoWifi logger parser tool'
        buttonboxmsg = 'Please open a directory which contains slog.'
        slogstring = 'Open the slog dir'
        samsungfile = "Open Samsung log file"

        choices = [slogstring, samsungfile , 'Exit']
        choice = buttonbox(buttonboxmsg, title = title, choices = choices)
        if choice != 'Exit':

            if choice == slogstring:


                folder = diropenbox()

                if not folder:
                    msgbox('please relaunch and open a directory.')
                    exit
                else:
                    helper = utils(configpath='./')
                    matches = helper.findlogs(folder)
                    for index,file in enumerate(matches):
                        #call the real parser
                        fp = flowParser(file)
                        len = fp.getFlow()
                        self.logger.logger.info('sip msgs len is ' + str(len))
                        #pop up a msg box
                        msg = 'log file is ' + file + '\n'
                        msg += 'totally sip msgs are ' + str(len) + '\n'
                        esttime = float(self.estimatetime)*int(len)
                        timelog = 'estimate time  is ' + str(esttime) + ' seconds'
                        msg = msg + timelog
                        msgbox(msg)
                        fp.parseFlow()
                        fp.drawLemonDiag()
            elif choice == samsungfile:
                file = fileopenbox()
                if not file:
                    msgbox('please relaunch and open a valid samsung log.')
                    exit
                else:
                    sp = samsungParser(logname=file)
                    sp.getflow()
        else:
            return

        #file = fileopenbox()
if __name__ == '__main__':
    gui = loggergui()
    gui.run()









