# Control No Man's Sky with the Launchpad X Grid Music Controller
# Leif Bloomquist - Schema Factor

import mido
import keyboard
import lpx_colors as lpx

# mido sends 0xF0 (start) and 0xF7 (end) automatically
MSG_HEADER = [0x00, 0x20, 0x29, 0x02,0x0C]
INIT_MSG   = [0x0E, 0x01]
DEINIT_MSG = [0x0E, 0x00]


# MIDI Codes
NOVATION_LOGO=0x63

INTERACT=11
SCAN=12

ANALYSIS=15
ANALYSIS_PREV=14
ANALYSIS_NEXT=16

JUMP=18

LAND=31
LAUNCH=32
THRUST=34
BOOST=35
PULSE=36
WEAPON=38

DISCOVERIES=71
INVENTORIES=72

TORCH=74
QUICK_MENU=75

FORWARD=91
BACKWARD=92
PREVIOUS_PAGE=93
NEXT_PAGE=94


# Key mappings
keydict = {
  INTERACT: "e",
  SCAN: "c",
  
  ANALYSIS_PREV: "1",
  ANALYSIS: "f",
  ANALYSIS_NEXT: "3",
  
  JUMP: " ",  
  
  DISCOVERIES: "Esc",
  INVENTORIES: "Tab",
  
  TORCH: "t",
  QUICK_MENU: "x",
  
  FORWARD: "w",
  BACKWARD: "s",
  PREVIOUS_PAGE: "a",  
  NEXT_PAGE: "d", 
  
  LAND: "e",
  LAUNCH: "w",  
  THRUST: "w",
  BOOST: "left shift",
  PULSE: " ",  
  WEAPON: "g",
}

# Color mappings
colordict = {
  INTERACT: lpx.COLOR_RED,
  SCAN: lpx.COLOR_CYAN,  
  ANALYSIS_PREV: lpx.COLOR_DARKBLUE,
  ANALYSIS: lpx.COLOR_BLUE,
  ANALYSIS_NEXT: lpx.COLOR_DARKBLUE,    
  JUMP: lpx.COLOR_YELLOW,
  
  DISCOVERIES: lpx.COLOR_PURPLE,
  INVENTORIES: lpx.COLOR_AQUA,  
  TORCH: lpx.COLOR_GREY1,
  QUICK_MENU: lpx.COLOR_LIGHTBLUE,
    
  LAND: lpx.COLOR_RED,
  LAUNCH: lpx.COLOR_GREEN,
  THRUST: lpx.COLOR_GREEN3,
  BOOST: lpx.COLOR_GREEN2,
  PULSE: lpx.COLOR_YELLOWGREEN,
  WEAPON: lpx.COLOR_REDORANGE,
  
  FORWARD: lpx.COLOR_GREY1,
  BACKWARD: lpx.COLOR_GREY1,
  PREVIOUS_PAGE: lpx.COLOR_WHITE,
  NEXT_PAGE: lpx.COLOR_WHITE,  
}


def connect_midi(in_port_name, out_port_name):
    return mido.open_input(in_port_name),mido.open_output(out_port_name)
    

def send_midi_cc(port, num, val):
    msg = mido.Message('control_change', control=int(num), value=int(val))
    port.send(msg)
    
    
def paint_cell(cell_id, color):
    msg = mido.Message('note_on', note=int(cell_id), velocity=int(color))
    outport.send(msg)


def init_colors():    
    for cell in range(11,100):
        paint_cell(cell, lpx.COLOR_BLACK)
    for cell in colordict:
        paint_cell(cell, colordict[cell])
    
    # Pulsing animation on logo
    msg = mido.Message('note_on', channel=2, note=NOVATION_LOGO, velocity=lpx.COLOR_RED)    
    outport.send(msg)


def handle_press(code):    
    if code in keydict:
        key = keydict[code]        
        keyboard.press(key)
        paint_cell(code, lpx.COLOR_WHITE)
 
 
def handle_release(code):
     if code in keydict:
        key = keydict[code]       
        keyboard.release(key)
        paint_cell(code, colordict[code])
    

if __name__ == '__main__':
    print("LaunchPad X Control for No Man's Sky\n")

    print('MIDI Output Ports Available:', mido.get_output_names())
    print('MIDI Input  Ports Available:', mido.get_input_names())

    print('Initializing MIDI')
    inport, outport = connect_midi('MIDIIN2 (LPX MIDI) 4', 'MIDIOUT2 (LPX MIDI) 5')
    
    print('Initializing Launchpad X')
    msg = mido.Message('sysex', data=MSG_HEADER+INIT_MSG)
    outport.send(msg)
    
    print('Initializing Colors')
    init_colors()

    print('Starting Control Loop')
    while True:
        msg = inport.receive()
        
        if msg.type=='polytouch':
            continue
        
        print(msg)
        
        # Main 
        if msg.type=='note_on':
            if msg.velocity > 0:        # Pressed
                handle_press(msg.note)
            elif msg.velocity == 0:     # Released
                handle_release(msg.note)
                
        # Arrows
        elif msg.is_cc():
            if msg.value > 0:        # Pressed
                handle_press(msg.control)
            elif msg.value == 0:     # Released
                handle_release(msg.control)



