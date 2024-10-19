# 1. Natural language
Please write a very simple python script for Opentrons that moves 20 uL of liquid from well 1A of a corning 96 well plate in deck slot 1 to well 1A of a corning 96 well plate in deck slot 2 using a 300 uL pipette tip mounted on the right side. 300 uL tips are in deck slot 3. 

# 2. Expected final deck state
DeckState:
    pipettes: 
        right: p300_single_gen2
    labware:
        slot1: corning_96_wellplate_360ul_flat
        slot2: corning_96_wellplate_360ul_flat
            1A: +20 uL
        slot3: opentrons_96_tiprack_300ul
    

