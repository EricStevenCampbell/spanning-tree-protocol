# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)

			    												

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):    
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.rootID = self.switchID # root ID
        self.distanceToRoot = 0 
        self.parent = None # parent ID
        self.span = {} # the data structure to keep track of which link are part of / not part of the spanning tree
        for neighbor in self.links:
            self.span[neighbor] = False # neighbor ID : linked or not

    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
	    #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            self.send_message(Message(self.switchID, 0, self.switchID, neighbor, False))
        
    def process_message(self, message):
        #TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        if message.root < self.rootID or (message.root == self.rootID and message.distance + 1 < self.distanceToRoot):
            self.rootID = message.root
            self.distanceToRoot = message.distance + 1    
            self.parent = message.origin
            for neighbor in self.links:
                if neighbor == message.origin:
                    self.span[neighbor] = True
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, neighbor, True))
                else:
                    self.span[neighbor] = False
                    self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, neighbor, False))
        
        elif message.root == self.rootID and message.distance + 1 == self.distanceToRoot and \
                    self.parent and message.origin < self.parent:
            # unlink and send msg to old parent
            self.span[self.parent] = False
            self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, self.parent, False))
            # update origin as new parent, add to spanning tree and msg the origin
            self.parent = message.origin
            self.span[message.origin] = True
            self.send_message(Message(self.rootID, self.distanceToRoot, self.switchID, message.origin, True))

        else: 
            self.span[message.origin] = message.pathThrough


    def generate_logstring(self):
        #TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        logstring = []
        for neighbor in sorted(self.span.iterkeys()):
            if self.span[neighbor] == True:
                logstring.append('{} - {}'.format(self.switchID, neighbor))
        return ', '.join(logstring)
