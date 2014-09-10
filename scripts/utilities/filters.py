#!/usr/bin/env python
# -*- python -*-

import logging
import logging.handlers

################################################################################
# Filter Class #
################################################################################
 
class Filters():
    """ 
    utility for filter dictionary based on specific attributes
    """

    def __init__(self, logger):
        """initialize the object"""
        self.logger = logger


    def attr_filters(self, data, condition):
        """
        Apply the condition to data and return true in case of matching.
        Expected conditions are like 'attributeName > attributeValue'
        """
        
        if condition is None or len(condition) == 0: return True 
        tuple = condition.split()
        if (len(tuple) != 3):
            self.logger.error("[attr_filters] condition words are %s, they "
                            + "must be 3; condition: %s", str(len(tuple)), \
                            condition)
            exit(1)
        if not tuple[0] in data: return False
        dataVal = self.interpret_string(data[tuple[0]])
        op = tuple[1]
        attValue = self.interpret_string(tuple[2])
        
        # if the two object to compare are not numbers, exit.
        if (dataVal is None or attValue is None):
            self.logger.error("[attr_filters] impossible to compare the two "
                            + "objects, according to the condition: %s", \
                            condition)
            exit(1)
        flag = False
        if (op == '>'):
            if dataVal > attValue:
                flag = True
        elif (op == '<'):
            if dataVal < attValue:
                flag = True
        elif (op == '=='):
            if dataVal == attValue:
                flag = True
        elif (op == '!='):
            if dataVal != attValue:
                flag = True
        elif (op == '>='):
            if dataVal >= attValue:
                flag = True
        elif (op == '<='):
            if dataVal <= attValue:
                flag = True
        else:
            self.logger.error("[attr_filters] wrong operation %s: ", op)
            exit(1)
        
        if flag:
            self.logger.debug("[attr_filters] condition %s is True", condition)
        else:
            self.logger.debug("[attr_filters] condition %s is False", condition)
        return flag
        
    def interpret_string(self, s):
        """try to identify whether a string can be converted to a number"""
        if not isinstance(s, str):
#            self.logger.debug("the object is not a string")
            return None
        if s.isdigit():
#            self.logger.debug("the object %s is an integer", s)
            return int(s)
        try:
#            self.logger.debug("the object %s is a float", s)
            return float(s)
        except:
#            self.logger.debug("the object %s is a string, but not a number", s)
            return None
