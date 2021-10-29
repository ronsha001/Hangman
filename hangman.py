import re
from photos import *
# import colors for output
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset = True)


def print_opening():
    # print opening message (blue)
    HANGMAN_ASCII_ART = Fore.BLUE+"""
Welcome to the game Hangman
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/

"""
    print(HANGMAN_ASCII_ART)

def check_win(secret_word, old_letters_guessed):
    """
    :param secret_word: complete secret word to guess
    :param old_letters_guessed: collected list of all letter guessed
    :type secret_word: string
    :type old_letters_guessed: list
    :return: whether user win or not
    :rtype: boolean
    """
    # check if old_letters_guessed list contains all of secret_word's letters
    found = False
    for i in secret_word:
        found = False
        for j in old_letters_guessed:
            if j == i:
                found = True
                break;
        
        if found == False:
            return False
    
    return True
    
def replacer(string , add_string , index):
    """
    :param string: origin string
    :param add_string: another string to replace slice from origin string
    :param index: index to tell where to replace 
    :type string: string
    :type add_string: string
    :type index: int
    :return: new string after replace add_string in string at the specific index
    :rtype: string
    """
    # insert the new string between "slices" of the original
    return string[:index] + add_string + string[index + 1:]

def inserter(string , add_string , index):
    """
    :param string: origin string
    :param add_string: another string to add to origin string
    :param index: index to tell where to add another string to origin string
    :type string: string
    :type add_string: string
    :type index: int
    :return: new string built with original string and added string between it
    :rtype: string
    """
    return string[:index] + add_string + string[index:]
    
def show_hidden_word(secret_word, old_letters_guessed):
    """
    :param secret_word: complete secret word to guess
    :param old_letters_guessed: collected list of all letter guessed
    :type secret_word: string
    :type old_letters_guessed: list
    :return: hidden format string
    :rtype: string
    """
    # return string without hidden letters_guessed after guessed
    
    string = ""
    for i in secret_word:
        string += "_"
    
    for i in old_letters_guessed:
        if i in secret_word:
            for j in range(0 , len(secret_word)):  
                if secret_word[j] == i:
                    string = replacer(string , i , j)
    
    for i in range(1 , len(string) * 2 - 1, 2):
        string = inserter(string , " " , i)
    
    return string
    
def count_lettes_in_word(word):
    """
    :param word: regular string word without spaces
    :type word: string
    :return: return count of unique letters in string. if some letter show up more then once it counts as 1 on counter
    :rtype: int
    """
    # return count of unique letters in string
    # if some letter show up more then once it counts as 1 on counter
    letter_list = []
    count = 0
    for letter in word:
        if letter not in letter_list:
            count += 1
            letter_list.append(letter)
    
    return count

def count_words_in_list(data_list):
    """
    :param data_list: list of words without spaces 
    :type data_list: list
    :return: return count of unique words in list. if some word show up more then once it counts as 1 on counter
    :rtype: int
    """
    # return count of unique words in list
    # if some word show up more then once it counts as 1 on counter
    letter_list = []
    count = 0
    for word in data_list:
        if word not in letter_list:
            count += 1
            letter_list.append(word)
    
    return count

def choose_word(file_path, index):
    """
    :param file_path: path to file with secret words, splitted with spaces
    :param index: index to choose from file_path
    :type file_path: string
    :type index: int
    :return: secret word from file_path in index index
    :rtype: string
    """

    file = open(file_path, "r")
    data = file.read()
    # split data words to list
    data_list = data.split(" ")
    # if user choosed index higher then the amount of words in file
    if (index > len(data_list)):
        index = index % len(data_list)
    # user's input index starts at 1 - len(data_list) instead of 0 - (len(data_list) - 1)
    secret_word = data_list[index-1]
    
    file.close()
    
    num_of_words = count_words_in_list(data_list)
    
    return (secret_word)
    
    
def is_english_chars(strg, search=re.compile(r'[^a-z]').search): 
    # return true if there is chars in this string that are not english chars
    return not bool(search(strg))

def is_valid_input(letter_guessed):
    """
    :param letter_guessed: user's letter input guessed
    :type letter_guessed: string
    :return: whether if letter_guessed is valid
    :rtype: boolean
    """
    # return true if chars count = 1 and char is english
    letter_guessed = letter_guessed.lower()
    
    if len(letter_guessed) == 1 and is_english_chars(letter_guessed):
        return True
    return False
        
def check_valid_input(letter_guessed):
    """
    :param letter_guessed: user's letter input guessed
    :type letter_guessed: string
    :return: whether if letter_guessed is valid
    :rtype: boolean
    """
    #check if input is just 1 english letter , if no return false
    #check if input exists in old_letters_guessed, if yes return false
    letter_guessed = letter_guessed.lower()
    valid_input = is_valid_input(letter_guessed)
    if valid_input == False:
        return False
     
    return True
        
def try_update_letter_guessed(letter_guessed, old_letters_guessed, secret_word):
    """
    :param letter_guessed: user's letter input guessed
    :param old_letters_guessed: collected list of all letter guessed
    :param secret_word: complete secret word to guess
    :type letter_guessed: string
    :type old_letters_guessed: list
    :type secret_word: string
    :return: whether if old_letters_guessed is updated with letter_guessed
    :rtype: boolean
    """
    #update letter guesses to old_letters_guessed
    #return true if updated successfully
    letter_guessed = letter_guessed.lower()
    if letter_guessed in old_letters_guessed:
        return False
        
    if not is_valid_input(letter_guessed):
        return False
        
    if letter_guessed not in secret_word:
        return False
        
    old_letters_guessed.append(letter_guessed)
    return True

def is_letter_in_old_letter_guessed(letter_guessed, old_letters_guessed):
    """
    :param letter_guessed: user's letter input guessed
    :param old_letters_guessed: collected list of all letter guessed
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: whether if letter_guessed is already in old_letters_guessed
    :rtype: boolean
    """
    if letter_guessed in old_letters_guessed:
        return True
        
    return False

def print_hangman(num_of_tries):
    """
    :param num_of_tries: number of user's tries to guess letter in secret_word
    :type num_of_tries: int
    :return: NONE. print the currect ASCII ART depends on num_of_tries
    """
    # print the correct image depending on num_of_tries
    if num_of_tries == 0:
        print_photo_0()
    elif num_of_tries == 1:
        print_photo_1()
    elif num_of_tries == 2:
        print_photo_2()
    elif num_of_tries == 3:
        print_photo_3()
    elif num_of_tries == 4:
        print_photo_4()
    elif num_of_tries == 5:
        print_photo_5()
    elif num_of_tries == 6:
        print_photo_6()    


def main():
    MAX_TRIES = 6

    print_opening()

    file_path = r"C:\Users\User\Desktop\Python\hangman\hangman_game\secret_animals.txt"
    print(Fore.GREEN + f"Enter word index in file: ", end='')
    index = int(input())
    
    secret_word = choose_word(file_path, index)
    old_letters_guessed = []
    
    print (Fore.CYAN + "\nLet's start!")

    print(Fore.YELLOW + show_hidden_word(secret_word, old_letters_guessed))
    
    num_of_tries = 0
    while num_of_tries < MAX_TRIES:
        print ("\n")
        print(Fore.MAGENTA + "Guess a letter: ", end='')
        letter_guessed = input()
        # check if letter_guessed is valid
        is_valid = check_valid_input(letter_guessed)
        # if not: dont count this run (num_of_tries remain the same)
        if is_valid == False:
            print(Back.RED + "X\n")
            print(Fore.YELLOW + show_hidden_word(secret_word, old_letters_guessed))
            continue
        # try update old_letters_guessed with letter_guessed
        succeeded = try_update_letter_guessed(letter_guessed, old_letters_guessed, secret_word)
        # if succeeded (means that letter_guessed is currect in secret_word)
        if succeeded == True:
            # print hidden word
            print(Fore.YELLOW + show_hidden_word(secret_word, old_letters_guessed))
            # check if win
            win = check_win(secret_word, old_letters_guessed)
            # if win
            if win == True:
                print(Fore.GREEN + "WIN")
                return
            # succeeded but not win continue (num_of_tries remain the same) 
            continue
        # if not succeeded 
        if succeeded == False:
            
            
            

            # check whether letter_guessed is already in old_letters_guessed
            is_letter_in_list = is_letter_in_old_letter_guessed(letter_guessed, old_letters_guessed)
            if is_letter_in_list == True:
                print(Back.RED + "X\n")
                print(Fore.YELLOW + show_hidden_word(secret_word, old_letters_guessed))
                print(*sorted(old_letters_guessed), sep = " -> ")
                continue
            else:
                print(Fore.GREEN + ":(\n")
                #raise user's guesses in 1
                num_of_tries += 1
                print_hangman(num_of_tries)
                
                old_letters_guessed.append(letter_guessed)
                print(Fore.YELLOW + show_hidden_word(secret_word, old_letters_guessed))
                print(*sorted(old_letters_guessed), sep = " -> ")
                
        # raise user num_of_tries in 1
        
        
    # if loop ended, means user lost   
    print(Fore.RED + "LOSE")
            
        
           
    
if __name__ == "__main__":
    main()




