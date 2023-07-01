"""
Just to see how it would go to try using treelang to represent the parse trees.
This is ... deeply incomplete at the moment.
"""

import json, os.path
from typing import Iterable, Any
from boozetools.macroparse.runtime import TypicalApplication
from boozetools.support.treelang import RankedAlphabet

_automaton_path = os.path.normpath(os.path.join(__file__, "../../bedspread/grammar.automaton"))
with open(_automaton_path, 'rb') as fh:
	_tables = json.load(fh)

class App(TypicalApplication):
	
	def bind_parse_actions(self, each_constructor: Iterable[tuple[Any, set[int]]]):
		return super().bind_parse_actions(each_constructor)
