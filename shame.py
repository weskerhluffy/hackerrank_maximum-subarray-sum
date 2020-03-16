#!/home/ernesto/programas/instalados/python/python3.8/bin/python3.8
from bisect import insort, bisect_right
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
from functools import partial, reduce
                       
from collections import defaultdict
from bisect import bisect_right
from builtins import set


class TreeNode(object): 

    def __init__(self, key, value): 
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL_Tree(object): 

    def __init__(self):
        self.root = None
    
    def insert(self, key, value):
        self.root = self.insertNode(self.root, key, value)
        
    def insertNode(self, root, key, value): 
        
        if not root: 
            return TreeNode(key, value) 
        elif key < root.key: 
            root.left = self.insertNode(root.left, key, value) 
        else: 
            if key > root.key:
                root.right = self.insertNode(root.right, key, value) 
            else:
                root.value = value
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

    def deleteNode(self, root, key): 

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
            root.value = temp.value
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

        self.preOrder(root.left) 
        logger.debug("{0} ".format(root.key))
        self.preOrder(root.right) 
    
    def find_ge(self, key):
        root = self.root
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
                    return cur.value
        
        return last.value if last else None
    
    def find_gt(self, key):
        root = self.root
        if not root: 
            return root 

        cur = root
        last = None
        
        while cur:
            if key < cur.key:
                last = cur
                cur = cur.left
            else:
                cur = cur.right
        
        return last.value if last else None


class OrderedSet():

    def __init__(self):
        self.arbol = AVL_Tree()
    
    def add(self, key):
        self.arbol.insert(key, key)
    
    def find_gt(self, key):
        return self.arbol.find_gt(key)


def fuerza_bruta(a, m):
    r = 0
    suma_mod = partial(lambda m, x, y:(x % m + y % m) % m, m)
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            st = reduce(suma_mod, a[i:j + 1], 0)
            if st > r:
                r = st
    return r




def maximumSum(a, m):
    # Create prefix tree
    prefix = [0] * len(a)
    curr = 0;
    for i in range(len(a)):
        curr = (a[i] % m + curr) % m
        prefix[i] = curr
    
    # Compute max modsum
    pq = [prefix[0]]
    maxmodsum = max(prefix)
    for i in range(1, len(a)):
        # Find cheapest prefix larger than prefix[i]
        left = bisect_right(pq, prefix[i])
        if left != len(pq):
            # Update maxmodsum if possible
            modsum = (prefix[i]%m - pq[left]%m + m) % m
            maxmodsum = max(maxmodsum, modsum)

        # add current prefix to heap
        insort(pq, prefix[i])

    return maxmodsum


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  %(levelname)-10s %function(processName)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(name)s %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
#    logger.setLevel(logging.ERROR)

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


