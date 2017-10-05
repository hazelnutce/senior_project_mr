import pickle
from pythainlp.tokenize import word_tokenize

open_file = open("pickled_aspect/aspect_generic.pickle", "rb")
aspect_generic_word = pickle.load(open_file)
open_file.close()

open_file = open("pickled_aspect/aspect_sound.pickle", "rb")
aspect_sound_word = pickle.load(open_file)
open_file.close()

open_file = open("pickled_aspect/aspect_actor.pickle", "rb")
aspect_actor_word = pickle.load(open_file)
open_file.close()

open_file = open("pickled_aspect/aspect_graphic.pickle", "rb")
aspect_graphic_word = pickle.load(open_file)
open_file.close()

def seperator(text):
    aspect = []
    word_in_text = word_tokenize(text, engine="mm")
    for word in word_in_text:
        if("NOT_" in word):
            word = word[4:]
        for aspect_word in aspect_sound_word:
            if(word == aspect_word):
                aspect.append('sound');
                break;
        for aspect_word in aspect_graphic_word:
            if(word == aspect_word):
                aspect.append('graphic')
                break;
        for aspect_word in aspect_generic_word:
            if(word == aspect_word):
                aspect.append('generic')
                break;
        for aspect_word in aspect_actor_word:
            if(word == aspect_word):
                aspect.append('actor')
                break;
    return set(aspect)

