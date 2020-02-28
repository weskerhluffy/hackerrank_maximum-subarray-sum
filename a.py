#!/bin/python3
'''
Created on Feb 27, 2020

@author: ernesto
'''

# XXX: https://www.hackerrank.com/challenges/maximum-subarray-sum/problem?h_l=interview&playlist_slugs%5B%5D=interview-preparation-kit&playlist_slugs%5B%5D=search

import math
import os
import random
import re
import sys
import logging
from functools import partial


class TreeNode(object): 

    def __init__(self, key): 
        self.key = key 
        self.left = None
        self.right = None
        self.height = 1


class AVL_Tree(object): 

    def insertNode(self, root, key): 
        
        if not root: 
            return TreeNode(key) 
        elif key < root.key: 
            root.left = self.insertNode(root.left, key) 
        else: 
            if key > root.key:
                root.right = self.insertNode(root.right, key) 
            else:
                # TODO: Actualizar valor
                return root

        root.height = 1 + max(self.getHeight(root.left),
                        self.getHeight(root.right)) 
 
        balanceFactor = self.getBalance(root) 

        if balanceFactor > 1:
            if key < root.left.key: 
                return self.rightRotate(root) 
            else:
                root.left = self.leftRotate(root.left) 
                return self.rightRotate(root)
        
        if balanceFactor < -1:
            if key > root.right.key: 
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right) 
                return self.leftRotate(root)
            
        return root 

    def delete(self, root, key): 

        if not root: 
            return root 

        elif key < root.key: 
            root.left = self.delete(root.left, key) 

        elif key > root.key: 
            root.right = self.delete(root.right, key) 

        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 

            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 

            temp = self.getMinValueNode(root.right) 
            root.key = temp.key 
            root.right = self.delete(root.right,
                                    temp.key) 

        if root is None: 
            return root 

        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right)) 

        balanceFactor = self.getBalance(root) 

        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0: 
                return self.rightRotate(root) 
            else:
                root.left = self.leftRotate(root.left) 
                return self.rightRotate(root) 

        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0: 
                return self.leftRotate(root) 
            else:
                root.right = self.rightRotate(root.right) 
                return self.leftRotate(root)

        return root 

    def leftRotate(self, z): 

        y = z.right 
        T2 = y.left 

        y.left = z 
        z.right = T2 

        z.height = 1 + max(self.getHeight(z.left),
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right)) 

        return y 

    def rightRotate(self, z): 

        y = z.left 
        T3 = y.right 

        y.right = z 
        z.left = T3 

        z.height = 1 + max(self.getHeight(z.left),
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right)) 

        return y 

    def getHeight(self, root): 
        if not root: 
            return 0

        return root.height 

    def getBalance(self, root): 
        if not root: 
            return 0

        return self.getHeight(root.left) - self.getHeight(root.right) 

    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 

        return self.getMinValueNode(root.left) 

    def preOrder(self, root): 

        if not root: 
            return

        logger.debug("{0} ".format(root.key), end="") 
        self.preOrder(root.left) 
        self.preOrder(root.right) 
    
    def find_ge(self, root, key):
        if not root: 
            return root 

        cur = root
        last = None
        
        while cur:
            if key < cur.key:
                last = cur
                cur = cur.left
            else:
                if key > cur.key:
                    cur = cur.right
                else:
                    return cur.key
        
        return last.key if last else None
        

def maximumSum(a, m):
    logger.debug("a {} m {}".format(a, m))
    suma_mod = partial(lambda m, a, b:(a % m + b % m) % m, m)
    resta_mod = partial(lambda m, a, b:(a % m - b % m) % m, m)

    ord_set = AVL_Tree()
    raiz = None
    acum = 0
    r = 0
    for n in a:
        acum = suma_mod(acum, n)
        sig = ord_set.find_ge(raiz, acum)
        if sig:
            optim = resta_mod(acum, sig)
            if optim > r:
                r = optim
        else:
            r = acum
        raiz = ord_set.insertNode(raiz, acum)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  %(levelname)-10s %function(processName)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(name)s %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())

    for q_itr in range(q):
        nm = input().split()

        n = int(nm[0])

        m = int(nm[1])

        a = list(map(int, input().rstrip().split()))

        result = maximumSum(a, m)

        fptr.write(str(result) + '\n')

    fptr.close()
