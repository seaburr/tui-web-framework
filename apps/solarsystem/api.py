"""
Solar System API.

Routes:
  GET /api/solarsystem/random   -> random planet record
  GET /api/solarsystem/count    -> total number of planets
  GET /api/solarsystem/<id>     -> planet by zero-based index
"""

import random

PLANETS = [
    {
        "name": "Mercury",
        "type": "TERRESTRIAL PLANET",
        "diameter_km": "4,879 km",
        "distance_au": "0.39 AU",
        "distance_km": "57.9 million km",
        "orbital_period": "88 Earth days",
        "moons": 0,
        "surface_temp": "−180°C to +430°C",
        "atmosphere": "Trace (sodium, oxygen)",
        "notable": "Smallest planet in the Solar System",
        "fun_fact": (
            "A day on Mercury (one full rotation) lasts 59 Earth days, but its year is only "
            "88 days — so the Sun rises just twice per Mercurian year. Despite being the "
            "closest planet to the Sun, Mercury is NOT the hottest. Venus beats it by far."
        ),
        "size_rank": 8,
        "ascii_art": [
            "      .-------.      ",
            "     / o . . o \\    ",
            "    | . o . o . |   ",
            "    | o . o . o |   ",
            "    | . . o . . |   ",
            "     \\ o . . o /    ",
            "      `-------'      ",
        ],
    },
    {
        "name": "Venus",
        "type": "TERRESTRIAL PLANET",
        "diameter_km": "12,104 km",
        "distance_au": "0.72 AU",
        "distance_km": "108.2 million km",
        "orbital_period": "225 Earth days",
        "moons": 0,
        "surface_temp": "+465°C (avg)",
        "atmosphere": "Dense CO₂ with sulfuric acid clouds",
        "notable": "Hottest planet in the Solar System",
        "fun_fact": (
            "Venus rotates backwards compared to most planets — the Sun rises in the west and "
            "sets in the east. It also rotates so slowly that a day on Venus is longer than "
            "its year. Atmospheric pressure on the surface is 90 times that of Earth."
        ),
        "size_rank": 6,
        "ascii_art": [
            "         .---------.         ",
            "       .'   ~~~~~   '.       ",
            "      /   ~~~~~~~~~   \\     ",
            "     |   ~~~~~~~~~~~   |     ",
            "     |   ~~~~~~~~~~~   |     ",
            "     |   ~~~~~~~~~~~   |     ",
            "      \\   ~~~~~~~~~   /     ",
            "       '.   ~~~~~   .'       ",
            "         `---------'         ",
        ],
    },
    {
        "name": "Earth",
        "type": "TERRESTRIAL PLANET",
        "diameter_km": "12,756 km",
        "distance_au": "1.00 AU",
        "distance_km": "149.6 million km",
        "orbital_period": "365.25 Earth days",
        "moons": 1,
        "surface_temp": "−88°C to +58°C",
        "atmosphere": "Nitrogen (78%), oxygen (21%)",
        "notable": "Only known planet with life",
        "fun_fact": (
            "Earth is the densest planet in the Solar System and the only one not named after "
            "a Roman or Greek god. The Moon is unusually large relative to its host planet — "
            "large enough to stabilize Earth's axial tilt and keep our seasons predictable."
        ),
        "size_rank": 5,
        "ascii_art": [
            "         .---------.         ",
            "       .'  ~~#~~    '.       ",
            "      /  ##~~~~~##~   \\     ",
            "     |  ~~~~##~~~~##   |     ",
            "     |  ~##~~~~~#~~~~  |     ",
            "     |  ~~~~##~~~~##   |     ",
            "      \\  ~~#~~~~~#~   /     ",
            "       '.  ~~~~~    .'       ",
            "         `---------'         ",
        ],
    },
    {
        "name": "Mars",
        "type": "TERRESTRIAL PLANET",
        "diameter_km": "6,792 km",
        "distance_au": "1.52 AU",
        "distance_km": "227.9 million km",
        "orbital_period": "687 Earth days",
        "moons": 2,
        "surface_temp": "−125°C to +20°C",
        "atmosphere": "Thin CO₂ (95%)",
        "notable": "Home to Olympus Mons, tallest volcano in Solar System",
        "fun_fact": (
            "Olympus Mons on Mars is three times taller than Mount Everest and so wide that "
            "if you stood at its base, the summit would be over the horizon. Mars has the "
            "longest canyon system in the Solar System: Valles Marineris, 4,000 km long."
        ),
        "size_rank": 7,
        "ascii_art": [
            "        .--------.        ",
            "       ( -------- )       ",
            "      /  . o . o . \\     ",
            "     |  o . . . . o |     ",
            "     |  . o . o . . |     ",
            "     |  o . . o . . |     ",
            "      \\  . . o . . /     ",
            "       ( -------- )       ",
            "        `--------'        ",
        ],
    },
    {
        "name": "Jupiter",
        "type": "GAS GIANT",
        "diameter_km": "142,984 km",
        "distance_au": "5.20 AU",
        "distance_km": "778.5 million km",
        "orbital_period": "~12 Earth years",
        "moons": 95,
        "surface_temp": "−108°C (cloud tops)",
        "atmosphere": "Hydrogen (89%), helium (10%)",
        "notable": "Great Red Spot — storm larger than Earth, raging 350+ years",
        "fun_fact": (
            "Jupiter is so massive that it doesn't actually orbit the Sun — both Jupiter and "
            "the Sun orbit a common point (barycenter) that lies just outside the Sun's surface. "
            "Its moon Europa likely has a liquid water ocean beneath its icy crust."
        ),
        "size_rank": 1,
        "ascii_art": [
            "            .-----------.            ",
            "          .'  ~~~~~~~~~~ '.          ",
            "         /  ~~~~~~~~~~~~~~  \\       ",
            "        |  ================  |       ",
            "        |  ~~~~~~~~~~~~~~    |       ",
            "        |  ================  |       ",
            "        |  ~~~( @ )~~~~~~~~  |       ",
            "        |  ================  |       ",
            "        |  ~~~~~~~~~~~~~~    |       ",
            "         \\  ==============  /       ",
            "          '.  ~~~~~~~~~~~ .'         ",
            "            `-----------'            ",
        ],
    },
    {
        "name": "Saturn",
        "type": "GAS GIANT",
        "diameter_km": "120,536 km",
        "distance_au": "9.54 AU",
        "distance_km": "1.43 billion km",
        "orbital_period": "~29 Earth years",
        "moons": 146,
        "surface_temp": "−138°C (cloud tops)",
        "atmosphere": "Hydrogen (96%), helium (3%)",
        "notable": "Ring system extends up to 282,000 km from the planet",
        "fun_fact": (
            "Saturn is the least dense planet — it would float in water if you could find a "
            "bathtub big enough. Its rings are made mostly of ice and rock, but are only about "
            "10–20 metres thick despite being hundreds of thousands of kilometres wide."
        ),
        "size_rank": 2,
        "ascii_art": [
            "  ─────────────────────────  ",
            "          .---------.        ",
            "        .'  ~~~~~~~  '.      ",
            "       /  ~~~~~~~~~~~  \\    ",
            "      |  ~~~~~~~~~~~~~  |    ",
            "       \\  ~~~~~~~~~~~  /    ",
            "        '.  ~~~~~~~  .'      ",
            "          `---------'        ",
            "  ─────────────────────────  ",
        ],
    },
    {
        "name": "Uranus",
        "type": "ICE GIANT",
        "diameter_km": "51,118 km",
        "distance_au": "19.2 AU",
        "distance_km": "2.87 billion km",
        "orbital_period": "~84 Earth years",
        "moons": 27,
        "surface_temp": "−195°C (avg)",
        "atmosphere": "Hydrogen, helium, methane (gives blue colour)",
        "notable": "Rotates on its side — axial tilt of 98°",
        "fun_fact": (
            "Uranus rotates on its side, possibly because of a massive collision billions of "
            "years ago. This means each pole experiences 42 years of continuous sunlight, then "
            "42 years of darkness. It's the coldest planetary atmosphere in the Solar System."
        ),
        "size_rank": 3,
        "ascii_art": [
            "  |        .·:::::·.        |  ",
            "  |      .'  ~~~~~~~  '.    |  ",
            "  |     /  ~~~~~~~~~~ \\    |  ",
            "  |    |  ~~~~~~~~~~~~  |   |  ",
            "  |    |  ~~~~~~~~~~~~  |   |  ",
            "  |     \\  ~~~~~~~~~~ /    |  ",
            "  |      '.  ~~~~~~~  .'   |  ",
            "  |        '·:::::·'       |  ",
        ],
    },
    {
        "name": "Neptune",
        "type": "ICE GIANT",
        "diameter_km": "49,528 km",
        "distance_au": "30.1 AU",
        "distance_km": "4.50 billion km",
        "orbital_period": "~165 Earth years",
        "moons": 14,
        "surface_temp": "−200°C (avg)",
        "atmosphere": "Hydrogen, helium, methane",
        "notable": "Fastest winds in the Solar System — up to 2,100 km/h",
        "fun_fact": (
            "Neptune was predicted mathematically before it was ever observed — astronomers "
            "noticed Uranus was being pulled off course and calculated where an unknown planet "
            "must be. It has only completed one orbit since its discovery in 1846."
        ),
        "size_rank": 4,
        "ascii_art": [
            "         .·::::·.          ",
            "       .'  ~~~~~~  '.      ",
            "      /  ~~~~~~~~~~  \\    ",
            "     |  ~~ [   ] ~~~  |    ",
            "     |  ~~ [   ] ~~~  |    ",
            "     |  ~~ [   ] ~~~  |    ",
            "      \\  ~~~~~~~~~~  /    ",
            "       '.  ~~~~~~  .'      ",
            "         '·::::·'          ",
        ],
    },
    {
        "name": "Pluto",
        "type": "DWARF PLANET",
        "diameter_km": "2,376 km",
        "distance_au": "39.5 AU",
        "distance_km": "5.91 billion km",
        "orbital_period": "~248 Earth years",
        "moons": 5,
        "surface_temp": "−225°C to −215°C",
        "atmosphere": "Thin nitrogen, methane, CO",
        "notable": "Heart-shaped nitrogen ice plain: Tombaugh Regio",
        "fun_fact": (
            "When Pluto was discovered in 1930, a young girl named Venetia Burney (age 11) "
            "suggested the name. New Horizons flew past in 2015 and revealed a surprisingly "
            "complex world with mountains made of water ice and a heart-shaped glacier."
        ),
        "size_rank": 9,
        "ascii_art": [
            "      .-----.      ",
            "     / . o . \\    ",
            "    | . <3 .  |    ",
            "     \\ . . . /    ",
            "      `-----'      ",
        ],
    },
]

_by_id = {i: p for i, p in enumerate(PLANETS)}


def handle(path_parts: list[str]) -> tuple[int, dict, dict]:
    if not path_parts or path_parts[0] == "random":
        idx = random.randrange(len(PLANETS))
        planet = dict(PLANETS[idx])
        planet["index"] = idx
        planet["total"] = len(PLANETS)
        return 200, planet, {}

    if path_parts[0] == "count":
        return 200, {"total": len(PLANETS)}, {}

    try:
        idx = int(path_parts[0])
        if 0 <= idx < len(PLANETS):
            planet = dict(PLANETS[idx])
            planet["index"] = idx
            planet["total"] = len(PLANETS)
            return 200, planet, {}
        return 404, {"error": "index out of range"}, {}
    except ValueError:
        return 400, {"error": "invalid id"}, {}
