VIZMAXDROP = 1


CHES2019DEFAULTATTVIZ = {
  'cbar_rect': [0.15, 0.6, 0.02, 0.3],
  'legend_loc': 'lower center',
  'limits': [-2, 12],
  'nudges': []
}


GPS2019DEFAULTATTVIZ = {
  'cbar_rect': [0.15, 0.6, 0.02, 0.3],
  'legend_loc': 'lower center',
  'limits': [-2, 12],
  'nudges': []
}


CHES2019LIMS = {
  'lrgen': [0, 10],
  'lrecon': [0, 10],
  'antielite_salience': [0, 10],
  'eu_position': [0, 7],
  'immigrate_policy': [0, 10],
  'galtan': [0, 10],
  'environment': [0, 10],
  'enviro_salience': [0, 10],
  'nationalism': [0, 10],
  'sociallifestyle': [0, 10],
  'people_vs_elite': [0, 10],
  'corrupt_salience': [0, 10],
}

GPS2019LIMS = {
  'V4_Scale': [0, 10],
  'V6_Scale': [0, 10],
  'V8_Scale': [0, 10],
  'v9': [0, 10],
  'v10': [0, 10],
  'v12': [0, 10],
  'v13': [0, 10],
  'v14': [0, 10],
  'v18': [0, 10],
  'v19': [0, 10],
  'v20': [0, 10],
  'v21': [0, 10],
}

CHES2019ATTDICT = {
    'lrgen': 'CHES Left – Right',
    'eu_position': 'CHES EU Integration',
    'antielite_salience': 'CHES Anti-elite Salience',
    'lrecon': 'CHES Economic Left – Right',
    'immigrate_policy': 'CHES Immigration Policy',
    'galtan': 'CHES GAL – TAN',
    'environment': 'CHES Environment – Economy',
    'enviro_salience': 'CHES enviro_salience',
    'nationalism': 'CHES nationalism',
    'sociallifestyle': 'CHES sociallifestyle',
    'people_vs_elite': 'CHES people_vs_elite',
    'corrupt_salience': 'CHES corrupt_salience',
}

GPS2019ATTDICT = {
  'V4_Scale': 'GPS economic left-right',
  'V6_Scale': 'GPS liberalism-conservatism',
  'V8_Scale': 'GPS populist rhetoric',
  'v9': 'GPS populist salience',
  'v10': 'GPS immigration',
  'v12': 'GPS environment',
  'v13': 'GPS nationalism',
  'v14': 'GPS women’s rights',
  'v18': 'GPS the will of the people',
  'v19': 'GPS people should decide',
  'v20': 'GPS corrupt politicians',
  'v21': 'GPS strongman rule',
}

LANGUAGES = {
    'Australia':{'languages':['en'],'marpor2020_countryname':'Australia'},
    'Austria':{'languages':['de'],'ches2019_country':'aus','marpor2020_countryname':'Austria'},
    'belgium':{'languages':['de','fr','nl'],'ches2019_country':'be','marpor2020_countryname':'Belgium'},
    'Canada':{'languages':['en','fr'],'marpor2020_countryname':'Canada'},
    'Denmark':{'languages':['da','de',],'ches2019_country':'dk','marpor2020_countryname':'Denmark'},
    'EuropeanParliament':{'languages':['ca', 'en', 'es', 'el', 'el-Latn', 'eu', 'de', 'fi', 'fr', 'ga', 'gl', 'is', 'it', 'lv', 'lb', 'nl', 'no', 'pl', 'pt', 'sv', 'sl', 'tr']},
    'Finland':{'languages':['fi','sv'],'ches2019_country':'fin','marpor2020_countryname':'Finland'},
    'france':{'languages':['fr'],'ches2019_country':'fr','marpor2020_countryname':'France'},
    'germany':{'languages':['de'],'ches2019_country':'ge','marpor2020_countryname':'Germany'},
    'Greece':{'languages':['el','el-Latn'],'ches2019_country':'gr','marpor2020_countryname':'Greece'},
    'Iceland':{'languages':['is'],'ches2019_country':'ice','marpor2020_countryname':'Iceland'},
    'Ireland':{'languages':['en','ga'],'ches2019_country':'irl','marpor2020_countryname':'Ireland'},
    'italy':{'languages':['it'],'ches2019_country':'it','marpor2020_countryname':'Italy'},
    'Latvia':{'languages':['lv'],'ches2019_country':'lat','marpor2020_countryname':'Latvia'},
    'Luxembourg':{'languages':['fr','de','lb'],'ches2019_country':'lux','marpor2020_countryname':'Luxembourg'},
    'Malta':{'languages':['mt','en','it'],'ches2019_country':'mal','marpor2020_countryname':'Malta'},
    'netherlands':{'languages':['nl','en'],'ches2019_country':'nl','marpor2020_countryname':'Netherlands'},
    'NewZealand':{'languages':['en'],'marpor2020_countryname':'New Zealand'},
    'Norway':{'languages':['no'],'ches2019_country':'nor','marpor2020_countryname':'Norway'},
    'poland':{'languages':['pl'],'ches2019_country':'pol','marpor2020_countryname':'Poland'},
    'romania':{'languages':['ro']},
    'slovenia':{'languages':['sl'],'ches2019_country':'sle','marpor2020_countryname':'Slovenia'},
    'spain':{'languages':['es','ca','eu','gl'],'ches2019_country':'esp','marpor2020_countryname':'Spain'},
    'Sweden':{'languages':['sv'],'ches2019_country':'sv','marpor2020_countryname':'Sweden'},
    'Switzerland':{'languages':['it','fr','de'],'ches2019_country':'swi','marpor2020_countryname':'Switzerland'},
    'Turkey':{'languages':['tr'],'ches2019_country':'tur','marpor2020_countryname':'Turkey'},
    'UnitedKingdom':{'languages':['en'],'ches2019_country':'uk','marpor2020_countryname':'United Kingdom'},
    'UnitedStates':{'languages':['en'],'marpor2020_countryname':'United States'},
    # Own collection
    'AustriaOwn':{'languages':['de'],'ches2019_country':'aus','marpor2020_countryname':'Austria'},
    'BrazilOwn':{'languages':['pt'],'marporLA2020_countryname':'Brazil'},
    'ChileOwn':{'languages':['es'],'marporLA2020_countryname':'Chile'},
    'FranceOwn':{'languages':['fr'],'ches2019_country':'fr','marpor2020_countryname':'France'},
    'GermanyOwn':{'languages':['de'],'ches2019_country':'ge','marpor2020_countryname':'Germany'},
    'ItalyOwn':{'languages':['it'],'ches2019_country':'it','marpor2020_countryname':'Italy'},
    'UKOwn':{'languages':['en'],'ches2019_country':'uk','marpor2020_countryname':'United Kingdom'},
    'USOwn':{'languages':['en'],'marpor2020_countryname':'United States'},
    }