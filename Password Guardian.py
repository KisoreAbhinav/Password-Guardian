#----------------------------PASSWORD GUARDIAN-----------------------------#
#------------------------------Libraries Used------------------------------#
import math
import string
import numpy as np
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
import re
from difflib import SequenceMatcher
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#--------------------------------------------------------------------------#


#       Phase 1 -> Taking A Password As An Input From The User
#--------------------------------------------------------------------------#
user_name = input("Enter Your Username -> ")
user_dob = input("Enter Your Date Of Birth (Format = DD-MM-YYYY) -> ")
password = input("Enter A Password (Max - 16 Characters) ->  ")
password = password[:16]
characters = list(password)
#--------------------------------------------------------------------------#


#              Phase 2 -> Extracting & Categorizing Data
#--------------------------------------------------------------------------#
length = len(password)
unique_characters = len(set(password))

lowercase = sum(1 for c in password if c.islower())
uppercase = sum(1 for c in password if c.isupper())
digit = sum(1 for c in password if c.isdigit())
special = sum(1 for c in password if not c.isalnum())

pool_size=0
if lowercase:
    pool_size+=26
if uppercase:
    pool_size+=26
if digit:
    pool_size+=10
if special:
    pool_size+=len(string.punctuation)

print("\nPassword Character Report")
print("Entered Password -> ",password)
print("List Of Characters Used -> ",characters)
print("Length Of The Password -> ",length)
print("Number of LowerCase Characters -> ",lowercase)
print("Number of UpperCase Characters -> ",uppercase)
print("Number of Digits -> ",digit)
print("Number of Special Symbols -> ",special)
print("Character Pool Size -> ",pool_size)
#--------------------------------------------------------------------------#


#              Phase 3.1 -> Space Search & Permutations 
#--------------------------------------------------------------------------#
search_space_category = pow(pool_size,length)
search_space_unique = pow(unique_characters,length)
char_counts = Counter(password)
perm_space = math.factorial(length)

for count in char_counts.values():
    perm_space = perm_space//math.factorial(count)

print("\nSpace Search Report")
print("Category Based Search Space -> ",search_space_category)
print("Password Unique Space Search With Repetition Allowed -> ",search_space_unique)
print("Distinct Permutations Of Current Password -> ",perm_space)
#--------------------------------------------------------------------------#


#              Phase 3.2 -> Pigeonhole Collision Risk
#--------------------------------------------------------------------------#
users = 1000
if search_space_unique>0:
    collision_prob = 1 - math.exp(-((users * (users - 1)) / (2 * search_space_unique)))
else:
    collision_prob = 1

print("\nCollision Risk Report")
print("Number of Users Assumed ->", users)
print("Search Space (Password-Unique) ->", search_space_unique)
print(f"Collision Probability -> {collision_prob:.6f} (~ {collision_prob*100:.2f}%)")
#--------------------------------------------------------------------------#


#              Phase 3.3 -> Categories Covered
#--------------------------------------------------------------------------#
categories_present = sum([1 if lowercase else 0, 1 if uppercase else 0, 1 if digit else 0, 1 if special else 0])

print("\nCategories Coverage Report")
print("Number Of Categories Present -> ",categories_present)

if categories_present>=3:
    print("Minimum Category Requirement Met")
else:
    print("Minimum Category Requrement Is Not Met")
#--------------------------------------------------------------------------#


#                      Phase 3.3 -> Nodes
#--------------------------------------------------------------------------#
G = nx.Graph()

for c in characters:
    G.add_node(c)

print("\nGraph Nodes Report")
print("Nodes (Characters In Password) -> ",list(G.nodes))
#--------------------------------------------------------------------------#


#                      Phase 3.3 -> Node Colors
#--------------------------------------------------------------------------#
node_colors = []

for c in G.nodes:
    if c.islower():
        node_colors.append("green")
    elif c.isupper():
        node_colors.append("yellow")
    elif c.isdigit():
        node_colors.append("red")
    else:
        node_colors.append("blue")

print("\nGraph Nodes Color Report")

for node,color in zip(G.nodes,node_colors):
    print(f"Node '{node}' -> Color: {color}")
#--------------------------------------------------------------------------#


#                      Phase 3.3 -> Edges
#--------------------------------------------------------------------------#
edges = []

for i in range (len(characters)-1):
    edges.append((characters[i], characters[i+1]))
    G.add_edge(characters[i],characters[i+1])

print("\nGraph Edges Report")
for edge in edges:
    print(f"Edge -> {edge}")
#--------------------------------------------------------------------------#


#                      Phase 3.4 -> Edge Weights
#--------------------------------------------------------------------------#
edge_weights = []

def get_category(c):
    if c.islower():
        return 'lower'
    elif c.isupper():
        return 'upper'
    elif c.isdigit():
        return 'digit'
    else:
        return 'special'

total_edges = len(edges)

for edge in edges:
    c1, c2 = edge
    cat1, cat2 = get_category(c1), get_category(c2)
    if c1 == c2:
        base_weight = 1.0         
    elif cat1 == cat2:
        base_weight = 0.7          
    else:
        base_weight = 0.4         

    weight = base_weight / total_edges
    edge_weights.append(weight)

print("\nGraph Edge Weights Report")
for edge, weight in zip(edges, edge_weights):
    print(f"Edge {edge} -> Weight: {weight:.3f}")
#--------------------------------------------------------------------------#


#                      Phase 3.5 -> Entropy
#--------------------------------------------------------------------------#
char_counts = Counter(characters)
char_probs = [count / length for count in char_counts.values()]

entropy = -sum(p * math.log2(p) for p in char_probs)

entropy_length_adjusted = entropy * length
print("\nShannon Entropy Report")
print(f"Entropy (per character) -> {entropy:.3f} bits")
print(f"Entropy adjusted for length -> {entropy_length_adjusted:.3f} bits") 
#--------------------------------------------------------------------------#


#                      Phase 3.6 -> Chromatic Number
#--------------------------------------------------------------------------#
coloring = nx.coloring.greedy_color(G, strategy="largest_first")

chromatic_number = max(coloring.values()) + 1 

print("\nChromatic Number Report")
print(f"Node Coloring -> {coloring}")
print(f"Chromatic Number -> {chromatic_number}")
#--------------------------------------------------------------------------#


#                 Phase 3.7 -> Markov-chain Transition Metric
#--------------------------------------------------------------------------#
transition_counts = {}
total_transitions = len(characters) - 1

for i in range(total_transitions):
    c1, c2 = characters[i], characters[i+1]
    if c1 not in transition_counts:
        transition_counts[c1] = Counter()
    transition_counts[c1][c2] += 1

transition_matrix = {}
for c1, counter in transition_counts.items():
    total = sum(counter.values())
    transition_matrix[c1] = {c2: count / total for c2, count in counter.items()}

print("\nMarkov-chain Transition Metric Report")
for c1, transitions in transition_matrix.items():
    for c2, prob in transitions.items():
        print(f"P({c2} | {c1}) = {prob:.3f}")
#--------------------------------------------------------------------------#



#                 Phase 3.8 -> Personal Information Check
#--------------------------------------------------------------------------#
print("\nPersonal Information Check")
dob_clean = re.split(r'[-/]', user_dob)
dob_parts = [p.lower() for p in dob_clean if p]

month_variants = []
for part in dob_parts:
    try:
        month_num = int(part)
        month_name = datetime(2000, month_num, 1).strftime("%b").lower()
        month_full = datetime(2000, month_num, 1).strftime("%B").lower()
        month_variants.extend([month_name, month_full])
    except:
        pass

dob_parts.extend(month_variants)

if len(dob_parts) >= 3:
    day, month, year = dob_parts[0], dob_parts[1], dob_parts[2]
    combined = [day+month, month+day, day+year[-2:], month+year[-2:], year]
    dob_parts.extend(combined)

dob_parts = list(set(dob_parts))
password_lower = password.lower()
flags = []
if len(user_name) >= 3:
    for i in range(len(user_name)-2):
        frag = user_name[i:i+3]
        if frag in password_lower:
            flags.append(f"Name fragment detected: '{frag}'")
for part in dob_parts:
    if part and part in password_lower:
        flags.append(f"DOB element detected: '{part}'")
if flags:
    print("Personal Info Detected in Password!")
    for f in flags:
        print(" -", f)
    personal_info_score = 0.0
else:
    print("No personal information found in password.")
    personal_info_score = 1.0
#--------------------------------------------------------------------------#

#---------------------------- Phase 3.9 -> Dictionary Fuzziness Check ----------------------------#
exclude_list = []

# Name fragments
if len(user_name) >= 3:
    for i in range(len(user_name)-2):
        exclude_list.append(user_name[i:i+3].lower())

# DOB fragments
dob_clean = re.split(r'[-/]', user_dob)
dob_parts = [p.lower() for p in dob_clean if p]

# Month variants
month_variants = []
for part in dob_parts:
    try:
        month_num = int(part)
        month_name = datetime(2000, month_num, 1).strftime("%b").lower()
        month_full = datetime(2000, month_num, 1).strftime("%B").lower()
        month_variants.extend([month_name, month_full])
    except:
        pass
dob_parts.extend(month_variants)

# Combine all exclusions
exclude_list.extend(dob_parts)
exclude_list = list(set([frag for frag in exclude_list if frag]))  # remove duplicates & empties

# Load dictionary
dictionary_file = os.path.join(BASE_DIR, "words.txt")
with open(dictionary_file, "r", encoding="utf-8") as f:
    dictionary_words = [line.strip().lower() for line in f if line.strip()]

password_lower = password.lower()
min_sub_len = 3 
max_similarity = 0

for word in dictionary_words:
    if word in exclude_list:  # skip user-specific words
        continue
    for i in range(len(password_lower)):
        for j in range(i + min_sub_len, len(password_lower) + 1):
            substring = password_lower[i:j]
            similarity = SequenceMatcher(None, substring, word).ratio()
            max_similarity = max(max_similarity, similarity)

fuzzy_word_score = 1 - max_similarity

print("\nDictionary Fuzziness Report")
print(f"Max similarity with dictionary words -> {max_similarity:.2f}")
print(f"Fuzzy Word Score (1 = safe, 0 = contains dictionary words) -> {fuzzy_word_score:.2f}")

#--------------------------------------------------------------------------#


#                 Phase 3.10 -> Leaked Passwords Dataset Check (Fast)
#--------------------------------------------------------------------------#
print("\nLeaked Passwords Check")
leaked_file = os.path.join(BASE_DIR, "leaked.txt")
 
try:
    with open(leaked_file, "r", encoding="utf-8", errors="ignore") as f:
        leaked_list = [line.strip().lower() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Leaked password file not found: '{leaked_file}'. Skipping check.")
    leaked_list = []

pw_low = password.lower()
leaked_flag = False
leaked_matches = []

for leaked_word in leaked_list:
    if leaked_word == pw_low:
        leaked_flag = True
        leaked_matches.append(("exact", leaked_word))
        break
    if len(leaked_word) >= 4 and leaked_word in pw_low:
        leaked_flag = True
        leaked_matches.append(("substring", leaked_word))
        break
    trans = str.maketrans({"4":"a","@":"a","3":"e","1":"l","0":"o","$":"s","5":"s","7":"t"})
    if leaked_word in pw_low.translate(trans):
        leaked_flag = True
        leaked_matches.append(("leet-substring", leaked_word))
        break

if leaked_flag:
    print("Leaked password indicator: password (or part of it) appears in dataset.")
    for kind, w in leaked_matches:
        print(f" - {kind} match -> '{w}'")
else:
    print("No match found in leaked-password dataset.")
#--------------------------------------------------------------------------#


#                 Phase 4 -> Computing Password Strength
#--------------------------------------------------------------------------#
max_entropy = math.log2(pool_size) if pool_size > 0 else 1
entropy_score = entropy / max_entropy 

length_score = min(length / 16, 1) 
category_score = categories_present / 4  
chromatic_score = chromatic_number / len(G.nodes) if len(G.nodes) > 0 else 0

if edge_weights:
    avg_edge_weight = sum(edge_weights) / len(edge_weights)
    edge_score = 1 - abs(avg_edge_weight - 0.7) 
else:
    edge_score = 0

collision_score = 1 - min(collision_prob, 1)

if length < 6:
    length_penalty = 0.4
elif length < 8:
    length_penalty = 0.7
elif length < 10:
    length_penalty = 0.9
else:
    length_penalty = 1.0

final_score = (
    0.30 * entropy_score +
    0.18 * length_score +
    0.15 * category_score +
    0.10 * chromatic_score +
    0.10 * edge_score +
    0.05 * collision_score +
    0.05 * personal_info_score+
    0.07 * fuzzy_word_score
)

final_score *= length_penalty
strength_percent = (final_score**1.2) * 100

print("\nFinal Password Strength Report")
print(f"Entropy Score\t\t-> {entropy_score:.2f}")
print(f"Length Score\t\t-> {length_score:.2f}")
print(f"Category Score\t\t-> {category_score:.2f}")
print(f"Chromatic Score\t\t-> {chromatic_score:.2f}")
print(f"Edge Score\t\t-> {edge_score:.2f}")
print(f"Collision Score\t\t-> {collision_score:.2f}")
print(f"Input Vector Score\t-> {personal_info_score:.2f}")
print(f"\nOverall Password Strength -> {strength_percent:.2f}/100")

if strength_percent >= 80:
    result = "Very Strong"
elif strength_percent >= 60:
    result = "Strong"
elif strength_percent >= 40:
    result = "Moderate"
else:
    result = "Weak"
print(f"Result -> {result}")
#--------------------------------------------------------------------------#


#                   Phase 5 -> Suggestions & Improvements
#--------------------------------------------------------------------------#
print("\nSuggestions Report")

improved = False

if entropy_score < 0.5:
    print(" - Increase entropy: avoid repeating characters, add more unique symbols.")
    improved = True

if length_score < 1.0:
    print(" - Make your password longer (up to 16 characters) to increase security.")
    improved = True

if category_score < 1.0:
    missing = []
    if lowercase == 0: missing.append("lowercase letters")
    if uppercase == 0: missing.append("uppercase letters")
    if digit == 0: missing.append("digits")
    if special == 0: missing.append("special symbols")
    print(f" - Add more character types ({', '.join(missing)}).")
    improved = True

if chromatic_score < 0.6:
    print(" - Mix character positions so different types of characters are spread out.")
    improved = True

if edge_score < 0.7:
    print(" - Avoid predictable sequences (like aaa, 1234, or abcd).")
    improved = True

if collision_score < 0.5:
    print(" - Use less common characters and longer length to reduce collision risk.")
    improved = True

if not improved:
    print("No major improvements needed!")
#--------------------------------------------------------------------------#


#                       Phase 6 -> Plotting Graphs
#--------------------------------------------------------------------------#
#Radar Chart
labels = ["Entropy", "Category", "Chromatic", "Transition", "Collision", "Input Vector", "Fuzzy"]
stats = [entropy_score, category_score, chromatic_score, edge_score, collision_score, personal_info_score, fuzzy_word_score]

num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
stats += stats[:1]
angles += angles[:1]

#Transition Chart
G_transition = nx.DiGraph()
transition_counts = {}

for (c1, c2), w in zip(edges, edge_weights):
    if G_transition.has_edge(c1, c2):
        G_transition[c1][c2]['weight'] += w
    else:
        G_transition.add_edge(c1, c2, weight=w)
    transition_counts[c1] = transition_counts.get(c1, 0) + w

char_freq = Counter(characters)

node_colors = []
node_sizes = []
for c in G_transition.nodes():
    if c.islower():
        node_colors.append("#2ca02c")
    elif c.isupper():
        node_colors.append("#ff7f0e")
    elif c.isdigit():
        node_colors.append("#d62728")
    else:
        node_colors.append("#1f77b4")
    node_sizes.append(400 + 200 * char_freq.get(c, 1))

pos = nx.circular_layout(G_transition)

weights = []
edge_colors = []
edge_labels = {}
for (u, v, d) in G_transition.edges(data=True):
    prob = d['weight'] / transition_counts[u] if transition_counts[u] > 0 else 0
    weights.append(1 + 6 * prob)
    edge_colors.append((0, 0, 0, 0.2 + 0.8 * prob))
    edge_labels[(u, v)] = f"{prob:.2f}"

fig = plt.figure(figsize=(20, 9))

ax = fig.add_subplot(1, 2, 1, projection="polar")
ax2 = fig.add_subplot(1, 2, 2)

# ---------------- RADAR CHART ---------------- #
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_ylim(0, 1.05)

ax.set_frame_on(False)
ax.patch.set_visible(False)
for spine in ax.spines.values():
    spine.set_visible(False)

cmap = LinearSegmentedColormap.from_list("grad_red_green", ["#ff4c4c","#ffd700","#4caf50"])
r = np.linspace(0, 1, 100)
theta_fill = np.linspace(0, 2*np.pi, 100)
for i in range(len(r)-1):
    ax.fill_between(theta_fill, r[i], r[i+1], color=cmap(r[i]), alpha=0.2)

ax.plot(angles, stats, color="tab:blue", linewidth=3, linestyle='solid')
ax.fill(angles, stats, color="tab:blue", alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=14, fontweight="bold", color="navy")
for i, label in enumerate(ax.get_xticklabels()):
    if i == 0:   # "Entropy"
        label.set_position((label.get_position()[0], label.get_position()[1] + 0.05))
    elif i == 1: # "Category"
        label.set_position((label.get_position()[0], label.get_position()[1] - 0.05))
    elif i == 2: # "Chromatic"
        label.set_position((label.get_position()[0], label.get_position()[1] - 0.01))
    elif i == 3: # "Transition"
        label.set_position((label.get_position()[0], label.get_position()[1] - 0.01))
    elif i == 4: # "Collision"
        label.set_position((label.get_position()[0], label.get_position()[1] - 0.05))
    elif i == 5: # "Input Vector"
        label.set_position((label.get_position()[0], label.get_position()[1] - 0.05))

ax.grid(color="gray", linestyle="--", linewidth=0.6, alpha=0.5)
ax.set_facecolor("#fdfdfd")
ax.set_title(f"Password Strength: {strength_percent:.2f}/100 ({result})",
             fontsize=18, fontweight="bold", pad=55)

# ---------------- TRANSITION GRAPH ---------------- #
ax = ax2

for c, node_color, node_size in zip(G_transition.nodes(), node_colors, node_sizes):
    x, y = pos[c]
    ax.scatter(x, y, s=node_size*1.2, color=node_color, alpha=0.25)

nx.draw_networkx_nodes(G_transition, pos,
                       node_color=node_colors,
                       node_size=node_sizes,
                       alpha=0.85,
                       ax=ax)

nx.draw_networkx_edges(G_transition, pos,
                       arrowstyle="->",
                       arrowsize=18,
                       width=weights,
                       edge_color=edge_colors,
                       connectionstyle="arc3,rad=0.2",
                       ax=ax)

nx.draw_networkx_labels(G_transition, pos,
                        font_size=12,
                        font_weight="bold",
                        font_color="black",
                        ax=ax)

nx.draw_networkx_edge_labels(G_transition, pos,
                             edge_labels=edge_labels,
                             font_size=10,
                             font_color="#555555",
                             label_pos=0.6,
                             rotate=False,
                             ax=ax)

legend_handles = [
    mpatches.Patch(color="#2ca02c", label="Lowercase"),
    mpatches.Patch(color="#ff7f0e", label="Uppercase"),
    mpatches.Patch(color="#d62728", label="Digit"),
    mpatches.Patch(color="#1f77b4", label="Special Character")
]
ax.legend(handles=legend_handles,
          loc="upper right",
          bbox_to_anchor=(1.18, 1.05),
          frameon=False,
          fontsize=11)

ax.set_axis_off()
ax.set_title("Character Transition Graph", fontsize=20, fontweight="bold", pad=28)

plt.tight_layout()
plt.show()
#--------------------------------------------------------------------------#
