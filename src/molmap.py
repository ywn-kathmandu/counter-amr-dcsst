"""Curated molecule classification for register rows whose DDA ATC field is blank.

ABX_EXTRA - molecules that ARE antibacterial and must reach the dispensing flow.
            Erring here is the costly error: a missed antibiotic is a missed sale.
CLASS     - therapeutic class label for the rest, so the tool can say WHAT a
            product is rather than only what it is not.

Anything in neither stays "cannot confirm" and is flagged for the research panel.
Every string below is an exact normalised composition token taken from the register.
"""

# ---------------------------------------------------------------- antibacterials
# veterinary antibacterials included: they are antibiotic sales, AMR-relevant, and
# the same shops carry them.
ABX_EXTRA = {
    'cephradine', 'benzathine penicillin', 'clavulanic acid', 'imipenam', 'cilastatin',
    'neomycin', 'framycetin', 'paromomycine',
    'minocycline',
    'enrofloxacin', 'nadifloxacin',
    'tylosin', 'tilmicosin', 'tiamulin hydrogen',
    'polymyxin b', 'bacitracin', 'bacitracin zinc', 'zinc bactracin',
    'ornidazole', 'nitrofurazone', 'furaltadone',
    'sulphadimidine', 'sulphadiazine', 'silver sulfadiazine', 'sulphamethoxazole',
    'sulfaclozine',
    'florfenicol', 'fusidate',
}

# names that invite a wrong antibiotic call - recorded so the call is auditable.
FALSE_FRIENDS = {
    'penicillamine': 'chelating agent, not a penicillin',
    'streptococcus faecalis': 'probiotic organism, not an antibiotic',
    'probiotics streptococcus faecalis': 'probiotic organism, not an antibiotic',
    'griseofulvin': 'antifungal, not antibacterial',
    'chlorhexidine': 'antiseptic, not a systemic antibiotic',
    'miltefosine': 'antileishmanial, not antibacterial',
    'amprollium': 'coccidiostat, not antibacterial',
    'nitroxinil': 'veterinary flukicide, not antibacterial',
    'levamisole': 'anthelmintic, not antibacterial',
}

CLASSES = {
 'Analgesic / antipyretic': [
    'paracetamol','acetaminophen','mefenamic acid','ketorolac','ketorolac tromethamine',
    'tramadol','tapentadol','pentazocine','pethidine','codeine','dexketoprofen',
    'tolfenamic acid','etodolac','flurbiprofen','diclofenac','diclofenac diethylamine',
    'indomethacin','benzydamine','choline salicylate','choline salicylate solution',
    'butorphanol tartarate','methyl salicylate','racementhol','diacereine','diacerein'],
 'Antihistamine / anti-allergy': [
    'pheniramine','chlorpheniramine','chlorpheniramine malate','promethazine',
    'promethazine theoclate','cyproheptadine','hydroxyzine','ebastine','olopatadine',
    'diphenhydramine','triprolidine','meclizine','dimenhydrinate','ketotifen',
    'cromglycate','cromolyn'],
 'Antifungal': [
    'natamycin','nystatin','amorolfine','butenafine','sertaconazole','eberconazole',
    'tioconazole','econazole','bifonazole','ciclopirox olamine','tolnaftate','miconazole',
    'griseofulvin','liposomal amphotericin b','crisaborole'],
 'Antiviral': [
    'ganciclovir','valganciclovir','famciclovir','ribavirin','zidovudine','stavudine',
    'lamivudine','entecavir','adefovir','sofosbuvir','daclatasvir','daclastavir',
    'favipiravir','amantadine'],
 'Anthelmintic / antiparasitic': [
    'praziquantel','pyrantel','piperazine','piperazine hydrate','levamisole','fenbendazole',
    'tetramisole','oxyclozanide','moxidectin','diethylcarbamazine','nitroxinil',
    'amprollium','lindane','gamma benzene hexachloride','crotamiton','benzyl benzoate',
    'miltefosine'],
 'Antimalarial': ['quinine','mefloquine','quinidine'],
 'Antiseptic / disinfectant': [
    'chlorhexidine','chlorhexidine solution','chlorhexidine digluconate','cetrimide',
    'triclosan','povidine iodine','iodine','boric acid','benzalkonium',
    'benzalkonium solution','phenol','mercurochrome','gention violet crystals',
    'ethanol','alcohol','absolute alcohol','dehydrated alcohol','rectified spirit',
    'benzoic acid','salicylic acid','chlorbutol','borax'],
 'Probiotic': [
    'streptococcus faecalis','probiotics streptococcus faecalis','lactobacillus sporogenes',
    'lactic acid bacillus','bacillus clausii','bacillus mesentericus','clostridium butyricum',
    'bifidobacterium longum','lactobacillus rhamnosus gr',
    'probiotics lactobacillous acedophillous l rhamnousus'],
 'Vaccine / immunological': [
    'newcastle disease virus lasota strain','newcastle disease virus i strain',
    'newcastle disease b strain','newcastle disease lasota','newcastle disease r b strain',
    'diphtheria toxoid','tetanus toxoid','tetanus immunoglobulin','rabies vaccine',
    'rabies immunoglobulin','rabies antiserum','hepatitis b surface antigen',
    'hepatitis a vaccine','influenza vaccine','inactivated influenza vaccine',
    'influenza vaccine surface antigen','purified inactive influenza virus antigen',
    'measles virus','rubella virus','poliovirus types','live attenuated polio virius type',
    'cholera vaccine','typhoid','japanese encephalities virus','yellow fever virus',
    'pneumococcal polysaccharide serotype','meningococcal polysaccharide',
    'immunoglobulin g','human normal immunoglobulin','snake venom antiserum',
    'anti d rh immune globulin','monoclonal anti d i h','anti thymocyte globulin',
    'anti human t lymphocyte immunoglobulin','fowl pox virus',
    'classical swine fever virus chinese strain','ppr nigerian strain',
    'marek s disease vaccine rispens strain','marek s disease hvt fc strain',
    'avian infectious bronchitis mass strain','avian infectious bronchitis mild mass strain',
    'avian infectious bronchitis disease virus strain',
    'infectious bursal disease virus winterfield strain',
    'infectious bursal disease virus intermediate strain',
    'infectious bursal disease virus invasive strain',
    'infectious bursal disease virus standard type strain',
    'infectious bursal disease standard type','ibd standard type',
    'ibd variant delaware a','ibd variant delaware e','ibd maryland','ibd baxandale',
    'ib ark type','ib mass','reo s','salmonella sg r','ibh fowl adeno virus type strain',
    'infectious coryza virus haemophilus paragallinarum serotypes a b and c',
    'newcastle disease b strain and avian infectious bronchitis disease virus mild mass strain',
    'live attenuated varicella zoster virus','live attenuated bovine human rotavirus',
    'rotavirus humain','rotavirus e bulk live attenuated','human rotavirus rix strain live',
    'hpv type l protein','human papillomavirus type l protein',
    'purified vi capsular polysaccharide of salmonella typhi ty',
    'a california reassortant virus nymcx','a singapore gp ivr',
    'conjugated to tetanus toxoid carrier protein','v cholerae o inaba cairo',
    'b pertussis','common krait venom','cobra','dried indian cobra','attenue rix',
    'vivant','attanuated','attenuated','inactivated'],
 'Antineoplastic / immunomodulator': [
    'docetaxel','temozolomide','epirubicin','capecitabine','irinotecan','pemetraxed',
    'pemetrexed','bevacizumab','gefitinib','cyclophospamide','cyclophosphamide',
    'bortezomib','l asparaginase','cytarabine','rituximab','dacarbazine','etoposide',
    'fluorouracil','sunitinib','lenalidomide','melphalan','afatinib','azacitidine',
    'bleomycin','abiraterone','bendamustine','daunorubicin','vinorelbine','dasatinib',
    'cabozantinib','palbociclib','vinblastine','everolimus','sorafenib','mitomycin',
    'trastuzumab','adalimumab','etanercept','ibrutinib','ceritinib','crizotinib',
    'niraparib','olaparib','brigatinib','regorafenib','acalabrutinib','alectinib',
    'baricitinib','busulphan','chlorambucil','carmustine','topotecan','idarubicin',
    'lapatinib','decitabine','dactinomycin','ramucirumab','cetuximab','procarbazine',
    'fludarabine','ifosfamide','trabectedin','nimotuzumab','mitoxantrone','exemestane',
    'megestrol','leuprolide','triptorelin','goserelin','bicalutamide','mycophenolic acid',
    'tofacitinib','apremilast','pirfenidone','basiliximab','osimertinib','lorlatinib',
    'venetoclax','vandetanib','axitinib','lenvatinib','hydroxy urea','mesna','leucovorin',
    'pegaspargase','tetradecyl'],
 'Vitamin / mineral / supplement': [
    'pyridoxine','cyanocobalamine','folic acid','thiamine','thiamine mononitrate',
    'riboflavin','riboflavine','riboflacine','niacinamide','nicotinamide','niacin',
    'nicotinic acid','ascorbic acid','vitamin c','vitamin a','vitamin d','vitamin e',
    'vitamin k','retinol','beta carotene','tocopheryl','alpha tocopheryl','cholecalciferol',
    'colecalciferol','calcitriol','alfacalcidol','phytomenadione','menaphthone bisulphate',
    'pantothenate','d panthenol','panthenol','dexpanthenol','elemental','elemental zinc',
    'zinc','elemental iron','elemeltal iron','dried ferrous','ferrous','ferric ammonium',
    'copper','fluoride','monofluorophosphate','benfotiamine','alpha lipoic acid',
    'ubidecarenone','levocarnitine','taurine','l isoleucine','l alanine','l argenine',
    'glycine','alpha ketoanalogue','cod liver oil','liquorice','ginkgo biloba extract',
    'ginkgo flavonglycosides','euphorbia prostrata extract','guduci','vasa',
    'terminalia arjuna','malaya vacha','oleum lini','linseed oil','melatonin','citicoline'],
 'Gastrointestinal': [
    'simethicone','simethicaine','activated dimethicone','methyl polysiloxane',
    'polydimethylsiloxane elastomer','polydimethyl siloxane','dicyclomine','diclyclomine',
    'mebeverine','magaldrate','aluminium hydroxide gel','dried aluminium hydroxide',
    'aluminium','hydroxide','trisilicate','tribasic','trisodium','bicarbonate',
    'milk of magnesia','dexrabeprazole','lafutidine','troxipide','mosapride',
    'metoclorpramide','prochlorperazine','ursodiol','mesalamine','lactitol','racecadotril',
    'diphenoxylate','docusate','isapgol husk','liquid paraffin','sorbitol','picosulphate',
    'polyethylene glycol','oxetacaine','pepsin','diastase','fungal diastase','alpha amylase',
    'lipase','protease','papain','pancreatin','trypsin chymotrypsin','bile extract',
    'hemicellulase','proteolysed liver','liver fraction','serratiopeptidase','trypsin',
    'activated charcoal','cholestyramine resin','l ornithine l aspartate','tricholine'],
 'Respiratory': [
    'terbutaline','bromhexine','guaiphenesin','dextromethorphan','levodropropizine',
    'pholcodine','acetylcysteine','etofylline','theophylline','bambuterol',
    'levosalbutamol','roflumilast','fluticasone','phenylephrine','pseudoephedrine',
    'naphazoline','ephedrine','nikethamide'],
 'Cardiovascular': [
    'frusemide','spironolactone','amiloride','metolazone','acetazolamide','eplerenone',
    'finerenone','tolvaptan','labetalol','esmolol','betaxolol','prazosin','terazosin',
    'alfuzosin','hydralazine','clonidine','nimodipine','cinnarizine','flunarizine',
    'flunarazine','trimetazidine','nicorandil','glyceryl trinitrate','isosorbide',
    'nitroprusside','dobutamine','adrenaline','mephentermine','vasopressin','terlipressin',
    'ticagrelor','cilostazol','pentoxifylline','nicoumalone','dalteparin','fondaparinux',
    'streptokinase','alteplase','tenecteplase','protamine','etamsylate','tannic acide',
    'adenosine','zatebradine','abanoquil mesilate','adaprolol','bosentan','diosmin',
    'isoxsuprine'],
 'Central nervous system': [
    'amitryptyline','imipramine','clomipramine','dothiepin','dosulepin','doxepin',
    'trazodone','fluvoxamine','desvenlafaxine','bupropion','atomoxetine','modafinil',
    'chlordiazepoxide','chlorodiazepoxide','clobazam','diazepam','haloperidol',
    'trifluoperazine','trifluperazine','thioridazide','fluphenazine decanoate',
    'flupentixol','trihexyphenidyl','benzhexol','levodopa','carbidopa','pramipexole',
    'ropinirole','selegiline','rivastigmine','piracetam','oxcarbazepine','lacosamide',
    'brivaracetam','eslicarbazepine','zonisamide','topiramatum','carisoprodol',
    'methocarbamol','chlorzoxazone','thiocolchicoside','rizatriptan','pizotifen',
    'betahistine','naltrexone','acamprosate','disulfiram','dapoxetine',
    'porcine brain derived peptide','acadesine','lithium'],
 'Anaesthetic / neuromuscular': [
    'lidocaine','lignocaine','bupivacaine','ropivacaine','prilocaine','benzocaine',
    'proparacaine','isoflurane','sevoflurane','halothane','dexmedetomidine','vecuronium',
    'atracurium','cisatracurium','rocuronium','succinylcholine','neostigmine methylsulphate',
    'pyridostigmine','glycopyrrolate','pralidoxime','xylazine','hyaluronidase',
    'botulinum toxin type a'],
 'Hormone / endocrine': [
    'thyroxine','l thyroxine','methimazole','voglibose','repaglinide','rosiglitazone',
    'danazol','estradiol','conjugated estrogen','ethinylestradiol','norethisterone',
    'norethindrone','norgestrel','levonorgestrel','desogestrel','drospirenone',
    'dydrogesterone','allylestrenol','medroxyprogesterone','hydroxyprogesterone caproate',
    'mifepristone','misoprostol','methylergometrine','carboprost','clomifene',
    'ormeloxifene','raloxifene','mesterolone','nandrolone','nandrolone phenylpropionate',
    'somatropin','somatotropin','recombinant human growth hormone','teriparatide',
    'octreotide','desmopressin','cabergoline','bromocriptine','follicle stimulating hormone',
    'recombinant human follicle stimulating hormone','follitropin alfa','lutropin alpha',
    'human chronic gonadotropin','chorionic gonadotrophin','menotrophine','cetrorelix',
    'etonogestrel','dutasteride','liraglutide','dulaglutide','zoledronic acid',
    'pamidronate disodium','ibandronic acid'],
 'Dermatological': [
    'halobetasol','hydroquinone','adapalene','tretinoin','isotretinoin','isotertinoin',
    'tazarotene','benzoyl peroxide','azelaic acid','glycolic acid','coal tar',
    'solution of coal tar','dithranol','minoxidil','mometasone','triamcinolone',
    'betamethasone','clobetasol','clobetasone butyrate','desonide','fluocinolone',
    'hydrocortison','deflazacort','methoxsalen','urea','allantoin','camphor','menthol',
    'mentha oil','clove oil','talc','diethyl phthalate','dried'],
 'Ophthalmic / ENT': [
    'tropicamide','cyclopentolate','bimatoprost','travoprost','brinzolamide',
    'fluorometholone','carboxymethylcellulose','carboxymethyl cellulose','hypromellose',
    'hydroxypropyl methylcellulose','hydroxyethyl cellulose','polyvinyl alcohol',
    'hyaluronate','hyaluronic acid','trypan blue','indocyanine green',
    'perfluoro n octane liquid','homatropine hbr'],
 'Urological': ['solifenacin','tolterodine','trospium','mirabegron','sevelamer','flavoxate'],
 'Contrast / diagnostic': [
    'iobitridol','iohexol','iopamidol','iopromide','iodixanol','gadoteric acid',
    'gadobutrol','gadodiamide','gadopentetate dimeglumine','dimeglumine gadopentetate',
    'gadopentetic acid','diatrizoic acid','diatrizoate meglumine','meglumine ioxitalamate',
    'ioxitalamate','meglumine'],
 'Blood / haematology': [
    'erythropoietin','recombinant human erythropoietin',
    'pegylated recombinant human erythropoietin',
    'methoxy polyethylene glycol epoetin beta','recombinant erythropoietin hu',
    'darbepoetin alfa','filgrastim','pegfilgrastim',
    'rh granulocyte colony stimulating factor','albumin human','human albumin',
    'human coagulation factor viii','dried factor viii fraction','eptacog alfa',
    'idarucizumab','ranibizumab','r dna derived human interferon beta a',
    'r human interferon beta a','ulinastatin','aprepitant'],
 'Fluid / parenteral base / excipient': [
    'water for injection','sterilised water for injection',
    'amino acids solution with electrolytes','lipid emulsion','soybean oil','phospholipids',
    'dextrose','invert sugar','lactose','lactose solution','lactate','dextran',
    'hydroxyethyl starch','modified fluid gelatin','poly starch','glycerin',
    'propylene glycol','polyoxyl castor oil','methyl paraben','propyl paraben','povidone',
    'benzyl alcohol','alginate','citric acid','acetic acid','lactic acid',
    'disodium hydrogen','ammonium','benzoate','caffeine','orlistat','fresh human placenta',
    'total protein','probenecide','penicillamine','acetic acid'],
}

CLASS = {}
for _label, _names in CLASSES.items():
    for _n in _names:
        CLASS.setdefault(_n, _label)

CLASS.setdefault('tripotassium', 'Gastrointestinal')
CLASS.setdefault('luteinizing hormone', 'Hormone / endocrine')

# ---------------------------------------------------------------- AWaRe assignment
# synonym -> the spelling the WHO AWaRe list uses
AWARE_SYN = {
    'cephradine': 'cefradine',
    'imipenam': 'imipenem',
    'benzathine penicillin': 'benzathine benzylpenicillin',
    'framycetin': 'neomycin',          # framycetin is neomycin B
    'paromomycine': 'paromomycin',
    'fusidate': 'fusidic acid',
    'sulphadimidine': 'sulfadimidine',
    'silver sulfadiazine': 'sulfadiazine',
    'sulphadiazine': 'sulfadiazine',
    'sulphamethoxazole': 'sulfamethoxazole',
}

# antibacterials the AWaRe list does not classify, decided explicitly.
ABX_GROUP_OVERRIDE = {
    'imipenam':          ('Watch', 'AWaRe lists imipenem only as imipenem + cilastatin (Watch)'),
    'clavulanic acid':   ('adjunct', 'beta-lactamase inhibitor; group taken from the partner molecule'),
    'cilastatin':        ('adjunct', 'renal dehydropeptidase inhibitor; group from imipenem'),
    'bacitracin':        ('Unclassified', 'topical polypeptide, not on the AWaRe list'),
    'bacitracin zinc':   ('Unclassified', 'topical polypeptide, not on the AWaRe list'),
    'zinc bactracin':    ('Unclassified', 'topical polypeptide, not on the AWaRe list'),
    'nitrofurazone':     ('Unclassified', 'topical nitrofuran, not on the AWaRe list'),
    'nadifloxacin':      ('Unclassified', 'topical quinolone; AWaRe lists levonadifloxacin only'),
    'enrofloxacin':      ('Unclassified', 'veterinary fluoroquinolone, not on the AWaRe list'),
    'florfenicol':       ('Unclassified', 'veterinary amphenicol, not on the AWaRe list'),
    'tylosin':           ('Unclassified', 'veterinary macrolide, not on the AWaRe list'),
    'tilmicosin':        ('Unclassified', 'veterinary macrolide, not on the AWaRe list'),
    'tiamulin hydrogen': ('Unclassified', 'veterinary pleuromutilin, not on the AWaRe list'),
    'sulfaclozine':      ('Unclassified', 'veterinary sulfonamide, not on the AWaRe list'),
    'furaltadone':       ('Unclassified', 'veterinary nitrofuran, not on the AWaRe list'),
}

VET_ONLY = {'enrofloxacin','florfenicol','tylosin','tilmicosin','tiamulin hydrogen',
            'sulfaclozine','furaltadone'}

# ---------------------------------------------------------------- audit round 2
# antibacterials found by auditing the residue of the first rebuild
ABX_EXTRA |= {
    'furazolidone',      # nitrofuran, not on the AWaRe list
    'mupirocin',         # topical, not on the AWaRe list
    'colistimethate',    # = colistin
    'ethambutol', 'isoniazid', 'pyrazinamide', 'ethionamide', 'cycloserine',
    'thiacetazone', 'protionamide', 'rifabutin', 'rifapentine', 'bedaquiline',
    'delamanid', 'clofazimine', 'dapsone',
}
AWARE_SYN.update({
    'amoxycillin': 'amoxicillin',
    'colistimethate': 'colistin',
    'cotrimoxazole': 'sulfamethoxazole + trimethoprim',
})
ABX_GROUP_OVERRIDE.update({
    'mupirocin': ('Unclassified', 'topical antibacterial, not on the AWaRe list'),
    'furazolidone': ('Unclassified', 'nitrofuran, not on the AWaRe list'),
})

# AWaRe excludes antituberculosis agents by design, so "Unclassified" misreads them.
# They get their own group: OTC sale of TB drugs is an AMR concern in its own right
# and a separate endpoint from AWaRe concordance.
TB_MOLS = {'ethambutol', 'isoniazid', 'pyrazinamide', 'ethionamide', 'cycloserine',
           'thiacetazone', 'protionamide', 'rifabutin', 'rifapentine', 'bedaquiline',
           'delamanid', 'clofazimine', 'dapsone'}

CLASS.setdefault('diloxanide', 'Anthelmintic / antiparasitic')   # luminal amoebicide
CLASS.setdefault('furazolidone', 'Antibacterial')                # never reached; kept for clarity

# ---------------------------------------------------------------- audit round 3
for _n, _l in {
    'torasemide': 'Cardiovascular', 'torsemide': 'Cardiovascular',
    'norepinephrine': 'Cardiovascular', 'noradrenaline': 'Cardiovascular',
    'chlorphenamine': 'Antihistamine / anti-allergy',
    'chlorphenamine maleate': 'Antihistamine / anti-allergy',
    'bcg': 'Vaccine / immunological',
    'isophane insulin': 'Hormone / endocrine', 'insulin': 'Hormone / endocrine',
    'sodium acetate': 'Fluid / parenteral base / excipient',
    'sodium citrate': 'Fluid / parenteral base / excipient',
    'potassium citrate': 'Fluid / parenteral base / excipient',
    'potassium citrate monohydrate': 'Fluid / parenteral base / excipient',
    'sodium chloride': 'Fluid / parenteral base / excipient',
    'potassium iodide': 'Vitamin / mineral / supplement',
    'calcium chloride': 'Fluid / parenteral base / excipient',
    'alumunium hydroxide': 'Gastrointestinal',
    'dried alumunium hydroxide': 'Gastrointestinal',
    'metoprolol': 'Cardiovascular', 'amlodipine': 'Cardiovascular',
    'pantoprazole': 'Gastrointestinal',
}.items():
    CLASS.setdefault(_n, _l)
