-- UDF Schema - Phase One
-- The first version is just proof-of-concept that functional code can live comfortably in a database.

create table version( version );
insert into version (version) values ('0.0.1');

create table kind (
    kind text not null primary key
);
insert into kind (kind) values ('formula'), ('record'), ('union'), ('text'), ('template');

create table symbol (
	name text not null PRIMARY KEY,
	kind text not null references kind(kind),
	parameters text null,
	body text null,
	comment text
);

create table typecase ( -- for functions and processes
    symbol text not null references symbol(name),
    ordinal int not null,
    typecase text not null,
    guard text null,
	body text null,
	comment text,
	primary key (symbol, ordinal)
);

create table constructor ( -- for union-types
    symbol text not null references symbol(name),
    tag text not null,
	parameters text null,
	comment text,
	primary key (symbol, tag)
);

insert into symbol (name, kind, parameters, body, comment) values
-- Simple example function(s)
('quadratic', 'formula', 'a b c', 'pair(hi:quad_1(m:1)(@), lo:quad_1(m:-1)(@))', 'Both roots of a quadratic expression.'),
('quad_1', 'formula', 'a b c m', '(-b + m*sqrt(b^2 - 4*a*c))/(2*a)', 'One root of a quadratic expression.'),
-- Sample record type
('pair', 'record', 'hi lo', null, 'A simple sample product type.'),
-- Example list:
('list', 'union', null, null, 'The standard elementary linked list.')
-- Standard list functions:
('map', 'formula', 'fn xs', 'empty', 'Standard list map.')
('fold', 'formula', 'fn xs a', 'empty', 'Standard list fold/reduce.')
('take', 'formula', 'n xs', 'empty', 'Standard "take" function.')
('filter', 'formula', 'predicate xs', 'empty', 'Standard "filter" function.')
-- Simple example template:
('greet', 'template', null, 'Hello, {who}! Nice to meet you.', 'Sample template.'),
-- Sample long-text, much more than you'd want taking up space in a formula:
('Gettysburg', 'text', null, 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.

But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth.

Abraham Lincoln
November 19, 1863', 'Bliss copy. See https://www.abrahamlincolnonline.org/lincoln/speeches/gettysburg.htm for background.');

insert into constructor(symbol, tag, parameters, comment) values
('list', 'cons', 'head tail', 'Elementary unit of list linkage'),
('list', 'empty', '', 'The nothing, but specifically for lists');

insert into typecase (symbol, ordinal, typecase, guard, body, comment) values
('map', 1, 'xs:cons', null, 'cons(head:fn(xs.head), tail:map(@fn, xs:xs.tail))', 'recursive case'),
('fold', 1, 'xs:cons', null, 'fold(@fn, xs:xs.tail, a:fn(@a, b:xs.head))', 'recursive case'),
('take', 1, 'xs:cons', 'n>0', 'cons(head:xs.head, tail:take(xs:xs.tail, n:n-1))', 'recursive case'),
('filter', 1, 'xs:cons', 'predicate(xs.head)', 'cons(head:xs.head, tail:filter(xs:xs.tail, @predicate))', 'keep-case'),
('filter', 2, 'xs:cons', null, 'filter(xs:xs.tail, @predicate)', 'drop-case');

