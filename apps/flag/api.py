"""
World Flags API.

Routes:
  GET /api/flag/random   -> random country record
  GET /api/flag/count    -> total number of countries
  GET /api/flag/<id>     -> country by zero-based index
"""

import random

# Flag types rendered by client JS:
#   tricolor_v   — three equal vertical stripes,  colors: [left, mid, right]
#   tricolor_h   — three equal horizontal stripes, colors: [top, mid, bottom]
#   bicolor_h    — two equal horizontal stripes,   colors: [top, bottom]
#   nordic_cross — Nordic/Scandinavian cross; keys: bg, cross (+ cross2 for two-colour)
#   sun_disc     — solid bg + circle;  keys: bg, disc, cx, cy, r
#   swiss_cross  — red square + white cross
#   brazil       — green, yellow diamond, blue disc
#   canada       — red / white / red + maple leaf
#   stripe_sun   — horizontal stripes + sun circle (Argentina)
#   stripe_wheel — horizontal stripes + navy wheel (India)
#   crescent     — solid bg + white crescent + star (Turkey)

COUNTRIES = [
    {
        "name": "France",
        "capital": "Paris",
        "population": "68 million",
        "area": "643,801 km²",
        "languages": ["French"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "France is the most visited country on Earth, welcoming over 90 million tourists "
            "a year. The Eiffel Tower was originally built as a temporary exhibit for the 1889 "
            "World's Fair — it was almost torn down in 1909."
        ),
        "flag": {"type": "tricolor_v", "colors": ["#0055A4", "#FFFFFF", "#EF4135"]},
    },
    {
        "name": "Germany",
        "capital": "Berlin",
        "population": "84 million",
        "area": "357,114 km²",
        "languages": ["German"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Germany has over 1,500 different types of beer and around 1,300 breweries. "
            "The country invented the printing press, the automobile, aspirin, and the MP3 "
            "audio format. Germany also has the world's largest train station by track count."
        ),
        "flag": {"type": "tricolor_h", "colors": ["#000000", "#DD0000", "#FFCE00"]},
    },
    {
        "name": "Japan",
        "capital": "Tokyo",
        "population": "124 million",
        "area": "377,975 km²",
        "languages": ["Japanese"],
        "currency": "Yen (¥)",
        "continent": "Asia",
        "fun_fact": (
            "Japan has 6,852 islands and more than 100 active volcanoes. Vending machines "
            "outnumber convenience stores — there's roughly one vending machine per 23 people. "
            "The Japanese railway system is so punctual that delays of more than a minute are "
            "considered newsworthy."
        ),
        "flag": {"type": "sun_disc", "bg": "#FFFFFF", "disc": "#BC002D",
                 "cx": 0.5, "cy": 0.5, "r": 0.3},
    },
    {
        "name": "Italy",
        "capital": "Rome",
        "population": "59 million",
        "area": "301,340 km²",
        "languages": ["Italian"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Italy has more UNESCO World Heritage Sites than any other country in the world. "
            "Pizza was invented in Naples in the 1800s. The Vatican, an independent country "
            "entirely surrounded by Rome, is the world's smallest nation by both area and "
            "population."
        ),
        "flag": {"type": "tricolor_v", "colors": ["#009246", "#FFFFFF", "#CE2B37"]},
    },
    {
        "name": "Sweden",
        "capital": "Stockholm",
        "population": "10.5 million",
        "area": "450,295 km²",
        "languages": ["Swedish"],
        "currency": "Swedish Krona (kr)",
        "continent": "Europe",
        "fun_fact": (
            "Sweden invented the three-point seatbelt, the pacemaker, the zipper, and "
            "flat-pack furniture. It's also home to ABBA, Spotify, Minecraft, and IKEA. "
            "Sweden has more islands than any other country — over 221,800 of them."
        ),
        "flag": {"type": "nordic_cross", "bg": "#006AA7", "cross": "#FECC02"},
    },
    {
        "name": "Norway",
        "capital": "Oslo",
        "population": "5.5 million",
        "area": "385,207 km²",
        "languages": ["Norwegian"],
        "currency": "Norwegian Krone (kr)",
        "continent": "Europe",
        "fun_fact": (
            "Norway introduced salmon sushi to Japan in the 1980s — it wasn't a traditional "
            "Japanese ingredient. The country has a 'Right to Roam' law that allows anyone to "
            "hike through private land. Norway also produces roughly 99% of its electricity "
            "from hydropower."
        ),
        "flag": {"type": "nordic_cross", "bg": "#EF2B2D", "cross": "#FFFFFF",
                 "cross2": "#003680"},
    },
    {
        "name": "Denmark",
        "capital": "Copenhagen",
        "population": "5.9 million",
        "area": "42,924 km²",
        "languages": ["Danish"],
        "currency": "Danish Krone (kr)",
        "continent": "Europe",
        "fun_fact": (
            "Denmark has the oldest national flag in the world still in use — the Dannebrog "
            "dates to 1219. LEGO was invented by a Danish carpenter in 1932 and the name "
            "comes from the Danish words 'leg godt', meaning 'play well'."
        ),
        "flag": {"type": "nordic_cross", "bg": "#C8102E", "cross": "#FFFFFF"},
    },
    {
        "name": "Netherlands",
        "capital": "Amsterdam",
        "population": "17.9 million",
        "area": "41,543 km²",
        "languages": ["Dutch"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "About 26% of the Netherlands lies below sea level — without its famous dikes and "
            "pumping systems, much of the country would be underwater. The Dutch invented the "
            "stock market and the modern telescope, and orange carrots were bred in the 16th "
            "century to honour the Dutch Royal House of Orange."
        ),
        "flag": {"type": "tricolor_h", "colors": ["#AE1C28", "#FFFFFF", "#21468B"]},
    },
    {
        "name": "Poland",
        "capital": "Warsaw",
        "population": "38 million",
        "area": "312,679 km²",
        "languages": ["Polish"],
        "currency": "Polish Zloty (zł)",
        "continent": "Europe",
        "fun_fact": (
            "Poland is home to the world's largest castle by land area: Malbork Castle, "
            "built by the Teutonic Knights in the 13th century. Marie Curie, the first person "
            "to win two Nobel Prizes in different sciences, was born in Warsaw."
        ),
        "flag": {"type": "bicolor_h", "colors": ["#FFFFFF", "#DC143C"]},
    },
    {
        "name": "Ukraine",
        "capital": "Kyiv",
        "population": "44 million",
        "area": "603,550 km²",
        "languages": ["Ukrainian"],
        "currency": "Hryvnia (₴)",
        "continent": "Europe",
        "fun_fact": (
            "Ukraine is the largest country located entirely within Europe. The blue and yellow "
            "of its flag represent blue sky over golden wheat fields. Ukraine is one of the "
            "world's top exporters of wheat, sunflower oil, and corn."
        ),
        "flag": {"type": "bicolor_h", "colors": ["#005BBB", "#FFD500"]},
    },
    {
        "name": "Ireland",
        "capital": "Dublin",
        "population": "5.1 million",
        "area": "70,273 km²",
        "languages": ["Irish (Gaeilge)", "English"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Ireland has no snakes — the island became separated from mainland Europe before "
            "snakes could colonise it after the last Ice Age. Halloween originated in Ireland "
            "from the ancient Celtic festival of Samhain, which marked the end of harvest season."
        ),
        "flag": {"type": "tricolor_v", "colors": ["#169B62", "#FFFFFF", "#FF883E"]},
    },
    {
        "name": "Switzerland",
        "capital": "Bern",
        "population": "8.7 million",
        "area": "41,285 km²",
        "languages": ["German", "French", "Italian", "Romansh"],
        "currency": "Swiss Franc (CHF)",
        "continent": "Europe",
        "fun_fact": (
            "Switzerland has one of only two square national flags in the world (the other is "
            "Vatican City). The country has been officially neutral in armed conflicts since 1815 "
            "and didn't join the United Nations until 2002. Swiss chocolate and cheese are major "
            "cultural exports."
        ),
        "flag": {"type": "swiss_cross"},
    },
    {
        "name": "Belgium",
        "capital": "Brussels",
        "population": "11.6 million",
        "area": "30,528 km²",
        "languages": ["Dutch (Flemish)", "French", "German"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Belgium invented French fries — despite the name, fries likely originated in the "
            "Wallonia region of Belgium, not France. Belgium also has more comic-book artists "
            "per square kilometre than any other country, including the creators of Tintin and "
            "the Smurfs."
        ),
        "flag": {"type": "tricolor_v", "colors": ["#000000", "#FDDA24", "#EF3340"]},
    },
    {
        "name": "Brazil",
        "capital": "Brasília",
        "population": "215 million",
        "area": "8,515,767 km²",
        "languages": ["Portuguese"],
        "currency": "Brazilian Real (R$)",
        "continent": "South America",
        "fun_fact": (
            "Brazil contains about 60% of the Amazon rainforest, which produces around 20% "
            "of the world's oxygen. It's the only Portuguese-speaking country in the Americas "
            "and the 5th largest country on Earth. Brazil has won the FIFA World Cup five times "
            "— more than any other nation."
        ),
        "flag": {"type": "brazil"},
    },
    {
        "name": "Canada",
        "capital": "Ottawa",
        "population": "38.2 million",
        "area": "9,984,670 km²",
        "languages": ["English", "French"],
        "currency": "Canadian Dollar (CA$)",
        "continent": "North America",
        "fun_fact": (
            "Canada is the second largest country in the world by total area, yet has a smaller "
            "population than the state of California. It has the longest coastline in the world "
            "at over 202,000 km — long enough to circle the Earth five times."
        ),
        "flag": {"type": "canada"},
    },
    {
        "name": "Argentina",
        "capital": "Buenos Aires",
        "population": "45.8 million",
        "area": "2,780,400 km²",
        "languages": ["Spanish"],
        "currency": "Argentine Peso ($)",
        "continent": "South America",
        "fun_fact": (
            "Argentina is home to the southern tip of South America — the Tierra del Fuego "
            "archipelago — and shares a border with Antarctica. The tango dance and music style "
            "originated in Buenos Aires in the late 19th century among immigrant communities."
        ),
        "flag": {"type": "stripe_sun",
                 "colors": ["#74ACDF", "#FFFFFF", "#74ACDF"],
                 "sun": "#F6B40E"},
    },
    {
        "name": "India",
        "capital": "New Delhi",
        "population": "1.43 billion",
        "area": "3,287,263 km²",
        "languages": ["Hindi", "English", "+ 21 other official languages"],
        "currency": "Indian Rupee (₹)",
        "continent": "Asia",
        "fun_fact": (
            "India is the world's most populous country and has the largest number of post "
            "offices of any country on Earth — over 155,000. Chess was invented in India, "
            "as were the concept of zero, the decimal system, and shampoo."
        ),
        "flag": {"type": "stripe_wheel",
                 "colors": ["#FF9933", "#FFFFFF", "#138808"],
                 "wheel": "#000080"},
    },
    {
        "name": "Kenya",
        "capital": "Nairobi",
        "population": "55 million",
        "area": "580,367 km²",
        "languages": ["Swahili (Kiswahili)", "English"],
        "currency": "Kenyan Shilling (KSh)",
        "continent": "Africa",
        "fun_fact": (
            "Kenya is home to the Great Rift Valley and the Maasai Mara, where one of the "
            "world's most spectacular wildlife events takes place: the annual wildebeest "
            "migration involving over 1.5 million animals. Kenya's long-distance runners "
            "have won more Olympic gold medals in distance events than any other nation."
        ),
        "flag": {"type": "kenya"},
    },
    {
        "name": "Mexico",
        "capital": "Mexico City",
        "population": "128 million",
        "area": "1,964,375 km²",
        "languages": ["Spanish"],
        "currency": "Mexican Peso ($)",
        "continent": "North America",
        "fun_fact": (
            "Mexico City was built on the ruins of Tenochtitlan, the Aztec capital, which "
            "was itself built on an island in the middle of a lake. The city sinks by up to "
            "50 cm per year in some areas due to drainage of the ancient lake bed. Mexico "
            "introduced chocolate, chilli, corn, tomatoes, and vanilla to the world."
        ),
        "flag": {"type": "tricolor_v_emblem",
                 "colors": ["#006847", "#FFFFFF", "#CE1126"]},
    },
    {
        "name": "Turkey",
        "capital": "Ankara",
        "population": "85 million",
        "area": "783,562 km²",
        "languages": ["Turkish"],
        "currency": "Turkish Lira (₺)",
        "continent": "Asia / Europe",
        "fun_fact": (
            "Turkey is one of only two countries that straddles two continents (the other is "
            "Russia). Istanbul is the only city in the world located on two continents. Turkey "
            "is the world's largest producer of hazelnuts and cherries — the word 'cherry' "
            "actually comes from the Turkish city of Giresun (ancient Kerasous)."
        ),
        "flag": {"type": "crescent",
                 "bg": "#E30A17",
                 "symbol": "#FFFFFF"},
    },
    {
        "name": "United Kingdom",
        "capital": "London",
        "population": "67 million",
        "area": "242,495 km²",
        "languages": ["English"],
        "currency": "Pound Sterling (£)",
        "continent": "Europe",
        "fun_fact": (
            "The UK invented the World Wide Web, the telephone, the television, penicillin, "
            "and the steam engine. It is also home to the oldest underground railway in the "
            "world (the London Tube, opened 1863) and drives on the left — a tradition dating "
            "back to sword-fighting knights keeping their right hand free."
        ),
        "flag": {"type": "union_jack"},
    },
    {
        "name": "United States",
        "capital": "Washington D.C.",
        "population": "331 million",
        "area": "9,833,517 km²",
        "languages": ["English"],
        "currency": "US Dollar ($)",
        "continent": "North America",
        "fun_fact": (
            "The United States has more public libraries than McDonald's restaurants. Montana "
            "has three times more cows than people. Alaska is simultaneously the westernmost, "
            "northernmost, and easternmost state — its Aleutian Islands cross the 180° meridian "
            "into the Eastern Hemisphere."
        ),
        "flag": {"type": "stars_stripes"},
    },
    {
        "name": "Spain",
        "capital": "Madrid",
        "population": "47.3 million",
        "area": "505,990 km²",
        "languages": ["Spanish (Castilian)"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Spain is the second largest country in the European Union by area. La Tomatina, "
            "an annual festival where participants throw tomatoes at each other, draws tens of "
            "thousands of participants to Buñol each August. Spain also has the second highest "
            "number of UNESCO World Heritage Sites in Europe."
        ),
        "flag": {"type": "tricolor_h", "colors": ["#AA151B", "#F1BF00", "#AA151B"],
                 "_note": "Spain flag: red top/bottom (wider) yellow centre — simplified as equal thirds"},
    },
    {
        "name": "China",
        "capital": "Beijing",
        "population": "1.41 billion",
        "area": "9,596,960 km²",
        "languages": ["Mandarin Chinese (Putonghua)"],
        "currency": "Renminbi / Yuan (¥)",
        "continent": "Asia",
        "fun_fact": (
            "China has the world's longest high-speed rail network — over 40,000 km of track, "
            "more than the rest of the world combined. Paper, printing, gunpowder, and the "
            "compass were all invented in China. The Great Wall, if fully extended, would "
            "stretch more than twice around the equator."
        ),
        "flag": {"type": "china_stars"},
    },
    {
        "name": "South Korea",
        "capital": "Seoul",
        "population": "51.7 million",
        "area": "100,210 km²",
        "languages": ["Korean"],
        "currency": "South Korean Won (₩)",
        "continent": "Asia",
        "fun_fact": (
            "South Korea has the world's fastest average internet speed and highest smartphone "
            "ownership rate. It is the birthplace of taekwondo, K-pop, and the 'Hallyu' Korean "
            "Wave of global cultural exports. Seoul's subway system is one of the largest and "
            "most technologically advanced in the world."
        ),
        "flag": {"type": "taegukgi"},
    },
    {
        "name": "Indonesia",
        "capital": "Jakarta",
        "population": "273 million",
        "area": "1,904,569 km²",
        "languages": ["Indonesian (Bahasa Indonesia)"],
        "currency": "Indonesian Rupiah (Rp)",
        "continent": "Asia / Oceania",
        "fun_fact": (
            "Indonesia is the world's largest archipelago nation, with over 17,000 islands. "
            "It is the fourth most populous country on Earth and home to the world's largest "
            "Buddhist temple (Borobudur) and Hindu temple complex (Prambanan). Indonesia sits "
            "on the 'Ring of Fire' and has more active volcanoes than any other country."
        ),
        "flag": {"type": "bicolor_h", "colors": ["#CE1126", "#FFFFFF"]},
    },
    {
        "name": "Australia",
        "capital": "Canberra",
        "population": "25.7 million",
        "area": "7,692,024 km²",
        "languages": ["English"],
        "currency": "Australian Dollar (A$)",
        "continent": "Oceania",
        "fun_fact": (
            "Australia is the only country that is also a continent. It has more species of "
            "venomous snakes than any other country. The kangaroo and emu on the Australian "
            "coat of arms were chosen because neither animal can walk backwards — symbolising "
            "a nation always moving forward."
        ),
        "flag": {"type": "australia"},
    },
    {
        "name": "South Africa",
        "capital": "Pretoria / Cape Town / Bloemfontein",
        "population": "59.3 million",
        "area": "1,221,037 km²",
        "languages": ["Zulu", "Xhosa", "Afrikaans", "English", "+ 7 more official"],
        "currency": "South African Rand (R)",
        "continent": "Africa",
        "fun_fact": (
            "South Africa is the only country in the world to have voluntarily dismantled its "
            "nuclear weapons programme. It has 11 official languages — the most of any country "
            "except Zimbabwe. The Cradle of Humankind, near Johannesburg, contains the world's "
            "richest hominid fossil site."
        ),
        "flag": {"type": "south_africa"},
    },
    {
        "name": "Portugal",
        "capital": "Lisbon",
        "population": "10.3 million",
        "area": "92,212 km²",
        "languages": ["Portuguese"],
        "currency": "Euro (€)",
        "continent": "Europe",
        "fun_fact": (
            "Portugal is the oldest nation-state in Europe — its borders have remained almost "
            "unchanged since 1139. It was once the greatest maritime power in the world and "
            "its explorers reached Brazil, India, China, and Japan first. Portuguese is now "
            "spoken by over 250 million people across five continents."
        ),
        "flag": {"type": "portugal"},
    },
    {
        "name": "Thailand",
        "capital": "Bangkok",
        "population": "70 million",
        "area": "513,120 km²",
        "languages": ["Thai"],
        "currency": "Thai Baht (฿)",
        "continent": "Asia",
        "fun_fact": (
            "Thailand is the only country in Southeast Asia never to have been colonised by a "
            "European power — in fact, 'Thailand' means 'Land of the Free'. It has more Buddhist "
            "temples than any other country. Bangkok's full ceremonial name is the longest city "
            "name in the world at 168 characters."
        ),
        "flag": {"type": "thailand"},
    },
    {
        "name": "Nigeria",
        "capital": "Abuja",
        "population": "218 million",
        "area": "923,768 km²",
        "languages": ["English", "Hausa", "Yoruba", "Igbo"],
        "currency": "Nigerian Naira (₦)",
        "continent": "Africa",
        "fun_fact": (
            "Nigeria is the most populous country in Africa and has the continent's largest "
            "economy. It produces more films per year than any country except India, giving its "
            "film industry the nickname 'Nollywood'. Nigeria also has the world's second highest "
            "number of twin births."
        ),
        "flag": {"type": "bicolor_v", "colors": ["#008751", "#FFFFFF", "#008751"]},
    },
    {
        "name": "Egypt",
        "capital": "Cairo",
        "population": "104 million",
        "area": "1,001,449 km²",
        "languages": ["Arabic"],
        "currency": "Egyptian Pound (£E)",
        "continent": "Africa",
        "fun_fact": (
            "Egypt is home to the only surviving Wonder of the Ancient World — the Great Pyramid "
            "of Giza. Ancient Egypt is one of the longest-lasting civilisations in history, "
            "spanning over 3,000 years. Cleopatra VII lived closer in time to the Moon landing "
            "than to the construction of the Great Pyramid."
        ),
        "flag": {"type": "egypt"},
    },
]

_total = len(COUNTRIES)


def handle(path_parts: list[str]) -> tuple[int, dict, dict]:
    if not path_parts or path_parts[0] == "random":
        idx = random.randrange(_total)
        country = dict(COUNTRIES[idx])
        country["index"] = idx
        country["total"] = _total
        return 200, country, {}

    if path_parts[0] == "count":
        return 200, {"total": _total}, {}

    try:
        idx = int(path_parts[0])
        if 0 <= idx < _total:
            country = dict(COUNTRIES[idx])
            country["index"] = idx
            country["total"] = _total
            return 200, country, {}
        return 404, {"error": "index out of range"}, {}
    except ValueError:
        return 400, {"error": "invalid id"}, {}
