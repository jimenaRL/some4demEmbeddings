issues = {
	'Left': {#aok
			'ca': [r'\besquerra\b',r'\besquerres?\b'],  #catalan
			'en': [r'\bleft\b',r'\bleftists?\b'],
			'es': [r'\bizquierda\b',r'\bzurd[a|o]\b',r'\bizquierdistas?\b'],
			'el': [r'\bαριστερ[α|ά]\b',r'\bαριστερ[ό|ο]φρονας\b'],
			'el-Latn': [r'\barister([á|a]|[ó|o]fronas)\b'],
			'eu': [r'\bezkerretara\b',r'\bezkertiarrak?\b'],  #basque
			'da': [r'\bvenstre(orienteret)?\b'],
			'de': [r'\blink(s|en?)\b'],
			'fi': [r'\bvasemmalle\b',r'\bvasemmistolai(nen|set)\b'],
			'fr': [r'\bgauche\b',r'\bgauchiste?s?\b'],
			'ga': [r'\bchl[e|é]\b',r'\bleftists?\b'],  #irish
			'gl': [r'\besquerd(as?|istas?)\b'],  #galician
			'is': [r'\bvinstri\b'],  #icelandic
			'it': [r'\bsinistra\b'],
			'lv': [r'\bkreis(ais|ie)\b',r'\bkreisi\b'],
			'lb': [r'\bl[e|é]nks?\b'],
			'mt': [r'\b(tax.?)?xellug(in)?\b',r'\bso[ċ|c]jalist(a|i)\b',r'\bkomunist[i|a]\b'],
			'nl': [r'\blinkse?n?\b'],
			'no': [r'\bvenstreorienterte\b'],
			'pl': [r'\blewo\b',r'\blew(icowy|acy)\b'],  #polish
			'pt': [r'\besquerd(istas?|a)\b'],  #portuguese
			'sv': [r'\bvanster\b'],  #swedish
			'sl': [r'\blev(o|i[č|c]ar|i[č|c]arji)\b'],  #slovenian
			'tr': [r'\bayr[i|ı]ld[i|ı]\b',r'\bsolcu(lar)?\b'],  #turkish
	},
	'Right': {  # aok
			'ca': [r'\bdret\b',r'\bdret([à\a]|es)\b'],  # catalan
			'en': [r'\bright\b',r'\brightist\b'],
			'es': [r'\bderech(a|ista)\b'],
			'el': [r'\bσωστ[ά|α]\b',r'\bδεξι[ό|ο]φρων\b',r'\bδεξιο[ί|ι]\b'],
			'el-Latn': [r'\bsost[á\a]\b',r'\bdexi[ó|o]fron\b',r'\bdexio[í|i]\b'],
			'eu': [r'\besku(indarrak?|bidea)\b'],  #basque
			'da': [r'\bh[ø|o]jrefl[ø|o]j?\b',r'\bh[ø|o]jre\b'],
			'de': [r'\brechts?\b',r'\brechte\b',r'\brechtling\b'],
			'fi': [r'\boiken\b',r'\boikeistolai(set|nen)\b'],
			'fr': [r'\bdroite\b',r'\bdroit[è|e]res?\b',r'\bdroitiers?\b'],
			'ga': [r'\bceart\b',r'\bceartaitheoir\b'],  #irish
			'gl': [r'\bdereita\b',r'\bdereitistas?\b'],  #galician
			'is': [r'\bh(æ|a|e|ae)grima(ð|d|dh|ed)ur\b',r'\bh(æ|a|e|ae)gri\b'],  #icelandic
			'it': [r'\bdestra\b'],
			'lv': [r'\blab(i|ais|[ē|e]jais)\b'],
			'lb': [r'\briet(s|ser)\b'],
			'mt': [r'\b(tal.?)?lemin(ista)?\b'],
			'nl': [r'\brechtervleugel\b',r'\brecht\b',r'\brechtsen?\b'],
			'no': [r'\bh[ø|o]yre(ist|ister)?\b'],
			'pl': [r'\bprawicow(cy|iec)\b',r'\bprawica\b',r'\bprawo\b'],  #polish
			'pt': [r'\bdireit(a|istas?)\b'],  #portuguese
			'sv': [r'\bh[ö|o]ger(man|ister)\b',r'\bh[ö|o]gra\b'],  #swedish
			'sl': [r'\bprav\b',r'\bdesni[č|c]ar(ji)?\b'],  #slovenian
			'tr': [r'\bsa[g|ğ]\b',r'\bsa[ğ|g]c[i|ı](lar)?\b'],  #turkish
	},

	'Liberal': {#
			'ca': [r'\bliberals?\b'],  #catalan
			'en': [r'\bliberals?\b'],
			'es': [r'\bliberal(es)?\b'],
			'el': [r'\bφιλελεύθερ(ος|οι|ων)\b'],  #greek
			'el-Latn': [r'\bfilel[é|e]fther(os|i)\b'],  #latinized greek
			'eu': [r'\bliberal(a|ak|en|entzat)\b'],  # basque
			'da': [r'\bliberale?\b'],  #danish
			'de': [r'\bliberale(r|n)?\b'],
			'fi': [r'\bliberaal(i|it|eista|eille)\b'],
			'fr': [r'\blib[e|é]ral(e|aux|s|es)\b'],
			'ga': [r'\bliobr[á|a]l(ach|aithe|acha)\b'],  #irish
			'gl': [r'\bliber(al|ais)\b'],  #galician
			'is': [r'\bfrj[á|a]lslynd(a|ur|ir|um)\b',r'\bfrjálshyggjumenn(irnir)?\b'],
			'it': [r'\bliberal(e|i)\b'],
			'lv': [r'\bliber[ā|a][l|ļ]i(s|em)?\b'],  #latvian
			'lb': [r'\bliberal(en)?\b'],  #luxem
			'mt': [r'\bliberali\b'],  #maltese
			'nl': [r'\bliberalen?\b'],  #dutch
			'no': [r'\bliberale\b'],
			'pl': [r'\blibera[ł|l](owie|[o|ó]w)?\b'],  #polish
			'pt': [r'\blibera(l|ais)\b'],
			'sv': [r'\bliberal(a|er|erna)?\b'],  #swedish
			'sl': [r'\bliberal(ni|ec|ci|cev|ce)\b'],  #slovenian
			'tr': [r'\bliberal(ler|lerin)?\b'],  #turkish
	},
	'Conservative': {#
			'ca': [r'\bconservador(a|s|es)?\b'],  #catalan
			'en': [r'\bconservatives?\b'],
			'es': [r'\bconservador(a|es)?\b'],
			'el': [r'\bσυντηρητικ([ό|o][ς|c]|[ό|o]|ο[ύ|υ][ς|c]|[ώ|ω]ν|ο[ί|ι])\b'],  #greek
			'el-Latn': [r'\bsyntiritik[ó|o]s?\b'],  #latinized greek
			'eu': [r'\bkontserbadore(a|ei|en|ari|entzat|ek)?\b'],  # basque
			'da': [r'\bkonservative?\b'],  #danish
			'de': [r'\bkonservativen?\b'],
			'fi': [r'\bkonservatiiv(i|inen|eille|eista|ille|it|ien)\b'],
			'fr': [r'\bconservat(eur|rice)s?\b'],
			'ga': [r'\bcoime[á|a]da(ch|igh)\b'],  #irish
			'gl': [r'\bconservador(a|es)?\b'],  #galician
			'is': [r'\b[í|i]hald(i[ð|d]|ss[o|ö]m|sins|smenn|inu)\b'],
			'it': [r'\bconservat(rice|ore|ori)\b'],
			'lv': [r'\bkonservat[ī|i]v(s|ais|ajam|ie|ajiem)\b'],  #latvian
			'lb': [r'\bkonservativ(en)?\b'],  #luxem
			'mt': [r'\bkonservattiv(a|i)?\b'],  #maltese
			'nl': [r'\bconservatie(f|ve|ven)\b'],  #dutch
			'no': [r'\bkonservative?\b'],
			'pl': [r'\bkonserwaty(wny|st[o|ó]w|wna|[ś|s]ci|sty)\b'],  #polish
			'pt': [r'\bconservador(a|es)?\b'],
			'sv': [r'\bkonservativa?\b'],  #swedish
			'sl': [r'\bkonservativ(ec|na|cev|ca|ce)\b'],  #slovenian
			'tr': [r'\bmuhafazakar(lar|lara|ların)?\b'],  #turkish
	},
	'LabourUK': {#
			'ca': [r'(?!x)x'],  #catalan
			'en': [r'\blabou?r\b'],
			'es': [r'(?!x)x'],
			'el': [r'(?!x)x'],  #greek
			'el-Latn': [r'(?!x)x'],  #latinized greek
			'eu': [r'(?!x)x'],  # basque
			'da': [r'(?!x)x'],  #danish
			'de': [r'(?!x)x'],
			'fi': [r'(?!x)x'],
			'fr': [r'(?!x)x'],
			'ga': [r'(?!x)x'],  #gaelic
			'gl': [r'(?!x)x'],  #galician
			'is': [r'(?!x)x'],
			'it': [r'(?!x)x'],
			'lv': [r'(?!x)x'],  #latvian
			'lb': [r'(?!x)x'],  #luxem
			'mt': [r'(?!x)x'],  #maltese
			'nl': [r'(?!x)x'],  #dutch
			'no': [r'(?!x)x'],
			'pl': [r'(?!x)x'],  #polish
			'pt': [r'(?!x)x'],
			'sv': [r'(?!x)x'],  #swedish
			'sl': [r'(?!x)x'],  #slovenian
			'tr': [r'(?!x)x'],  #turkish
	},
	'ConservativeUK': {#
			'ca': [r'(?!x)x'],  #catalan
			'en': [r'\btor(y|ies)\b'],
			'es': [r'(?!x)x'],
			'el': [r'(?!x)x'],  #greek
			'el-Latn': [r'(?!x)x'],  #latinized greek
			'eu': [r'(?!x)x'],  # basque
			'da': [r'(?!x)x'],  #danish
			'de': [r'(?!x)x'],
			'fi': [r'(?!x)x'],
			'fr': [r'(?!x)x'],
			'ga': [r'(?!x)x'],  #gaelic
			'gl': [r'(?!x)x'],  #galician
			'is': [r'(?!x)x'],
			'it': [r'(?!x)x'],
			'lv': [r'(?!x)x'],  #latvian
			'lb': [r'(?!x)x'],  #luxem
			'mt': [r'(?!x)x'],  #maltese
			'nl': [r'(?!x)x'],  #dutch
			'no': [r'(?!x)x'],
			'pl': [r'(?!x)x'],  #polish
			'pt': [r'(?!x)x'],
			'sv': [r'(?!x)x'],  #swedish
			'sl': [r'(?!x)x'],  #slovenian
			'tr': [r'(?!x)x'],  #turkish
	},
	'DemocratUS': {#
			'ca': [r'(?!x)x'],  #catalan
			'en': [r'\bdemocrats?\b'],
			'es': [r'(?!x)x'],
			'el': [r'(?!x)x'],  #greek
			'el-Latn': [r'(?!x)x'],  #latinized greek
			'eu': [r'(?!x)x'],  # basque
			'da': [r'(?!x)x'],  #danish
			'de': [r'(?!x)x'],
			'fi': [r'(?!x)x'],
			'fr': [r'(?!x)x'],
			'ga': [r'(?!x)x'],  #gaelic
			'gl': [r'(?!x)x'],  #galician
			'is': [r'(?!x)x'],
			'it': [r'(?!x)x'],
			'lv': [r'(?!x)x'],  #latvian
			'lb': [r'(?!x)x'],  #luxem
			'mt': [r'(?!x)x'],  #maltese
			'nl': [r'(?!x)x'],  #dutch
			'no': [r'(?!x)x'],
			'pl': [r'(?!x)x'],  #polish
			'pt': [r'(?!x)x'],
			'sv': [r'(?!x)x'],  #swedish
			'sl': [r'(?!x)x'],  #slovenian
			'tr': [r'(?!x)x'],  #turkish
	},
	'RepublicanUS': {#
			'ca': [r'(?!x)x'],  #catalan
			'en': [r'\brepublicans?\b'],
			'es': [r'(?!x)x'],
			'el': [r'(?!x)x'],  #greek
			'el-Latn': [r'(?!x)x'],  #latinized greek
			'eu': [r'(?!x)x'],  # basque
			'da': [r'(?!x)x'],  #danish
			'de': [r'(?!x)x'],
			'fi': [r'(?!x)x'],
			'fr': [r'(?!x)x'],
			'ga': [r'(?!x)x'],  #gaelic
			'gl': [r'(?!x)x'],  #galician
			'is': [r'(?!x)x'],
			'it': [r'(?!x)x'],
			'lv': [r'(?!x)x'],  #latvian
			'lb': [r'(?!x)x'],  #luxem
			'mt': [r'(?!x)x'],  #maltese
			'nl': [r'(?!x)x'],  #dutch
			'no': [r'(?!x)x'],
			'pl': [r'(?!x)x'],  #polish
			'pt': [r'(?!x)x'],
			'sv': [r'(?!x)x'],  #swedish
			'sl': [r'(?!x)x'],  #slovenian
			'tr': [r'(?!x)x'],  #turkish
	},
	'Populism': {#
			'ca': [r'\bpopulis(ta|tes|me)\b'],  #catalan
			'en': [r'\bpopulis(t|ts|m)\b'],
			'es': [r'\bpopulis(ta|mo|tas)\b'],
			'el': [r'\bλαϊκισ(τής|τ[έ|ε][ς|c]|μ[ό|o][ς|c]|τικο[ύ|υ]ς|τ[ώ|ω]ν)\b'],  #greek
			'el-Latn': [r'\bla[ï|i]kis(t[í|i]s|t[e|é]s|m[ó|o]s|tiko[u\ú]s|t[o|ó]n)\b'],  #latinized greek
			'eu': [r'\bpopulis(ta|moa|tenak|tentzat|tak)\b'],  # basque
			'da': [r'\bpopulis(ten|ter|me|terne|tiske)\b'],  #danish
			'de': [r'\bpopulis(t|ten|mus|tische)\b'],
			'fi': [r'\bpopulist(i|it|mi|teista|eille|tisia)\b'],
			'fr': [r'\bpopulis(te|tes|me)\b'],
			'ga': [r'\bpopulists?\b',r'\bchoinníonn\b'],  #gaelic
			'gl': [r'\bpopulis(ta|mo|tas)\b'],  #galician
			'is': [r'\bpop[ú|u]l[i|í]s(tinn|tar|ma|tana|sk)\b'],
			'it': [r'\bpopulis(ta|ti|te|mo)\b'],
			'lv': [r'\bpopulis(ts|ti|ms|tiem|tiskie)\b'],  #latvian
			'lb': [r'\bpopulis(tesche|ten|mus|tesch)\b'],  #luxem
			'mt': [r'\bpopulis(ta|ti|)\b',r'\bpopuli[ż|z]mu\b'],  #maltese
			'nl': [r'\bpopulis(tische|ten|me|tische)\b'],  #dutch
			'no': [r'\bpopulis(ten|ter|me|tene|tiske)\b'],
			'pl': [r'\bpopuli[ś|s](ci|ta|t[o|ó]w|tyczne)\b',r'\bpopulizm\b'],  #polish
			'pt': [r'\bpopulis(tas|mo|ta)\b'],
			'sv': [r'\bpopulis(ten|ter|terna|m|tiska)\b'],  #swedish
			'sl': [r'\bpopulis(t|ti|tov|te|ti[č|c]ni)\b'],  #slovenian
			'tr': [r'\bpop[ü|u]li[s|z](t|tler|tlerin)\b'],  #turkish
	},



	'Socialism': {#aok
			'ca': [r'\bsocialis(tas?|me)\b'],  #catalan
			'en': [r'\bsocialis(ts?|m)\b'],
			'es': [r'\bsocialis(tas?|mo)\b'],
			'el': [r'\bσοσιαλιστής\b',r'\bσολιαλισμ[ό|ο]ς\b'],
			'el-Latn': [r'\bsosialis(t[í|i]s|t[é|e]s)\b',r'\bsolialism[ó|o]s\b'],
			'eu': [r'\bsozialis(tak?|moa)\b'],  #basque
			'da': [r'\bsocialis(mo|t|er|en|terne|ter)?\b'],
			'de': [r'\bsozialis(mus|tisch|tinnen|ten)\b'],
			'fi': [r'\bsosialis(mi|tit|tinen)\b'],
			'fr': [r'\bsocialis(me|te?s?)\b'],
			'ga': [r'\bs[ó|o]isiala(ch|igh|chas)\b'],  #irish
			'gl': [r'\bsocialis(mo|tas?)\b'],  #galician
			'is': [r'\bs[o|ó]s[i|í]alis(ti|tar|mi)\b'],  #icelandic
			'it': [r'\bsocialis(mo|ta|ti)\b'],
			'lv': [r'\bsoci[a|ā]lis(ts|ti|ms)\b'],
			'lb': [r'\bsozialis(mus|tesch|ten)\b'],
			'mt': [r'\bso[ċ|c]jalist(a|i)\b'],
			'nl': [r'\bsocialis(me|tisch|ten)\b'],
			'no': [r'\bsocialis(ter|t|me)\b'],
			'pl': [r'\bsocjali(zm|sta|[s|ś]ci)\b'],  #polish
			'pt': [r'\bsocialis(mo|tas?)\b'],  #portuguese
			'sv': [r'\bsocialis(m|tisk|ter)\b'],  #swedish
			'sl': [r'\bsociali(sti|zem|sti[č|c]na)\b'],  #slovenian
			'tr': [r'\bsosyali(zm|st|stler)\b',],  #turkish
	},
	'Communism': {#aok
			'ca': [r'\bcomunis(tas?|me)\b'],  #catalan
			'en': [r'\bcommu?nis(ts?|m)\b'],
			'es': [r'\bcomunis(tas?|mo)\b'],
			'el': [r'\bκομμουνισμ[ό|ο]ς',r'\bκομμουνιστικ[ό|ο]ς\b'],
			'el-Latn': [r'\bkommounis(tik[ó|o]s|m[ó|o]s)\b'],
			'eu': [r'\bkommunis(moa|tak?)\b'],  #basque
			'da': [r'\bkommunis(mo|t|er|en|terne|ter)?\b'],
			'de': [r'\bkomm?unis(mus|tisch|tinnen|ten)\b'],
			'fi': [r'\bkommunis(mi|tit?)\b'],
			'fr': [r'\bcomm?unis(me|te?s?)\b'],
			'ga': [r'\bcomm?unn?a(ch|ithe|chas)\b'],  #irish
			'gl': [r'\bcomunis(mo|tas?)\b'],  #galician
			'is': [r'\bkomm?[u|ú]nis(ti|tar|mi)\b'],  #icelandic
			'it': [r'\bcomunis(mo|ta|ti)\b'],
			'lv': [r'\bkomunis(ts|ti|ms)\b'],
			'lb': [r'\bkommunis(mus|tesch|ten)\b'],
			'mt': [r'\bkomunist[i|a]\b'],
			'nl': [r'\bcomm?unis(me|tisch|ten)\b'],
			'no': [r'\bkomm?unis(ter|tik|me)\b'],
			'pl': [r'\bkomuni[s|ś|z](ci|tyczny|m)\b'],  #polish
			'pt': [r'\bcomunis(mo|tas?)\b'],  #portuguese
			'sv': [r'\bkomm?unis(ter|t|men)\b'],  #swedish
			'sl': [r'\bkomm?uni(izma|sti|sti[č|c]na)\b'],  #slovenian
			'tr': [r'\bkom[ü|u]uni(st|zm|istler)\b'],  #turkish
	},
	'Europe': {
			'ca': [r'\beurop(a|eu|ea|ees|eus)\b',r'\buni[o|ó] europea\b',r'\beurope(istas?|anists?)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #catalan
			'en': [r'\beurop(e|eans?)\b',r'\beuropean union\b',r'\beurope(ists?|anist?m?)\b',r'\be.?u.?\b',r'\bu.?e.?\b',r'\b.*european\b'],
			'es': [r'\beurop(a|eo|ea)s?\b',r'\buni[o|ó]n europea\b',r'\beuropeista\b',r'\b.*europe[o|a]\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'el': [r'\bευρ[ώ|ω]π(α|αϊκ[ό|ο]ς|[ί|ι]στας|α[ί|ι]οι)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'el-Latn': [r'\bevr[ó|ο]p(a|[i|í]stas|a[í|i]oi)\b',r'\bevropaïk[ó|ο]s\b',r'\bevropa[ï|i]k[i|í] [e|é]nosi\b',r'\b#e.?e.?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'eu': [r'\beuropa(rra)?k?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #basque
			'da': [r'\beuropa\b',r'\beurop(æ|a|e|ae|[ä|a]isch)(iske?|re|ere|ist)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'de': [r'\beurop(a|[a|ä]ische?|[a|ä]er|[a|ä]ismus)\b',r'\bunion europa\b',r'\be.?u.?\b',r'\bu.?e.?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'fi': [r'\beuroop(assa|palainen|palaiset)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'fr': [r'\beurop[e|a]\b',r'\beurop[é|e]e?n(n?e)?\b',r'\bunion europeenne\b',r'\beurop[é|e]iste\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'ga': [r'\be[o|ò]rpa(ch|ich)?\b',r'\be.?a.?\b',r'\ba.?e.?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #gaelic
			'gl': [r'\beurop(a|eo|ea)s?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #galician
			'is': [r'\bevr[ó|o]p(u|skt|ub[u|ú]ar)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #icelandic
			'it': [r'\beurop(a|eo|ea|ei|eista)\b',r'\bunione europea\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'lv': [r'\beirop([ā|a]|ie[s|š]u|ie[s|š]i)\b',r'\be.?u.?\b',r'\bu.?e.?\b',r'\be.?s.?\b',r'\bs.?e.?\b'],
			'lb': [r'\beurop[a|ä](esch|er)?\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'mt': [r'\b(l.?)?ewrop(a|ew|ej)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'nl': [r'\beurop(a|ese|eanen)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'no': [r'\beurop(a|eisk|eere)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],
			'pl': [r'\beurop(a|ejski|ejczycy)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #polish
			'pt': [r'\beurop(a|eu|eus)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #portuguese
			'sv': [r'\beuro(a|eisk|[e|é]er)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #swedish
			'sl': [r'\bevrop(i|ski|ejci)\b',r'\be.?u.?\b',r'\bu.?e.?\b'],  #slovenian
			'tr': [r'\bavrupa(lı|li)?(lar)\b',r'\be.?u.?\b',r'\bu.?e.?\b',r'\ba.?b.?\b',r'\bb.?a.?\b'],  #turkish
	},
	'Immigration': {
			'ca': [r'\bimmigracio\b',r'\bimigracio\b',r'\bmigrant\b',r'\bmigrants\b',r'\bimmigrant\b',r'\bimigrant\b'],  #catalan
			'en': [r'\bimmigration\b',r'\bimigration\b',r'\bmigrant\b',r'\bmigrants\b',r'\bimmigrant\b'],
			'es': [r'\binmigracion\b',r'\bmigrante\b',r'\binmigrante\b'],
			'el': [r'\bμετανάστης\b',r'\bμετανάστευση\b',r'\bμετανάστες\b'],
			'el-Latn': [r'\bmetan[á|a]stefsi\b',r'\bmetan[á|a]stis\b',r'\bmetan[á|a]stes\b'],
			'eu': [r'\betorkinak?\b',r'\betorkinak\b',r'\bimmigrazioa\b'],  #basque
			'da': [r'\bindvandr(ing|er)\b',r'\bimmigranten\b'],
			'de': [r'\beinwander(ung|er)\b',r'\b(im)?migration\b',r'\b(im)?migrant(in|en)?\b',r'\bwanderarbeiter\b',r''],
			'fi': [r'\bmaahanmuutt(o|aja)\b'],
			'fr': [r'\bimm?igrante?s?\b',r'\bimm?igrations?\b',r'\bmigrante?s?\b',],
			'ga': [r'\bin-?imriche\b'],  #gaelic
			'gl': [r'\binmigracion\b',r'\bmigrante\b',r'\binmigrante\b'],  #galician
			'is': [r'\binnflytj(enda|andi|andanum)\b'],  #icelandic
			'it': [r'\bimmigrato\b',r'\bimigrato\b',r'\bimmigrata\b',r'\bimigrata\b',r'\bmigrante\b',r'\bmigranti\b',r'\bimmigrati\b',r'\bimigrati\b',r'\bimmigrazione\b',r'\bimigrazione\b'],
			'lv': [r'\bimigr([āc|a]ija|ants|)\b'],
			'lb': [r'\bimmigrat(ioun|ant)\b'],
			'mt': [r'\bl?-?immigra(zzjoni|nt)\b'],
			'nl': [r'\bi?m?migra(tie|ant)\b'],
			'no': [r'\binnvandr(ing|er|eren)\b'],
			'pl': [r'\bimigra(cja|nt)\b'],  #polish
			'pt': [r'\bimigra([ç|c][ã|a]o|nte)\b'],  #portuguese
			'sv': [r'\binnvandr(ing|er|eren)\b'],  #swedish
			'sl': [r'\bpriselje(vanje|nec)\b'],  #slovenian
			'tr': [r'\bgoçmenlik\b',r'\bgoçmen\b'],  #turkish
	},
	'Islam': {
			'ca': [r'\bislam\b',r'\bmusulma\b'],  #catalan
			'en': [r'\bislam\b',r'\bmuslim\b'],
			'es': [r'\bislam\b',r'\bmusulman\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bislam\b',r'\bm[u|o]sl(im|imin|eme?|[i|e]misch)\b'],
			'fi': [],
			'fr': [r'\bislam\b',r'\bmusulman\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bislam\b',r'\bmusulmano\b',r'\bmusulmana\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\bislam\b',r'\bmusulman\b'],  #turkish
	},
	'Environment': {
			'ca': [r'\bentorn\b',r'\becologia\b',r'\becologic\b'],  #catalan
			'en': [r'\benvironment(al)?\b',r'\becology\b',r'\becologic(al?)s?\b'],
			'es': [r'\bmedio ambiente\b',r'\becolog[i|í]a\b',r'\becol[o|ó]gic[o|a]s?\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bumwelt\b',r'\b[ö|o]kolog(ie|isch)\b'],
			'fi': [],
			'fr': [r'\benvironnement\b',r'\benvironement\b',r'\becologie\b',r'\becologique\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bambiente\b',r'\becologia\b',r'\becologico\b',r'\becologica\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\bçevre\b',r'\bekoloji\b',r'\bekolojik\b'],  #turkish
	},
	'Recycling': {
			'ca': [r'\b\b'],  #catalan
			'en': [r'\brecycling\b',r'\brecyclage\b'],
			'es': [r'\breciclage\b',r'\becologia\b',r'\becologic\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\brecycling\b',r'\bwieder(verwer|aufberei)tung\b'],
			'fi': [],
			'fr': [r'\brecyclage\b',r'\brecycler\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bricupero\b',r'\braccolta\b',r'\becologico\b',r'\becologica\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\bgeri d[o|ö]n[u|ü][s|ş]um\b'],  #turkish
	},
	'Crime': {
			'ca': [r'\bdelicte\b',r'\bdelictes\b',r'\bcriminal\b',r'\bcriminals\b'],  #catalan
			'en': [r'\bcrime\b',r'\bcriminal\b'],
			'es': [r'\bcrimen\b',r'\bcriminal\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bkrimin(elle?|alit[ä|a]t)\b',r'\bverbrecher\b',r'\bstraft[ä|a]ter\b'],
			'fi': [],
			'fr': [r'\bcriminalite\b',r'\bcriminel\b',r'\bcriminelle\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bcrimine\b',r'\bcriminale\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\bsuç\b'],  #turkish
	},
	'LifeStyle': {
			'ca': [r'\bgai\b',r'\bgais\b',r'\bhomosexual\b',r'\bhomosexuals\b',r'\bfeminista\b',r'\bfeministas\b','lgbt'],  #catalan
			'en': [r'\bgay\b',r'\bhomosexual\b',r'\bfeminist\b',r'\bfeminists\b',r'\bfeminism\b','lgbt'],
			'es': [r'\bgay\b',r'\bhomosexual\b',r'\bfeminismo\b',r'\bfeminista\b','lgbt'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bschwul\b',r'\blesbisch\b',r'\bhomosexuell\b',r'\bfeminist(ich|in)?\b','lgbt'],
			'fi': [],
			'fr': [r'\bgay\b',r'\bhomosexuel\b',r'\bfeminisme\b',r'\bfeministe\b','lgbt'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bgay\b',r'\bomosessuale\b',r'\bfeminista\b',r'\bfeminismo\b','lgbt'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\beşcinsel\b',r'\bfeminizm\b',r'\bfeminist\b','lgbt'],  #turkish
	},
	'Religion': {
			'ca': [r'\breligio\b',r'\breligions\b',],  #catalan
			'en': [r'\breligion\b',r'\breligions\b',r'\breligious\b',r'\bgod\b'],
			'es': [r'\breligi[o|ó]n\b',r'\breligios(o|a)\b',r'\bdios\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\breligion\b',r'\breligi[ö|o]s\b',r'\bgott\b'],
			'fi': [],
			'fr': [r'\breligion\b',r'\breligieux\b',r'\breligieuse\b',r'\bdieu\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\breligione\b',r'\breligioso\b',r'\breligiosa\b',r'\bdio\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\bdin\b',r'\bdini\b',r'\btanri\b'],  #turkish
	},
	'People': {
			'ca': [r'\bgents?\b',r'\bpobles\b'],  #catalan
			'en': [r'\bpeople\b'],
			'es': [r'\bgentes?\b',r'\bpueblos?\b'],
			'el': [r'\bπ[ό|ο]λ(η|εις)\b'],
			'el-Latn': [r'\bp[o|ó]l(i|eis)\b'],
			'eu': [r'\bherriak?\b'],  #basque
			'da': [r'\bby(er)?\b'],
			'de': [r'\bv[o|ö]lk(es)?\b'],
			'fi': [r'\bkaupun(ki|git)\b'],
			'fr': [r'\bgens\b',r'\bpeuple\b'],
			'ga': [r'\bbailtean\b',r'\bbhaile\b'],  #gaelic
			'gl': [r'\bcidades?\b'],  #galician
			'is': [r'\bb(æ|a|e|ae)(inn|jum)\b'],  #icelandic
			'it': [r'\bpersone\b',r'\bpopolo\b'],
			'lv': [r'\bpils[ē|e]tas?\b'],
			'lb': [r'\bst(ie|a)d\b'],
			'mt': [r'\bbliet\b',r'\bbelt\b'],
			'nl': [r'\bsteden\b',r'\bdorp\b'],
			'no': [r'\bby(er)?\b'],
			'pl': [r'\bmiast[o|a]\b'],  #polish
			'pt': [r'\bcidades?\b'],  #portuguese
			'sv': [r'\bst[ä|a]d(er)?\b'],  #swedish
			'sl': [r'\bmest[o|a]\b'],  #slovenian
			'tr': [r'\binsanlar\b'],  #turkish
	},
	'Elites': {
			'ca': [r'\b[e|é]lit\b',r'\b[e|é]lits\b'],  #catalan
			'en': [r'\b[e|é]lite\b',r'\b[e|é]lites\b'],
			'es': [r'\b[e|é]lite\b',r'\b[e|é]lites\b'],
			'el': [r'\bαφρόκρεμα\b',r'\bελίτ\b'],
			'el-Latn': [r'\bafr[ó|o]krema\b',r'\bel[í|i]t\b'],
			'eu': [r'\beliteak?\b'],  #basque
			'da': [r'\beliter?\b'],
			'de': [r'\beliten?\b'],
			'fi': [r'\beliit(ti|it)\b'],
			'fr': [r'\b[e|é]lites?\b'],
			'ga': [r'\bmionlach\b',r'\belites\b'],  #gaelic
			'gl': [r'\b[e|é]lite\b',r'\b[e|é]lites\b'],  #galician
			'is': [r'\belite\b',r'\bel[í|i]tur\b'],  #icelandic
			'it': [r'\b[e|é]lite\b',r'\b[e|é]lites\b'],
			'lv': [r'\belites?\b'],
			'lb': [r'\beliten?\b'],
			'mt': [r'\belites?\b'],
			'nl': [r'\belites?\b'],
			'no': [r'\beliter?\b'],
			'pl': [r'\belit[a|y]\b'],  #polish
			'pt': [r'\b[e|é]lite\b',r'\b[e|é]lites\b'],  #portuguese
			'sv': [r'\belit(er)\b'],  #swedish
			'sl': [r'\belit[a|e]\b'],  #slovenian
			'tr': [r'\bseçkinler\b'],  #turkish
	},
	'Politicians': {
			'ca': [r'\bpolitic\b',r'\bpolitics\b'],  #catalan
			'en': [r'\bpolitician\b',r'\bpoliticians\b'],
			'es': [r'\bpolitic[o|a]\b',r'\bpolitic[o|a]s\b'],
			'el': [r'\bπολιτικ[οί|ή]\b'],
			'el-Latn': [r'\bpolitiko[í|i]\b'],
			'eu': [r'\bpolitika(riak)?\b'],  #basque
			'da': [r'\bpolitik(ere)?\b'],
			'de': [r'\bpoliti(kers?|kerin|kerinnen)\b'],
			'fi': [r'\bpoli(itikot|tiikka)\b'],
			'fr': [r'\bpoliticien(ne)?\b'],
			'ga': [r'\b(luchd)?-?poileataigs\b'],  #gaelic
			'gl': [r'\bpolitic[o|a]\b',r'\bpolitic[o|a]s\b'],  #galician
			'is': [r'\bp[ó|o]lit[í|i]k\b',r'\bstj[ó|o]rnm[á|a]lamenn\b'],  #icelandic
			'it': [r'\bpolitic[i|o]\b'],
			'lv': [r'\bpolit(ik[ā|a]|iem)\b'],
			'lb': [r'\bpolitik(er)?\b'],
			'mt': [r'\bpoliti([ċ|c]i|kanti|ka)\b'],
			'nl': [r'\bpoliti(ci|ek)\b'],
			'no': [r'\bpolitik(k|ere)\b'],
			'pl': [r'\bpolity(cy|ka)\b'],  #polish
			'pt': [r'\bpolitic[o|a]\b',r'\bpolitic[o|a]s\b'],  #portuguese
			'sv': [r'\bpolitik(er)?\b'],  #swedish
			'sl': [r'\bpolitik[a|i]\b'],  #slovenian
			'tr': [r'\bpolitikacı\b',r'\bpolitikac[ı|i]lar\b'],  #turkish
	},
	'Corruption': {
			'ca': [r'\bcorrupcio\b'],  #catalan
			'en': [r'\bcorrupt(ion)?\b'],
			'es': [r'\bcorrup(ci[o|ó]n|t[o|a]s?)\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bkorrupt(ion)?\b'],
			'fi': [],
			'fr': [r'\bcorruption\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bcorruzione\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [r'\byolsuzluk\b'],  #turkish
	},
	'Negative': {
			'ca': [],  #catalan
			'en': [],
			'es': [],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [],
			'fi': [],
			'fr': ['anti','contre','d[e|é]teste'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Catholicism': {
			'ca': [r'\bsacerdots?\b'],  #catalan
			'en': [r'\bpriests?\b'],
			'es': [r'\bsacerdotes?\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [],
			'fi': [],
			'fr': [],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Patriot': {
			'ca': [r'\bpatriot(a|es)\b'],  #catalan
			'en': [r'\bpatriot(ic|ism)?s?\b'],
			'es': [r'\bpatri[o|ó]t(a|ico)?s?\b'],
			'el': [r'\bπατριώτης\b',r'\bπατριώτες\b'],
			'el-Latn': [r'\bpatriótis\b',r'\bpatriótes\b'],
			'eu': [r'\babertzale\b'],  #basque
			'da': [r'\bpatriot(er)?\b'],
			'de': [r'\bvatansever(lik)?\b'],
			'fi': [r'\bisänmaalli(nen|set)\b'],
			'fr': [r'\bpatriot(ism|ique|e)?s?\b'],
			'ga': [r'\b(fear|luch)?-?(gr[à|a]dhach|d[ù|u]thcha)\b'],  #gaelic
			'gl': [r'\bpatri[o|ó]t(a|ico)?s?\b'],  #galician
			'is': [r'\bföðurlandsvinur\b',r'\bættjarðarástar\b'],  #icelandic
			'it': [r'\bpatriot(a|ico|ica|ici|ismo)\b'],
			'lv': [r'\bpatriot[s|i]\b'],
			'lb': [r'\bpatriot(en)?\b'],
			'mt': [r'\bpatrijotti?\b'],
			'nl': [r'\bpatrio(ten)?\b'],
			'no': [r'\bpatriot(er)?\b'],
			'pl': [r'\bpatrio(ta|ci)\b'],  #polish
			'pt': [r'\bpatri[o|ó]t(a|ico)?s?\b'],  #portuguese
			'sv': [r'\bpatriot(er)?\b'],  #swedish
			'sl': [r'\bdomoljubi?\b'],  #slovenian
			'tr': [r'\bvatansever(ler)?\b'],  #turkish
	},
	'Traditional': {
			'ca': [],  #catalan
			'en': [r'\btradition(al|s)?\b'],
			'es': [r'\btradici[o|ó]n(al|ales|es)\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bgelenek(sel)?\b'],
			'fi': [],
			'fr': [r'\btradition(nel|el|s|elle|nelle)s?\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\btradizion(e|ale)\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Islamophobia': {
			'ca': [],  #catalan
			'en': [r'\bislamophobi(a|c)s?\b'],
			'es': [r'\bislamof[o|ó]bi(a|co|ca)s?\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bIslam(ophobie|feindlich)\b'],
			'fi': [],
			'fr': [r'\bislamophobi(e|ique)s?\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bislamofob(ia|o)\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'International': {
			'ca': [],  #catalan
			'en': [r'\binternational\b'],
			'es': [r'\binternacional\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\binternational\b'],
			'fi': [],
			'fr': [r'\binternationa(l|le|aux)s?\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\binternazional[e|i]\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'StartUp': {
			'ca': [r'\bstart.?ups?\b'],  #catalan
			'en': [r'\bstart.?ups?\b'],
			'es': [r'\bstart.?ups?\b'],
			'el': [r'\bstart.?ups?\b'],
			'el-Latn': [r'\bstart.?ups?\b'],
			'eu': [r'\bstart.?ups?\b'],  #basque
			'da': [r'\bstart.?ups?\b'],
			'de': [r'\bstart.?ups?\b'],
			'fi': [r'\bstart.?ups?\b'],
			'fr': [r'\bstart.?ups?\b'],
			'ga': [r'\bstart.?ups?\b'],  #gaelic
			'gl': [r'\bstart.?ups?\b'],  #galician
			'is': [r'\bstart.?ups?\b'],  #icelandic
			'it': [r'\bstart.?ups?\b'],
			'lv': [r'\bstart.?ups?\b'],
			'lb': [r'\bstart.?ups?\b'],
			'mt': [r'\bstart.?ups?\b'],
			'nl': [r'\bstart.?ups?\b'],
			'no': [r'\bstart.?ups?\b'],
			'pl': [r'\bstart.?ups?\b'],  #polish
			'pt': [r'\bstart.?ups?\b'],  #portuguese
			'sv': [r'\bstart.?ups?\b'],  #swedish
			'sl': [r'\bstart.?ups?\b'],  #slovenian
			'tr': [r'\bstart.?ups?\b'],  #turkish
	},
	'Entrepreneur': {
			'ca': [r'\bemprenedora?\b'],  #catalan
			'en': [r'\bentrepreneurs?\b'],
			'es': [r'\bemprendedor(a|es)?\b'],
			'el': [r'\bεπιχειρηματίας\b'],
			'el-Latn': [r'\bepicheirimatías\b'],
			'eu': [r'\bekintzailea\b'],  #basque
			'da': [r'\biv(æ|ae)rks(æ|ae)tter(en)?\b'],
			'de': [r'\bunternehmer\b',r'\banlaufen\b'],
			'fi': [r'\byritt[ä|a]j[ä|a]\b'],
			'fr': [r'\bentrepreneure?s?\b'],
			'ga': [r'\bneach-?tionnsgain\b'],  #gaelic
			'gl': [r'\bempresario\b',r'\bemprendedora?\b'],  #galician
			'is': [r'\bfrumkvöðull(inn)?\b'],  #icelandic
			'it': [r'\bimprenditor[e|i]\b',r'\bstart.?ups?\b'],
			'lv': [r'\buz[ņ|n][ē|e]m([ē|e]j|[ī|i]g)s\b'],
			'lb': [r'\bentrepreneure?\b'],
			'mt': [r'\bintraprendituri?\b'],
			'nl': [r'\bonderneme(r|nd)\b'],
			'no': [r'\bgr[ü|u]nder\b'],
			'pl': [r'\bprzedsiębiorc(a|zy)\b'],  #polish
			'pt': [r'\bempreendedor\b'],  #portuguese
			'sv': [r'\bentreprenör\b',r'\bföretagsam\b'],  #swedish
			'sl': [r'\bpodjetnik?\b'],  #slovenian
			'tr': [r'\bgiri[ş|s]imci\b'],  #turkish
	},
	'Defense': {
			'ca': [],  #catalan
			'en': [r'\bdefense\b',r'\barmy\b',r'\bnavy\b',r'\bair.?force\b',r'\bmilitary\b'],
			'es': [r'\bdefensa\b',r'\bej[e|é]rcito\b',r'\bmarina\b',r'\baviaci[ó|o]n\b',r'\bfuerza.a[e|é]rea\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bverteidigung\b',r'\bheer\b',r'\bmarine\b',r'\bluftfahrt\b',r'\bluftwaffe\b'],
			'fi': [],
			'fr': [r'\barm[e|é]e\b',r'\bd[e|é]fence\b',r'\baviation\b',r'\bmilitaire\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bdifesa\b',r'\bmilitare\b',r'\bmarina\b',r'\baviazione\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'ClimateChange': {
			'ca': [],  #catalan
			'en': [r'\bclimate change\b',r'\bglobal warming\b'],
			'es': [r'\bcambio clim[á|a]tigoc\b',r'\becalentamiento global\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\b\b'],
			'fi': [],
			'fr': [r'\bchangement climatique\b',r'\br[é|e]chauffement climatique\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bcambiamento climatico\b',r'\briscaldamento globale\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Police': {
			'ca': [],  #catalan
			'en': [r'\bpolice\b'],
			'es': [r'\bpolic[í|i]a\b',r'\bcarabineros?\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\b\b'],
			'fi': [],
			'fr': [r'\bpolice\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bpolizie\b',r'\bgendarme\b',r'\bguardia\b',r'\bcarabiner[o|i]\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Nuclear': {
			'ca': [],  #catalan
			'en': [r'\bnuclear\b'],
			'es': [r'\bnuclear\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\bkernenergie\b'],
			'fi': [],
			'fr': [r'\bnucl[e|é]aire\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\bnucleare\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},
	'Renewable': {
			'ca': [],  #catalan
			'en': [r'\brenewables?\b'],
			'es': [r'\brenovables?\b'],
			'el': [],
			'el-Latn': [],
			'eu': [],  #basque
			'da': [],
			'de': [r'\berneuerbare\b'],
			'fi': [],
			'fr': [r'\brenouvelables?\b'],
			'ga': [],  #gaelic
			'gl': [],  #galician
			'is': [],  #icelandic
			'it': [r'\brinn?ovabil[e|i]\b'],
			'lv': [],
			'lb': [],
			'mt': [],
			'nl': [],
			'no': [],
			'pl': [],  #polish
			'pt': [],  #portuguese
			'sv': [],  #swedish
			'sl': [],  #slovenian
			'tr': [],  #turkish
	},




}