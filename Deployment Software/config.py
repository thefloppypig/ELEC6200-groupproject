RAM_directory = '../RAM/'
safe_directory = '../SAFE/'
monitor_directory = '../data/unknowndata/'

# Read from files (Fake sensors only)
attack = "Normal"
data_directory = '../data/'
use_realdata = False

# Sampling rates = Sleep time + Skipping lines from file
sr_level_1 = 3 
sr_level_2 = 1 

# Up in severity
no_attacks_1_to_2 = 3
no_attacks_2_to_attack = 6

# Down in severity
no_normal_1_to_sleep = 10
no_normal_2_to_1 = 4