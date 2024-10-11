from opentrons import protocol_api

metadata = {
    'protocolName': 'Simple Transfer',
    'author': 'Assistant',
    'description': 'Transfer 20 uL from well A1 of plate in slot 1 to well A1 of plate in slot 2',
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    source_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    destination_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 3)
    
    # Load pipette
    pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
    
    # Perform transfer
    pipette.pick_up_tip()
    pipette.transfer(100, source_plate['A1'], destination_plate['A1'], new_tip='never')
    pipette.drop_tip()