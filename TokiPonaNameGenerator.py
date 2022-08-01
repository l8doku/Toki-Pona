# toki pona name generator
from random import choice
from random import choices
def generator(amount) -> list[str]:
    # the structure of toki pona syllables is (C)V(N), where C is a consonant, V is a vowel, and N is a nasal sound
    # double consonants and double vowels are forbidden
    # n and m can't be next to each other. in other words, nn, mm, nm, mn are forbidden
    # official words are not used to avoid confusion

    n_syllable_weight = 0.25
    starts_with_vowel_weight = 5 / 9
    n_second_letter_weight = 2 / 9
    break_weight = 2 / 3

    consontants = ['p', 't', 'k', 's', 'm', 'n', 'l', 'w', 'j']
    vowels = ['a', 'e', 'i', 'o', 'u']
    forbidden = ['ti', 'ji', 'wo', 'wu']
    with open('TokiPonaWords.txt', 'r') as f:
        words = f.read().splitlines()
    
    def random_syllable(ends_in: str = None) -> str:
        while True:
            syllable = choice(consontants) + choice(vowels) 
            if syllable not in forbidden:
                if choices([True, False], cum_weights=[n_syllable_weight, 1], k=1)[0]:
                    syllable += 'n'
                if {ends_in, syllable[0]} not in [{'m', 'n'}, {'n', 'n'}, {'m', 'm'}]:
                    return syllable
    names = []
    for _ in range(amount):
        while True: # make sure the name is not a official word or duplicated
            name = ''
            start_with_vowel = choices(
                [True, False], cum_weights=[starts_with_vowel_weight, 1], k=1
            )[0]
            if start_with_vowel:
                name += choice(vowels)
                if choices([True, False], cum_weights=[n_second_letter_weight, 1], k=1)[0]:
                    name += 'n'
            else:
                name += random_syllable()
            # determine how many syllables are in the name
            while True:
                name += random_syllable(name[-1])
                if choices([True, False], cum_weights=[break_weight, 1], k=1)[0]:
                    break
            
            if name not in words and name.capitalize() not in names:
                names.append(name.capitalize())
                break
    
    return sorted(names)
        
with open('Output.txt', 'w') as f:
    for name in generator(1000):
        f.write(name + '\n')
