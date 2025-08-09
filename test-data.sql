CREATE TABLE bookmark (
        bid INTEGER NOT NULL,
        url VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        description VARCHAR NOT NULL,
        date_created DATETIME NOT NULL,
        PRIMARY KEY (bid)
);

CREATE TABLE tag (
        tid INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        bkm_id INTEGER NOT NULL,
        PRIMARY KEY (tid),
        FOREIGN KEY(bkm_id) REFERENCES bookmark (id)
);


insert into bookmark (url, title, description, date_created) values 
        ("https://mhhollomon.github.io/RachGen/", "RachGen",
        'A browser based random chord generator. It knows about scales and is highly configurable. At the end you can export MIDI or MusicXML to import into your favorite DAW or notation software.', 
        current_timestamp);
insert into tag (name, bkm_id) values('tonaldrift', (select bid from bookmark where title = 'RachGen'));
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'RachGen'));
insert into tag (name, bkm_id) values('midi', (select bid from bookmark where title = 'RachGen'));
insert into tag (name, bkm_id) values('musicxml', (select bid from bookmark where title = 'RachGen'));

insert into bookmark (url, title, description, date_created) values ('https://8notes.com/', '8notes', 
        'Sheet music - free. Classical works.', 
        current_timestamp);

insert into tag (name, bkm_id) values('sheet-music', (select bid from bookmark where title = '8notes'));
insert into tag (name, bkm_id) values('classical', (select bid from bookmark where title = '8notes'));

insert into bookmark (url, title, description, date_created) values 
        ("https://mhhollomon.github.io/cf-gen/", "Cantus Fortuitus",
        'A browser based random cantus firmus generator. Useful for counter point practice. Has the ability to generate a MIDI file for use in your DAW or notation software.', 
        current_timestamp);

insert into tag (name, bkm_id) values('tonaldrift', (select bid from bookmark where title = 'Cantus Fortuitus'));
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Cantus Fortuitus'));
insert into tag (name, bkm_id) values('counter-point', (select bid from bookmark where title = 'Cantus Fortuitus'));


insert into bookmark (url, title, description, date_created) values 
        ("https://www.wqxr.org/story/essential-women-composers/", "Women Composers",
        'A "starter" list of women composers and pointers to recordings of their music. Ranges from Early-Baroque to 21st Century.', 
        current_timestamp);
insert into tag (name, bkm_id) values('woman', (select bid from bookmark where title = 'Women Composers'));
insert into tag (name, bkm_id) values('composer', (select bid from bookmark where title = 'Women Composers'));

insert into bookmark (url, title, description, date_created) values 
        ("https://viva.pressbooks.pub/openmusictheory/", "Open Source Music Theory Textbook",
        'A complete textbook for a beginning music theory class. Also includes the cantus fermi from "Gradus and Parnassum" to help with counterpoint exercises.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Open Source Music Theory Textbook'));
insert into tag (name, bkm_id) values('textbook', (select bid from bookmark where title = 'Open Source Music Theory Textbook'));
insert into tag (name, bkm_id) values('counter-point', (select bid from bookmark where title = 'Open Source Music Theory Textbook'));
insert into tag (name, bkm_id) values('beginner', (select bid from bookmark where title = 'Open Source Music Theory Textbook'));

insert into bookmark (url, title, description, date_created) values 
        ("https://musictheory.pugetsound.edu/mt21c/MusicTheory.html", "Music Theory for the 21st-Century Classroom",
        'A complete textbook for a beginning music theory class. Includes exercises.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Music Theory for the 21st-Century Classroom'));
insert into tag (name, bkm_id) values('textbook', (select bid from bookmark where title = 'Music Theory for the 21st-Century Classroom'));
insert into tag (name, bkm_id) values('beginner', (select bid from bookmark where title = 'Music Theory for the 21st-Century Classroom'));

insert into bookmark (url, title, description, date_created) values 
        ("https://www.youtube.com/@SethMonahan/videos", "Seth Monahan Videos",
        'A collection of excellent videos on Common Practice Era Harmony and Counterpoint. Dr Monahan is an associate Professor of Analysis at the Yale School of Music.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Seth Monahan Videos'));
insert into tag (name, bkm_id) values('counter-point', (select bid from bookmark where title = 'Seth Monahan Videos'));
insert into tag (name, bkm_id) values('beginner', (select bid from bookmark where title = 'Seth Monahan Videos'));
insert into tag (name, bkm_id) values('advanced', (select bid from bookmark where title = 'Seth Monahan Videos'));
insert into tag (name, bkm_id) values('video', (select bid from bookmark where title = 'Seth Monahan Videos'));
insert into tag (name, bkm_id) values('youtube', (select bid from bookmark where title = 'Seth Monahan Videos'));

insert into bookmark (url, title, description, date_created) values 
        ("https://www.youtube.com/playlist?list=PL6Towqbh0pdpxUL5NlGTOW2hwVVo1IhdQ", "Jacob Gran Tonal Counterpoint Videos",
        'An introduction to counterpoint by Dr Jacob Gran. This is a very hands-on series. There are several follow on series that go deeper into fugues and the like.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));
insert into tag (name, bkm_id) values('counter-point', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));
insert into tag (name, bkm_id) values('beginner', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));
insert into tag (name, bkm_id) values('advanced', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));
insert into tag (name, bkm_id) values('video', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));
insert into tag (name, bkm_id) values('youtube', (select bid from bookmark where title = 'Jacob Gran Tonal Counterpoint Videos'));

insert into bookmark (url, title, description, date_created) values 
        ("https://www.youtube.com/@EarlyMusicSources", "Early Music Sources.com Youtube",
        'Really great resources for 17th and 18th century music theory, etc. Be sure to checkout the companion website <a href="https://www.earlymusicsources.com/">Early Music Sources</a>.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Early Music Sources.com Youtube'));
insert into tag (name, bkm_id) values('counter-point', (select bid from bookmark where title = 'Early Music Sources.com Youtube'));
insert into tag (name, bkm_id) values('early-music', (select bid from bookmark where title = 'Early Music Sources.com Youtube'));
insert into tag (name, bkm_id) values('video', (select bid from bookmark where title = 'Early Music Sources.com Youtube'));
insert into tag (name, bkm_id) values('youtube', (select bid from bookmark where title = 'Early Music Sources.com Youtube'));

insert into bookmark (url, title, description, date_created) values 
        ("https://www.w3.org/2021/06/musicxml40/", "MusicXML W3C info",
        'Official information on the MusicXML format', 
        current_timestamp);
insert into tag (name, bkm_id) values('coding', (select bid from bookmark where title = 'MusicXML W3C info'));
insert into tag (name, bkm_id) values('musicxml', (select bid from bookmark where title = 'MusicXML W3C info'));-

insert into bookmark (url, title, description, date_created) values 
        ("https://lotusmusic.com/", "Lotus Music Theory Page",
        'Nice site with a bunch of theory content.', 
        current_timestamp);
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Lotus Music Theory Page'));

insert into bookmark (url, title, description, date_created) values 
        ("https://www.pianobook.co.uk/", "Pianobook",
        'Lots of free, high quality sample packs to use in any DAW. The packs are not just samples, 
      but instruments for either Kontakt (full version, not the free player) or 
      <a href="https://www.decentsamples.com/product/decent-sampler-plugin/">Decent Sampler</a>, which is free.', 
        current_timestamp);
insert into tag (name, bkm_id) values('samples', (select bid from bookmark where title = 'Pianobook'));
insert into tag (name, bkm_id) values('vst', (select bid from bookmark where title = 'Pianobook'));
insert into tag (name, bkm_id) values('production', (select bid from bookmark where title = 'Pianobook'));

insert into bookmark (url, title, description, date_created) values 
        ("https://sound-effects.bbcrewind.co.uk/", "BBC Sound Effects Library",
        '33,000 sound effects from the BBC along with a mixer to allow you
      to layer the sounds.', 
        current_timestamp);
insert into tag (name, bkm_id) values('samples', (select bid from bookmark where title = 'BBC Sound Effects Library'));
insert into tag (name, bkm_id) values('production', (select bid from bookmark where title = 'BBC Sound Effects Library'));

insert into bookmark (url, title, description, date_created) values 
        ("http://midi.teragonaudio.com/progs/software.htm", "Teragon Audio Midi Page",
        'Some helpful, if dated, applications for working with MIDI (Windows Only)', 
        current_timestamp);
insert into tag (name, bkm_id) values('midi', (select bid from bookmark where title = 'Teragon Audio Midi Page'));
insert into tag (name, bkm_id) values('coding', (select bid from bookmark where title = 'Teragon Audio Midi Page'));
insert into tag (name, bkm_id) values('software', (select bid from bookmark where title = 'Teragon Audio Midi Page'));

insert into bookmark (url, title, description, date_created) values 
        ("https://mhhollomon.github.io/MusicStuff/", "Musical Miscellany",
        "Some Music Theory tools I have created - 
      including a tool to help you learn Dr. Monahan's Big18 chords", 
        current_timestamp);

insert into tag (name, bkm_id) values('tonaldrift', (select bid from bookmark where title = 'Musical Miscellany'));
insert into tag (name, bkm_id) values('music-theory', (select bid from bookmark where title = 'Musical Miscellany'));


update bookmark set url="https://mhhollomon.github.io/cf-gen/" where title = "Cantus Fortuitus";