from __future__ import division

import csv
import pandas
import re
import itertools

colnames = ['year', 'gender', 'race', 'name', 'cnt','rank']
babynames = pandas.read_csv('babynames2.csv', names=colnames)
year = babynames.year.tolist()
gender = babynames.gender.tolist()
race = babynames.race.tolist()
name = babynames.name.tolist()
name.pop(0)
count = babynames.cnt.tolist()

first_letter = ['first_letter']
for n in name:
    first_letter.append(n[0])

last_letter = ['last_letter']
for n in name:
    last_letter.append(n[len(n)-1])

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

a_count=["num_a"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='A' or n[i]=='a':
            x=x+1
    a_count.append(x)

b_count=["num_b"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='B' or n[i]=='b':
            x=x+1
    b_count.append(x)

c_count=["num_c"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='C' or n[i]=='c':
            x=x+1
    c_count.append(x)

d_count=["num_d"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='D' or n[i]=='d':
            x=x+1
    d_count.append(x)

e_count=["num_e"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='E' or n[i]=='e':
            x=x+1
    e_count.append(x)

f_count=["num_f"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='F' or n[i]=='f':
            x=x+1
    f_count.append(x)

g_count=["num_g"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='G' or n[i]=='g':
            x=x+1
    g_count.append(x)

h_count=["num_h"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='H' or n[i]=='h':
            x=x+1
    h_count.append(x)

i_count=["num_i"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='I' or n[i]=='i':
            x=x+1
    i_count.append(x)

j_count=["num_j"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='J' or n[i]=='j':
            x=x+1
    j_count.append(x)

k_count=["num_k"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='K' or n[i]=='k':
            x=x+1
    k_count.append(x)

l_count=["num_l"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='L' or n[i]=='l':
            x=x+1
    l_count.append(x)

m_count=["num_m"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='M' or n[i]=='m':
            x=x+1
    m_count.append(x)

n_count=["num_n"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='N' or n[i]=='n':
            x=x+1
    n_count.append(x)

o_count=["num_o"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='O' or n[i]=='o':
            x=x+1
    o_count.append(x)

p_count=["num_p"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='P' or n[i]=='p':
            x=x+1
    p_count.append(x)

q_count=["num_q"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='Q' or n[i]=='q':
            x=x+1
    q_count.append(x)

r_count=["num_r"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='R' or n[i]=='r':
            x=x+1
    r_count.append(x)

s_count=["num_s"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='S' or n[i]=='s':
            x=x+1
    s_count.append(x)

t_count=["num_t"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='T' or n[i]=='t':
            x=x+1
    t_count.append(x)

u_count=["num_u"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='U' or n[i]=='u':
            x=x+1
    u_count.append(x)

v_count=["num_v"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='V' or n[i]=='v':
            x=x+1
    v_count.append(x)

w_count=["num_w"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='W' or n[i]=='w':
            x=x+1
    w_count.append(x)

x_count=["num_x"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='X' or n[i]=='x':
            x=x+1
    x_count.append(x)

y_count=["num_y"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='Y' or n[i]=='y':
            x=x+1
    y_count.append(x)

z_count=["num_z"]
for n in name:
    x=0
    for i in range(len(n)):
        if n[i]=='Z' or n[i]=='z':
            x=x+1
    z_count.append(x)

# vowel/consonant proportion
# number of syllables

name.insert(0, 'name')
rows = itertools.izip(year, gender, race, name, count, first_letter, last_letter, name_length, v_c_prop, double_letter, num_syll,
                      a_count, b_count, c_count, d_count, e_count, f_count, g_count, h_count, i_count, j_count, k_count, l_count, m_count,
                      n_count, o_count, p_count, q_count, r_count, s_count, t_count, u_count, v_count, w_count, x_count, y_count, z_count)
with open('babynames3.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for item in rows:
        wr.writerow(item)