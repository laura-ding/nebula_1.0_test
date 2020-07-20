# --coding:utf-8--
#
# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License,
# attached with Common Clause Condition 1.0, found in the LICENSES directory.

import sys
import time
import threading
import traceback

from graph import ttypes
from nebula.ConnectionPool import ConnectionPool
from nebula.Client import GraphClient
from nebula.Common import *

player_name_to_id_dict = {}
player_id_to_name_dict = {}
team_name_to_id_dict = {}
team_id_to_name_dict = {}
client = None

players = [
    "Tim Duncan",
    "Tony Parker",
    "LaMarcus Aldridge",
    "Rudy Gay",
    "Marco Belinelli",
    "Danny Green",
    "Kyle Anderson",
    "Aron Baynes",
    "Boris Diaw",
    "Tiago Splitter",
    "Cory Joseph",
    "David West",
    "Jonathon Simmons",
    "Dejounte Murray",
    "Tracy McGrady",
    "Kobe Bryant",
    "LeBron James",
    "Stephen Curry",
    "Russell Westbrook",
    "Kevin Durant",
    "James Harden",
    "Chris Paul",
    "DeAndre Jordan",
    "Ricky Rubio",
    "Rajon Rondo",
    "Manu Ginobili",
    "Kyrie Irving",
    "Vince Carter",
    "Carmelo Anthony",
    "Dwyane Wade",
    "Joel Embiid",
    "Paul George",
    "Giannis Antetokounmpo",
    "Yao Ming",
    "Blake Griffin",
    "Damian Lillard",
    "Steve Nash",
    "Dirk Nowitzki",
    "Paul Gasol",
    "Marc Gasol",
    "Grant Hill",
    "Ray Allen",
    "Klay Thompson",
    "Kristaps Porzingis",
    "Shaquile O'Neal",
    "JaVale McGee",
    "Dwight Howard",
    "Amar'e Stoudemire",
    "Jason Kidd",
    "Ben Simmons",
    "Luka Doncic",
    "Nobody",
]

teams = [
    "Warriors",
    "Nuggets",
    "Rockets",
    "Trail Blazers",
    "Spurs",
    "Thunders",
    "Jazz",
    "Clippers",
    "Kings",
    "Timberwolves",
    "Lakers",
    "Pelicans",
    "Grizzlies",
    "Mavericks",
    "Suns",
    "Hornets",
    "Cavaliers",
    "Celtics",
    "Raptors",
    "76ers",
    "Pacers",
    "Bulls",
    "Hawks",
    "Knicks",
    "Pistons",
    "Bucks",
    "Magic",
    "Nets",
    "Wizards",
    "Heat",
]


def insert_data():
    # prepare schema
    client.execute('CREATE SPACE IF NOT EXISTS nba(partition_num=1, replica_factor=1);'
                   'USE nba; CREATE TAG IF NOT EXISTS player(name string, age int);'
                   'CREATE TAG IF NOT EXISTS team(name string);'
                   'CREATE EDGE IF NOT EXISTS serve(start_year int, end_year int);'
                   'CREATE EDGE IF NOT EXISTS like(likeness int);'
                   'CREATE EDGE IF NOT EXISTS teammate(start_year int, end_year int);'
                   'CREATE TAG IF NOT EXISTS bachelor(name string, speciality string);')

    time.sleep(10);

    # insert vertex player
    client.execute('''
                    INSERT VERTEX player(name, age) VALUES 
                    -835937448829988801: ("Nobody",0),
                    -8379929135833483044: ("Amar'e Stoudemire",36),
                    -2953535798644081749: ("Russell Westbrook",30),
                    -7187791973189815797: ("James Harden",29),
                    -2308681984240312228: ("Kobe Bryant",40),
                    4823234394086728974: ("Tracy McGrady",39),
                    -6952676908621237908: ("Chris Paul",33),
                    -7391649757245641883: ("Boris Diaw",36),
                    -8864869605086585744: ("LeBron James",34),
                    -3159397121379009673: ("Klay Thompson",29),
                    -1808363682563220400: ("Kristaps Porzingis",23),
                    6315667670552355223: ("Jonathon Simmons",29),
                    -8206304902611825447: ("Marco Belinelli",32),
                    -1527627220316645914: ("Luka Doncic",20),
                    2922505246153125262: ("David West",38),
                    -7579316172763586624: ("Tony Parker",36),
                    -4246510323023722591: ("Danny Green",31),
                    -3212290852619976819: ("Rudy Gay",32),
                    -1782445125509592239: ("LaMarcus Aldridge",33),
                    5662213458193308137: ("Tim Duncan",42),
                    3778194419743477824: ("Kevin Durant",30),
                    8136836558163210487: ("Stephen Curry",31),
                    7749522836357656167: ("Ray Allen",43),
                    -8160811731890648949: ("Tiago Splitter",34),
                    2357802964435032110: ("DeAndre Jordan",30),
                    8988238998692066522: ("Paul Gasol",38),
                    -7034133662712739796: ("Aron Baynes",32),
                    -2020854379915135447: ("Cory Joseph",27),
                    -6581004839648359804: ("Vince Carter",42),
                    -2748242588091293411: ("Marc Gasol",34),
                    8939337962333576684: ("Ricky Rubio",28),
                    -3310404127039111439: ("Ben Simmons",22),
                    -2500659820593255893: ("Giannis Antetokounmpo",24),
                    -7984366606588005471: ("Rajon Rondo",33),
                    3394245602834314645: ("Manu Ginobili",41),
                    -7276938555819111674: ("Kyrie Irving",26),
                    -4722009539442865199: ("Carmelo Anthony",34),
                    -4725743394557506923: ("Dwyane Wade",37),
                    -7419439655175297510: ("Joel Embiid",25),
                    -8899043049306086446: ("Damian Lillard",28),
                    4651420795228053868: ("Yao Ming",38),
                    -8310021930715358072: ("Kyle Anderson",25),
                    5209979940224249985: ("Dejounte Murray",29),
                    -6761803129056739448: ("Blake Griffin",30),
                    6663720087669302163: ("Steve Nash",45),
                    7339407009759737412: ("Jason Kidd",45),
                    8666973159269157201: ("Dirk Nowitzki",40),
                    4312213929524069862: ("Paul George",28),
                    6293765385213992205: ("Grant Hill",46),
                    -7176373918218927568: ("Shaquile O'Neal",47),
                    -6714656557196607176: ("JaVale McGee",31),
                    -7291604415594599833: ("Dwight Howard",33)
                    ''')

    # insert vertex player with uuid
    client.execute('''
                    INSERT VERTEX player(name, age) VALUES 
                    uuid("Nobody"): ("Nobody",0),
                    uuid("Amar'e Stoudemire"): ("Amar'e Stoudemire",36),
                    uuid("Russell Westbrook"): ("Russell Westbrook",30),
                    uuid("James Harden"): ("James Harden",29),
                    uuid("Kobe Bryant"): ("Kobe Bryant",40),
                    uuid("Tracy McGrady"): ("Tracy McGrady",39),
                    uuid("Chris Paul"): ("Chris Paul",33),
                    uuid("Boris Diaw"): ("Boris Diaw",36),
                    uuid("LeBron James"): ("LeBron James",34),
                    uuid("Klay Thompson"): ("Klay Thompson",29),
                    uuid("Kristaps Porzingis"): ("Kristaps Porzingis",23),
                    uuid("Jonathon Simmons"): ("Jonathon Simmons",29),
                    uuid("Marco Belinelli"): ("Marco Belinelli",32),
                    uuid("Luka Doncic"): ("Luka Doncic",20),
                    uuid("David West"): ("David West",38),
                    uuid("Tony Parker"): ("Tony Parker",36),
                    uuid("Danny Green"): ("Danny Green",31),
                    uuid("Rudy Gay"): ("Rudy Gay",32),
                    uuid("LaMarcus Aldridge"): ("LaMarcus Aldridge",33),
                    uuid("Tim Duncan"): ("Tim Duncan",42),
                    uuid("Kevin Durant"): ("Kevin Durant",30),
                    uuid("Stephen Curry"): ("Stephen Curry",31),
                    uuid("Ray Allen"): ("Ray Allen",43),
                    uuid("Tiago Splitter"): ("Tiago Splitter",34),
                    uuid("DeAndre Jordan"): ("DeAndre Jordan",30),
                    uuid("Paul Gasol"): ("Paul Gasol",38),
                    uuid("Aron Baynes"): ("Aron Baynes",32),
                    uuid("Cory Joseph"): ("Cory Joseph",27),
                    uuid("Vince Carter"): ("Vince Carter",42),
                    uuid("Marc Gasol"): ("Marc Gasol",34),
                    uuid("Ricky Rubio"): ("Ricky Rubio",28),
                    uuid("Ben Simmons"): ("Ben Simmons",22),
                    uuid("Giannis Antetokounmpo"): ("Giannis Antetokounmpo",24),
                    uuid("Rajon Rondo"): ("Rajon Rondo",33),
                    uuid("Manu Ginobili"): ("Manu Ginobili",41),
                    uuid("Kyrie Irving"): ("Kyrie Irving",26),
                    uuid("Carmelo Anthony"): ("Carmelo Anthony",34),
                    uuid("Dwyane Wade"): ("Dwyane Wade",37),
                    uuid("Joel Embiid"): ("Joel Embiid",25),
                    uuid("Damian Lillard"): ("Damian Lillard",28),
                    uuid("Yao Ming"): ("Yao Ming",38),
                    uuid("Kyle Anderson"): ("Kyle Anderson",25),
                    uuid("Dejounte Murray"): ("Dejounte Murray",29),
                    uuid("Blake Griffin"): ("Blake Griffin",30),
                    uuid("Steve Nash"): ("Steve Nash",45),
                    uuid("Jason Kidd"): ("Jason Kidd",45),
                    uuid("Dirk Nowitzki"): ("Dirk Nowitzki",40),
                    uuid("Paul George"): ("Paul George",28),
                    uuid("Grant Hill"): ("Grant Hill",46),
                    uuid("Shaquile O'Neal"): ("Shaquile O'Neal",47),
                    uuid("JaVale McGee"): ("JaVale McGee",31),
                    uuid("Dwight Howard"): ("Dwight Howard",33)
                    ''')

    # insert vertex team
    client.execute('''
                    INSERT VERTEX team(name) VALUES 
                    -2318401216565722165: ("Nets"),
                    -2742277443392542725: ("Pistons"),
                    5806152984018701956: ("Bucks"),
                    7011978635221384332: ("Mavericks"),
                    -4249073228602996854: ("Clippers"),
                    -2708974440339147602: ("Thunders"),
                    4896863909272272220: ("Lakers"),
                    -387811533900522498: ("Jazz"),
                    -8700501352446189652: ("Nuggets"),
                    7810074228982596296: ("Wizards"),
                    -1309840256273367735: ("Pacers"),
                    6725794663354105876: ("Timberwolves"),
                    3973677957398111287: ("Hawks"),
                    -3911019097593851745: ("Warriors"),
                    -9110170398241263635: ("Magic"),
                    -7081823478649345536: ("Rockets"),
                    2851446500980388888: ("Pelicans"),
                    635461671590608292: ("Raptors"),
                    7193291116733635180: ("Spurs"),
                    -5725771886986242911: ("Heat"),
                    8076177756672387643: ("Grizzlies"),
                    -24407060583402289: ("Knicks"),
                    868103967282670864: ("Suns"),
                    1106406639891543428: ("Hornets"),
                    -8630442141511519924: ("Cavaliers"),
                    2219497852896967815: ("Kings"),
                    7739801094663213767: ("Celtics"),
                    4349533032529872265: ("76ers"),
                    8319893554523355767: ("Trail Blazers"),
                    7276941027486377550: ("Bulls")
                    ''')

    # insert vertex team with uuid
    client.execute('''
                    INSERT VERTEX team(name) VALUES uuid("Nets"): ("Nets"),
                    uuid("Pistons"): ("Pistons"),
                    uuid("Bucks"): ("Bucks"),
                    uuid("Mavericks"): ("Mavericks"),
                    uuid("Clippers"): ("Clippers"),
                    uuid("Thunders"): ("Thunders"),
                    uuid("Lakers"): ("Lakers"),
                    uuid("Jazz"): ("Jazz"),
                    uuid("Nuggets"): ("Nuggets"),
                    uuid("Wizards"): ("Wizards"),
                    uuid("Pacers"): ("Pacers"),
                    uuid("Timberwolves"): ("Timberwolves"),
                    uuid("Hawks"): ("Hawks"),
                    uuid("Warriors"): ("Warriors"),
                    uuid("Magic"): ("Magic"),
                    uuid("Rockets"): ("Rockets"),
                    uuid("Pelicans"): ("Pelicans"),
                    uuid("Raptors"): ("Raptors"),
                    uuid("Spurs"): ("Spurs"),
                    uuid("Heat"): ("Heat"),
                    uuid("Grizzlies"): ("Grizzlies"),
                    uuid("Knicks"): ("Knicks"),
                    uuid("Suns"): ("Suns"),
                    uuid("Hornets"): ("Hornets"),
                    uuid("Cavaliers"): ("Cavaliers"),
                    uuid("Kings"): ("Kings"),
                    uuid("Celtics"): ("Celtics"),
                    uuid("76ers"): ("76ers"),
                    uuid("Trail Blazers"): ("Trail Blazers"),
                    uuid("Bulls"): ("Bulls")
                    ''')

    client.execute('INSERT VERTEX bachelor(name, speciality) '
                   'VALUES 5662213458193308137: ("Tim Duncan",psychology)')

    # insert edge serve
    client.execute('''
                    INSERT EDGE serve(start_year, end_year) VALUES 
                    -8379929135833483044 -> 868103967282670864: (2002, 2010),
                    -8379929135833483044 -> -24407060583402289: (2010, 2015),
                    -8379929135833483044 -> -5725771886986242911: (2015, 2016),
                    -2953535798644081749 -> -2708974440339147602: (2008, 2019),
                    -7187791973189815797 -> -2708974440339147602: (2009, 2012),
                    -7187791973189815797 -> -7081823478649345536: (2012, 2019),
                    -2308681984240312228 -> 4896863909272272220: (1996, 2016),
                    4823234394086728974 -> 635461671590608292: (1997, 2000),
                    4823234394086728974 -> -9110170398241263635: (2000, 2004),
                    4823234394086728974 -> -7081823478649345536: (2004, 2010),
                    4823234394086728974 -> 7193291116733635180: (2013, 2013),
                    -6952676908621237908 -> 1106406639891543428: (2005, 2011),
                    -6952676908621237908 -> -4249073228602996854: (2011, 2017),
                    -6952676908621237908 -> -7081823478649345536: (2017, 2021),
                    -7391649757245641883 -> 3973677957398111287: (2003, 2005),
                    -7391649757245641883 -> 868103967282670864: (2005, 2008),
                    -7391649757245641883 -> 1106406639891543428: (2008, 2012),
                    -7391649757245641883 -> 7193291116733635180: (2012, 2016),
                    -7391649757245641883 -> -387811533900522498: (2016, 2017),
                    -8864869605086585744 -> -8630442141511519924: (2003, 2010),
                    -8864869605086585744 -> -5725771886986242911: (2010, 2014),
                    -8864869605086585744 -> -8630442141511519924: (2014, 2018),
                    -8864869605086585744 -> 4896863909272272220: (2018, 2019),
                    -3159397121379009673 -> -3911019097593851745: (2011, 2019),
                    -1808363682563220400 -> -24407060583402289: (2015, 2019),
                    -1808363682563220400 -> 7011978635221384332: (2019, 2020),
                    6315667670552355223 -> 7193291116733635180: (2015, 2017),
                    6315667670552355223 -> -9110170398241263635: (2017, 2019),
                    6315667670552355223 -> 4349533032529872265: (2019, 2019),
                    -8206304902611825447 -> -3911019097593851745: (2007, 2009),
                    -8206304902611825447 -> 635461671590608292: (2009, 2010),
                    -8206304902611825447 -> 1106406639891543428: (2010, 2012),
                    -8206304902611825447 -> 7276941027486377550: (2012, 2013),
                    -8206304902611825447 -> 7193291116733635180: (2013, 2015),
                    -8206304902611825447 -> 2219497852896967815: (2015, 2016),
                    -8206304902611825447 -> 1106406639891543428: (2016, 2017),
                    -8206304902611825447 -> 3973677957398111287: (2017, 2018),
                    -8206304902611825447 -> 4349533032529872265: (2018, 2018),
                    -8206304902611825447 -> 7193291116733635180: (2018, 2019),
                    -1527627220316645914 -> 7011978635221384332: (2018, 2019),
                    2922505246153125262 -> 1106406639891543428: (2003, 2011),
                    2922505246153125262 -> -1309840256273367735: (2011, 2015),
                    2922505246153125262 -> 7193291116733635180: (2015, 2016),
                    2922505246153125262 -> -3911019097593851745: (2016, 2018),
                    -7579316172763586624 -> 7193291116733635180: (1999, 2018),
                    -7579316172763586624 -> 1106406639891543428: (2018, 2019),
                    -4246510323023722591 -> -8630442141511519924: (2009, 2010),
                    -4246510323023722591 -> 7193291116733635180: (2010, 2018),
                    -4246510323023722591 -> 635461671590608292: (2018, 2019),
                    -3212290852619976819 -> 8076177756672387643: (2006, 2013),
                    -3212290852619976819 -> 635461671590608292: (2013, 2013),
                    -3212290852619976819 -> 2219497852896967815: (2013, 2017),
                    -3212290852619976819 -> 7193291116733635180: (2017, 2019),
                    -1782445125509592239 -> 8319893554523355767: (2006, 2015),
                    -1782445125509592239 -> 7193291116733635180: (2015, 2019),
                    5662213458193308137 -> 7193291116733635180: (1997, 2016),
                    3778194419743477824 -> -2708974440339147602: (2007, 2016),
                    3778194419743477824 -> -3911019097593851745: (2016, 2019),
                    8136836558163210487 -> -3911019097593851745: (2009, 2019),
                    7749522836357656167 -> 5806152984018701956: (1996, 2003),
                    7749522836357656167 -> -2708974440339147602: (2003, 2007),
                    7749522836357656167 -> 7739801094663213767: (2007, 2012),
                    7749522836357656167 -> -5725771886986242911: (2012, 2014),
                    -8160811731890648949 -> 7193291116733635180: (2010, 2015),
                    -8160811731890648949 -> 3973677957398111287: (2015, 2017),
                    -8160811731890648949 -> 4349533032529872265: (2017, 2017),
                    2357802964435032110 -> -4249073228602996854: (2008, 2018),
                    2357802964435032110 -> 7011978635221384332: (2018, 2019),
                    2357802964435032110 -> -24407060583402289: (2019, 2019),
                    8988238998692066522 -> 8076177756672387643: (2001, 2008),
                    8988238998692066522 -> 4896863909272272220: (2008, 2014),
                    8988238998692066522 -> 7276941027486377550: (2014, 2016),
                    8988238998692066522 -> 7193291116733635180: (2016, 2019),
                    8988238998692066522 -> 5806152984018701956: (2019, 2020),
                    -7034133662712739796 -> 7193291116733635180: (2013, 2015),
                    -7034133662712739796 -> -2742277443392542725: (2015, 2017),
                    -7034133662712739796 -> 7739801094663213767: (2017, 2019),
                    -2020854379915135447 -> 7193291116733635180: (2011, 2015),
                    -2020854379915135447 -> 635461671590608292: (2015, 2017),
                    -2020854379915135447 -> -1309840256273367735: (2017, 2019),
                    -6581004839648359804 -> 635461671590608292: (1998, 2004),
                    -6581004839648359804 -> -2318401216565722165: (2004, 2009),
                    -6581004839648359804 -> -9110170398241263635: (2009, 2010),
                    -6581004839648359804 -> 868103967282670864: (2010, 2011),
                    -6581004839648359804 -> 7011978635221384332: (2011, 2014),
                    -6581004839648359804 -> 8076177756672387643: (2014, 2017),
                    -6581004839648359804 -> 2219497852896967815: (2017, 2018),
                    -6581004839648359804 -> 3973677957398111287: (2018, 2019),
                    -2748242588091293411 -> 8076177756672387643: (2008, 2019),
                    -2748242588091293411 -> 635461671590608292: (2019, 2019),
                    8939337962333576684 -> 6725794663354105876: (2011, 2017),
                    8939337962333576684 -> -387811533900522498: (2017, 2019),
                    -3310404127039111439 -> 4349533032529872265: (2016, 2019),
                    -2500659820593255893 -> 5806152984018701956: (2013, 2019),
                    -7984366606588005471 -> 7739801094663213767: (2006, 2014),
                    -7984366606588005471 -> 7011978635221384332: (2014, 2015),
                    -7984366606588005471 -> 2219497852896967815: (2015, 2016),
                    -7984366606588005471 -> 7276941027486377550: (2016, 2017),
                    -7984366606588005471 -> 2851446500980388888: (2017, 2018),
                    -7984366606588005471 -> 4896863909272272220: (2018, 2019),
                    3394245602834314645 -> 7193291116733635180: (2002, 2018),
                    -7276938555819111674 -> -8630442141511519924: (2011, 2017),
                    -7276938555819111674 -> 7739801094663213767: (2017, 2019),
                    -4722009539442865199 -> -8700501352446189652: (2003, 2011),
                    -4722009539442865199 -> -24407060583402289: (2011, 2017),
                    -4722009539442865199 -> -2708974440339147602: (2017, 2018),
                    -4722009539442865199 -> -7081823478649345536: (2018, 2019),
                    -4725743394557506923 -> -5725771886986242911: (2003, 2016),
                    -4725743394557506923 -> 7276941027486377550: (2016, 2017),
                    -4725743394557506923 -> -8630442141511519924: (2017, 2018),
                    -4725743394557506923 -> -5725771886986242911: (2018, 2019),
                    -7419439655175297510 -> 4349533032529872265: (2014, 2019),
                    -8899043049306086446 -> 8319893554523355767: (2012, 2019),
                    4651420795228053868 -> -7081823478649345536: (2002, 2011),
                    -8310021930715358072 -> 7193291116733635180: (2014, 2018),
                    -8310021930715358072 -> 8076177756672387643: (2018, 2019),
                    5209979940224249985 -> 7193291116733635180: (2016, 2019),
                    -6761803129056739448 -> -4249073228602996854: (2009, 2018),
                    -6761803129056739448 -> -2742277443392542725: (2018, 2019),
                    6663720087669302163 -> 868103967282670864: (1996, 1998),
                    6663720087669302163 -> 7011978635221384332: (1998, 2004),
                    6663720087669302163 -> 868103967282670864: (2004, 2012),
                    6663720087669302163 -> 4896863909272272220: (2012, 2015),
                    7339407009759737412 -> 7011978635221384332: (1994, 1996),
                    7339407009759737412 -> 868103967282670864: (1996, 2001),
                    7339407009759737412 -> -2318401216565722165: (2001, 2008),
                    7339407009759737412 -> 7011978635221384332: (2008, 2012),
                    7339407009759737412 -> -24407060583402289: (2012, 2013),
                    8666973159269157201 -> 7011978635221384332: (1998, 2019),
                    4312213929524069862 -> -1309840256273367735: (2010, 2017),
                    4312213929524069862 -> -2708974440339147602: (2017, 2019),
                    6293765385213992205 -> -2742277443392542725: (1994, 2000),
                    6293765385213992205 -> -9110170398241263635: (2000, 2007),
                    6293765385213992205 -> 868103967282670864: (2007, 2012),
                    6293765385213992205 -> -4249073228602996854: (2012, 2013),
                    -7176373918218927568 -> -9110170398241263635: (1992, 1996),
                    -7176373918218927568 -> 4896863909272272220: (1996, 2004),
                    -7176373918218927568 -> -5725771886986242911: (2004, 2008),
                    -7176373918218927568 -> 868103967282670864: (2008, 2009),
                    -7176373918218927568 -> -8630442141511519924: (2009, 2010),
                    -7176373918218927568 -> 7739801094663213767: (2010, 2011),
                    -6714656557196607176 -> 7810074228982596296: (2008, 2012),
                    -6714656557196607176 -> -8700501352446189652: (2012, 2015),
                    -6714656557196607176 -> 7011978635221384332: (2015, 2016),
                    -6714656557196607176 -> -3911019097593851745: (2016, 2018),
                    -6714656557196607176 -> 4896863909272272220: (2018, 2019),
                    -7291604415594599833 -> -9110170398241263635: (2004, 2012),
                    -7291604415594599833 -> 4896863909272272220: (2012, 2013),
                    -7291604415594599833 -> -7081823478649345536: (2013, 2016),
                    -7291604415594599833 -> 3973677957398111287: (2016, 2017),
                    -7291604415594599833 -> 1106406639891543428: (2017, 2018),
                    -7291604415594599833 -> 7810074228982596296: (2018, 2019);
                    ''')

    # insert edge serve with uuid
    client.execute('''
                    INSERT EDGE serve(start_year, end_year) VALUES 
                    uuid("Amar'e Stoudemire") -> uuid("Suns"): (2002, 2010),
                    uuid("Amar'e Stoudemire") -> uuid("Knicks"): (2010, 2015),
                    uuid("Amar'e Stoudemire") -> uuid("Heat"): (2015, 2016),
                    uuid("Russell Westbrook") -> uuid("Thunders"): (2008, 2019),
                    uuid("James Harden") -> uuid("Thunders"): (2009, 2012),
                    uuid("James Harden") -> uuid("Rockets"): (2012, 2019),
                    uuid("Kobe Bryant") -> uuid("Lakers"): (1996, 2016),
                    uuid("Tracy McGrady") -> uuid("Raptors"): (1997, 2000),
                    uuid("Tracy McGrady") -> uuid("Magic"): (2000, 2004),
                    uuid("Tracy McGrady") -> uuid("Rockets"): (2004, 2010),
                    uuid("Tracy McGrady") -> uuid("Spurs"): (2013, 2013),
                    uuid("Chris Paul") -> uuid("Hornets"): (2005, 2011),
                    uuid("Chris Paul") -> uuid("Clippers"): (2011, 2017),
                    uuid("Chris Paul") -> uuid("Rockets"): (2017, 2021),
                    uuid("Boris Diaw") -> uuid("Hawks"): (2003, 2005),
                    uuid("Boris Diaw") -> uuid("Suns"): (2005, 2008),
                    uuid("Boris Diaw") -> uuid("Hornets"): (2008, 2012),
                    uuid("Boris Diaw") -> uuid("Spurs"): (2012, 2016),
                    uuid("Boris Diaw") -> uuid("Jazz"): (2016, 2017),
                    uuid("LeBron James") -> uuid("Cavaliers"): (2003, 2010),
                    uuid("LeBron James") -> uuid("Heat"): (2010, 2014),
                    uuid("LeBron James") -> uuid("Cavaliers"): (2014, 2018),
                    uuid("LeBron James") -> uuid("Lakers"): (2018, 2019),
                    uuid("Klay Thompson") -> uuid("Warriors"): (2011, 2019),
                    uuid("Kristaps Porzingis") -> uuid("Knicks"): (2015, 2019),
                    uuid("Kristaps Porzingis") -> uuid("Mavericks"): (2019, 2020),
                    uuid("Jonathon Simmons") -> uuid("Spurs"): (2015, 2017),
                    uuid("Jonathon Simmons") -> uuid("Magic"): (2017, 2019),
                    uuid("Jonathon Simmons") -> uuid("76ers"): (2019, 2019),
                    uuid("Marco Belinelli") -> uuid("Warriors"): (2007, 2009),
                    uuid("Marco Belinelli") -> uuid("Raptors"): (2009, 2010),
                    uuid("Marco Belinelli") -> uuid("Hornets"): (2010, 2012),
                    uuid("Marco Belinelli") -> uuid("Bulls"): (2012, 2013),
                    uuid("Marco Belinelli") -> uuid("Spurs"): (2013, 2015),
                    uuid("Marco Belinelli") -> uuid("Kings"): (2015, 2016),
                    uuid("Marco Belinelli") -> uuid("Hornets"): (2016, 2017),
                    uuid("Marco Belinelli") -> uuid("Hawks"): (2017, 2018),
                    uuid("Marco Belinelli") -> uuid("76ers"): (2018, 2018),
                    uuid("Marco Belinelli") -> uuid("Spurs"): (2018, 2019),
                    uuid("Luka Doncic") -> uuid("Mavericks"): (2018, 2019),
                    uuid("David West") -> uuid("Hornets"): (2003, 2011),
                    uuid("David West") -> uuid("Pacers"): (2011, 2015),
                    uuid("David West") -> uuid("Spurs"): (2015, 2016),
                    uuid("David West") -> uuid("Warriors"): (2016, 2018),
                    uuid("Tony Parker") -> uuid("Spurs"): (1999, 2018),
                    uuid("Tony Parker") -> uuid("Hornets"): (2018, 2019),
                    uuid("Danny Green") -> uuid("Cavaliers"): (2009, 2010),
                    uuid("Danny Green") -> uuid("Spurs"): (2010, 2018),
                    uuid("Danny Green") -> uuid("Raptors"): (2018, 2019),
                    uuid("Rudy Gay") -> uuid("Grizzlies"): (2006, 2013),
                    uuid("Rudy Gay") -> uuid("Raptors"): (2013, 2013),
                    uuid("Rudy Gay") -> uuid("Kings"): (2013, 2017),
                    uuid("Rudy Gay") -> uuid("Spurs"): (2017, 2019),
                    uuid("LaMarcus Aldridge") -> uuid("Trail Blazers"): (2006, 2015),
                    uuid("LaMarcus Aldridge") -> uuid("Spurs"): (2015, 2019),
                    uuid("Tim Duncan") -> uuid("Spurs"): (1997, 2016),
                    uuid("Kevin Durant") -> uuid("Thunders"): (2007, 2016),
                    uuid("Kevin Durant") -> uuid("Warriors"): (2016, 2019),
                    uuid("Stephen Curry") -> uuid("Warriors"): (2009, 2019),
                    uuid("Ray Allen") -> uuid("Bucks"): (1996, 2003),
                    uuid("Ray Allen") -> uuid("Thunders"): (2003, 2007),
                    uuid("Ray Allen") -> uuid("Celtics"): (2007, 2012),
                    uuid("Ray Allen") -> uuid("Heat"): (2012, 2014),
                    uuid("Tiago Splitter") -> uuid("Spurs"): (2010, 2015),
                    uuid("Tiago Splitter") -> uuid("Hawks"): (2015, 2017),
                    uuid("Tiago Splitter") -> uuid("76ers"): (2017, 2017),
                    uuid("DeAndre Jordan") -> uuid("Clippers"): (2008, 2018),
                    uuid("DeAndre Jordan") -> uuid("Mavericks"): (2018, 2019),
                    uuid("DeAndre Jordan") -> uuid("Knicks"): (2019, 2019),
                    uuid("Paul Gasol") -> uuid("Grizzlies"): (2001, 2008),
                    uuid("Paul Gasol") -> uuid("Lakers"): (2008, 2014),
                    uuid("Paul Gasol") -> uuid("Bulls"): (2014, 2016),
                    uuid("Paul Gasol") -> uuid("Spurs"): (2016, 2019),
                    uuid("Paul Gasol") -> uuid("Bucks"): (2019, 2020),
                    uuid("Aron Baynes") -> uuid("Spurs"): (2013, 2015),
                    uuid("Aron Baynes") -> uuid("Pistons"): (2015, 2017),
                    uuid("Aron Baynes") -> uuid("Celtics"): (2017, 2019),
                    uuid("Cory Joseph") -> uuid("Spurs"): (2011, 2015),
                    uuid("Cory Joseph") -> uuid("Raptors"): (2015, 2017),
                    uuid("Cory Joseph") -> uuid("Pacers"): (2017, 2019),
                    uuid("Vince Carter") -> uuid("Raptors"): (1998, 2004),
                    uuid("Vince Carter") -> uuid("Nets"): (2004, 2009),
                    uuid("Vince Carter") -> uuid("Magic"): (2009, 2010),
                    uuid("Vince Carter") -> uuid("Suns"): (2010, 2011),
                    uuid("Vince Carter") -> uuid("Mavericks"): (2011, 2014),
                    uuid("Vince Carter") -> uuid("Grizzlies"): (2014, 2017),
                    uuid("Vince Carter") -> uuid("Kings"): (2017, 2018),
                    uuid("Vince Carter") -> uuid("Hawks"): (2018, 2019),
                    uuid("Marc Gasol") -> uuid("Grizzlies"): (2008, 2019),
                    uuid("Marc Gasol") -> uuid("Raptors"): (2019, 2019),
                    uuid("Ricky Rubio") -> uuid("Timberwolves"): (2011, 2017),
                    uuid("Ricky Rubio") -> uuid("Jazz"): (2017, 2019),
                    uuid("Ben Simmons") -> uuid("76ers"): (2016, 2019),
                    uuid("Giannis Antetokounmpo") -> uuid("Bucks"): (2013, 2019),
                    uuid("Rajon Rondo") -> uuid("Celtics"): (2006, 2014),
                    uuid("Rajon Rondo") -> uuid("Mavericks"): (2014, 2015),
                    uuid("Rajon Rondo") -> uuid("Kings"): (2015, 2016),
                    uuid("Rajon Rondo") -> uuid("Bulls"): (2016, 2017),
                    uuid("Rajon Rondo") -> uuid("Pelicans"): (2017, 2018),
                    uuid("Rajon Rondo") -> uuid("Lakers"): (2018, 2019),
                    uuid("Manu Ginobili") -> uuid("Spurs"): (2002, 2018),
                    uuid("Kyrie Irving") -> uuid("Cavaliers"): (2011, 2017),
                    uuid("Kyrie Irving") -> uuid("Celtics"): (2017, 2019),
                    uuid("Carmelo Anthony") -> uuid("Nuggets"): (2003, 2011),
                    uuid("Carmelo Anthony") -> uuid("Knicks"): (2011, 2017),
                    uuid("Carmelo Anthony") -> uuid("Thunders"): (2017, 2018),
                    uuid("Carmelo Anthony") -> uuid("Rockets"): (2018, 2019),
                    uuid("Dwyane Wade") -> uuid("Heat"): (2003, 2016),
                    uuid("Dwyane Wade") -> uuid("Bulls"): (2016, 2017),
                    uuid("Dwyane Wade") -> uuid("Cavaliers"): (2017, 2018),
                    uuid("Dwyane Wade") -> uuid("Heat"): (2018, 2019),
                    uuid("Joel Embiid") -> uuid("76ers"): (2014, 2019),
                    uuid("Damian Lillard") -> uuid("Trail Blazers"): (2012, 2019),
                    uuid("Yao Ming") -> uuid("Rockets"): (2002, 2011),
                    uuid("Kyle Anderson") -> uuid("Spurs"): (2014, 2018),
                    uuid("Kyle Anderson") -> uuid("Grizzlies"): (2018, 2019),
                    uuid("Dejounte Murray") -> uuid("Spurs"): (2016, 2019),
                    uuid("Blake Griffin") -> uuid("Clippers"): (2009, 2018),
                    uuid("Blake Griffin") -> uuid("Pistons"): (2018, 2019),
                    uuid("Steve Nash") -> uuid("Suns"): (1996, 1998),
                    uuid("Steve Nash") -> uuid("Mavericks"): (1998, 2004),
                    uuid("Steve Nash") -> uuid("Suns"): (2004, 2012),
                    uuid("Steve Nash") -> uuid("Lakers"): (2012, 2015),
                    uuid("Jason Kidd") -> uuid("Mavericks"): (1994, 1996),
                    uuid("Jason Kidd") -> uuid("Suns"): (1996, 2001),
                    uuid("Jason Kidd") -> uuid("Nets"): (2001, 2008),
                    uuid("Jason Kidd") -> uuid("Mavericks"): (2008, 2012),
                    uuid("Jason Kidd") -> uuid("Knicks"): (2012, 2013),
                    uuid("Dirk Nowitzki") -> uuid("Mavericks"): (1998, 2019),
                    uuid("Paul George") -> uuid("Pacers"): (2010, 2017),
                    uuid("Paul George") -> uuid("Thunders"): (2017, 2019),
                    uuid("Grant Hill") -> uuid("Pistons"): (1994, 2000),
                    uuid("Grant Hill") -> uuid("Magic"): (2000, 2007),
                    uuid("Grant Hill") -> uuid("Suns"): (2007, 2012),
                    uuid("Grant Hill") -> uuid("Clippers"): (2012, 2013),
                    uuid("Shaquile O'Neal") -> uuid("Magic"): (1992, 1996),
                    uuid("Shaquile O'Neal") -> uuid("Lakers"): (1996, 2004),
                    uuid("Shaquile O'Neal") -> uuid("Heat"): (2004, 2008),
                    uuid("Shaquile O'Neal") -> uuid("Suns"): (2008, 2009),
                    uuid("Shaquile O'Neal") -> uuid("Cavaliers"): (2009, 2010),
                    uuid("Shaquile O'Neal") -> uuid("Celtics"): (2010, 2011),
                    uuid("JaVale McGee") -> uuid("Wizards"): (2008, 2012),
                    uuid("JaVale McGee") -> uuid("Nuggets"): (2012, 2015),
                    uuid("JaVale McGee") -> uuid("Mavericks"): (2015, 2016),
                    uuid("JaVale McGee") -> uuid("Warriors"): (2016, 2018),
                    uuid("JaVale McGee") -> uuid("Lakers"): (2018, 2019),
                    uuid("Dwight Howard") -> uuid("Magic"): (2004, 2012),
                    uuid("Dwight Howard") -> uuid("Lakers"): (2012, 2013),
                    uuid("Dwight Howard") -> uuid("Rockets"): (2013, 2016),
                    uuid("Dwight Howard") -> uuid("Hawks"): (2016, 2017),
                    uuid("Dwight Howard") -> uuid("Hornets"): (2017, 2018),
                    uuid("Dwight Howard") -> uuid("Wizards"): (2018, 2019)
                    ''')

    # insert edge like
    client.execute('''
                    INSERT EDGE like(likeness) VALUES 
                    -8379929135833483044 -> 6663720087669302163: (90),
                    -2953535798644081749 -> 4312213929524069862: (90),
                    -2953535798644081749 -> -7187791973189815797: (90),
                    -7187791973189815797 -> -2953535798644081749: (80),
                    4823234394086728974 -> -2308681984240312228: (90),
                    4823234394086728974 -> 6293765385213992205: (90),
                    4823234394086728974 -> -3212290852619976819: (90),
                    -6952676908621237908 -> -8864869605086585744: (90),
                    -6952676908621237908 -> -4722009539442865199: (90),
                    -6952676908621237908 -> -4725743394557506923: (90),
                    -7391649757245641883 -> -7579316172763586624: (80),
                    -7391649757245641883 -> 5662213458193308137: (80),
                    -8864869605086585744 -> 7749522836357656167: (100),
                    -3159397121379009673 -> 8136836558163210487: (90),
                    -1808363682563220400 -> -1527627220316645914: (90),
                    -8206304902611825447 -> -7579316172763586624: (50),
                    -8206304902611825447 -> 5662213458193308137: (55),
                    -8206304902611825447 -> -4246510323023722591: (60),
                    -1527627220316645914 -> 8666973159269157201: (90),
                    -1527627220316645914 -> -1808363682563220400: (90),
                    -1527627220316645914 -> -7187791973189815797: (80),
                    -7579316172763586624 -> 5662213458193308137: (95),
                    -7579316172763586624 -> 3394245602834314645: (95),
                    -7579316172763586624 -> -1782445125509592239: (90),
                    -4246510323023722591 -> -8206304902611825447: (83),
                    -4246510323023722591 -> 5662213458193308137: (70),
                    -4246510323023722591 -> -8864869605086585744: (80),
                    -3212290852619976819 -> -1782445125509592239: (70),
                    -1782445125509592239 -> -7579316172763586624: (75),
                    -1782445125509592239 -> 5662213458193308137: (75),
                    5662213458193308137 -> -7579316172763586624: (95),
                    5662213458193308137 -> 3394245602834314645: (95),
                    7749522836357656167 -> -7984366606588005471: (9),
                    -8160811731890648949 -> 5662213458193308137: (80),
                    -8160811731890648949 -> 3394245602834314645: (90),
                    8988238998692066522 -> -2308681984240312228: (90),
                    8988238998692066522 -> -2748242588091293411: (99),
                    -7034133662712739796 -> 5662213458193308137: (80),
                    -6581004839648359804 -> 4823234394086728974: (90),
                    -6581004839648359804 -> 7339407009759737412: (70),
                    -2748242588091293411 -> 8988238998692066522: (99),
                    -3310404127039111439 -> -7419439655175297510: (80),
                    -7984366606588005471 -> 7749522836357656167: (-1),
                    3394245602834314645 -> 5662213458193308137: (90),
                    -7276938555819111674 -> -8864869605086585744: (13),
                    -4722009539442865199 -> -8864869605086585744: (90),
                    -4722009539442865199 -> -6952676908621237908: (90),
                    -4722009539442865199 -> -4725743394557506923: (90),
                    -4725743394557506923 -> -8864869605086585744: (90),
                    -4725743394557506923 -> -6952676908621237908: (90),
                    -4725743394557506923 -> -4722009539442865199: (90),
                    -7419439655175297510 -> -3310404127039111439: (80),
                    -8899043049306086446 -> -1782445125509592239: (80),
                    4651420795228053868 -> 4823234394086728974: (90),
                    4651420795228053868 -> -7176373918218927568: (90),
                    5209979940224249985 -> 5662213458193308137: (99),
                    5209979940224249985 -> -7579316172763586624: (99),
                    5209979940224249985 -> 3394245602834314645: (99),
                    5209979940224249985 -> -8206304902611825447: (99),
                    5209979940224249985 -> -4246510323023722591: (99),
                    5209979940224249985 -> -8864869605086585744: (99),
                    5209979940224249985 -> -2953535798644081749: (99),
                    5209979940224249985 -> -6952676908621237908: (99),
                    5209979940224249985 -> -8310021930715358072: (99),
                    5209979940224249985 -> 3778194419743477824: (99),
                    5209979940224249985 -> -7187791973189815797: (99),
                    5209979940224249985 -> -7579316172763586624: (99),
                    -6761803129056739448 -> -6952676908621237908: (-1),
                    6663720087669302163 -> -8379929135833483044: (90),
                    6663720087669302163 -> 8666973159269157201: (88),
                    6663720087669302163 -> 8136836558163210487: (90),
                    6663720087669302163 -> 7339407009759737412: (85),
                    7339407009759737412 -> -6581004839648359804: (80),
                    7339407009759737412 -> 6663720087669302163: (90),
                    7339407009759737412 -> 8666973159269157201: (85),
                    8666973159269157201 -> 6663720087669302163: (80),
                    8666973159269157201 -> 7339407009759737412: (80),
                    8666973159269157201 -> -4725743394557506923: (10),
                    4312213929524069862 -> -2953535798644081749: (95),
                    6293765385213992205 -> 4823234394086728974: (90),
                    -7176373918218927568 -> -6714656557196607176: (100),
                    -7176373918218927568 -> 5662213458193308137: (80)
                    ''')

    # insert edge like with uuid
    client.execute('''
                    INSERT EDGE like(likeness) VALUES 
                    uuid("Amar'e Stoudemire") -> uuid("Steve Nash"): (90),
                    uuid("Russell Westbrook") -> uuid("Paul George"): (90),
                    uuid("Russell Westbrook") -> uuid("James Harden"): (90),
                    uuid("James Harden") -> uuid("Russell Westbrook"): (80),
                    uuid("Tracy McGrady") -> uuid("Kobe Bryant"): (90),
                    uuid("Tracy McGrady") -> uuid("Grant Hill"): (90),
                    uuid("Tracy McGrady") -> uuid("Rudy Gay"): (90),
                    uuid("Chris Paul") -> uuid("LeBron James"): (90),
                    uuid("Chris Paul") -> uuid("Carmelo Anthony"): (90),
                    uuid("Chris Paul") -> uuid("Dwyane Wade"): (90),
                    uuid("Boris Diaw") -> uuid("Tony Parker"): (80),
                    uuid("Boris Diaw") -> uuid("Tim Duncan"): (80),
                    uuid("LeBron James") -> uuid("Ray Allen"): (100),
                    uuid("Klay Thompson") -> uuid("Stephen Curry"): (90),
                    uuid("Kristaps Porzingis") -> uuid("Luka Doncic"): (90),
                    uuid("Marco Belinelli") -> uuid("Tony Parker"): (50),
                    uuid("Marco Belinelli") -> uuid("Tim Duncan"): (55),
                    uuid("Marco Belinelli") -> uuid("Danny Green"): (60),
                    uuid("Luka Doncic") -> uuid("Dirk Nowitzki"): (90),
                    uuid("Luka Doncic") -> uuid("Kristaps Porzingis"): (90),
                    uuid("Luka Doncic") -> uuid("James Harden"): (80),
                    uuid("Tony Parker") -> uuid("Tim Duncan"): (95),
                    uuid("Tony Parker") -> uuid("Manu Ginobili"): (95),
                    uuid("Tony Parker") -> uuid("LaMarcus Aldridge"): (90),
                    uuid("Danny Green") -> uuid("Marco Belinelli"): (83),
                    uuid("Danny Green") -> uuid("Tim Duncan"): (70),
                    uuid("Danny Green") -> uuid("LeBron James"): (80),
                    uuid("Rudy Gay") -> uuid("LaMarcus Aldridge"): (70),
                    uuid("LaMarcus Aldridge") -> uuid("Tony Parker"): (75),
                    uuid("LaMarcus Aldridge") -> uuid("Tim Duncan"): (75),
                    uuid("Tim Duncan") -> uuid("Tony Parker"): (95),
                    uuid("Tim Duncan") -> uuid("Manu Ginobili"): (95),
                    uuid("Ray Allen") -> uuid("Rajon Rondo"): (9),
                    uuid("Tiago Splitter") -> uuid("Tim Duncan"): (80),
                    uuid("Tiago Splitter") -> uuid("Manu Ginobili"): (90),
                    uuid("Paul Gasol") -> uuid("Kobe Bryant"): (90),
                    uuid("Paul Gasol") -> uuid("Marc Gasol"): (99),
                    uuid("Aron Baynes") -> uuid("Tim Duncan"): (80),
                    uuid("Vince Carter") -> uuid("Tracy McGrady"): (90),
                    uuid("Vince Carter") -> uuid("Jason Kidd"): (70),
                    uuid("Marc Gasol") -> uuid("Paul Gasol"): (99),
                    uuid("Ben Simmons") -> uuid("Joel Embiid"): (80),
                    uuid("Rajon Rondo") -> uuid("Ray Allen"): (-1),
                    uuid("Manu Ginobili") -> uuid("Tim Duncan"): (90),
                    uuid("Kyrie Irving") -> uuid("LeBron James"): (13),
                    uuid("Carmelo Anthony") -> uuid("LeBron James"): (90),
                    uuid("Carmelo Anthony") -> uuid("Chris Paul"): (90),
                    uuid("Carmelo Anthony") -> uuid("Dwyane Wade"): (90),
                    uuid("Dwyane Wade") -> uuid("LeBron James"): (90),
                    uuid("Dwyane Wade") -> uuid("Chris Paul"): (90),
                    uuid("Dwyane Wade") -> uuid("Carmelo Anthony"): (90),
                    uuid("Joel Embiid") -> uuid("Ben Simmons"): (80),
                    uuid("Damian Lillard") -> uuid("LaMarcus Aldridge"): (80),
                    uuid("Yao Ming") -> uuid("Tracy McGrady"): (90),
                    uuid("Yao Ming") -> uuid("Shaquile O'Neal"): (90),
                    uuid("Dejounte Murray") -> uuid("Tim Duncan"): (99),
                    uuid("Dejounte Murray") -> uuid("Tony Parker"): (99),
                    uuid("Dejounte Murray") -> uuid("Manu Ginobili"): (99),
                    uuid("Dejounte Murray") -> uuid("Marco Belinelli"): (99),
                    uuid("Dejounte Murray") -> uuid("Danny Green"): (99),
                    uuid("Dejounte Murray") -> uuid("LeBron James"): (99),
                    uuid("Dejounte Murray") -> uuid("Russell Westbrook"): (99),
                    uuid("Dejounte Murray") -> uuid("Chris Paul"): (99),
                    uuid("Dejounte Murray") -> uuid("Kyle Anderson"): (99),
                    uuid("Dejounte Murray") -> uuid("Kevin Durant"): (99),
                    uuid("Dejounte Murray") -> uuid("James Harden"): (99),
                    uuid("Dejounte Murray") -> uuid("Tony Parker"): (99),
                    uuid("Blake Griffin") -> uuid("Chris Paul"): (-1),
                    uuid("Steve Nash") -> uuid("Amar'e Stoudemire"): (90),
                    uuid("Steve Nash") -> uuid("Dirk Nowitzki"): (88),
                    uuid("Steve Nash") -> uuid("Stephen Curry"): (90),
                    uuid("Steve Nash") -> uuid("Jason Kidd"): (85),
                    uuid("Jason Kidd") -> uuid("Vince Carter"): (80),
                    uuid("Jason Kidd") -> uuid("Steve Nash"): (90),
                    uuid("Jason Kidd") -> uuid("Dirk Nowitzki"): (85),
                    uuid("Dirk Nowitzki") -> uuid("Steve Nash"): (80),
                    uuid("Dirk Nowitzki") -> uuid("Jason Kidd"): (80),
                    uuid("Dirk Nowitzki") -> uuid("Dwyane Wade"): (10),
                    uuid("Paul George") -> uuid("Russell Westbrook"): (95),
                    uuid("Grant Hill") -> uuid("Tracy McGrady"): (90),
                    uuid("Shaquile O'Neal") -> uuid("JaVale McGee"): (100),
                    uuid("Shaquile O'Neal") -> uuid("Tim Duncan"): (80)
                    ''')

    # insert edge teammate
    client.execute('''
                    INSERT EDGE teammate(start_year, end_year) VALUES 
                    -7579316172763586624 -> 5662213458193308137: (2001, 2016),
                    -7579316172763586624 -> 3394245602834314645: (2002, 2018),
                    -7579316172763586624 -> -1782445125509592239: (2015, 2018),
                    -7579316172763586624 -> -8310021930715358072: (2014, 2016),
                    5662213458193308137 -> -7579316172763586624: (2001, 2016),
                    5662213458193308137 -> 3394245602834314645: (2002, 2016),
                    5662213458193308137 -> -1782445125509592239: (2015, 2016),
                    5662213458193308137 -> -4246510323023722591: (2010, 2016),
                    3394245602834314645 -> 5662213458193308137: (2002, 2016),
                    3394245602834314645 -> -7579316172763586624: (2002, 2016)
                    ''')

    # insert edge teammate with uuid
    client.execute('''
                    INSERT EDGE teammate(start_year, end_year) VALUES 
                    uuid("Tony Parker") -> uuid("Tim Duncan"): (2001, 2016),
                    uuid("Tony Parker") -> uuid("Manu Ginobili"): (2002, 2018),
                    uuid("Tony Parker") -> uuid("LaMarcus Aldridge"): (2015, 2018),
                    uuid("Tony Parker") -> uuid("Kyle Anderson"): (2014, 2016),
                    uuid("Tim Duncan") -> uuid("Tony Parker"): (2001, 2016),
                    uuid("Tim Duncan") -> uuid("Manu Ginobili"): (2002, 2016),
                    uuid("Tim Duncan") -> uuid("LaMarcus Aldridge"): (2015, 2016),
                    uuid("Tim Duncan") -> uuid("Danny Green"): (2010, 2016),
                    uuid("Manu Ginobili") -> uuid("Tim Duncan"): (2002, 2016),
                    uuid("Manu Ginobili") -> uuid("Tony Parker"): (2002, 2016)
                    ''')


def get_player_name_id():
    cmd = 'YIELD '
    for player in players:
        cmd = cmd + ' hash("{}"),'.format(player)
    cmd = cmd[:-1]
    resp = client.execute_query(cmd)
    if resp.error_code != 0 or resp.rows is None:
        print("Execute `YIELD hash()'.... failed")
        exit(-1)

    columns = resp.rows[0].columns
    if len(players) != len(columns):
        print("Wrong rows size from `YIELD hash()': resp[{}] : expect[{}]".
              format(len(players), len(resp.columns)))
        exit(-1)

    for player, col in zip(players, columns):
        vid = col.get_integer()
        player_name_to_id_dict[player] = vid
        player_id_to_name_dict[vid] = player


def get_team_name_id():
    cmd = 'YIELD '
    for team in teams:
        cmd = cmd + ' hash("{}"),'.format(team)
    cmd = cmd[:-1]
    resp = client.execute_query(cmd)
    if resp.error_code != 0 or resp.rows is None:
        print("Execute `YIELD hash()'.... failed: get_team_name_id failed ")
        exit(-1)

    columns = resp.rows[0].columns
    if len(teams) != len(columns):
        print("Wrong rows size from `YIELD hash()': resp[{}] : expect[{}]".
              format(len(teams), len(resp.columns)))
        exit(-1)

    for team, col in zip(teams, columns):
        vid = col.get_integer()
        team_name_to_id_dict[team] = vid
        team_id_to_name_dict[vid] = team


def print_result(cmd, resp):
    if resp.error_code != 0:
        return
    print('Cmd: {}\n'.format(cmd))
    result = ''
    if resp.rows is not None:
        result = '['
        for row in resp.rows:
            if len(row.columns) == 0:
                continue
            row_str = '['
            for col in row.columns:
                if col.getType() == ttypes.ColumnValue.__EMPTY__:
                    print('ERROR: type is empty')
                    exit(-1)
                elif col.getType() == ttypes.ColumnValue.ID:
                    if col.get_id() in player_id_to_name_dict.keys():
                        row_str = row_str + '"' + str(player_id_to_name_dict[col.get_id()]) + '"' + ', '
                    elif col.get_id() in team_id_to_name_dict.keys():
                        row_str = row_str + '"' + str(team_id_to_name_dict[col.get_id()])  + '"' + ', '
                    else:
                        print('Unknown vid: {}'.format(col.get_id()))
                        exit(-1)
                elif col.getType() == ttypes.ColumnValue.BOOL_VAL:
                    row_str = row_str + str(col.get_bool_val()) + ', '
                elif col.getType() == ttypes.ColumnValue.INTEGER:
                    row_str = row_str + str(col.get_integer()) + ', '
                elif col.getType() == ttypes.ColumnValue.STR:
                    row_str = row_str + '"' + str(col.get_str().decode('utf-8')) + '", '
                elif col.getType() == ttypes.ColumnValue.DOUBLE_PRECISION:
                    row_str = row_str + str(col.get_double_precision()) + ', '
                elif col.getType() == ttypes.ColumnValue.TIMESTAMP:
                    row_str = row_str + str(col.get_timestamp()) + ', '
                else:
                    print('ERROR: Type unsupported')
                    exit(-1)
            row_str = row_str[:-2] + ']'
            result = result + row_str + ', '

    if resp.column_names is None:
        print('Result colNames: \n')
    else:
        colNames = '['
        for colName in resp.column_names:
           colNames = colNames + '"' + colName.decode('utf-8') + '"' + ', '
        colNames = colNames[:-2] + ']'
        print('Result colNames: {}\n'.format(colNames))

    if len(result) == 0:
        print('Result data:\n')
    else:
        print('Result data: {}\n'.format(result[:-2] + ']'))


def execute_cmd_from_file():
    client.execute('USE nba;')
    cmds_file = open('./nGQL.txt', 'r')
    cmd = ''
    cmds = []

    for line in cmds_file.readlines():
        if len(line.strip()) == 0:
            continue
        if line.find('--BEGIN--') != -1:
            cmd = ''
            continue
        if line.find('--END--') != -1:
            cmds.append(cmd)
            continue
        cmd = cmd + line.replace('\n', '').replace('\r', '') + ' '

    for cmd in cmds:
        resp = client.execute_query(cmd)
        if resp.error_code != ttypes.ErrorCode.SUCCEEDED and resp.error_code != ttypes.ErrorCode.E_STATEMENT_EMTPY:
            print("Execute `{}' failed, error_msg: {}\n".format(cmd, resp.error_msg))
            continue

        print_result(cmd, resp)


if __name__ == '__main__':

    g_ip = '127.0.0.1'
    g_port = 3699

    print('input argv num is %d' % len(sys.argv))
    if len(sys.argv) == 3:
        print('input argv num is 3')
        g_ip = sys.argv[1]
        print('ip: %s' % g_ip)
        g_port = sys.argv[2]
        print('port: %s' % g_port)

    try:
        # init connection pool
        connection_pool = ConnectionPool(g_ip, g_port, 1, 0)
        # Get one client
        client = GraphClient(connection_pool)
        auth_resp = client.authenticate('user', 'password')
        if auth_resp.error_code:
            raise AuthException("Auth failed")

        insert_data()
        get_player_name_id()
        get_team_name_id()
        execute_cmd_from_file()
        # close connect pool
        connection_pool.close()

    except Exception as x:
        print(x)
        # close connect pool
        connection_pool.close()
        exit(-1)

