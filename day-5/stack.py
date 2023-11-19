#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stack.py
@author Luc Kusters
@date 11-11-2023
"""

import abc


class BaseNode(abc.ABC):

    @abc.abstractproperty
    def value(self):
        pass

    @abc.abstractproperty
    def next(self):
        pass


class NextNodeTypeError(TypeError):
    pass


class Node(BaseNode):

    def __init__(self, value, next_node=None):
        super().__init__()
        self.__value = value
        self.__next = next_node

    @property
    def value(self):
        return self.__value

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next_node: BaseNode):
        if not isinstance(next_node, (Node, type(None))):
            raise NextNodeTypeError(
                "Node.next only allows"
                " setting objects of type"
                f" {type(self).__name__} or None."
                )
        self.__next = next_node

    def __repr__(self):
        return f"Node(value={self.value}, next={self.next})"


class Stack(object):
    """Implements a Stack using a linked list"""

    def __init__(self):
        self.__head = None
        self.__counter: int = 0

    def push(self, value) -> None:
        """Push a value to the stack

        The stack creates a new Node object
        and sets its next_node to the current head.

        The new head is then set to the new node
        """
        new_node = Node(value, next_node=self.__head)
        self.__head = new_node
        self.__counter += 1

    def pop(self) -> Node.value:
        node = self.__head
        if node is not None:
            self.__head = self.__head.next
        self.__counter -= 1
        return node.value

    def head(self) -> Node.value:
        if self.__head is None:
            return None
        return self.__head.value

    def to_list(self):
        out = []
        current = self.__head
        while current is not None:
            out.append(current)
            current = current.next
        return reversed(out)

    def to_tuple(self):
        return tuple(self.to_list())

    def __len__(self):
        return self.__counter

    def __repr__(self):
        return f"Stack{tuple(n.value for n in self.to_list())}"


if __name__ == "__main__":
    # basic node tests
    assert Node(1).value == 1
    assert Node("a").value == "a"
    assert Node("abcdeg1234").value == "abcdeg1234"
    assert Node("abcdeg1234").next == None
    # linked list like tests
    assert isinstance(Node(1, Node(2)), Node)
    assert Node(1, Node(2)).next.value == 2
    assert Node(1, Node(2)).next.next == None
    # setting tests
    try:
        node = Node(1)
        node.next = Node(2)
        assert node.next.value == 2
        node.next = None
    except Exception:
        raise AssertionError("This try except block should"
                             " not raise any exceptions")
    try:
        node = Node(1)
        node.next = "a"
        node.next = 1
        node.next = 1.
        node.next = 1.j
        node.next = 1.j
        raise AssertionError("this try except block should"
                             " raise an exception but"
                             " didn't")
    except NextNodeTypeError:
        pass
    except Exception as e:
        raise AssertionError("this try except block should"
                             " only raise NextNodeTypeError"
                             " but raised the following"
                             f" exception:\n{e}")
    
    # stack tests
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push("c")
    assert stack.pop() == "c"
    assert stack.pop() == 2
    assert stack.pop() == 1
