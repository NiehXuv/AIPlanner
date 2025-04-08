# backend/data/pois.py
hardcoded_pois = {
    "Paris": [
        {"name": "Eiffel Tower", "category": "LANDMARK"},
        {"name": "Louvre Museum", "category": "MUSEUM"},
        {"name": "Notre-Dame Cathedral", "category": "HISTORIC"},
        {"name": "Sacré-Cœur Basilica", "category": "HISTORIC"},
        {"name": "Champs-Élysées", "category": "SIGHTSEEING"},
        {"name": "Arc de Triomphe", "category": "MONUMENT"},
        {"name": "Luxembourg Gardens", "category": "PARK"},
        {"name": "Musée d'Orsay", "category": "MUSEUM"},
        {"name": "Montmartre", "category": "SIGHTSEEING"},
        {"name": "Palace of Versailles", "category": "HISTORIC"},
        {"name": "Sainte-Chapelle", "category": "HISTORIC"},
        {"name": "Centre Pompidou", "category": "MUSEUM"},
        {"name": "Jardin des Tuileries", "category": "PARK"},
        {"name": "Panthéon", "category": "HISTORIC"},
        {"name": "Les Invalides", "category": "HISTORIC"},
        {"name": "Galeries Lafayette", "category": "SHOPPING"},
        {"name": "Le Marais District", "category": "SIGHTSEEING"},
        {"name": "Moulin Rouge", "category": "ENTERTAINMENT"},
        {"name": "Seine River Cruise", "category": "SIGHTSEEING"},
        {"name": "Place de la Concorde", "category": "SIGHTSEEING"},
        {"name": "Musée Rodin", "category": "MUSEUM"},
        {"name": "Catacombs of Paris", "category": "HISTORIC"},
        {"name": "Bois de Boulogne", "category": "PARK"},
        {"name": "Opéra Garnier", "category": "HISTORIC"},
        {"name": "Latin Quarter", "category": "SIGHTSEEING"}
    ],
    "Tokyo": [
        {"name": "Tokyo Skytree", "category": "LANDMARK"},
        {"name": "Senso-ji Temple", "category": "HISTORIC"},
        {"name": "Shibuya Crossing", "category": "SIGHTSEEING"},
        {"name": "Tokyo Tower", "category": "LANDMARK"},
        {"name": "Ueno Park", "category": "PARK"},
        {"name": "Akihabara District", "category": "SHOPPING"},
        {"name": "Meiji Shrine", "category": "HISTORIC"},
        {"name": "Shinjuku Gyoen National Garden", "category": "PARK"},
        {"name": "Tsukiji Fish Market", "category": "SIGHTSEEING"},
        {"name": "Harajuku Takeshita Street", "category": "SHOPPING"},
        {"name": "Imperial Palace", "category": "HISTORIC"},
        {"name": "Odaiba Island", "category": "ENTERTAINMENT"},
        {"name": "Roppongi Hills", "category": "SIGHTSEEING"},
        {"name": "Ginza Shopping District", "category": "SHOPPING"},
        {"name": "Asakusa District", "category": "SIGHTSEEING"},
        {"name": "Tokyo National Museum", "category": "MUSEUM"},
        {"name": "Yoyogi Park", "category": "PARK"},
        {"name": "Sumida Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Kabukiza Theatre", "category": "ENTERTAINMENT"},
        {"name": "DiverCity Tokyo Plaza", "category": "SHOPPING"},
        {"name": "Ghibli Museum", "category": "MUSEUM"},
        {"name": "Rikugien Gardens", "category": "PARK"},
        {"name": "Shibuya Sky", "category": "SIGHTSEEING"},
        {"name": "Nakamise Shopping Street", "category": "SHOPPING"},
        {"name": "Tokyo Disneyland", "category": "ENTERTAINMENT"}
    ],
    "Barcelona": [
        {"name": "Sagrada Família", "category": "LANDMARK"},
        {"name": "Park Güell", "category": "PARK"},
        {"name": "La Rambla", "category": "SIGHTSEEING"},
        {"name": "Casa Batlló", "category": "HISTORIC"},
        {"name": "Gothic Quarter", "category": "HISTORIC"},
        {"name": "Montjuïc Castle", "category": "HISTORIC"},
        {"name": "Picasso Museum", "category": "MUSEUM"},
        {"name": "Camp Nou Stadium", "category": "SPORT"},
        {"name": "Barceloneta Beach", "category": "BEACH"},
        {"name": "La Boqueria Market", "category": "SIGHTSEEING"},
        {"name": "Tibidabo Amusement Park", "category": "ENTERTAINMENT"},
        {"name": "Palau de la Música Catalana", "category": "HISTORIC"},
        {"name": "Ciutadella Park", "category": "PARK"},
        {"name": "Casa Milà (La Pedrera)", "category": "HISTORIC"},
        {"name": "Poble Espanyol", "category": "SIGHTSEEING"},
        {"name": "Barcelona Cathedral", "category": "HISTORIC"},
        {"name": "Magic Fountain of Montjuïc", "category": "SIGHTSEEING"},
        {"name": "Joan Miró Foundation", "category": "MUSEUM"},
        {"name": "Passeig de Gràcia", "category": "SHOPPING"},
        {"name": "Montserrat Mountain", "category": "ADVENTURE"},
        {"name": "Labyrinth Park of Horta", "category": "PARK"},
        {"name": "El Born District", "category": "SIGHTSEEING"},
        {"name": "CosmoCaixa Science Museum", "category": "MUSEUM"},
        {"name": "Port Vell", "category": "SIGHTSEEING"},
        {"name": "Barcelona Aquarium", "category": "ENTERTAINMENT"}
    ],
    "New York": [
        {"name": "Statue of Liberty", "category": "LANDMARK"},
        {"name": "Central Park", "category": "PARK"},
        {"name": "Times Square", "category": "SIGHTSEEING"},
        {"name": "Empire State Building", "category": "LANDMARK"},
        {"name": "Metropolitan Museum of Art", "category": "MUSEUM"},
        {"name": "Brooklyn Bridge", "category": "LANDMARK"},
        {"name": "One World Trade Center", "category": "LANDMARK"},
        {"name": "Broadway Show", "category": "ENTERTAINMENT"},
        {"name": "Fifth Avenue", "category": "SHOPPING"},
        {"name": "Museum of Modern Art (MoMA)", "category": "MUSEUM"},
        {"name": "Rockefeller Center", "category": "SIGHTSEEING"},
        {"name": "High Line", "category": "PARK"},
        {"name": "9/11 Memorial & Museum", "category": "HISTORIC"},
        {"name": "Grand Central Terminal", "category": "HISTORIC"},
        {"name": "Bryant Park", "category": "PARK"},
        {"name": "Wall Street", "category": "SIGHTSEEING"},
        {"name": "New York Public Library", "category": "HISTORIC"},
        {"name": "Coney Island", "category": "ENTERTAINMENT"},
        {"name": "Madison Square Garden", "category": "SPORT"},
        {"name": "Chinatown", "category": "SIGHTSEEING"},
        {"name": "Little Italy", "category": "SIGHTSEEING"},
        {"name": "The Cloisters", "category": "MUSEUM"},
        {"name": "Top of the Rock", "category": "SIGHTSEEING"},
        {"name": "SoHo District", "category": "SHOPPING"},
        {"name": "Yankee Stadium", "category": "SPORT"}
    ],
    "London": [
        {"name": "Big Ben", "category": "LANDMARK"},
        {"name": "Tower of London", "category": "HISTORIC"},
        {"name": "British Museum", "category": "MUSEUM"},
        {"name": "Buckingham Palace", "category": "HISTORIC"},
        {"name": "London Eye", "category": "LANDMARK"},
        {"name": "Hyde Park", "category": "PARK"},
        {"name": "Westminster Abbey", "category": "HISTORIC"},
        {"name": "Trafalgar Square", "category": "SIGHTSEEING"},
        {"name": "St. Paul’s Cathedral", "category": "HISTORIC"},
        {"name": "Tate Modern", "category": "MUSEUM"},
        {"name": "Covent Garden", "category": "SIGHTSEEING"},
        {"name": "Piccadilly Circus", "category": "SIGHTSEEING"},
        {"name": "Kensington Gardens", "category": "PARK"},
        {"name": "Natural History Museum", "category": "MUSEUM"},
        {"name": "The Shard", "category": "LANDMARK"},
        {"name": "Camden Market", "category": "SHOPPING"},
        {"name": "Oxford Street", "category": "SHOPPING"},
        {"name": "Madame Tussauds", "category": "ENTERTAINMENT"},
        {"name": "Regent’s Park", "category": "PARK"},
        {"name": "Shakespeare’s Globe", "category": "HISTORIC"},
        {"name": "London Zoo", "category": "ENTERTAINMENT"},
        {"name": "Hampton Court Palace", "category": "HISTORIC"},
        {"name": "Greenwich Park", "category": "PARK"},
        {"name": "Royal Observatory Greenwich", "category": "SIGHTSEEING"},
        {"name": "West End Theatre", "category": "ENTERTAINMENT"}
    ],
    "Rome": [
        {"name": "Colosseum", "category": "HISTORIC"},
        {"name": "Roman Forum", "category": "HISTORIC"},
        {"name": "Pantheon", "category": "HISTORIC"},
        {"name": "Trevi Fountain", "category": "LANDMARK"},
        {"name": "Vatican Museums", "category": "MUSEUM"},
        {"name": "Sistine Chapel", "category": "HISTORIC"},
        {"name": "St. Peter’s Basilica", "category": "HISTORIC"},
        {"name": "Piazza Navona", "category": "SIGHTSEEING"},
        {"name": "Spanish Steps", "category": "SIGHTSEEING"},
        {"name": "Villa Borghese Gardens", "category": "PARK"},
        {"name": "Capitoline Museums", "category": "MUSEUM"},
        {"name": "Castel Sant’Angelo", "category": "HISTORIC"},
        {"name": "Trastevere District", "category": "SIGHTSEEING"},
        {"name": "Piazza del Popolo", "category": "SIGHTSEEING"},
        {"name": "Borghese Gallery", "category": "MUSEUM"},
        {"name": "Aventine Hill", "category": "SIGHTSEEING"},
        {"name": "Campo de’ Fiori", "category": "SIGHTSEEING"},
        {"name": "Palatine Hill", "category": "HISTORIC"},
        {"name": "Baths of Caracalla", "category": "HISTORIC"},
        {"name": "Via del Corso", "category": "SHOPPING"},
        {"name": "Circus Maximus", "category": "HISTORIC"},
        {"name": "Janiculum Hill", "category": "PARK"},
        {"name": "MAXXI Museum", "category": "MUSEUM"},
        {"name": "Piazza Venezia", "category": "SIGHTSEEING"},
        {"name": "Tiber River Walk", "category": "SIGHTSEEING"}
    ],
    "Sydney": [
        {"name": "Sydney Opera House", "category": "LANDMARK"},
        {"name": "Sydney Harbour Bridge", "category": "LANDMARK"},
        {"name": "Bondi Beach", "category": "BEACH"},
        {"name": "The Rocks", "category": "HISTORIC"},
        {"name": "Taronga Zoo", "category": "ENTERTAINMENT"},
        {"name": "Royal Botanic Garden", "category": "PARK"},
        {"name": "Darling Harbour", "category": "SIGHTSEEING"},
        {"name": "Queen Victoria Building", "category": "SHOPPING"},
        {"name": "Art Gallery of New South Wales", "category": "MUSEUM"},
        {"name": "Circular Quay", "category": "SIGHTSEEING"},
        {"name": "Manly Beach", "category": "BEACH"},
        {"name": "Luna Park Sydney", "category": "ENTERTAINMENT"},
        {"name": "Hyde Park", "category": "PARK"},
        {"name": "Australian Museum", "category": "MUSEUM"},
        {"name": "Centennial Parklands", "category": "PARK"},
        {"name": "Paddy’s Markets", "category": "SHOPPING"},
        {"name": "Sydney Tower Eye", "category": "LANDMARK"},
        {"name": "Wendy’s Secret Garden", "category": "PARK"},
        {"name": "Cockatoo Island", "category": "HISTORIC"},
        {"name": "Blue Mountains", "category": "ADVENTURE"},
        {"name": "Sea Life Sydney Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Barangaroo Reserve", "category": "PARK"},
        {"name": "Powerhouse Museum", "category": "MUSEUM"},
        {"name": "Mrs Macquarie’s Chair", "category": "SIGHTSEEING"},
        {"name": "Bondi to Coogee Coastal Walk", "category": "ADVENTURE"}
    ],
    "Dubai": [
        {"name": "Burj Khalifa", "category": "LANDMARK"},
        {"name": "Dubai Mall", "category": "SHOPPING"},
        {"name": "Palm Jumeirah", "category": "SIGHTSEEING"},
        {"name": "Burj Al Arab", "category": "LANDMARK"},
        {"name": "Dubai Marina", "category": "SIGHTSEEING"},
        {"name": "Desert Safari", "category": "ADVENTURE"},
        {"name": "Jumeirah Beach", "category": "BEACH"},
        {"name": "Dubai Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Gold Souk", "category": "SHOPPING"},
        {"name": "Ski Dubai", "category": "ENTERTAINMENT"},
        {"name": "Dubai Fountain", "category": "SIGHTSEEING"},
        {"name": "Atlantis The Palm", "category": "ENTERTAINMENT"},
        {"name": "Global Village", "category": "ENTERTAINMENT"},
        {"name": "Al Fahidi Historic District", "category": "HISTORIC"},
        {"name": "Dubai Museum", "category": "MUSEUM"},
        {"name": "Jumeirah Mosque", "category": "HISTORIC"},
        {"name": "Mall of the Emirates", "category": "SHOPPING"},
        {"name": "Dubai Frame", "category": "LANDMARK"},
        {"name": "Miracle Garden", "category": "PARK"},
        {"name": "Kite Beach", "category": "BEACH"},
        {"name": "Deira Spice Souk", "category": "SHOPPING"},
        {"name": "IMG Worlds of Adventure", "category": "ENTERTAINMENT"},
        {"name": "Hatta Heritage Village", "category": "HISTORIC"},
        {"name": "Dubai Creek", "category": "SIGHTSEEING"},
        {"name": "Wild Wadi Waterpark", "category": "ENTERTAINMENT"}
    ],
    "Singapore": [
        {"name": "Marina Bay Sands", "category": "LANDMARK"},
        {"name": "Gardens by the Bay", "category": "PARK"},
        {"name": "Sentosa Island", "category": "ENTERTAINMENT"},
        {"name": "Merlion Park", "category": "LANDMARK"},
        {"name": "Universal Studios Singapore", "category": "ENTERTAINMENT"},
        {"name": "Orchard Road", "category": "SHOPPING"},
        {"name": "Singapore Zoo", "category": "ENTERTAINMENT"},
        {"name": "Chinatown", "category": "SIGHTSEEING"},
        {"name": "Little India", "category": "SIGHTSEEING"},
        {"name": "Clarke Quay", "category": "SIGHTSEEING"},
        {"name": "National Gallery Singapore", "category": "MUSEUM"},
        {"name": "Botanic Gardens", "category": "PARK"},
        {"name": "Haw Par Villa", "category": "SIGHTSEEING"},
        {"name": "Jurong Bird Park", "category": "ENTERTAINMENT"},
        {"name": "S.E.A. Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Fort Canning Park", "category": "PARK"},
        {"name": "Buddha Tooth Relic Temple", "category": "HISTORIC"},
        {"name": "Haji Lane", "category": "SHOPPING"},
        {"name": "Singapore Flyer", "category": "LANDMARK"},
        {"name": "Peranakan Museum", "category": "MUSEUM"},
        {"name": "East Coast Park", "category": "PARK"},
        {"name": "Pulau Ubin", "category": "ADVENTURE"},
        {"name": "ArtScience Museum", "category": "MUSEUM"},
        {"name": "Kampong Glam", "category": "SIGHTSEEING"},
        {"name": "Night Safari", "category": "ENTERTAINMENT"}
    ],
    "Cape Town": [
        {"name": "Table Mountain", "category": "LANDMARK"},
        {"name": "Cape of Good Hope", "category": "SIGHTSEEING"},
        {"name": "Robben Island", "category": "HISTORIC"},
        {"name": "V&A Waterfront", "category": "SIGHTSEEING"},
        {"name": "Kirstenbosch Botanical Gardens", "category": "PARK"},
        {"name": "Boulders Beach", "category": "BEACH"},
        {"name": "Lion’s Head", "category": "ADVENTURE"},
        {"name": "District Six Museum", "category": "MUSEUM"},
        {"name": "Cape Point", "category": "SIGHTSEEING"},
        {"name": "Bo-Kaap", "category": "HISTORIC"},
        {"name": "Clifton Beaches", "category": "BEACH"},
        {"name": "Greenmarket Square", "category": "SHOPPING"},
        {"name": "Signal Hill", "category": "SIGHTSEEING"},
        {"name": "Two Oceans Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Hout Bay", "category": "SIGHTSEEING"},
        {"name": "Iziko South African Museum", "category": "MUSEUM"},
        {"name": "Camps Bay Beach", "category": "BEACH"},
        {"name": "Company’s Garden", "category": "PARK"},
        {"name": "Castle of Good Hope", "category": "HISTORIC"},
        {"name": "Chapman’s Peak Drive", "category": "SIGHTSEEING"},
        {"name": "Muizenberg Beach", "category": "BEACH"},
        {"name": "Old Biscuit Mill", "category": "SHOPPING"},
        {"name": "Zeitz MOCAA", "category": "MUSEUM"},
        {"name": "Table Mountain Aerial Cableway", "category": "ADVENTURE"},
        {"name": "Stellenbosch Wine Region", "category": "SIGHTSEEING"}
    ],
    "Rio de Janeiro": [
        {"name": "Christ the Redeemer", "category": "LANDMARK"},
        {"name": "Sugarloaf Mountain", "category": "LANDMARK"},
        {"name": "Copacabana Beach", "category": "BEACH"},
        {"name": "Ipanema Beach", "category": "BEACH"},
        {"name": "Maracanã Stadium", "category": "SPORT"},
        {"name": "Tijuca National Park", "category": "PARK"},
        {"name": "Selarón Steps", "category": "SIGHTSEEING"},
        {"name": "Santa Teresa Neighborhood", "category": "SIGHTSEEING"},
        {"name": "Lapa Arches", "category": "HISTORIC"},
        {"name": "Museum of Tomorrow", "category": "MUSEUM"},
        {"name": "Botanical Garden", "category": "PARK"},
        {"name": "Sambadrome Marquês de Sapucaí", "category": "ENTERTAINMENT"},
        {"name": "Flamengo Park", "category": "PARK"},
        {"name": "Carioca Aqueduct", "category": "HISTORIC"},
        {"name": "Pedra do Sal", "category": "HISTORIC"},
        {"name": "Lagoa Rodrigo de Freitas", "category": "SIGHTSEEING"},
        {"name": "National Historical Museum", "category": "MUSEUM"},
        {"name": "Prainha Beach", "category": "BEACH"},
        {"name": "Corcovado Mountain", "category": "ADVENTURE"},
        {"name": "Downtown Rio (Centro)", "category": "SIGHTSEEING"},
        {"name": "Leblon Beach", "category": "BEACH"},
        {"name": "Parque Lage", "category": "PARK"},
        {"name": "Niterói Contemporary Art Museum", "category": "MUSEUM"},
        {"name": "Saara Market", "category": "SHOPPING"},
        {"name": "Pedra da Gávea", "category": "ADVENTURE"}
    ],
    "Bangkok": [
        {"name": "Grand Palace", "category": "HISTORIC"},
        {"name": "Wat Arun", "category": "HISTORIC"},
        {"name": "Wat Pho", "category": "HISTORIC"},
        {"name": "Chatuchak Weekend Market", "category": "SHOPPING"},
        {"name": "Jim Thompson House", "category": "MUSEUM"},
        {"name": "Chao Phraya River", "category": "SIGHTSEEING"},
        {"name": "Khao San Road", "category": "SIGHTSEEING"},
        {"name": "MBK Center", "category": "SHOPPING"},
        {"name": "Lumpini Park", "category": "PARK"},
        {"name": "Asiatique The Riverfront", "category": "SIGHTSEEING"},
        {"name": "Siam Paragon", "category": "SHOPPING"},
        {"name": "Erawan Shrine", "category": "HISTORIC"},
        {"name": "Bangkok National Museum", "category": "MUSEUM"},
        {"name": "Floating Markets", "category": "SIGHTSEEING"},
        {"name": "Safari World", "category": "ENTERTAINMENT"},
        {"name": "Sukhumvit Road", "category": "SIGHTSEEING"},
        {"name": "Wat Benchamabophit", "category": "HISTORIC"},
        {"name": "Siam Square", "category": "SHOPPING"},
        {"name": "Sea Life Bangkok Ocean World", "category": "ENTERTAINMENT"},
        {"name": "Benjakitti Park", "category": "PARK"},
        {"name": "Patpong Night Market", "category": "SHOPPING"},
        {"name": "Museum Siam", "category": "MUSEUM"},
        {"name": "Golden Mount (Wat Saket)", "category": "HISTORIC"},
        {"name": "Ratchada Train Night Market", "category": "SHOPPING"},
        {"name": "Ayutthaya Day Trip", "category": "ADVENTURE"}
    ],
    "Istanbul": [
        {"name": "Hagia Sophia", "category": "HISTORIC"},
        {"name": "Topkapi Palace", "category": "HISTORIC"},
        {"name": "Blue Mosque", "category": "HISTORIC"},
        {"name": "Grand Bazaar", "category": "SHOPPING"},
        {"name": "Spice Bazaar", "category": "SHOPPING"},
        {"name": "Bosphorus Cruise", "category": "SIGHTSEEING"},
        {"name": "Dolmabahçe Palace", "category": "HISTORIC"},
        {"name": "Süleymaniye Mosque", "category": "HISTORIC"},
        {"name": "Taksim Square", "category": "SIGHTSEEING"},
        {"name": "Istiklal Avenue", "category": "SIGHTSEEING"},
        {"name": "Basilica Cistern", "category": "HISTORIC"},
        {"name": "Galata Tower", "category": "LANDMARK"},
        {"name": "Chora Church", "category": "HISTORIC"},
        {"name": "Istanbul Archaeology Museums", "category": "MUSEUM"},
        {"name": "Princes’ Islands", "category": "SIGHTSEEING"},
        {"name": "Gülhane Park", "category": "PARK"},
        {"name": "Maiden’s Tower", "category": "LANDMARK"},
        {"name": "Emirgan Park", "category": "PARK"},
        {"name": "Miniatürk", "category": "ENTERTAINMENT"},
        {"name": "Pera Museum", "category": "MUSEUM"},
        {"name": "Ortaköy Mosque", "category": "HISTORIC"},
        {"name": "Kadiköy Market", "category": "SHOPPING"},
        {"name": "Belgrad Forest", "category": "PARK"},
        {"name": "Vialand Theme Park", "category": "ENTERTAINMENT"},
        {"name": "Camlica Hill", "category": "SIGHTSEEING"}
    ],
    "Seoul": [
        {"name": "Gyeongbokgung Palace", "category": "HISTORIC"},
        {"name": "N Seoul Tower", "category": "LANDMARK"},
        {"name": "Myeongdong Shopping Street", "category": "SHOPPING"},
        {"name": "Bukchon Hanok Village", "category": "HISTORIC"},
        {"name": "Dongdaemun Design Plaza", "category": "SIGHTSEEING"},
        {"name": "Han River Park", "category": "PARK"},
        {"name": "Lotte World Tower", "category": "LANDMARK"},
        {"name": "Insadong", "category": "SIGHTSEEING"},
        {"name": "National Museum of Korea", "category": "MUSEUM"},
        {"name": "Namdaemun Market", "category": "SHOPPING"},
        {"name": "Changdeokgung Palace", "category": "HISTORIC"},
        {"name": "Seoul Forest", "category": "PARK"},
        {"name": "Hongdae Street", "category": "SIGHTSEEING"},
        {"name": "Everland Theme Park", "category": "ENTERTAINMENT"},
        {"name": "Gwangjang Market", "category": "SHOPPING"},
        {"name": "Cheonggyecheon Stream", "category": "SIGHTSEEING"},
        {"name": "Namsan Park", "category": "PARK"},
        {"name": "Leeum Samsung Museum of Art", "category": "MUSEUM"},
        {"name": "Itaewon District", "category": "SIGHTSEEING"},
        {"name": "Lotte World Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Jogyesa Temple", "category": "HISTORIC"},
        {"name": "Seodaemun Prison History Hall", "category": "MUSEUM"},
        {"name": "Bongeunsa Temple", "category": "HISTORIC"},
        {"name": "Gangnam District", "category": "SIGHTSEEING"},
        {"name": "Nami Island Day Trip", "category": "ADVENTURE"}
    ],
    "Amsterdam": [
        {"name": "Rijksmuseum", "category": "MUSEUM"},
        {"name": "Van Gogh Museum", "category": "MUSEUM"},
        {"name": "Anne Frank House", "category": "HISTORIC"},
        {"name": "Dam Square", "category": "SIGHTSEEING"},
        {"name": "Vondelpark", "category": "PARK"},
        {"name": "Canal Cruise", "category": "SIGHTSEEING"},
        {"name": "Red Light District", "category": "SIGHTSEEING"},
        {"name": "Jordaan Neighborhood", "category": "SIGHTSEEING"},
        {"name": "Heineken Experience", "category": "ENTERTAINMENT"},
        {"name": "Royal Palace Amsterdam", "category": "HISTORIC"},
        {"name": "Stedelijk Museum", "category": "MUSEUM"},
        {"name": "Albert Cuyp Market", "category": "SHOPPING"},
        {"name": "Westerkerk", "category": "HISTORIC"},
        {"name": "Amsterdam Museum", "category": "MUSEUM"},
        {"name": "Keukenhof Gardens", "category": "PARK"},
        {"name": "De Pijp District", "category": "SIGHTSEEING"},
        {"name": "NEMO Science Museum", "category": "MUSEUM"},
        {"name": "Oude Kerk", "category": "HISTORIC"},
        {"name": "Flower Market", "category": "SHOPPING"},
        {"name": "Artis Zoo", "category": "ENTERTAINMENT"},
        {"name": "Hortus Botanicus", "category": "PARK"},
        {"name": "Rembrandt House Museum", "category": "MUSEUM"},
        {"name": "Zaanse Schans Windmills", "category": "SIGHTSEEING"},
        {"name": "Museumplein", "category": "SIGHTSEEING"},
        {"name": "A’DAM Lookout", "category": "LANDMARK"}
    ],
    "Prague": [
        {"name": "Prague Castle", "category": "HISTORIC"},
        {"name": "Charles Bridge", "category": "LANDMARK"},
        {"name": "Old Town Square", "category": "SIGHTSEEING"},
        {"name": "Astronomical Clock", "category": "LANDMARK"},
        {"name": "St. Vitus Cathedral", "category": "HISTORIC"},
        {"name": "Vyšehrad", "category": "HISTORIC"},
        {"name": "Petřín Hill", "category": "PARK"},
        {"name": "Jewish Quarter", "category": "HISTORIC"},
        {"name": "National Museum", "category": "MUSEUM"},
        {"name": "Wenceslas Square", "category": "SIGHTSEEING"},
        {"name": "Letná Park", "category": "PARK"},
        {"name": "Prague Zoo", "category": "ENTERTAINMENT"},
        {"name": "Kampa Island", "category": "SIGHTSEEING"},
        {"name": "Municipal House", "category": "HISTORIC"},
        {"name": "Franz Kafka Museum", "category": "MUSEUM"},
        {"name": "Palladium Shopping Centre", "category": "SHOPPING"},
        {"name": "Dancing House", "category": "LANDMARK"},
        {"name": "Strahov Monastery", "category": "HISTORIC"},
        {"name": "Lobkowicz Palace", "category": "MUSEUM"},
        {"name": "Havelské Tržiště Market", "category": "SHOPPING"},
        {"name": "Divoká Šárka", "category": "PARK"},
        {"name": "John Lennon Wall", "category": "SIGHTSEEING"},
        {"name": "National Theatre", "category": "ENTERTAINMENT"},
        {"name": "Žižkov Television Tower", "category": "LANDMARK"},
        {"name": "Karlštejn Castle Day Trip", "category": "ADVENTURE"}
    ],
    "Vienna": [
        {"name": "Schönbrunn Palace", "category": "HISTORIC"},
        {"name": "St. Stephen’s Cathedral", "category": "HISTORIC"},
        {"name": "Hofburg Palace", "category": "HISTORIC"},
        {"name": "Belvedere Palace", "category": "MUSEUM"},
        {"name": "Prater Park", "category": "PARK"},
        {"name": "Vienna State Opera", "category": "ENTERTAINMENT"},
        {"name": "Naschmarkt", "category": "SHOPPING"},
        {"name": "Albertina Museum", "category": "MUSEUM"},
        {"name": "Kunsthistorisches Museum", "category": "MUSEUM"},
        {"name": "Danube Tower", "category": "LANDMARK"},
        {"name": "Stephansplatz", "category": "SIGHTSEEING"},
        {"name": "Donauinsel", "category": "PARK"},
        {"name": "Spanish Riding School", "category": "ENTERTAINMENT"},
        {"name": "Graben Street", "category": "SHOPPING"},
        {"name": "Hundertwasserhaus", "category": "SIGHTSEEING"},
        {"name": "MuseumsQuartier", "category": "SIGHTSEEING"},
        {"name": "Vienna Zoo", "category": "ENTERTAINMENT"},
        {"name": "Augarten", "category": "PARK"},
        {"name": "Leopold Museum", "category": "MUSEUM"},
        {"name": "Kärntner Straße", "category": "SHOPPING"},
        {"name": "Rathaus (City Hall)", "category": "HISTORIC"},
        {"name": "Volksgarten", "category": "PARK"},
        {"name": "Karlskirche", "category": "HISTORIC"},
        {"name": "Mariahilfer Straße", "category": "SHOPPING"},
        {"name": "Danube River Cruise", "category": "SIGHTSEEING"}
    ],
    "San Francisco": [
        {"name": "Golden Gate Bridge", "category": "LANDMARK"},
        {"name": "Alcatraz Island", "category": "HISTORIC"},
        {"name": "Fisherman’s Wharf", "category": "SIGHTSEEING"},
        {"name": "Golden Gate Park", "category": "PARK"},
        {"name": "Pier 39", "category": "SIGHTSEEING"},
        {"name": "Lombard Street", "category": "SIGHTSEEING"},
        {"name": "San Francisco Museum of Modern Art", "category": "MUSEUM"},
        {"name": "Chinatown", "category": "SIGHTSEEING"},
        {"name": "Coit Tower", "category": "LANDMARK"},
        {"name": "Exploratorium", "category": "MUSEUM"},
        {"name": "Union Square", "category": "SHOPPING"},
        {"name": "Cable Car Ride", "category": "SIGHTSEEING"},
        {"name": "Twin Peaks", "category": "SIGHTSEEING"},
        {"name": "California Academy of Sciences", "category": "MUSEUM"},
        {"name": "Presidio of San Francisco", "category": "PARK"},
        {"name": "Ferry Building Marketplace", "category": "SHOPPING"},
        {"name": "Mission Dolores Park", "category": "PARK"},
        {"name": "Painted Ladies", "category": "HISTORIC"},
        {"name": "Oracle Park", "category": "SPORT"},
        {"name": "Haight-Ashbury District", "category": "SIGHTSEEING"},
        {"name": "Japanese Tea Garden", "category": "PARK"},
        {"name": "de Young Museum", "category": "MUSEUM"},
        {"name": "San Francisco Zoo", "category": "ENTERTAINMENT"},
        {"name": "Muir Woods National Monument", "category": "ADVENTURE"},
        {"name": "Ghirardelli Square", "category": "SIGHTSEEING"}
    ],
    "Kyoto": [
        {"name": "Fushimi Inari Shrine", "category": "HISTORIC"},
        {"name": "Kinkaku-ji (Golden Pavilion)", "category": "HISTORIC"},
        {"name": "Arashiyama Bamboo Grove", "category": "SIGHTSEEING"},
        {"name": "Kiyomizu-dera Temple", "category": "HISTORIC"},
        {"name": "Gion District", "category": "SIGHTSEEING"},
        {"name": "Nijō Castle", "category": "HISTORIC"},
        {"name": "Philosopher’s Path", "category": "SIGHTSEEING"},
        {"name": "Ryoan-ji Temple", "category": "HISTORIC"},
        {"name": "Kyoto Imperial Palace", "category": "HISTORIC"},
        {"name": "Tō-ji Temple", "category": "HISTORIC"},
        {"name": "Kyoto Tower", "category": "LANDMARK"},
        {"name": "Pontocho Alley", "category": "SIGHTSEEING"},
        {"name": "Kyoto National Museum", "category": "MUSEUM"},
        {"name": "Maruyama Park", "category": "PARK"},
        {"name": "Heian Shrine", "category": "HISTORIC"},
        {"name": "Nishiki Market", "category": "SHOPPING"},
        {"name": "Kyoto Botanical Gardens", "category": "PARK"},
        {"name": "Ginkaku-ji (Silver Pavilion)", "category": "HISTORIC"},
        {"name": "Kyoto Railway Museum", "category": "MUSEUM"},
        {"name": "Kamo River", "category": "SIGHTSEEING"},
        {"name": "Sanjūsangen-dō Temple", "category": "HISTORIC"},
        {"name": "Kyoto Aquarium", "category": "ENTERTAINMENT"},
        {"name": "Higashiyama District", "category": "SIGHTSEEING"},
        {"name": "Kyoto Handicraft Center", "category": "SHOPPING"},
        {"name": "Mount Hiei", "category": "ADVENTURE"}
    ],
    "Marrakech": [
        {"name": "Medina of Marrakech", "category": "HISTORIC"},
        {"name": "Jemaa el-Fnaa Square", "category": "SIGHTSEEING"},
        {"name": "Koutoubia Mosque", "category": "HISTORIC"},
        {"name": "Bahia Palace", "category": "HISTORIC"},
        {"name": "Majorelle Garden", "category": "PARK"},
        {"name": "Saadian Tombs", "category": "HISTORIC"},
        {"name": "Marrakech Souk", "category": "SHOPPING"},
        {"name": "El Badi Palace", "category": "HISTORIC"},
        {"name": "Menara Gardens", "category": "PARK"},
        {"name": "Dar Si Said Museum", "category": "MUSEUM"},
        {"name": "Marrakech Museum", "category": "MUSEUM"},
        {"name": "Ben Youssef Madrasa", "category": "HISTORIC"},
        {"name": "Le Jardin Secret", "category": "PARK"},
        {"name": "Palais de la Bahia", "category": "HISTORIC"},
        {"name": "Anima Garden", "category": "PARK"},
        {"name": "Yves Saint-Laurent Museum", "category": "MUSEUM"},
        {"name": "Tanneries of Marrakech", "category": "SIGHTSEEING"},
        {"name": "Oasiria Water Park", "category": "ENTERTAINMENT"},
        {"name": "Cyber Park", "category": "PARK"},
        {"name": "Ensemble Artisanal", "category": "SHOPPING"},
        {"name": "Atlas Mountains Day Trip", "category": "ADVENTURE"},
        {"name": "La Mamounia Gardens", "category": "PARK"},
        {"name": "Marrakech Ramparts", "category": "HISTORIC"},
        {"name": "Berber Villages", "category": "SIGHTSEEING"},
        {"name": "Marrakech Palm Grove", "category": "SIGHTSEEING"}
    ],
    "Edinburgh": [
        {"name": "Edinburgh Castle", "category": "HISTORIC"},
        {"name": "Royal Mile", "category": "SIGHTSEEING"},
        {"name": "Arthur’s Seat", "category": "ADVENTURE"},
        {"name": "Palace of Holyroodhouse", "category": "HISTORIC"},
        {"name": "National Museum of Scotland", "category": "MUSEUM"},
        {"name": "Calton Hill", "category": "SIGHTSEEING"},
        {"name": "Scott Monument", "category": "LANDMARK"},
        {"name": "Princes Street Gardens", "category": "PARK"},
        {"name": "St Giles’ Cathedral", "category": "HISTORIC"},
        {"name": "Scottish National Gallery", "category": "MUSEUM"},
        {"name": "Grassmarket", "category": "SIGHTSEEING"},
        {"name": "Dean Village", "category": "SIGHTSEEING"},
        {"name": "The Real Mary King’s Close", "category": "HISTORIC"},
        {"name": "Royal Botanic Garden Edinburgh", "category": "PARK"},
        {"name": "Edinburgh Zoo", "category": "ENTERTAINMENT"},
        {"name": "Greyfriars Kirkyard", "category": "HISTORIC"},
        {"name": "Victoria Street", "category": "SIGHTSEEING"},
        {"name": "Museum of Edinburgh", "category": "MUSEUM"},
        {"name": "Leith Walk", "category": "SIGHTSEEING"},
        {"name": "Dynamic Earth", "category": "ENTERTAINMENT"},
        {"name": "Portobello Beach", "category": "BEACH"},
        {"name": "Scottish Parliament Building", "category": "HISTORIC"},
        {"name": "West End", "category": "SHOPPING"},
        {"name": "Craigmillar Castle", "category": "HISTORIC"},
        {"name": "Forth Bridge Viewpoint", "category": "SIGHTSEEING"}
    ],
    "Havana": [
        {"name": "Old Havana", "category": "HISTORIC"},
        {"name": "Malecón", "category": "SIGHTSEEING"},
        {"name": "El Capitolio", "category": "HISTORIC"},
        {"name": "Plaza de la Revolución", "category": "SIGHTSEEING"},
        {"name": "Museum of the Revolution", "category": "MUSEUM"},
        {"name": "Castillo de la Real Fuerza", "category": "HISTORIC"},
        {"name": "Havana Cathedral", "category": "HISTORIC"},
        {"name": "Paseo del Prado", "category": "SIGHTSEEING"},
        {"name": "Fusterlandia", "category": "SIGHTSEEING"},
        {"name": "National Museum of Fine Arts", "category": "MUSEUM"},
        {"name": "Morro Castle", "category": "HISTORIC"},
        {"name": "Vedado District", "category": "SIGHTSEEING"},
        {"name": "Callejón de Hamel", "category": "SIGHTSEEING"},
        {"name": "Plaza Vieja", "category": "SIGHTSEEING"},
        {"name": "Necrópolis de Colón", "category": "HISTORIC"},
        {"name": "Partagás Cigar Factory", "category": "SIGHTSEEING"},
        {"name": "Gran Teatro de La Habana", "category": "ENTERTAINMENT"},
        {"name": "Hotel Nacional de Cuba", "category": "HISTORIC"},
        {"name": "La Bodeguita del Medio", "category": "SIGHTSEEING"},
        {"name": "El Floridita Bar", "category": "SIGHTSEEING"},
        {"name": "Playas del Este", "category": "BEACH"},
        {"name": "Finca Vigía (Hemingway’s House)", "category": "HISTORIC"},
        {"name": "Parque Almendares", "category": "PARK"},
        {"name": "Casa de la Música", "category": "ENTERTAINMENT"},
        {"name": "Viñales Valley Day Trip", "category": "ADVENTURE"}
    ]
}