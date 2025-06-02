from tamil_letter_split import tamil_letter_split

def tamil_syllable_split_01(word):
    special_conjunctions = ["ஸ்ரீ", "க்ஷெள", "க்ஷ",	"க்ஷா",	"க்ஷி",	"க்ஷீ",	"க்ஷு",	"க்ஷூ",	"க்ஷெ",	"க்ஷே",	"க்ஷை",	"க்ஷொ",	"க்ஷோ"] 
    
    graphemes = tamil_letter_split(word)
    labels = []

    for g in graphemes:
        if g in special_conjunctions:
            labels.append((g, 'O'))  # Always treat special conjunctions as 'O'
        elif '்' in g:
            labels.append((g, 'C'))  # Consonant
        else:
            labels.append((g, 'O'))  # Vowel or consonant-vowel

    #print("Labeled Graphemes:", labels)  # Debug

    syllables = []
    used = [False] * len(labels)

    # attach consonants to nearest vowels
    for i, (g, l) in enumerate(labels):
        if l == 'C':
            # Look left and right for closest 'O'
            left = right = float('inf')
            left_index = right_index = -1

            # Look left
            for j in range(i-1, -1, -1):
                if labels[j][1] == 'O' and not used[j]:
                    left = i - j
                    left_index = j
                    break

            # Look right
            for j in range(i+1, len(labels)):
                if labels[j][1] == 'O' and not used[j]:
                    right = j - i
                    right_index = j
                    break

            # Attach to the nearest
            if left <= right and left_index != -1:
                labels[left_index] = (labels[left_index][0] + g, 'O')
                used[i] = True
            elif right_index != -1:
                labels[right_index] = (g + labels[right_index][0], 'O')
                used[i] = True
            else:
                # No vowel to attach to, treat as orphan
                pass

    # collect syllables
    for i, (g, l) in enumerate(labels):
        if not used[i]:
            syllables.append(g)

    return syllables

def tamil_syllable_split(word):
    special_conjunctions = [
        "ஸ்ரீ", "க்ஷெள", "க்ஷ", "க்ஷா", "க்ஷி", "க்ஷீ", "க்ஷு",
        "க்ஷூ", "க்ஷெ", "க்ஷே", "க்ஷை", "க்ஷொ", "க்ஷோ"
    ]

    graphemes = tamil_letter_split(word)
    labels = []

    for g in graphemes:
        if g in special_conjunctions:
            labels.append((g, 'O'))
        elif '்' in g:
            labels.append((g, 'C'))
        else:
            labels.append((g, 'O'))

    print("Labeled Graphemes:", labels)  # Debug

    syllables = []
    used = [False] * len(labels)

    # Handle the very first grapheme separately (attach to next vowel if it's a consonant)
    i = 0
    if labels and labels[0][1] == 'C':
        # Look for the next vowel
        for j in range(1, len(labels)):
            if labels[j][1] == 'O':
                labels[j] = (labels[0][0] + labels[j][0], 'O')
                used[0] = True
                break

    # From second grapheme onward: attach consonants to the previous vowel
    for i in range(1, len(labels)):
        if labels[i][1] == 'C' and not used[i]:
            # Look left for nearest vowel
            for j in range(i - 1, -1, -1):
                if labels[j][1] == 'O' and not used[j]:
                    labels[j] = (labels[j][0] + labels[i][0], 'O')
                    used[i] = True
                    break

    # Collect final syllables
    for i, (g, _) in enumerate(labels):
        if not used[i]:
            syllables.append(g)

    return syllables