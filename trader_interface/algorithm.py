import numpy as np

## Constants

# UQ
UQ = "UQ Dollar"
UQ_WAIT = 20
UQ_AVG = 100
UQ_SAFETY_MARGIN = 0.002

# Fintech Token
FT = "Fintech Token"

# Thriften Jeans
TJ = "Thrifted Jeans"

# Boat Party Ticket
BPT = "Boat Party Ticket"

# Sausage Sizzle
SS = "Sausage Sizzle"
SIZZLE_SAFETY_MARGIN = 0.002 # 1% Increase

# Bread
B = "Bread"

# Sausage
S = "Sausage"

# MenuDash
MD = "MenuDash"

# Liferaft Ticket
LT = "Liferaft Ticket"

# Custom trading Algorithm
class Algorithm():

    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        self.data = {}              # Historical data of all instruments
        self.positionLimits = {}    # Initialise position limits
        self.day = 0                # Initialise the current day as 0
        self.positions = positions  # Initialise the current positions
        
    def get_current_price(self, instrument):
        """
        Helper function to fetch current price of an instrument.
        """
        return self.data[instrument][-1]
    
    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits
        
        # Declare a store for desired positions
        desiredPositions = {}
        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initilise desired position to zero
            desiredPositions[instrument] = 0

        #######################################################################
        # Display the current trading day
        print("Starting Algorithm for Day:", self.day)
                
        # Display the prices of instruments to be traded
        trade_instruments = [UQ, FT, TJ, BPT, SS, B, S, MD, LT]
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")

        #######################################################################
        # UQ Dollar
        if self.day > UQ_WAIT:
            if self.data[UQ][-1]/UQ_AVG > 1 + UQ_SAFETY_MARGIN:
                desiredPositions[UQ] = -positionLimits[UQ]
            elif self.data[UQ][-1]/UQ_AVG < 1 - UQ_SAFETY_MARGIN:
                desiredPositions[UQ] = positionLimits[UQ]

        # Fintech Token

        # Thrifted Jeans
        if self.day >= 2:
            for ins in trade_instruments:
                # if price has gone down, buy
                todays_price = self.data[TJ][-1]
                yesterdays_price = self.data[TJ][-2]
                if yesterdays_price > todays_price:
                    desiredPositions[TJ] = positionLimits[TJ]
                else: # else, short
                    desiredPositions[TJ] = -positionLimits[TJ]

        # Boat Party Ticket
        if self.day % 365 <= 30:
            desiredPositions[BPT] = positionLimits[BPT]
        elif 30 < self.day % 365 <= 130:
            desiredPositions[BPT] = -positionLimits[BPT]
        elif 130 < self.day % 365 <= 190:
            desiredPositions[BPT] = positionLimits[BPT]
        elif 190 < self.day % 365 <= 300:
            desiredPositions[BPT] = -positionLimits[BPT]
        elif 300 < self.day % 365:
            desiredPositions[BPT] = positionLimits[BPT]

        # Sausage Sizzle
        if self.day >= 2:
            bread_change = self.data[B][-1] / self.data[B][-2]
            sausage_change = self.data[S][-1] / self.data[S][-2]
            menu_dash_change = self.data[MD][-1] / self.data[MD][-2]

            avg_change = (bread_change + sausage_change + menu_dash_change) / 3
            
            sausage_sizzle_change = self.data[SS][-1] / self.data[SS][-2]
            if sausage_sizzle_change > avg_change:
                desiredPositions[SS] = -positionLimits[SS]
            else:
                desiredPositions[SS] = positionLimits[SS]

            # Bread
            if bread_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions[B] = -positionLimits[B]
            elif bread_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions[B] = positionLimits[B]

            # Sausage
            if sausage_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions[S] = -positionLimits[S]
            elif sausage_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions[S] = positionLimits[S]

            # MenuDash
            if menu_dash_change > sausage_sizzle_change + SIZZLE_SAFETY_MARGIN:
                desiredPositions[MD] = -positionLimits[MD]
            elif menu_dash_change < sausage_sizzle_change - SIZZLE_SAFETY_MARGIN:
                desiredPositions[MD] = positionLimits[MD]

        # Liferaft Ticket
        

        #######################################################################
        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        # Return the desired positions
        return desiredPositions
