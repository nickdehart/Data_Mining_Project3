"""
Nicholas DeHart
njd12b
Assignment 3 Data Mining
Using python 2.7.6 on Ubuntu 14.04 LTS
"""

import sys

class dataset():
    def __init__(self, dataset):
        self.dataset = dataset
        self.records = []
        self.largest_index = 0
        self.num_plus = 0
        self.num_minus = 0
        self.plus_probability = 0.0
        self.minus_probability = 0.0
        self.plus_attributes = [{}, {}, {}, {}, {}]
        self.minus_attributes = [{}, {}, {}, {}, {}]
        self.setup()

    def setup(self):
        for line in self.dataset:
            self.records.append(record(self, line.strip()))
        self.plus_probability = float(self.num_plus) / float(self.num_plus + self.num_minus)
        self.minus_probability = float(self.num_minus) / float(self.num_plus + self.num_minus)
        for each in self.records:
            for i in range(self.largest_index):
                if each.data.has_key(i):
                    continue
                else:
                    each.data[i] = 0
                    if each.label == "+1":
                        if self.plus_attributes[i].has_key(0):
                            self.plus_attributes[i][0] += 1
                        else:
                            self.plus_attributes[i][0] = 1
                    else:
                        if self.minus_attributes[i].has_key(0):
                            self.minus_attributes[i][0] += 1
                        else:
                            self.minus_attributes[i][0] = 1

class record():
    def __init__(self, parent, line):
        self.label = ""
        self.line = line
        self.data = {}
        self.setup(parent)

    def setup(self, parent):
        self.label = self.line[0:2]
        if self.label == "+1":
            parent.num_plus = parent.num_plus + 1
        else: parent.num_minus = parent.num_minus + 1
        self.line = self.line[2:]
        key = ""
        for i in range(len(self.line)):
            """grab a one digit key"""
            if i != (len(self.line)-1):
                if self.line[i+1] == ":":
                    key = self.line[i]
                    if int(key) > parent.largest_index:
                        parent.largest_index = int(key)
            """grab a two digit key"""
            if i < (len(self.line)-2):
                if (self.line[i] != " ") and (self.line[i+2] == ":"):
                    key = self.line[i] + self.line[i+1]
                    if int(key) > parent.largest_index:
                        parent.largest_index = int(key)
                    i = i + 1
            """grab a two digit value"""
            if (i != (len(self.line)-1)):
                if ((self.line[i-1] == ":") and (self.line[i+1] != " ")):
                    self.data[int(key)] = int(self.line[i] + self.line[i+1])
                    i = i + 1
                    value = self.data[int(key)]
                    if self.label == "+1":
                        index_list = parent.plus_attributes
                        if len(index_list) > int(key):
                            if index_list[int(key)].has_key(value):
                                index_list[int(key)][value] += 1
                            else:
                                index_list[int(key)][value] = 1
                        else:
                            while len(index_list) <= int(key):
                                index_list.append({})
                            if index_list[int(key)].has_key(value):
                                index_list[int(key)][value] += 1
                            else:
                                index_list[int(key)][value] = 1
                    else:
                        index_list = parent.minus_attributes
                        if len(index_list) > int(key):
                            if index_list[int(key)].has_key(value):
                                index_list[int(key)][value] += 1
                            else:
                                index_list[int(key)][value] = 1
                        else:
                            while len(index_list) <= int(key):
                                index_list.append({})
                            if index_list[int(key)].has_key(value):
                                index_list[int(key)][value] += 1
                            else:
                                index_list[int(key)][value] = 1
            """grab a one digit value"""
            if self.line[i-1] == ":":
                self.data[int(key)] = int(self.line[i])
                value = self.data[int(key)]
                if self.label == "+1":
                    index_list = parent.plus_attributes
                    if len(index_list) > int(key):
                        if index_list[int(key)].has_key(value):
                            index_list[int(key)][value] += 1
                        else:
                            index_list[int(key)][value] = 1
                    else:
                        while len(index_list) <= int(key):
                            index_list.append({})
                        if index_list[int(key)].has_key(value):
                            index_list[int(key)][value] += 1
                        else:
                            index_list[int(key)][value] = 1
                else:
                    index_list = parent.minus_attributes
                    if len(index_list) > int(key):
                        if index_list[int(key)].has_key(value):
                            index_list[int(key)][value] += 1
                        else:
                            index_list[int(key)][value] = 1
                    else:
                        while len(index_list) <= int(key):
                            index_list.append({})
                        if index_list[int(key)].has_key(value):
                            index_list[int(key)][value] += 1
                        else:
                            index_list[int(key)][value] = 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Error: Incorrect number of command line arguments."
        print "Usage: python assignment3DM.py training_file testing_file"
        exit(0)
    with open(sys.argv[1]) as file:
        training = file.readlines()
    training_set = dataset(training)
    with open(sys.argv[2]) as f:
        testing = f.readlines()
    testing_set = dataset(testing)
    true_positive = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    plus_probability = 0.0
    minus_probability = 0.0

    """for each record to be tested"""
    for record in training_set.records:
        """set beginning probability for each"""
        plus_probability = 0.0
        minus_probability = 0.0
        modifier = .01
        """for attribute in each record to be tested"""
        for key in record.data:
            value = record.data[key]
            index_list = training_set.plus_attributes
            if len(index_list) > key:
                if index_list[key].has_key(value):
                    if plus_probability == 0.0:
                        plus_probability = float(index_list[key][value]) / float(training_set.num_plus)
                    else:
                        plus_probability = plus_probability * (float(index_list[key][value]) / float(training_set.num_plus))
                else:
                    if plus_probability == 0.0:
                        plus_probability = modifier
                    else:
                        plus_probability = plus_probability * modifier
            minus_list = training_set.minus_attributes
            if len(minus_list) > key:
                if minus_list[key].has_key(value):
                    if minus_probability == 0.0:
                        minus_probability = float(minus_list[key][value]) / float(training_set.num_minus)
                    else:
                        minus_probability = minus_probability * (float(minus_list[key][value]) / float(training_set.num_minus))
                else:
                    if minus_probability == 0.0:
                        minus_probability = modifier
                    else:
                        minus_probability = minus_probability * modifier

        plus_probability = plus_probability * training_set.plus_probability
        minus_probability = minus_probability * training_set.minus_probability
        """if i predict plus"""
        if plus_probability > minus_probability:
            if record.label == "+1":
                true_positive += 1
            else:
                false_positive += 1
        else:
            if record.label == "-1":
                true_negative += 1
            else:
                false_negative += 1

    print true_positive,
    print " ",
    print false_negative,
    print " ",
    print false_positive,
    print " ",
    print true_negative

    true_positive = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0

    """for each record to be tested"""
    for record in testing_set.records:
        """set beginning probability for each"""
        plus_probability = 0.0
        minus_probability = 0.0
        """for attribute in each record to be tested"""
        for key in record.data:
            value = record.data[key]
            index_list = training_set.plus_attributes
            if len(index_list) > key:
                if index_list[key].has_key(value):
                    if plus_probability == 0.0:
                        plus_probability = float(index_list[key][value]) / float(training_set.num_plus)
                    else:
                        plus_probability = plus_probability * (float(index_list[key][value]) / float(training_set.num_plus))
                else:
                    if plus_probability == 0.0:
                        plus_probability = modifier
                    else:
                        plus_probability = plus_probability * modifier
            minus_list = training_set.minus_attributes
            if len(minus_list) > key:
                if minus_list[key].has_key(value):
                    if minus_probability == 0.0:
                        minus_probability = float(minus_list[key][value]) / float(training_set.num_minus)
                    else:
                        minus_probability = minus_probability * (float(minus_list[key][value]) / float(training_set.num_minus))
                else:
                    if minus_probability == 0.0:
                        minus_probability = modifier
                    else:
                        minus_probability = minus_probability * modifier

        plus_probability = plus_probability * training_set.plus_probability
        minus_probability = minus_probability * training_set.minus_probability
        """if i predict plus"""
        if plus_probability > minus_probability:
            if record.label == "+1":
                true_positive += 1
            else:
                false_positive += 1
        else:
            if record.label == "-1":
                true_negative += 1
            else:
                false_negative += 1

    print true_positive,
    print " ",
    print false_negative,
    print " ",
    print false_positive,
    print " ",
    print true_negative
