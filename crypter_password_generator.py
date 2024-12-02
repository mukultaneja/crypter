# BSD 3-Clause License
# Copyright (c) 2024, mac
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.


import random
import string


class CrypterPasswordGenerator():
    ASCII_LOWER_LETTERS = list(string.ascii_lowercase)
    ASCII_UPPPER_LETTERS = list(string.ascii_uppercase)
    DIGITS = list(string.digits)
    PUNCTUATION = list(string.punctuation)

    @classmethod
    def generate_random_salt(cls, start, end):
        random_number = random.randint(start, end)
        random_salt = list()
        while random_number:
            num = random_number % 10
            num = random.randint(1, 5) if num == 0 else num
            random_salt.append(num)
            random.shuffle(random_salt)
            random_number = random_number // 10
        random.shuffle(random_salt)
        return random_salt

    @classmethod
    def generate_password(cls, chunk_size=4):
        possible_words = [cls.ASCII_LOWER_LETTERS, cls.ASCII_UPPPER_LETTERS, cls.DIGITS, cls.PUNCTUATION]
        random.shuffle(possible_words)
        final_combination = list()
        for index, num in enumerate(cls.generate_random_salt(1111, 5555)):
            for _ in range(num):
                random.shuffle(possible_words[index])
            final_combination += random.sample(possible_words[index], chunk_size)
        random.shuffle(final_combination)
        return ''.join(final_combination)