"""
Module for symbol table(s)

This part is meant to be generic and agnostic to storage formats.
It should represent the static structure of a (potentially large, multi-part) program.

* Nodes are organized into various types with suitable attributes.
* Each node has a parent and is marked one level deeper than its parent, except for a "root" node at level zero.
* Parentage determines visibility: a node can see any immediate child of itself or any ancestor.
* Most nodes have names. In particular, the ancestor of a named node either has a name or is a root.
* Disjoint name-spaces may be done with by prepending a namespace identifier to a name.
* Not every scope has a name.

There must be a built-in scope, an FFI scope, and user scope.

Names can resolve either as static references to a given definition or else as dynamic references to a parameter.
These last are given as a pair of numbers telling how many static links to follow (i.e. relative nesting depth)
and then the offset into the activation record at that depth.
"""
from dataclasses import dataclass
from typing import Union, Optional, NamedTuple

class ParamRef(NamedTuple):
	level: int
	offset: int
	name: str  # In case I decide to look stuff up by name.

@dataclass
class Definition:
	parent: Optional["Definition"]
	symbol_id: int  # Presumably a key into a database
	kind: str  # Tells generally what sort of thing this is.
	level: int
	children: dict[str:Union["Definition", "Parameter"]]
	body: object  # Something to evaluate dynamically, given proper arguments.
	
	def find(self, name:str):
		if name in self.children:
			return self.children[name]
		elif self.parent:
			return self.parent.find(name)
		else:
			return None
		
@dataclass
class Parameter:
	offset: int

@dataclass
class Abstraction:
	parent: Union["Abstraction", Definition]
	level: int
	params: dict[str:Parameter]
	body: object  # Something to evaluate dynamically, given proper arguments.
	
	def find(self, name):
		if name in self.params:
			return self.params[name]
		else:
			return self.parent.find(name)

@dataclass
class Builtin:
	params: dict[str:Parameter]
	body: object

