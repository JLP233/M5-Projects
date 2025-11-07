from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
from stack import Stack

OPERATORS = {"+", "-", "*", "/"}

@dataclass
class TreeNode:
    value: str
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None

class BinaryExpressionTree:
    "ADT Per Spec: Build from Postfix then Evaluate; Infix and Postfix Traversals."
    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    # Core operations
    def is_empty(self) -> bool:
        return self.root is None

    def clear_tree(self) -> None:
        self.root = None

    def build_from_postfix(self, postfix: str) -> None:
        if postfix is None:
            raise ValueError("Postfix Expression is None")
        stk = Stack()
        tokens = [t for t in postfix.split() if t]
        for tok in tokens:
            if tok in OPERATORS:
                # need two operands
                if stk.is_empty():
                    raise ValueError("Too Few Operands Before Operator '{}'".format(tok))
                right = stk.pop()
                if stk.is_empty():
                    raise ValueError("Too Few Operands Before Operator '{}'".format(tok))
                left = stk.pop()
                node = TreeNode(tok, left, right)
                stk.push(node)
            else:
                # number?
                try:
                    float(tok)  # validate
                except ValueError:
                    raise ValueError(f"Invalid Token: {tok!r}")
                stk.push(TreeNode(tok))
        if stk.is_empty():
            raise ValueError("Empty Expression")
        self.root = stk.pop()
        if not stk.is_empty():
            raise ValueError("Additional nused Tokens Left in Stack; Invalid Postfix")

    def evaluate_tree(self) -> float:
        if self.root is None:
            raise ValueError("Tree is Empty")
        return float(self._evaluate(self.root))

    def infix_traversal(self) -> str:
        if self.root is None:
            raise ValueError("Tree is Empty")
        out: List[str] = []
        self._inorder(self.root, out)
        return "".join(out)

    def postfix_traversal(self) -> str:
        if self.root is None:
            raise ValueError("Tree is Empty")
        out: List[str] = []
        self._postorder(self.root, out)
        return " ".join(out)

    
