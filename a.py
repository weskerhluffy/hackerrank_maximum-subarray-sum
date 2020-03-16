#!/home/ernesto/programas/instalados/python/python3.8/bin/python3.8
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
        
        child = TreeNode(key, value)
        if not root: 
            return child
        
        cur = root
        v = []
        
        while cur:
            v.append(cur)
            if key < cur.key: 
                cur = cur.left
            else: 
                if key > cur.key:
                    cur = cur.right
                else:
                    # Actualizar valor si llave ya esta
                    cur.value = value
                    return root
        
        while v:
            cur = v.pop()
            if key < cur.key:
                cur.left = child
            else:
                cur.right = child
            child = self.rebalancea(cur, key)
            

        return child
    
    def rebalancea(self, root, key):
        root.height = 1 + max(self.getHeight(root.left),
                        self.getHeight(root.right)) 
 
        balanceFactor = self.getBalance(root) 

        if balanceFactor > 3:
            if key < root.left.key: 
                return self.rightRotate(root) 
            else:
                root.left = self.leftRotate(root.left) 
                return self.rightRotate(root)
        
        if balanceFactor < -3:
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

    def preOrder(self): 
        return self.preOrderRec(self.root, [])
        
    def preOrderRec(self, root, res): 

        if not root: 
            return res

        return self.preOrderRec(root.right, self.preOrderRec(root.left, res) + [root])
    
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

    # XXX: https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    def __iter__(self):
        return iter(self.arbol.preOrder())


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
#    logger.debug("a {} m {}".format(a, m))
    suma_mod = partial(lambda m, x, y:(x % m + y % m) % m, m)
    resta_mod = partial(lambda m, x, y:(x - y + m) % m, m)

    ord_set = OrderedSet()
    unord_set = set()
    acum = 0
    r = 0
    for n in a:
        acum = suma_mod(acum, n)
        logger.debug("acm {}".format(acum))
        sig = ord_set.find_gt(acum)
        optim = acum
        if sig:
            optim = resta_mod(acum, sig)
            logger.debug("optimus {}".format(optim))
        if optim > r:
            r = optim
        if acum not in unord_set:
            ord_set.add(acum)
            unord_set.add(acum)
#            todos = list(map(lambda n:n.key, ord_set))
#            todos_s = sorted(todos)
#            assert todos == todos_s, "esperado {} obtenido {}".format(todos_s, todos)
#        logger.debug("r es {} ord set {}".format(r, list(map(lambda n:n.key, ord_set))))

#    rt=fuerza_bruta(a, m)
#    assert r==rt, "esperado {} real {}".format(r,rt)
    return r


if __name__ == '__main__':
#    logging.basicConfig(format='%(asctime)s  %(levelname)-10s %function(processName)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(name)s %(message)s')
    logging.basicConfig(format='%(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)

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
