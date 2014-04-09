from anki.cards import Card
from anki.hooks import addHook, wrap
from aqt import mw
from anki.sound import play, hasSound
from stardict.stardict import IfoFileReader, IdxFileReader, DictFileReader

ifo_file_lw = "/home/glyme/.goldendict/dicts/lazyworm-ec.ifo"
idx_file_lw = "/home/glyme/.goldendict/dicts/lazyworm-ec.idx"
dict_file_lw = "/home/glyme/.goldendict/dicts/lazyworm-ec.dict"
ifo_reader_lw = IfoFileReader(ifo_file_lw)
idx_reader_lw = IdxFileReader(idx_file_lw)
dict_reader_lw = DictFileReader(dict_file_lw, ifo_reader_lw, idx_reader_lw)

ifo_file_gre = "/home/glyme/.goldendict/dicts/gre-bible.ifo"
idx_file_gre = "/home/glyme/.goldendict/dicts/gre-bible.idx"
dict_file_gre = "/home/glyme/.goldendict/dicts/gre-bible.dict"
ifo_reader_gre = IfoFileReader(ifo_file_gre)
idx_reader_gre = IdxFileReader(idx_file_gre)
dict_reader_gre = DictFileReader(dict_file_gre, ifo_reader_gre, idx_reader_gre)

def get_word(word):
    trans = ''
    gre = dict_reader_gre.get_dict_by_word(word)
    if(gre):
        trans = trans + 'gre:</br>' + gre[0].values()[0] + '</br>'

    lw = dict_reader_lw.get_dict_by_word(word)
    if(lw):
        trans = trans + 'lazyworm:</br>' + lw[0].values()[0]
    return trans

def is_empty_answer(card):
    note = card.note()
    return note.fields[1]==u''

def read():
    q = mw.reviewer.card.note().fields[0]
    if(not hasSound(q)):
        q = './voice/' + q[0] + '/' + q + '.mp3'
        play(q)

def my_a(card):
    if(is_empty_answer(card)):
        return original_a(card) + get_word(mw.reviewer.card.note().fields[0]).decode('utf8').replace('\n','<br/>\n')
    else:
        return original_a(card)

addHook("showQuestion", read)

original_a = Card.a
Card.a = my_a