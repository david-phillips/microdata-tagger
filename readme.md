microdata-tagger
----------------

----

microdata-tagger automatically puts HTML5 Microdata items into your markup.

It does this by reading in a 'lexicon' that maps semantic types to regex patterns.
When a pattern matches your markup, an item of the given type will be created.
The new item will minimally have a 'name' property set to the matched text.

This isn't meant to exhaustively mark your document up with microdata.  It is meant
to automate repetitive annotation tasks.  You'll want a human in the loop.
