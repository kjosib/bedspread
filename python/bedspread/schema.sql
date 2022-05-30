-- UDF Schema - Phase One
-- The first version is just proof-of-concept that functional code can live comfortably in a database.

create table version( version );
insert into version (version) values ('0.0.1');

create table kind (
    kind text not null primary key
);
insert into kind (kind) values ('formula'), ('record'), ('text'), ('template');

create table symbol (
	name text not null PRIMARY KEY,
	kind text not null references kind(kind),
	parameters text null,
	body text null,
	comment text
);

insert into symbol (name, kind, parameters, body, comment) values
-- Simple example function
('quadratic', 'formula', 'a b c', '(-b + sqrt(b^2 - 4*a*c))/(2*a)', 'One root of a quadratic expression.'),
-- Simple example type
('cons', 'record', 'head tail', null, 'The standard elementary unit of list linkage.'),
-- Simple example template:
('greet', 'template', null, 'Hello, {who}! Nice to meet you.', 'Sample template.'),
-- Sample long-text, much more than you'd want taking up space in a formula:
('Gettysburg', 'text', null, 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.

But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth.

Abraham Lincoln
November 19, 1863', 'Bliss copy. See https://www.abrahamlincolnonline.org/lincoln/speeches/gettysburg.htm for background.');
