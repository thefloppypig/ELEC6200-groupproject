RAM_directory = '../RAM/'
safe_directory = '../SAFE/'
monitor_directory = '../data/unknowndata/'

# File to read
attack = "Normal"
use_realdata = False

# Sampling rates
sr_level_1 = 3 # Skipping lines from file
sr_level_2 = 1 # Skipping linesfrom file

# Up in severity
no_attacks_1_to_2 = 30000000
no_attacks_2_to_attack = 600000000000

# Down in severity
no_normal_1_to_sleep = 100000000000
no_normal_2_to_1 = 4