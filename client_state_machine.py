"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import TicTacToe
import random
import os
# hellohell0
#hey
#heyheyhey

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.result = ''   # store dice result
        self.roll_first = ''
        self.peer_result = ''

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''
    
    def game_to(self, peer):
        msg = json.dumps({"action":"game", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot game to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)
        

    
    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                        
                elif my_msg[0] == "g":
                    os.system("clear")
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.game_to(peer) == True:
                        self.state = S_GAMING_DICE
                        self.out_msg += 'Connect to ' + peer + '. Game away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        self.out_msg += '''\nWelcome to Tic-Tac-Toe!\n
                        1 | 2 | 3 
                        ----------
                        4 | 5 | 6 
                        ----------
                        7 | 8 | 9 
                        \nLet's Start!\n\n '''
                        self.out_msg += "Please enter D to roll a dice.\n"
                        self.out_msg += "Whoever gets a larger number goes first!\n"
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                    
                if peer_msg["action"] == "game":
                    os.system("clear")
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Game away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.out_msg += '''\nWelcome to Tic-Tac-Toe!\n
                        1 | 2 | 3 
                        ----------
                        4 | 5 | 6 
                        ----------
                        7 | 8 | 9 
                        \nLet's Start!\n\n '''
                    self.state = S_GAMING_DICE
                    self.out_msg += "Please enter D to roll a dice.\n"
                    self.out_msg += "Whoever gets a larger number goes first!\n"
                    
                    

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                
            if len(peer_msg) > 0:    # peer's stuff, coming in
                #peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]


            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
                
                
#==============================================================================
# Start GAMING, 'q' for quit
# This is event handling instate "S_GAMING"
#==============================================================================
        elif self.state == S_GAMING_DICE:
            #self.out_msg += TicTacToe.print_header()
            
            
            if len(my_msg) > 0:
                if my_msg == "q":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ""
#                else:
#                    TicTacToe.Board.update_cell(my_msg, "X")
                if my_msg == "d" or "D":
                    self.result = str(random.randint(1,6))
                    self.out_msg += "You get " + self.result + "\n"
                    mysend(self.s, json.dumps({"action":"dice","from": self.me, "result":self.result}))
                    if self.roll_first == False:
                        if self.peer_result > self.result:
                            self.out_msg += self.peer + " goes first!\n"
                            self.state = S_GAMING_TTT
                        elif self.result == self.peer_result:
                            self.out_msg += "opps, same results. Throw again!\n"
                            self.result = ''
                            self.peer_result = ''
                            self.roll_first = ''
                        else:
                            self.out_msg += "You go first!\n"
                            self.state = S_GAMING_TTT
                           
                        
                    
                    
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                #print(peer_msg)
                if peer_msg["action"] == "game":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "dice":
                    self.peer_result = peer_msg["result"]
                    self.out_msg += peer_msg["from"] + " got " + self.peer_result + "\n"
                    if self.result == "":
                        self.roll_first = False
                        self.out_msg += "Waiting for you to roll...\n"
                    else:
                        self.roll_first = True
                        if self.result < self.peer_result:
                            self.out_msg += peer_msg["from"] + " goes first!\n"
                            self.state = S_GAMING_TTT
                        elif self.result == self.peer_result:
                            self.out_msg += "opps, same results. Throw again!\n"
                            self.result = ''
                            self.peer_result = ''
                            self.roll_first = ''
                        else:
                            self.out_msg += "You go first!\n"
                            self.state = S_GAMING_TTT
                        
                
            if self.state == S_LOGGEDIN:
                self.out_msg += menu    
                
                
        elif self.state == S_GAMING_TTT:
            pass
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg


        
        
        
        
        
        
        
        
        
        
