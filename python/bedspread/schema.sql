-- UDF Schema - Phase One
-- The first version is just proof-of-concept that functional code can live comfortably in a database.

create table version( version );
insert into version (version) values ('0.0.1');

create table kind (
    kind text not null primary key
);
insert into kind (kind) values ('formula'), ('record'), ('union'), ('text'), ('template');

create table symbol (
    symbol_id integer primary key,
	scope integer null,
	name text not null,
	kind text not null references kind(kind),
	unique (scope, name)
);

create table typecase ( -- for functions and processes
    symbol_id integer not null references symbol(symbol_id),
    ordinal int not null,
    typecase text not null,
    guard text null,
	body text null,
	comment text,
	primary key (symbol, ordinal)
);

create table constructor ( -- for union-types
    symbol_id integer not null references symbol(symbol_id),
    tag text not null,
	parameters text null,
	comment text,
	primary key (symbol, tag)
);

/*
insert into symbol (name, kind, parameters, body, comment) values
-- Sample record type
('pair', 'record', 'hi lo', null, 'A simple sample product type.'),
-- Example list:
('list', 'union', null, null, 'The standard elementary linked list.')
-- Standard list functions:
('map', 'formula', 'fn xs', 'empty', 'Standard list map.')
('fold', 'formula', 'fn xs a', 'empty', 'Standard list fold/reduce.')
('take', 'formula', 'n xs', 'empty', 'Standard "take" function.')
('filter', 'formula', 'predicate xs', 'empty', 'Standard "filter" function.')

insert into constructor(symbol, tag, parameters, comment) values
('list', 'cons', 'head tail', 'Elementary unit of list linkage'),
('list', 'empty', '', 'The nothing, but specifically for lists');

insert into typecase (symbol, ordinal, typecase, guard, body, comment) values
('map', 1, 'xs:cons', null, 'cons(head:fn(xs.head), tail:map(@fn, xs:xs.tail))', 'recursive case'),
('fold', 1, 'xs:cons', null, 'fold(@fn, xs:xs.tail, a:fn(@a, b:xs.head))', 'recursive case'),
('take', 1, 'xs:cons', 'n>0', 'cons(head:xs.head, tail:take(xs:xs.tail, n:n-1))', 'recursive case'),
('filter', 1, 'xs:cons', 'predicate(xs.head)', 'cons(head:xs.head, tail:filter(xs:xs.tail, @predicate))', 'keep-case'),
('filter', 2, 'xs:cons', null, 'filter(xs:xs.tail, @predicate)', 'drop-case');
*/
