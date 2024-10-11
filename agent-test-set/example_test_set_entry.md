# 1. Natural language
Please write a very simple python script for Opentrons that moves 20 uL of liquid from well 1A of a corning 96 well plate in deck slot 1 to well 1A of a corning 96 well plate in deck slot 2 using a 300 uL pipette tip mounted on the right side. 300 uL tips are in deck slot 3. 

# 2. Expected final deck state
DeckState:
  pipettes:
    right:
      type: p300_single_gen2
      current_volume: 0
    left: null  

  labware:
    slot1:
      type: corning_96_wellplate_360ul_flat
      wells:
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row A
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row B
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row C
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row D
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row E
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row F
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row G
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row H

    slot2:
      type: corning_96_wellplate_360ul_flat
      wells:
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row A
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row B
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row C
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row D
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row E
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row F
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row G
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row H

    slot3:
      type: opentrons_96_tiprack_300ul
      tips:
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row A
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row B
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row C
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row D
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row E
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row F
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row G
        - [null, null, null, null, null, null, null, null, null, null, null, null]  # Row H

    slot4: null
    slot5: null
    slot6: null
    slot7: null
    slot8: null
    slot9: null
    slot10: null
    slot11: null
    slot12: null
