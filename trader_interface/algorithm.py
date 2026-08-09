import numpy as np
import pandas as pd

## Constants

# UQ
UQ = "UQ Dollar"
UQ_AVG = 100
UQ_SAFETY_MARGIN = 0.002

# Fintech Token
FT = "Fintech Token"

# Thriften Jeans
TJ = "Thrifted Jeans"
TJ_SAFETY_MARGIN = 0.005

# Boat Party Ticket
BPT = "Boat Party Ticket"

# Sausage Sizzle
SS = "Sausage Sizzle"
SIZZLE_SAFETY_MARGIN = 0

# Bread
B = "Bread"
# Sausage
S = "Sausage"
BS_SAFETY_MARGIN = 0

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

        # Create data frame to be used for EMAs
        df = pd.DataFrame(self.data)

        #######################################################################
        # UQ Dollar
        if self.data[UQ][-1]/UQ_AVG > 1 + UQ_SAFETY_MARGIN:
            desiredPositions[UQ] = -positionLimits[UQ]
        elif self.data[UQ][-1]/UQ_AVG < 1 - UQ_SAFETY_MARGIN:
            desiredPositions[UQ] = positionLimits[UQ]

        # Fintech Token

        # Thrifted Jeans (Most volatility)
        if self.day >= 7:
            # if price has gone down, buy
            df['TJ_EMA_8'] = df[TJ].ewm(span=8, adjust=False).mean()
            df['TJ_EMA_5'] = df[TJ].ewm(span=5, adjust=False).mean()
            if df['TJ_EMA_5'].iloc[-1] / df['TJ_EMA_8'].iloc[-1] > 1 + TJ_SAFETY_MARGIN:
                desiredPositions[TJ] = positionLimits[TJ]
            elif df['TJ_EMA_5'].iloc[-1] / df['TJ_EMA_8'].iloc[-1] < 1 - TJ_SAFETY_MARGIN:
                desiredPositions[TJ] = -positionLimits[TJ]

        # Boat Party Ticket (Hard coded based of timeline of uni year)
        if self.day % 365 <= 50:
            desiredPositions[BPT] = positionLimits[BPT]
        elif 30 < self.day % 365 <= 160:
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
            avg_change = (bread_change + sausage_change) / 2
            
            sausage_sizzle_change = self.data[SS][-1] / self.data[SS][-2]
            if avg_change < 1:
                desiredPositions[SS] = -positionLimits[SS]
            else:
                desiredPositions[SS] = positionLimits[SS]

            # Bread and Sausage
            df['B_EMA_8'] = df[B].ewm(span=8, adjust=False).mean()
            df['B_EMA_5'] = df[B].ewm(span=5, adjust=False).mean()
            df['S_EMA_8'] = df[S].ewm(span=8, adjust=False).mean()
            df['S_EMA_5'] = df[S].ewm(span=5, adjust=False).mean()

            if df['B_EMA_5'].iloc[-1] / df['B_EMA_8'].iloc[-1] > 1 + BS_SAFETY_MARGIN:
                desiredPositions[B] = positionLimits[B]
            elif df['B_EMA_5'].iloc[-1] / df['B_EMA_8'].iloc[-1] < 1 - BS_SAFETY_MARGIN:
                desiredPositions[B] = -positionLimits[B] * 0.5

            if df['S_EMA_5'].iloc[-1] / df['S_EMA_8'].iloc[-1] > 1 + BS_SAFETY_MARGIN:
                desiredPositions[S] = positionLimits[S]
            elif df['S_EMA_5'].iloc[-1] / df['S_EMA_8'].iloc[-1] < 1 - BS_SAFETY_MARGIN:
                desiredPositions[S] = -positionLimits[S] * 0.5

        # MenuDash
        if self.day >= 7:
            # Create exponential moving average
            df['SS_EMA_14'] = df[SS].ewm(span=14, adjust=False).mean()

            if df['SS_EMA_14'].iloc[-1] > self.data[SS][-1]:
                desiredPositions[MD] = -positionLimits[MD]
            else:
                desiredPositions[MD] = positionLimits[MD]

        # Liferaft Ticket
        

        #######################################################################
        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        # Return the desired positions
        return desiredPositions
