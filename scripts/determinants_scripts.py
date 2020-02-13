
classes={
    'wipo_sector':{
        '0' :'Chemistry',
        '1' :'Electrical Eng',
        '2' :'Instruments',
        '3' :'Mechanical Eng',
        '4' :'Other fields',
        '5' :'Plant'
    },
    'cpc_section':{
        'A':'Human Necessities',
#         'B':'Performing Operations; Transporting',
        'B':'Oper; Transporting',
        'C':'Chem; Metallurgy',
        'D':'Textiles; Paper',
#         'E':'Fixed Constructions',
        'E':'Constructions',
#         'F':'Mechanical Engineering; Lighting; Heating; Weapons;Blasting; Engines or Pumps',
        'F':'Mechanical Eng',
        'G':'Physics',
        'H':'Electricity',
#         'Y':'General Tagging of New Technological Developments'
        'Y':'New Tech Dev'
    },
    'ipcr_section':{
        'A':'Human Necessities',
#         'B':'Performing Operations; Transporting',
        'B':'Oper; Transporting',
#         'C':'Chemistry; Metallurgy',
        'C':'Chem; Metallurgy',
        'D':'Textiles; Paper',
#         'E':'Fixed Constructions',
        'E':'Constructions',
#         'F':'Mechanical Engineering; Lighting; Heating; Weapons; Blasting',
        'F':'Mechanical Eng',
        'G':'Physics',
        'H':'Electricity'
    },
    'nber_category':{
        '1':'Chemical',
        '2':'Cmp&Cmm',
        '3':'Drgs&Med',
        '4':'Elec',
        '5':'Mech',
        '6':'Others'
    }
}

dtypes={'id':object,'type':object, 'kind':object, 'num_claims':float, 'cit_received':float, 'cit_made':float,
       'cit_received_delay':float, 'cit_made_delay':float, 'parent_citation':float,
       'originality':float, 'generality':float, 'wipo_sector_id':object, 'ipcr_section':object,
       'ipcr_ipc_class':object, 'ipcr_subclass':object, 'cpc_section_id':object,
       'cpc_subsection_id':object, 'cpc_group_id':object, 'nber_category_id':object,
       'nber_subcategory_id':object, 'uspc_mainclass_id':object, 'uspc_subclass_id':object}