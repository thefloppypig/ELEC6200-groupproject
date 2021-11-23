# L1 to L1 

RAM_directory = '../RAM/'
safe_directory = '../SAFE/'
monitor_directory = '../data/unknowndata/'

# Sampling rates
sr_level_1 = 1 # sec
sr_level_2 = 1 # sec

# Up in severity
potential_attacks = 2
no_attacks_1_to_2 = 1
no_attacks_2_to_attack = 4

# Down in severity
sleep_count = 100
no_normal_1_to_sleep = 100
reset_count = 0
no_normal_2_to_1 = 1


# LEVEL
# potential_attacks < no_attacks_1_to_2 --> L1
# potential_attacks >= no_attacks_1_to_2 --> L2

# DOWN IN RISK
# If normal activity --> sleep_count++ or reset_count++
# If sleep_count > no_normal_1_to_sleep --> L1 to Sleep
# If reset_count > no_normal_2_to_1 --> L2 to L1

# UP IN RISK
# If attack detected --> potential_attacks = potential_attacks + 1
# potential_attacks == no_attacks_1_to_2 --> Defense L1
# potential_attacks == no_attacks_2_to_attac --> Defense L2