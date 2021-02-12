# -*- coding: utf-8 -*-

from colorama import Fore, Back, Style
from colorama import init
import argparse
import re
import pathlib
import itertools
import tldextract

init(autoreset=True)
NUM_COUNT = 2

def writefile(domains, path):
    with open(path, "a") as opfile:
        opfile.write("\n".join(domains)+"\n")
        

def partiate_domain(domain):
    ext = tldextract.extract(domain.lower())
    parts = (ext.subdomain.split('.') + [ext.registered_domain])

    return parts

def insert_word_every_index(parts, words):
    domains = []
    
    for w in words:
        for i in range(len(parts)):
            tmp_parts = parts[:-1]
            tmp_parts.insert(i, w)
            domains.append('.'.join(tmp_parts + [parts[-1]]))

    return domains 


def increase_num_found(parts):
    domains = []
    replacement_list = []
    parts_joined = '.'.join(parts[:-1])
    digits = re.findall(r'\d{1,5}', parts_joined)

    part_list = re.findall(r'[^0-9]+', parts_joined)

    for d in digits:
        tmp_list = []
        for m in range(NUM_COUNT):
            replacement = str(int(d) + 1 + m).zfill(len(d))
            tmp_list.append(replacement)

        replacement_list.append(tmp_list)

    n = len(replacement_list)


    r_list = []
    if n == 3 :
        for x in replacement_list[0]:
            for y in replacement_list[1]:
              for z in replacement_list[2]:
                    r_list.append([x,y,z])
    
    elif n == 2:
        for x in replacement_list[0]:
            for y in replacement_list[1]:
                r_list.append([x,y])
    
    elif n == 1:
        for x in replacement_list[0]:
            r_list.append([x])

    elif n > 3:
        return domains


    for replacements in r_list:
        tmp_domain = ""
        for replacement, part in zip(replacements,part_list) :
            tmp_domain = tmp_domain + part + replacement
        
        if (part_list[-1] == part):
            tmp_domain = tmp_domain + "." +parts[-1]
        else :
            tmp_domain = tmp_domain + part_list[-1] +"." +parts[-1]
        domains.append(tmp_domain) 

    return domains
            
def decrease_num_found(parts): 
    domains = []
    replacement_list = []
    parts_joined = '.'.join(parts[:-1])
    digits = re.findall(r'\d{1,5}', parts_joined)

    part_list = re.findall(r'[^0-9]+', parts_joined)

    for d in digits:
        tmp_list = []
        for m in range(NUM_COUNT):
            new_digit = (int(d) - 1 - m)
            if new_digit < 0:
                break

            replacement = str(new_digit).zfill(len(d))
            tmp_list.append(replacement)
        replacement_list.append(tmp_list)
  
    n = len(replacement_list)

    r_list = []

    if n == 3 :
        for x in replacement_list[0]:
            for y in replacement_list[1]:
                for z in replacement_list[2]:
                    r_list.append([x,y,z])

    elif n == 2:
        for x in replacement_list[0]:
            for y in replacement_list[1]:
                r_list.append([x,y])

    elif n == 1:
        for x in replacement_list[0]:
            r_list.append([x])

    elif n > 3:
        return domains

    for replacements in r_list:
        tmp_domain = ""
        for replacement, part in zip(replacements,part_list) :
            tmp_domain = tmp_domain + part + replacement

        if (part_list[-1] == part):
            tmp_domain = tmp_domain + "." +parts[-1]
        else :
             tmp_domain = tmp_domain + part_list[-1] +"." +parts[-1]

        domains.append(tmp_domain) 

    return domains


def prepend_word_every_index(parts, words):
    domains = []
    
    for w in words:
        for i in range(len(parts[:-1])):
            tmp_parts = parts[:-1]
            tmp_parts[i] = '{}{}'.format(w, tmp_parts[i])
            domains.append('.'.join(tmp_parts + [parts[-1]]))

            tmp_parts = parts[:-1]
            tmp_parts[i] = '{}-{}'.format(w, tmp_parts[i])
            domains.append('.'.join(tmp_parts + [parts[-1]]))

    return domains
    

def append_word_every_index(parts, words):
    domains = []

    for w in words:
        for i in range(len(parts[:-1])):
            tmp_parts = parts[:-1]
            tmp_parts[i] = '{}{}'.format(tmp_parts[i], w)
            domains.append('.'.join(tmp_parts + [parts[-1]]))

            tmp_parts = parts[:-1]
            tmp_parts[i] = '{}-{}'.format(tmp_parts[i], w)
            domains.append('.'.join(tmp_parts + [parts[-1]]))

    return domains


def replace_word_with_word(parts, words):
    domains = []

    for w in words:
        if w in '.'.join(parts[:-1]):
            for w_alt in words:
                if w == w_alt:
                    continue

                domains.append('{}.{}'.format('.'.join(parts[:-1]).replace(w, w_alt), parts[-1]))
    
    return domains


def extract_custom_words(domains):

    valid_tokens = set()

    wordlen = 2


    for domain in domains:
        partition = partiate_domain(domain)[:-1]
        tokens = set(itertools.chain(*[word.lower().split('-') for word in partition]))
        tokens = tokens.union({word.lower() for word in partition})

        for t in tokens:
            if len(t) >= wordlen:
                valid_tokens.add(t)

    return valid_tokens


def add_words(domains, words):
    words = list(set(words).union(extract_custom_words(domains)))
    return words



def identify(parts, output):
    parts_joined = '.'.join(parts[:-1])
    digits = re.findall(r'\d{1,5}', parts_joined)

    if (len(digits) != 0) :
        domains_gen = increase_num_found(parts)
        if len(domains_gen) != 0 :
            writefile(domains_gen,output)

        domains_gen = decrease_num_found(parts)
        if len(domains_gen) != 0 :
            writefile(domains_gen,output)

    

def main():
    
    
    parser = argparse.ArgumentParser()
   
    parser.add_argument("-w", "--words",
            help= "生成新的字典",
            action="store_true")
    
    parser.add_argument("-a", "--add",
            help= "追加单词",
            action="store_true")


    parser.add_argument("-n1", "--number1",
            help= "增数字",
            action="store_true")

    parser.add_argument("-n2", "--number2",
            help= "减数字",
            action="store_true")


    parser.add_argument("-r", "--replace",
            help= "替换单词",
            action="store_true")


    args = parser.parse_args()

    
    with open(pathlib.Path(__file__).parent / 'domains.txt', "r") as f:
        domains = f.read().splitlines()

    print(Fore.YELLOW + "[~] 域名读取完成")
    print(domains)

    
    with open(pathlib.Path(__file__).parent / 'words.txt', "r") as f:
        words = f.read().splitlines()
    
    print(Fore.YELLOW + "[~] 字典读取完成")
    print(words)

    if args.words:
        print(Fore.YELLOW + "[~] 生成新的字典")
        writefile(add_words(domains, words), pathlib.Path(__file__).parent / 'gen_words.txt')
        return 



    output= "gen_domains.txt"

    
    for domain in set(domains):
        parts = partiate_domain(domain)
        domains_gen = []

        identify(parts, output)


        if args.add :
            domains_gen = insert_word_every_index(parts, words)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)

            domains_gen = prepend_word_every_index(parts, words)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)

            domains_gen = append_word_every_index(parts, words)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)

       
        if args.number1 :
            domains_gen = increase_num_found(parts)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)

        
        if args.number2 :
            domains_gen = decrease_num_found(parts)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)


        if args.replace :
            domains_gen = replace_word_with_word(parts, words)
            if len(domains_gen) != 0 :
                writefile(domains_gen,output)
        

    print(Fore.YELLOW + "[~] 新域名生成完成")


if __name__ == "__main__":
    main()

