from __future__ import division

import csv
import pandas
import re
import itertools

colnames = ['name', 'gender', 'cnt', 'cnt_norm']
babynames = pandas.read_csv('testnames_min1000.csv', names=colnames)

name = babynames.name.tolist()
name.pop(0)
gender = babynames.gender.tolist()
cnt = babynames.cnt.tolist()
cnt_norm = babynames.cnt_norm.tolist()

first_letter = ['first_letter']
for n in name:
    first_letter.append(n[0].lower())

last_letter = ['last_letter']
for n in name:
    last_letter.append(n[len(n)-1].lower())

name_length = ['name_length']
for n in name:
    name_length.append(len(n))

v_c_prop = ['vowel_consonant_prop']
vowels = ('a','e','i','o','u','y','A','E','I','O','U','Y')
for n in name:
    v = 0
    c = 0
    if n[0].lower() == 'y':
        c = c+1
        v = v-1
    for letter in n:
        if letter in vowels:
            v = v+1
        else:
            c = c+1
    if c == 0:
        v_c_prop.append(v)
    else:
        v_c_prop.append(v/c)

double_letter = ['double_letter']
for n in name:
    for i in range(len(n)):
        try:
            if n[i]==n[i+1]:
                double_letter.append(True)
                break
        except:
            double_letter.append(False)
double_vowel = ['double_vowel']
for n in name:
    for i in range(len(n)):
        try:
            if n[i]==n[i+1]:
                # print n + " has " + n[i] + " repeated"
                if n[i].lower() in ('a', 'e', 'i', 'o', 'u'):
                    # print "appending for " + n[i]
                    double_vowel.append(True)
                    break
        except:
            double_vowel.append(False)
double_consonant = ['double_consonant']
for n in name:
    for i in range(len(n)):
        try:
            if n[i]==n[i+1]:
                if n[i].lower() not in ('a', 'e', 'i', 'o', 'u'):
                    double_consonant.append(True)
                    break
        except:
            double_consonant.append(False)


# from http://eayd.in/?p=232
def sylco(word) :
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables
    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']

    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']

    pre_one = ['preach']

    syls = 0 #added syllable number
    disc = 0 #discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        return syls

    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                disc+=1

    #3) discard trailing "e", except where ending is "le"

    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']

    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass

        else :
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
    disc+=doubleAndtripple + tripple

    #5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian" :
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui' :

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]

    if word[-3:] == "n't" :
        if word in negative :
            syls+=1
        else :
            pass

    #14) Handling the exceptional words.

    if word in exception_del :
        disc+=1

    if word in exception_add :
        syls+=1

    # calculate the output
    return numVowels - disc + syls

num_syll = ['num_syllables']
for n in name:
    num_syll.append(sylco(n))

alphabet = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
letter_count = {}
for letter in alphabet:
    value = letter + "_count"
    letter_count[letter] = [value]
for let in alphabet:
    for n in name:
        x=0
        for letter in n:
            if letter.lower() == let:
                x=x+1
        letter_count[let].append(x)

num_cons=["num_consonants"]
cons_prop=["consonant_prop"]
for n in name:
    x=0
    for letter in n:
        if letter not in vowels:
            x=x+1
    num_cons.append(x)
    y=x/len(n)
    cons_prop.append(y)

num_vowels=["num_vowels"]
vowels_prop=["vowel_prop"]
for n in name:
    x=0
    for letter in n:
        if letter in vowels:
            x=x+1
    num_vowels.append(x)
    y=x/len(n)
    vowels_prop.append(y)


name.insert(0, 'name')
rows = itertools.izip(name, gender, cnt, cnt_norm, first_letter, last_letter, name_length, v_c_prop,
                      double_letter, double_vowel, double_consonant, num_syll,
                      letter_count['a'], letter_count['b'], letter_count['c'], letter_count['d'], letter_count['e'],
                      letter_count['f'], letter_count['g'], letter_count['h'], letter_count['i'], letter_count['j'],
                      letter_count['k'], letter_count['l'], letter_count['m'], letter_count['n'], letter_count['o'],
                      letter_count['p'], letter_count['q'], letter_count['r'], letter_count['s'], letter_count['t'],
                      letter_count['u'], letter_count['v'], letter_count['w'], letter_count['x'], letter_count['y'],
                      letter_count['z'], num_cons, num_vowels, cons_prop, vowels_prop)
with open('testdata2012.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for item in rows:
        wr.writerow(item)