from random import choice, random, shuffle, randint
words = {
5: ['ABOUT', 'ABOVE', 'ACTOR', 'ADAPT', 'ADDED', 'ADEPT', 'ADOBE', 'AFTER', 'AGAIN', 'AGENT',
    'AGILE', 'AGREE', 'AHEAD', 'ALARM', 'ALERT', 'ALIEN', 'ALIKE', 'ALIVE', 'ALLEY', 'ALLOW',
    'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGRY', 'ANGUS', 'ANKLE', 'APART', 'APPLY', 'APTLY',
    'AREAS', 'ARENA', 'ARMED', 'ARMOR', 'AROSE', 'ASIDE', 'ASKED', 'AVOID', 'AWAIT', 'AWARE',
    'AWAYS', 'BADLY', 'BANDS', 'BASED', 'BASES', 'BASIC', 'BASIN', 'BATON', 'BEAST', 'BEATS',
    'BEGAN', 'BEGIN', 'BEING', 'BELOW', 'BESET', 'BETTY', 'BLACK', 'BLADE', 'BLAST', 'BLEND',
    'BLOCK', 'BLOOD', 'BLOWN', 'BOARD', 'BOMBS', 'BONDS', 'BONES', 'BONUS', 'BOOKS', 'BOOST',
    'BOOTH', 'BOOTS', 'BOOTY', 'BOOZE', 'BORED', 'BRAIN', 'BRASS', 'BREAK', 'BRICK', 'BRIEF',
    'BRING', 'BRINK', 'BROKE', 'BROOM', 'BRUNT', 'BRUTE', 'BUILD', 'BUILT', 'BULLY', 'BUNCH',
    'BUTCH', 'CACHE', 'CAGES', 'CALLS', 'CANDY', 'CARDS', 'CARED', 'CARES', 'CARGO', 'CARRY',
    'CASES', 'CASTE', 'CATCH', 'CAUSE', 'CAVES', 'CELLS', 'CHAIR', 'CHAOS', 'CHEAP', 'CHEAT',
    'CHECK', 'CHEST', 'CHILD', 'CHOSE', 'CIVIL', 'CLAIM', 'CLANS', 'CLASS', 'CLAWS', 'CLEAN',
    'CLEAR', 'CLIMB', 'CLIPS', 'CLOCK', 'CLOSE', 'CLOTH', 'CLOUD', 'CLUBS', 'CLUES', 'CLUMP',
    'COATS', 'COBRA', 'CODES', 'COLOR', 'COMES', 'COULD', 'COVER', 'CRAFT', 'CRANE', 'CRASH',
    'CRASS', 'CRAZY', 'CREED', 'CRIED', 'CRIME', 'CROSS', 'CRUDE', 'CRUEL', 'DAILY', 'DAISY',
    'DARED', 'DAREN', 'DAZED', 'DEATH', 'DECAY', 'DEEDS', 'DEEMS', 'DEITY', 'DELAY', 'DEMON',
    'DIARY', 'DIRTY', 'DISKS', 'DOING', 'DOORS', 'DOZEN', 'DRANK', 'DRAWN', 'DREAM', 'DREGS',
    'DRESS', 'DRIED', 'DRINK', 'DUNES', 'DYING', 'EAGER', 'EAGLE', 'EARLY', 'EARTH', 'ELDER',
    'ELITE', 'EMPTY', 'ENACT', 'ENDED', 'ENEMY', 'ENTER', 'ENTRY', 'EQUAL', 'ERUPT', 'ETHAN',
    'EVENT', 'EVERY', 'EXCEL', 'EXIST', 'EXTRA', 'FACES', 'FAILS', 'FAITH', 'FALLS', 'FALSE',
    'FARGO', 'FARMS', 'FAULT', 'FAUST', 'FAVOR', 'FENCE', 'FERAL', 'FETCH', 'FIBER', 'FIELD',
    'FIFTH', 'FIGHT', 'FINAL', 'FINDS', 'FIRST', 'FISTS', 'FIXES', 'FLAME', 'FLARE', 'FLASH',
    'FLASK', 'FLESH', 'FLOCK', 'FLOOR', 'FLUID', 'FOODS', 'FORCE', 'FORTH', 'FOUND', 'FOYER',
    'FRAME', 'FRANK', 'FREED', 'FREES', 'FRIED', 'FRIES', 'FRONT', 'FRUIT', 'FURRY', 'GAINS',
    'GAMES', 'GANGS', 'GATES', 'GAUNT', 'GEEKS', 'GHOST', 'GHOUL', 'GIANT', 'GIVEN', 'GIVES',
    'GLASS', 'GLEAM', 'GLOBE', 'GLORY', 'GLOVE', 'GOALS', 'GOING', 'GOODS', 'GOONS', 'GRADE',
    'GRASP', 'GRASS', 'GRAVE', 'GREAT', 'GREED', 'GREEN', 'GRIEF', 'GROUP', 'GROWN', 'GROWS',
    'GUARD', 'GUESS', 'GUIDE', 'GUIDO', 'GURPS', 'HALLS', 'HANDS', 'HANDY', 'HAPPY', 'HAREM',
    'HARSH', 'HATCH', 'HATES', 'HAVEN', 'HEADS', 'HEALS', 'HEARD', 'HEARS', 'HEART', 'HEAVY',
    'HELPS', 'HENCE', 'HERBS', 'HIDES', 'HILLS', 'HINTS', 'HIRED', 'HOLDS', 'HOLES', 'HOMES',
    'HONOR', 'HOPED', 'HOPES', 'HORDE', 'HOURS', 'HOUSE', 'HOWLS', 'HUMAN', 'HUMOR', 'HYDES',
    'IDEAL', 'IDEAS', 'IMAGE', 'INNER', 'ITALY', 'ITEMS', 'JACOB', 'JAMES', 'JERRY', 'JOINS',
    'JOKES', 'JOLLY', 'JONES', 'KEEPS', 'KHANS', 'KICKS', 'KILLS', 'KINDA', 'KINDS', 'KNIFE',
    'KNOCK', 'KNOWN', 'KNOWS', 'LANCE', 'LANDS', 'LARGE', 'LASER', 'LATER', 'LAWNS', 'LEADS',
    'LEARN', 'LEAST', 'LEAVE', 'LEVEL', 'LIGHT', 'LIKES', 'LIMIT', 'LINED', 'LINES', 'LISTS',
    'LIVED', 'LIVES', 'LOADS', 'LOCAL', 'LOCKS', 'LODGE', 'LOGIC', 'LOOKS', 'LOOMS', 'LOONY',
    'LOOSE', 'LORDS', 'LOSES', 'LOVED', 'LOVER', 'LOVES', 'LOWER', 'LOYAL', 'LUCKY', 'LYING',
    'MACHO', 'MAGIC', 'MAJOR', 'MAKES', 'MALES', 'MARCH', 'MARKS', 'MASKS', 'MAYBE', 'MAZES',
    'MEANS', 'MEANT', 'MEATS', 'MEETS', 'METAL', 'METER', 'MICRO', 'MIDST', 'MIGHT', 'MILES',
    'MINDS', 'MINES', 'MINOR', 'MODEL', 'MONEY', 'MONTH', 'MOUTH', 'MOVED', 'MUSIC', 'NAILS',
    'NAMED', 'NAMES', 'NASTY', 'NEARS', 'NEEDS', 'NERVE', 'NESTS', 'NEVER', 'NEWLY', 'NIGHT',
    'NOISE', 'NORTH', 'NOTED', 'NOTES', 'NUKES', 'OASIS', 'OCCUR', 'OFFER', 'OFTEN', 'OMEGA',
    'OPENS', 'ORBIT', 'ORDER', 'OTHER', 'OUTER', 'OWNED', 'OWNER', 'PACKS', 'PAGES', 'PAINT',
    'PANEL', 'PAPER', 'PARTS', 'PARTY', 'PATHS', 'PEACE', 'PERIL', 'PICKS', 'PIECE', 'PILED',
    'PIPES', 'PLACE', 'PLANS', 'PLANT', 'PLATE', 'PLAYS', 'PLOTS', 'PLUSH', 'POINT', 'POSED',
    'POSTS', 'POUCH', 'POWER', 'PRICE', 'PRODS', 'PRONE', 'PROOF', 'PROUD', 'PROVE', 'PULLS',
    'PUNKS', 'QUEST', 'QUICK', 'QUIET', 'QUITE', 'RACES', 'RADIO', 'RAGED', 'RAIDS', 'RAISE',
    'RANGE', 'RANKS', 'RATES', 'RAZED', 'RAZOR', 'REACH', 'READY', 'REFER', 'RELAY', 'RELIC',
    'REPEL', 'RESTS', 'REVEL', 'RIGHT', 'RIGID', 'RIVAL', 'RIVER', 'ROBES', 'ROBOT', 'ROCKS',
    'ROCKY', 'ROLLS', 'ROMAN', 'ROOMS', 'ROUGH', 'ROUND', 'RUINS', 'RULED', 'RULER', 'RULES',
    'RUMOR', 'SADLY', 'SAFER', 'SAMBA', 'SANDS', 'SAVED', 'SAVES', 'SCALE', 'SCANT', 'SCARF',
    'SCENE', 'SCENT', 'SCOPE', 'SCOTT', 'SCOUR', 'SCOUT', 'SCRAP', 'SEALS', 'SEEDS', 'SEEDY',
    'SEEMS', 'SEIZE', 'SELLS', 'SENDS', 'SENSE', 'SERVE', 'SETUP', 'SEVEN', 'SEVER', 'SEWER',
    'SHADY', 'SHAPE', 'SHAVE', 'SHEER', 'SHINY', 'SHOCK', 'SHOPS', 'SHORT', 'SHOTS', 'SHOWN',
    'SHOWS', 'SHRUG', 'SIDES', 'SIEGE', 'SIGHT', 'SIGNS', 'SILKS', 'SINCE', 'SIXTY', 'SIZES',
    'SKIES', 'SKILL', 'SKINS', 'SKULL', 'SLATE', 'SLAVE', 'SLEEP', 'SLIDE', 'SLING', 'SLIPS',
    'SLITS', 'SMALL', 'SMILE', 'SMOKE', 'SNAKE', 'SNARE', 'SNEAK', 'SNIFF', 'SNUCK', 'SOLAR',
    'SONIC', 'SORTS', 'SOUND', 'SOUTH', 'SPANS', 'SPARE', 'SPARK', 'SPEAK', 'SPEAR', 'SPEED',
    'SPEND', 'SPENT', 'SPIED', 'SPIES', 'SPIKE', 'SPILL', 'SPLIT', 'SPOKE', 'SPOON', 'SPRAY',
    'SPREE', 'SQUAD', 'STAFF', 'STAKE', 'STAND', 'STARK', 'STARS', 'START', 'STASH', 'STATE',
    'STAYS', 'STEAD', 'STEAL', 'STEEL', 'STEPS', 'STERN', 'STEVE', 'STILL', 'STOCK', 'STOLE',
    'STONE', 'STOOL', 'STOPS', 'STORE', 'STORM', 'STORY', 'STOUT', 'STRAY', 'STUCK', 'STUDY',
    'STUFF', 'STYLE', 'SUITS', 'SUPER', 'SURGE', 'SWAMP', 'SWEAR', 'SWEPT', 'SWISS', 'SWORD',
    'SWORE', 'TABLE', 'TAINT', 'TAKEN', 'TAKES', 'TALKS', 'TANDY', 'TANKS', 'TASKS', 'TAUNT',
    'TEAMS', 'TEETH', 'TELLS', 'TERMS', 'TESTS', 'TEXAS', 'TEXTS', 'THANK', 'THEIR', 'THERE',
    'THESE', 'THICK', 'THIEF', 'THING', 'THINK', 'THIRD', 'THOSE', 'THREE', 'THREW', 'THROW',
    'THUGS', 'TIGHT', 'TILES', 'TIMER', 'TIMES', 'TIRED', 'TIRES', 'TODAY', 'TOMES', 'TORCH',
    'TOUGH', 'TOWEL', 'TOWER', 'TOWNS', 'TOXIC', 'TRACE', 'TRACK', 'TRACT', 'TRADE', 'TRAIL',
    'TRAIN', 'TRAPS', 'TRASH', 'TREES', 'TRIAL', 'TRIBE', 'TRICK', 'TRIED', 'TRIES', 'TRIPS',
    'TRITE', 'TROOP', 'TRULY', 'TRUST', 'TRUTH', 'TURNS', 'TWANG', 'TWIGS', 'TWIST', 'TYPED',
    'TYPES', 'UNDER', 'UNITE', 'UNITS', 'UNITY', 'UNTIL', 'UPSET', 'USING', 'USUAL', 'VALUE',
    'VAULT', 'VENOM', 'VENTS', 'VIEWS', 'VIPER', 'VIRAL', 'VIRUS', 'VITAL', 'VOICE', 'WAGON',
    'WAITS', 'WAKES', 'WALKS', 'WALLS', 'WANTS', 'WARES', 'WARNS', 'WASTE', 'WATCH', 'WATER',
    'WAVES', 'WEARS', 'WEEKS', 'WEIRD', 'WHEEL', 'WHERE', 'WHICH', 'WHILE', 'WHITE', 'WHOLE',
    'WHOSE', 'WIELD', 'WINDS', 'WIPED', 'WIRES', 'WISER', 'WITCH', 'WOMAN', 'WOMEN', 'WOODS',
    'WORDS', 'WORKS', 'WORLD', 'WORRY', 'WORSE', 'WORTH', 'WOULD', 'WRATH', 'WRIST', 'WRITE',
    'WRONG', 'WROTE', 'YEARS', 'YIELD', 'YOUNG'],

7: ['ABILITY', 'ACHIEVE', 'ACQUIRE', 'ACTIONS', 'ACTRESS', 'ADOPTED', 'ADORNED', 'ADVISES', 'AFFRONT', 'AGAINST',
    'AIRLOCK', 'ALCOHOL', 'ALLOWED', 'ALREADY', 'AMALGAM', 'AMONGST', 'AMOUNTS', 'ANCIENT', 'ANDROID', 'ANGELIC',
    'ANGERED', 'ANGUISH', 'ANIMALS', 'ANNOYED', 'ANOTHER', 'ANSWERS', 'ANYTIME', 'APPEARS', 'ARMORED', 'ARRIVAL',
    'ARRIVED', 'ASHAMED', 'ASSIGNS', 'ASSUMED', 'ATTACKS', 'ATTEMPT', 'ATTENDS', 'AVERAGE', 'AWESOME', 'BANDITS',
    'BANNING', 'BANSHEE', 'BARRAGE', 'BARRENS', 'BARRIER', 'BASTARD', 'BASTION', 'BATTLES', 'BEATING', 'BECAUSE',
    'BECOMES', 'BEDROOM', 'BEEPING', 'BELIEFS', 'BELIEVE', 'BELONGS', 'BENCHES', 'BENEATH', 'BENEFIT', 'BESIDES',
    'BETWEEN', 'BIGGEST', 'BIGOTRY', 'BIZARRE', 'BLANKET', 'BLASTED', 'BLAZING', 'BLESSED', 'BLOWING', 'BORROWS',
    'BOTTLES', 'BRACERS', 'BRIEFLY', 'BROTHER', 'BROUGHT', 'BUILDER', 'BUNDLED', 'BURNING', 'BURROWS', 'CABINET',
    'CALIBER', 'CALLING', 'CAMPING', 'CANCERS', 'CANTEEN', 'CANTINA', 'CAPABLE', 'CAPITOL', 'CAPTAIN', 'CAPTORS',
    'CAPTURE', 'CARAVAN', 'CAREFUL', 'CARRIED', 'CARRIER', 'CARRIES', 'CAUSING', 'CAVERNS', 'CEILING', 'CENTRAL',
    'CERAMIC', 'CERTAIN', 'CHAINED', 'CHAMBER', 'CHANGED', 'CHOOSES', 'CIRCUIT', 'CISTERN', 'CITADEL', 'CLAWING',
    'CLEANSE', 'CLEARED', 'CLEAVER', 'CLIMATE', 'CLOSELY', 'CLOSEST', 'CLOSING', 'CLOTHES', 'COCHISE', 'COHORTS',
    'COLLECT', 'COMMAND', 'COMMITS', 'COMPANY', 'COMPASS', 'COMPLEX', 'CONCERN', 'CONDUCT', 'CONFESS', 'CONFIRM',
    'CONQUER', 'CONSIST', 'CONSUME', 'CONTACT', 'CONTAIN', 'CONTENT', 'CONTEST', 'CONTROL', 'COOKERY', 'COPYING',
    'CORNERS', 'CORRALS', 'COSTING', 'COUNCIL', 'COUNTER', 'COUNTRY', 'COUSINS', 'COVERED', 'COWARDS', 'CRAFTED',
    'CRAZIES', 'CREATED', 'CREDITS', 'CRIMSON', 'CRIPPLE', 'CROSSED', 'CROWBAR', 'CROWDED', 'CRUCIAL', 'CRUSADE',
    'CRUSHED', 'CURIOUS', 'CURRENT', 'CUTTERS', 'CUTTING', 'CYBORGS', 'DAGGERS', 'DAMAGED', 'DANCERS', 'DANCING',
    'DANGERS', 'DEALING', 'DEATHLY', 'DECADES', 'DECIDED', 'DECLARE', 'DECLINE', 'DECORUM', 'DECREES', 'DECRIED',
    'DECRIES', 'DEFEATS', 'DEFENSE', 'DEMANDS', 'DENYING', 'DEPARTS', 'DESERTS', 'DESIRED', 'DESIRES', 'DESPAIR',
    'DESPITE', 'DESTROY', 'DETAILS', 'DEVELOP', 'DEVICES', 'DEVIOUS', 'DEVOLVE', 'DISABLE', 'DISBAND', 'DISCUSS',
    'DIVIDED', 'DOLLARS', 'DOORWAY', 'DRAGONS', 'DRAINED', 'DRESSED', 'DRESSES', 'DRIVING', 'DROPPED', 'DUNGEON',
    'DURABLE', 'DUSTERS', 'DWELLER', 'DWINDLE', 'EASIEST', 'EFFECTS', 'EFFORTS', 'ELDERLY', 'ELECTED', 'ELEGANT',
    'ELEMENT', 'EMBRACE', 'EMERGED', 'EMOTION', 'EMPEROR', 'ENABLES', 'ENCASED', 'ENCLAVE', 'ENDINGS', 'ENEMIES',
    'ENFORCE', 'ENGLISH', 'ENHANCE', 'ENSLAVE', 'ENSUING', 'ERECTED', 'ERRANDS', 'ESCAPED', 'ESCAPES', 'ESCORTS',
    'ESSENCE', 'EXACTLY', 'EXCLAIM', 'EXPANSE', 'EXPECTS', 'EXPLAIN', 'EXPOSED', 'EXPRESS', 'EXTRACT', 'EXTREME',
    'FACTION', 'FAILURE', 'FALLING', 'FALLOUT', 'FANATIC', 'FARMING', 'FARTHER', 'FAVORED', 'FEARING', 'FEELING',
    'FENCING', 'FERTILE', 'FESTERS', 'FIGHTER', 'FILTERS', 'FINALLY', 'FINDING', 'FIREARM', 'FISHING', 'FITTING',
    'FIZZLES', 'FLOWERS', 'FLOWING', 'FOCUSED', 'FOLLOWS', 'FORBADE', 'FOREVER', 'FORTIFY', 'FOUNDED', 'FREEDOM',
    'FREIGHT', 'FRIENDS', 'FURTHER', 'GABBING', 'GAINING', 'GANGERS', 'GARBAGE', 'GATEWAY', 'GENERAL', 'GENGHIS',
    'GENUINE', 'GETTING', 'GHENGIS', 'GHOSTLY', 'GODLIKE', 'GOGGLES', 'GRADUAL', 'GRANITE', 'GRANTED', 'GREATLY',
    'GREENED', 'GREETED', 'GRENADE', 'GROCERY', 'GROOMED', 'GROUPED', 'GROWING', 'GUARDED', 'GUMMING', 'GUNFIRE',
    'HALBERD', 'HALLWAY', 'HAMMERS', 'HANDGUN', 'HANDLES', 'HANGING', 'HANGOUT', 'HAPPENS', 'HARMFUL', 'HARNESS',
    'HATCHET', 'HAZARDS', 'HEADING', 'HEADSET', 'HEALING', 'HEALTHY', 'HEARING', 'HEARTED', 'HEAVENS', 'HEAVILY',
    'HEIGHTS', 'HELPFUL', 'HELPING', 'HERSELF', 'HIDEOUT', 'HIMSELF', 'HISSING', 'HISTORY', 'HOLDING', 'HOLSTER',
    'HORIZON', 'HOSTILE', 'HOUSING', 'HOWEVER', 'HOWLING', 'HUNDRED', 'HUNTERS', 'HUNTING', 'HURTING', 'HUSBAND',
    'ILLNESS', 'IMAGINE', 'IMPLIES', 'IMPROVE', 'INCLUDE', 'INGROWN', 'INHUMAN', 'INITIAL', 'INQUIRE', 'INSISTS',
    'INSTANT', 'INSTEAD', 'INSTORE', 'INSULTS', 'INTENSE', 'INVADED', 'INVOLVE', 'ITCHING', 'JACKALS', 'JESSICA',
    'JOINING', 'JOURNAL', 'JOURNEY', 'JUNGLES', 'JUSTICE', 'JUTTING', 'KEDRICK', 'KEEPING', 'KIDNAPS', 'KILLING',
    'KINDRED', 'KITCHEN', 'KNIGHTS', 'KNOWING', 'LABELED', 'LANDING', 'LANTERN', 'LARGEST', 'LAUGHED', 'LAUNDRY',
    'LAWLESS', 'LEADERS', 'LEADING', 'LEARNED', 'LEATHER', 'LEAVING', 'LECTURE', 'LEGENDS', 'LEGIONS', 'LENDING',
    'LEPROSY', 'LETTING', 'LIBERAL', 'LIBRARY', 'LIGHTER', 'LIMITED', 'LOCALES', 'LOCATED', 'LOCKING', 'LOOKING',
    'LOOTING', 'LOWDOWN', 'LOYALTY', 'LURKING', 'MACHETE', 'MACHINE', 'MALTASE', 'MANAGED', 'MANAGES', 'MANHOOD',
    'MANKIND', 'MASSIVE', 'MASTERS', 'MASTERY', 'MATCHES', 'MATTERS', 'MAXIMUM', 'MEANING', 'MEETING', 'MELISSA',
    'MELTING', 'MEMBERS', 'MENTION', 'MESSAGE', 'MESSIAH', 'METHODS', 'MICHAEL', 'MILLING', 'MINIGUN', 'MINIMAL',
    'MIRRORS', 'MISSING', 'MISSION', 'MIXTURE', 'MOLOTOV', 'MONITOR', 'MONSTER', 'MONTHLY', 'MORNING', 'MOTIVES',
    'MOUNTED', 'MUTANTS', 'MUTATED', 'MYSTERY', 'NATURAL', 'NEGLECT', 'NEITHER', 'NERVOUS', 'NOTABLE', 'NOTHING',
    'NOTICED', 'NOURISH', 'NOWHERE', 'NUCLEAR', 'NULLMOD', 'NUMBERS', 'OBJECTS', 'OBVIOUS', 'OCTOBER', 'OFFENSE',
    'OFFERED', 'OFFICER', 'OFFICES', 'OFFLINE', 'ONESELF', 'OPENING', 'OPTIONS', 'ORBITAL', 'ORDERED', 'ORIGINS',
    'ORLEANS', 'OUTCAST', 'OUTCOME', 'OUTLAWS', 'OUTPOST', 'OUTRAGE', 'OUTSIDE', 'OVERALL', 'OVERLAP', 'OVERRUN',
    'OVERSEE', 'PACINKO', 'PACKETS', 'PACKING', 'PARENTS', 'PARTIES', 'PASSING', 'PASSION', 'PATCHES', 'PATTERN',
    'PENALTY', 'PERFECT', 'PERIODS', 'PERSONA', 'PHYSICS', 'PICTURE', 'PILLAGE', 'PILLOWS', 'PISTOLS', 'PITIFUL',
    'PLAGUED', 'PLANNED', 'PLASTIC', 'PLAYERS', 'PLAYING', 'PLEASED', 'PLOTTED', 'PLUMING', 'POISONS', 'POPULAR',
    'POURING', 'POWERED', 'PRAISED', 'PRECISE', 'PREPARE', 'PRESENT', 'PRESSED', 'PRIESTS', 'PRIMATE', 'PRISONS',
    'PRIVATE', 'PROBLEM', 'PROCEED', 'PROCESS', 'PRODUCE', 'PROJECT', 'PROTECT', 'PROVIDE', 'PROWESS', 'PSIONIC',
    'PSYCHIC', 'PUPPETS', 'PURPOSE', 'PUTTING', 'PUZZLES', 'PYRAMID', 'QUALIFY', 'QUALITY', 'QUICKLY', 'RAIDERS',
    'RAIDING', 'RAMPAGE', 'RANGERS', 'RANKING', 'RANSACK', 'RATIONS', 'RAVAGES', 'REACHED', 'REACHES', 'REACTOR',
    'READILY', 'READING', 'REALIZE', 'REASONS', 'REBUILD', 'RECEIVE', 'RECORDS', 'RECOVER', 'RECRUIT', 'REDUCED',
    'REENTER', 'REFUSES', 'REGULAR', 'RELATED', 'RELEASE', 'REMAINS', 'REMORSE', 'REMOVES', 'REQUIRE', 'RESIDES',
    'RESPECT', 'RESTING', 'RETIRED', 'RETREAT', 'RETURNS', 'REVENGE', 'REVERED', 'RHOMBUS', 'RITUALS', 'ROAMING',
    'ROBBERS', 'ROBERTS', 'RODENTS', 'ROUTING', 'RUMBLES', 'RUNDOWN', 'RUNNING', 'SALVAGE', 'SANCTUM', 'SAVIORS',
    'SCALPEL', 'SCONCES', 'SCRAPER', 'SCREENS', 'SCRIBES', 'SEALANT', 'SEALING', 'SEASIDE', 'SECRETS', 'SECTION',
    'SEEKING', 'SELLING', 'SENDING', 'SERIOUS', 'SERMONS', 'SERVANT', 'SERVICE', 'SERVING', 'SESSION', 'SETTING',
    'SETTLED', 'SEVERAL', 'SHADOWS', 'SHARPER', 'SHELTER', 'SHELVES', 'SHERIFF', 'SHOTGUN', 'SHOWING', 'SHRINES',
    'SHUNNED', 'SIGNALS', 'SIMILAR', 'SIPHONS', 'SKEPTIC', 'SKETCHY', 'SKILLED', 'SLAMMED', 'SLAVERS', 'SLAVERY',
    'SLIDING', 'SLIPPED', 'SLITHER', 'SLUMBER', 'SMALLER', 'SMARTER', 'SMASHED', 'SMOKING', 'SOCIETY', 'SOLDIER',
    'SOMEHOW', 'SOMEONE', 'SOUNDED', 'SPARING', 'SPECIAL', 'SPOTTED', 'STACKED', 'STAINED', 'STAMINA', 'STARTED',
    'STATING', 'STATION', 'STATUES', 'STAYING', 'STEALTH', 'STERILE', 'STOPPED', 'STORAGE', 'STORIES', 'STORMED',
    'STRANGE', 'STREAKS', 'STREETS', 'STRIPES', 'STUDIES', 'STUNNED', 'SUBJECT', 'SUCCEED', 'SUCCESS', 'SUGGEST',
    'SUPPORT', 'SURFACE', 'SURVIVE', 'SYSTEMS', 'TACTICS', 'TAINTED', 'TAKINGS', 'TALENTS', 'TALKING', 'TARGETS',
    'TATTOOS', 'TAUNTED', 'TEACHER', 'TEMPLES', 'TENANTS', 'TESTING', 'THEATER', 'THEATRE', 'THICKER', 'THIEVES',
    'THIRSTY', 'THOUGHT', 'THROUGH', 'THROWER', 'TONIGHT', 'TOPPLED', 'TORCHES', 'TORTURE', 'TOWARDS', 'TRADERS',
    'TRADING', 'TRAINED', 'TRAITOR', 'TREATED', 'TRINITY', 'TROUSER', 'TRUSTED', 'TUNNELS', 'TURRETS', 'TWINKIE',
    'TWISTED', 'TYPICAL', 'TYRANNY', 'UNDERGO', 'UNKNOWN', 'UNLUCKY', 'UNUSUAL', 'URANIUM', 'USELESS', 'USUALLY',
    'UTENSIL', 'VARIETY', 'VARIOUS', 'VARYING', 'VASSALS', 'VEGGIES', 'VENTURE', 'VERSION', 'VICTIMS', 'VICTORY',
    'VILLAGE', 'VILLAIN', 'VIOLATE', 'VIOLENT', 'VIRTUAL', 'VISIBLE', 'VISITED', 'VOLUMES', 'WAITING', 'WALKING',
    'WALKWAY', 'WANTING', 'WARFARE', 'WARLIKE', 'WARNING', 'WARPATH', 'WARRING', 'WARRIOR', 'WASTING', 'WATCHED',
    'WEALTHY', 'WEAPONS', 'WEARING', 'WELCOME', 'WELFARE', 'WESTERN', 'WHETHER', 'WHISPER', 'WHOEVER', 'WILLING',
    'WINDING', 'WINDOWS', 'WINNING', 'WISHING', 'WITHOUT', 'WONDERS', 'WORKING', 'WORRIED', 'WORSHIP', 'WOUNDED',
    'WRITING', 'WRITTEN', 'YOUNGER', 'ZEALOTS', 'ZEALOUS'],

9: ['ABANDONED', 'ABSORBING', 'ACCEPTING', 'ACCOMPANY', 'ACCORDING', 'ADDRESSED', 'ADVENTURE', 'ADVERTISE', 'AFTERNOON', 'AGREEMENT',
    'AMBITIONS', 'AMERICANS', 'AMPLIFIES', 'ANNOUNCES', 'APARTMENT', 'APOLOGIZE', 'ARMADILLO', 'ARRANGING', 'ARTIFACTS', 'ASCENSION',
    'ASSAULTED', 'ASSISTANT', 'ATTACKERS', 'ATTEMPTED', 'ATTENTION', 'AUTHORITY', 'AUTOMATED', 'AVAILABLE', 'AWAKENING', 'BACKSTABS',
    'BANDOLEER', 'BARNSTORM', 'BARTERING', 'BASICALLY', 'BATHROOMS', 'BATTERIES', 'BEAUTIFUL', 'BEGINNING', 'BELIEVING', 'BELONGING',
    'BLACKJACK', 'BLASPHEMY', 'BLOODLUST', 'BLOODSHED', 'BODYGUARD', 'BREAKFAST', 'BRIEFCASE', 'BROADCAST', 'BRUTALITY', 'BUILDINGS',
    'CANISTERS', 'CAPTURING', 'CARDINALS', 'CARPETING', 'CARRIAGES', 'CATACOMBS', 'CATHEDRAL', 'CERTAINLY', 'CHALLENGE', 'CHARACTER',
    'CHEMICALS', 'CHEMISTRY', 'CHILDLIKE', 'CHITINOUS', 'CIRCUITRY', 'CLOCKWORK', 'CLUSTERED', 'CLUTTERED', 'COCKROACH', 'COLLECTED',
    'COLLECTOR', 'COMMANDED', 'COMMITTEE', 'COMMUNITY', 'COMPANIES', 'COMPLETES', 'COMPUTERS', 'CONCEALED', 'CONCERNED', 'CONDUCTED',
    'CONFUSING', 'CONQUORER', 'CONSIDERS', 'CONSISTED', 'CONSTRUCT', 'CONTAINED', 'CONTINUED', 'CONVERTED', 'CONVICTED', 'CONVINCED',
    'CONVINCES', 'CORPORATE', 'CORRECTLY', 'COUNTDOWN', 'COUNTRIES', 'COURTYARD', 'CREATURES', 'CRIMINALS', 'CRUMBLING', 'CURIOSITY',
    'CURRENTLY', 'CUSTOMERS', 'DANGEROUS', 'DEATHCLAW', 'DECISIONS', 'DEDICATED', 'DEFEATING', 'DEFENDERS', 'DEFENSIVE', 'DEFORMITY',
    'DELIMITER', 'DELIVERED', 'DEPENDING', 'DESERTERS', 'DESPERATE', 'DESTROYED', 'DETERMINE', 'DETERRENT', 'DETHRONED', 'DEVELOPED',
    'DIFFERENT', 'DIFFICULT', 'DIRECTION', 'DISAGREES', 'DISAPPEAR', 'DISCOVERY', 'DISGRACED', 'DISGUISES', 'DISGUSTED', 'DISPARATE',
    'DISPLAYED', 'DISTANCES', 'DIVISIONS', 'DOCTRINES', 'DOCUMENTS', 'DOWNRIGHT', 'DURASTEEL', 'DWINDLING', 'ELABORATE', 'ELIMINATE',
    'ELSEWHERE', 'EMERGENCY', 'ENCOUNTER', 'ENDORPHIN', 'ENGINEERS', 'ENTRANCES', 'EQUIPMENT', 'ESTABLISH', 'EVERYTIME', 'EXCHANGED',
    'EXECUTION', 'EXPENSIVE', 'EXPLORING', 'EXPLOSIVE', 'EXPRESSES', 'EXTENSIVE', 'EXTREMELY', 'FANATICAL', 'FAVORABLE', 'FEARFULLY',
    'FEROCIOUS', 'FINALIZES', 'FIREFIGHT', 'FLATTENED', 'FLAVORING', 'FOLLOWERS', 'FOLLOWING', 'FOOTSTEPS', 'FORBIDDEN', 'FORGOTTEN',
    'FORTIFIED', 'FORTITUDE', 'FURNITURE', 'GATHERING', 'GENERALLY', 'GENERATED', 'GENERATOR', 'GENTLEMAN', 'GLADIATOR', 'GODFATHER',
    'GOSSIPING', 'GRADUALLY', 'GRAPPLING', 'GRATITUDE', 'GROTESQUE', 'GUARDIANS', 'GYMNASIUM', 'HANDCUFFS', 'HAPPENING', 'HAPPINESS',
    'HARNESSED', 'HEALTHIER', 'HIGHTOWER', 'HISTORIES', 'HOLOCAUST', 'HONORABLE', 'HUMANKIND', 'HURRIEDLY', 'IDENTICAL', 'IGNORANCE',
    'ILLNESSES', 'IMMEDIATE', 'IMPLANTED', 'IMPORTANT', 'IMPROVING', 'INCESSANT', 'INCLUDING', 'INCREASED', 'INDICATED', 'INFLUENCE',
    'INITIALLY', 'INITIATES', 'INNERMOST', 'INNOCENTS', 'INSISTENT', 'INSTANTLY', 'INSTINCTS', 'INTELLECT', 'INTERCEPT', 'INTERFACE',
    'INTERIORS', 'INTRICATE', 'INTRUSION', 'INVENTORS', 'INVOLVING', 'ISOLATION', 'JAILBREAK', 'KIDNAPPED', 'KNOWLEDGE', 'LEGENDARY',
    'LEUTENANT', 'LISTENING', 'LITERALLY', 'LOCATIONS', 'LOCKPICKS', 'MACHINERY', 'MAGICIANS', 'MAGNITUDE', 'MARAUDERS', 'MARAUDING',
    'MARVELOUS', 'MECHANISM', 'MENTIONED', 'MERCHANTS', 'MERCILESS', 'MESSIANIC', 'MICROCHIP', 'MICROWAVE', 'MONASTERY', 'MONITORED',
    'MONOBLADE', 'MONOCOLOR', 'MONSTROUS', 'MOONSHINE', 'MOUNTAINS', 'MURDEROUS', 'MUTATIONS', 'NECESSARY', 'NEGOTIATE', 'NIGHTCLUB',
    'NORTHWEST', 'NOTORIOUS', 'OBJECTIVE', 'OBTAINING', 'OBVIOUSLY', 'OCCASIONS', 'OCCUPANTS', 'OCCUPYING', 'OFFICIALS', 'OFFSPRING',
    'OPERATING', 'OPERATION', 'OTHERWISE', 'OUTSIDERS', 'OUTSKIRTS', 'OVERMATCH', 'OVERPRICE', 'OVERTHROW', 'PACIFISTS', 'PAINTINGS',
    'PANTHEIST', 'PARALYSES', 'PARTICLES', 'PATIENTLY', 'PATROLLED', 'PENDELTON', 'PERFORMED', 'PERIMETER', 'PERSONNEL', 'PIERCINGS',
    'PLUNDERED', 'POISONING', 'POISONOUS', 'PONDEROUS', 'POSITIONS', 'POSSESSES', 'PRAGMATIC', 'PRECISION', 'PREDATORS', 'PREPARING',
    'PRESENTED', 'PRIMARILY', 'PRIMITIVE', 'PRISONERS', 'PROCESSOR', 'PROJECTOR', 'PROLONGED', 'PROTECTED', 'PURIFYING', 'QUALITIES',
    'QUESTIONS', 'RADIATION', 'RAMBLINGS', 'RANSACKED', 'REALISTIC', 'REARGUARD', 'RECEIVING', 'RECEPTORS', 'RECOGNIZE', 'RECOVERED',
    'RECYCLING', 'REFERENCE', 'REFRESHED', 'REGARDING', 'REGULATES', 'RELEASERS', 'RELEASING', 'RELIGIONS', 'RELIGIOUS', 'REMAINING',
    'REMINDING', 'RENOVATED', 'REPAIRING', 'REPELLENT', 'REPLICATE', 'REPRESSED', 'REPRIMAND', 'REQUIRING', 'RESEMBLES', 'RESERVOIR',
    'RESIDENCE', 'RESIDENTS', 'RESILIENT', 'RESOURCES', 'RESPECTED', 'RETREATED', 'RETURNING', 'REVERENCE', 'SACRIFICE', 'SALVATION',
    'SANCTUARY', 'SCATTERED', 'SCIENTIST', 'SCORPIONS', 'SCRIPTING', 'SCRUBBERS', 'SEARCHING', 'SECLUSION', 'SECRETIVE', 'SELECTING',
    'SEPARATED', 'SEPTEMBER', 'SERIOUSLY', 'SERVITORS', 'SHAMBLING', 'SITUATION', 'SKEPTICAL', 'SLITHERED', 'SNAKELIKE', 'SOMETHING',
    'SOMETIMES', 'SOMEWHERE', 'SOUTHEAST', 'SOUTHWARD', 'SPIRITUAL', 'SPONSORED', 'SPREADING', 'STARTLING', 'STATIONED', 'STERILIZE',
    'STOREROOM', 'STRANGERS', 'STRANGEST', 'STRETCHES', 'STRONGEST', 'STRUCTURE', 'STRUGGLES', 'STUMBLING', 'SUBJECTED', 'SUICIDALY',
    'SUMMONING', 'SURRENDER', 'SURROUNDS', 'SURVIVING', 'SURVIVORS', 'SUSPECTED', 'SWIVELING', 'TECHNICAL', 'TELEPHONE', 'TEMPORARY',
    'TERRIFIED', 'TERRITORY', 'THEREFORE', 'THREATENS', 'TOLERANCE', 'TORTURING', 'TRAVELERS', 'TRAVELING', 'TREATMENT', 'TRIUMPHED',
    'TROUBLING', 'TWOBYFOUR', 'UNCOVERED', 'UNDERGONE', 'UNDERWENT', 'UNIVERSAL', 'UNLOCKING', 'UNTOUCHED', 'VAPORIZES', 'VENGEANCE',
    'VIGILANCE', 'VILLAGERS', 'VIOLENTLY', 'VIRTUALLY', 'VOLUNTEER', 'WANDERING', 'WAREHOUSE', 'WASTELAND', 'WASTELORD', 'WHISPERED',
    'WILLINGLY', 'WONDERFUL', 'WORSHIPER', 'WRENCHING'],

11: ['ACCELERATES', 'ACCESSORIES', 'ACCOMPANIED', 'ACKNOWLEDGE', 'AGRICULTURE', 'ANIMALISTIC', 'ANNIHILATED', 'APPROPRIATE', 'APPROXIMATE',
     'ASSASSINATE', 'ATMOSPHERIC', 'BACKGROUNDS', 'BARTERTOWNE', 'BECKONINGLY', 'BLASPHEMERS', 'BOMBARDMENT', 'BRAINWASHED', 'BROTHERHOOD',
     'CAMOUFLAGED', 'CANDELABRAS', 'CATEGORIZED', 'CHALLENGING', 'CHARISMATIC', 'CHIMPANZEES', 'COMBINATION', 'COMFORTABLE', 'CONNECTIONS',
     'CONSTRUCTED', 'CONTAINMENT', 'CONTROLLING', 'COUNTERMAND', 'DECEPTIVELY', 'DESCENDANTS', 'DESCRIPTION', 'DESPERATELY', 'DESTRUCTION',
     'DESTRUCTIVE', 'DEVASTATION', 'DISAPPEARED', 'DISCIPLINES', 'DISCOVERIES', 'DISCOVERING', 'DISMEMBERED', 'DISTINGUISH', 'DISTRUSTFUL',
     'EFFECTIVELY', 'ELECTRICITY', 'ELECTRIFIED', 'ELECTRONICS', 'ELIMINATING', 'EMANCIPATED', 'EMBROIDERED', 'ENGINEERING', 'ERRATICALLY',
     'ESSENTIALLY', 'EXAMINATION', 'EXCLUSIVELY', 'EXPERIENCED', 'EXPERIENCES', 'EXPERIMENTS', 'EXPLANATION', 'FREELOADERS', 'FURNISHINGS',
     'GENERATIONS', 'GRANDFATHER', 'HOLOGRAPHIC', 'HOSPITALITY', 'IMMEDIATELY', 'IMPORTANTLY', 'INDEPENDENT', 'INDIVIDUALS', 'INFATICALLY',
     'INFESTATION', 'INFLUENTIAL', 'INFORMATION', 'INGREDIENTS', 'INHABITANTS', 'INSTRUMENTS', 'INTELLIGENT', 'INTERESTING', 'INTERROGATE',
     'LOBOTOMIZED', 'MAINTENANCE', 'MANUFACTURE', 'MASTERFULLY', 'MISTRUSTFUL', 'MISTRUSTING', 'NIGHTVISION', 'NONDESCRIPT', 'NOTORIOUSLY',
     'OBSERVATION', 'OPPORTUNITY', 'OVERCROWDED', 'OVERLOADING', 'OVERLOOKING', 'OVERPOWERED', 'OVERWHELMED', 'PARTITIONED', 'PERMANENTLY',
     'PERPETRATOR', 'PERSECUTION', 'PERSONALITY', 'POPULATIONS', 'POSSIBILITY', 'PRIESTESSES', 'PROGRAMMING', 'RADIOACTIVE', 'RANGEFINDER',
     'RECOGNITION', 'RECTANGULAR', 'RELUCTANTLY', 'REMEMBERING', 'REPRIMANDED', 'RESEARCHING', 'RESIDENTIAL', 'RESPONSIBLE', 'SETTLEMENTS',
     'SHOPLIFTING', 'SNAKEKEEPER', 'STOREHOUSES', 'SURROUNDING', 'SURVIVALIST', 'SYNTHESIZED', 'TECHNICIANS', 'TELEVISIONS', 'TEMPERATURE',
     'TEMPORARILY', 'THREATENING', 'TRANSMITTER', 'TREACHEROUS', 'UNBEKNOWNST', 'UNBELIEVERS', 'UNCONSCIOUS', 'UNDERGROUND', 'UNDRINKABLE',
     'UNIMPORTANT', 'UNORGANIZED', 'UNSPEAKABLE', 'UPHOLSTERED', 'WHEREABOUTS', 'WORSHIPPING'],

12: ['ABOMINATIONS', 'ACCOMPANYING', 'ACCOMPLISHED', 'AFTEREFFECTS', 'AMPHITHEATER', 'ANNOUNCEMENT', 'ANTICIPATING', 'APPRECIATION', 'APPREHENSIVE',
     'ASSASSINATED', 'AUTHENTICITY', 'BRAINWASHING', 'BROADCASTING', 'CIRCUMSTANCE', 'CIVILIZATION', 'CONSPIRATORS', 'CONSTRUCTION', 'CONTAMINATED',
     'CONVERSATION', 'DISAPPEARING', 'ENCOUNTERING', 'ENHANCEMENTS', 'EVOLUTIONARY', 'EXECUTIONERS', 'EXTINGUISHER', 'GOVERNMENTAL', 'HEADQUARTERS',
     'IMMACULATELY', 'IMPENETRABLE', 'INACCESSIBLE', 'INCREASINGLY', 'INDEFINITELY', 'INFILTRATION', 'INITIATEHOOD', 'INTELLIGENCE', 'INTERROGATED',
     'INVESTIGATES', 'LABORATORIES', 'LOUDSPEAKERS', 'MAGNETICALLY', 'NORTHERNMOST', 'OCCASIONALLY', 'ORGANIZATION', 'OVERWHELMING', 'PARTICULARLY',
     'PARTNERSHIPS', 'PUPPETMASTER', 'PURIFICATION', 'QUARTERSTAFF', 'QUESTIONABLE', 'RECUPERATING', 'RELATIONSHIP', 'REPLENISHING', 'REPRIMANDING',
     'RESURRECTION', 'SECLUSIONIST', 'SPECIFICALLY', 'SPOKESPERSON', 'SUBTERRANEAN', 'SUCCESSFULLY', 'SURROUNDINGS', 'SURVEILLANCE', 'SURVIVALISTS',
     'SYMPATHIZERS', 'TECHNOLOGIES', 'THOUGHTFULLY', 'TRANQUILLITY', 'TRANSCRIBING', 'TRANSMISSION', 'TRANSMITTERS', 'TRIUMPHANTLY', 'UNAUTHORIZED',
     'WALKIETALKIE']
}


def get_random_word(key):
    word = choice(words[key])
    return word


def get_words(key, secret_word, word_count):
    word_set = words[key]
    word_list = [secret_word]
    for x in range(word_count):
        found = False
        count = 0
        while not found:
            # get random word from word_set
            word = choice(word_set)
            # test likeness of word to secret word
            likeness = 0
            target_likeness = randint(1,3)
            for enum, letter in enumerate(secret_word):
                if word[enum] == letter:
                    likeness += 1
            if word not in word_list and likeness >= target_likeness or count > 100:  # important to avoid infinite loop
                word_list.append(word)
                # print('likeness:' + str(likeness))
                # print('target likeness:' + str(target_likeness))
                # print('count:' + str(count))
                found = True
            count += 1
        shuffle(word_list)
    return word_list
