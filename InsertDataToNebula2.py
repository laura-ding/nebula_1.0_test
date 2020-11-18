# --coding:utf-8--
#
# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License,
# attached with Common Clause Condition 1.0, found in the LICENSES directory.

import sys
import time


from nebula2.graph import ttypes
from nebula2.ConnectionPool import ConnectionPool
from nebula2.Client import GraphClient
from nebula2.Common import *

player_name_to_id_dict = {}
player_id_to_name_dict = {}
team_name_to_id_dict = {}
team_id_to_name_dict = {}
client = None


def insert_data():
    # prepare schema
    client.execute('CREATE SPACE IF NOT EXISTS nba(partition_num=1, replica_factor=1, vid_type = fixed_string(30));'
                   'USE nba; CREATE TAG IF NOT EXISTS player(name string, age int);'
                   'CREATE TAG IF NOT EXISTS team(name string);'
                   'CREATE EDGE IF NOT EXISTS serve(start_year int, end_year int);'
                   'CREATE EDGE IF NOT EXISTS like(likeness int);'
                   'CREATE EDGE IF NOT EXISTS teammate(start_year int, end_year int);'
                   'CREATE TAG IF NOT EXISTS bachelor(name string, speciality string);')

    time.sleep(10)

    # insert vertex team with uuid
    resp = client.execute('''
                    INSERT VERTEX team(name) VALUES "Nets": ("Nets"),
                    "Pistons": ("Pistons"),
                    "Bucks": ("Bucks"),
                    "Mavericks": ("Mavericks"),
                    "Clippers": ("Clippers"),
                    "Thunders": ("Thunders"),
                    "Lakers": ("Lakers"),
                    "Jazz": ("Jazz"),
                    "Nuggets": ("Nuggets"),
                    "Wizards": ("Wizards"),
                    "Pacers": ("Pacers"),
                    "Timberwolves": ("Timberwolves"),
                    "Hawks": ("Hawks"),
                    "Warriors": ("Warriors"),
                    "Magic": ("Magic"),
                    "Rockets": ("Rockets"),
                    "Pelicans": ("Pelicans"),
                    "Raptors": ("Raptors"),
                    "Spurs": ("Spurs"),
                    "Heat": ("Heat"),
                    "Grizzlies": ("Grizzlies"),
                    "Knicks": ("Knicks"),
                    "Suns": ("Suns"),
                    "Hornets": ("Hornets"),
                    "Cavaliers": ("Cavaliers"),
                    "Kings": ("Kings"),
                    "Celtics": ("Celtics"),
                    "76ers": ("76ers"),
                    "Trail Blazers": ("Trail Blazers"),
                    "Bulls": ("Bulls")
                    ''')
    assert resp.error_code == 0, resp.error_msg

    # insert edge serve with uuid
    client.execute('''
                    INSERT EDGE serve(start_year, end_year) VALUES 
                    "Amar'e Stoudemire" -> "Suns": (2002, 2010),
                    "Amar'e Stoudemire" -> "Knicks": (2010, 2015),
                    "Amar'e Stoudemire" -> "Heat": (2015, 2016),
                    "Russell Westbrook" -> "Thunders": (2008, 2019),
                    "James Harden" -> "Thunders": (2009, 2012),
                    "James Harden" -> "Rockets": (2012, 2019),
                    "Kobe Bryant" -> "Lakers": (1996, 2016),
                    "Tracy McGrady" -> "Raptors": (1997, 2000),
                    "Tracy McGrady" -> "Magic": (2000, 2004),
                    "Tracy McGrady" -> "Rockets": (2004, 2010),
                    "Tracy McGrady" -> "Spurs": (2013, 2013),
                    "Chris Paul" -> "Hornets": (2005, 2011),
                    "Chris Paul" -> "Clippers": (2011, 2017),
                    "Chris Paul" -> "Rockets": (2017, 2021),
                    "Boris Diaw" -> "Hawks": (2003, 2005),
                    "Boris Diaw" -> "Suns": (2005, 2008),
                    "Boris Diaw" -> "Hornets": (2008, 2012),
                    "Boris Diaw" -> "Spurs": (2012, 2016),
                    "Boris Diaw" -> "Jazz": (2016, 2017),
                    "LeBron James" -> "Cavaliers": (2003, 2010),
                    "LeBron James" -> "Heat": (2010, 2014),
                    "LeBron James" -> "Cavaliers": (2014, 2018),
                    "LeBron James" -> "Lakers": (2018, 2019),
                    "Klay Thompson" -> "Warriors": (2011, 2019),
                    "Kristaps Porzingis" -> "Knicks": (2015, 2019),
                    "Kristaps Porzingis" -> "Mavericks": (2019, 2020),
                    "Jonathon Simmons" -> "Spurs": (2015, 2017),
                    "Jonathon Simmons" -> "Magic": (2017, 2019),
                    "Jonathon Simmons" -> "76ers": (2019, 2019),
                    "Marco Belinelli" -> "Warriors": (2007, 2009),
                    "Marco Belinelli" -> "Raptors": (2009, 2010),
                    "Marco Belinelli" -> "Hornets": (2010, 2012),
                    "Marco Belinelli" -> "Bulls": (2012, 2013),
                    "Marco Belinelli" -> "Spurs": (2013, 2015),
                    "Marco Belinelli" -> "Kings": (2015, 2016),
                    "Marco Belinelli" -> "Hornets": (2016, 2017),
                    "Marco Belinelli" -> "Hawks": (2017, 2018),
                    "Marco Belinelli" -> "76ers": (2018, 2018),
                    "Marco Belinelli" -> "Spurs": (2018, 2019),
                    "Luka Doncic" -> "Mavericks": (2018, 2019),
                    "David West" -> "Hornets": (2003, 2011),
                    "David West" -> "Pacers": (2011, 2015),
                    "David West" -> "Spurs": (2015, 2016),
                    "David West" -> "Warriors": (2016, 2018),
                    "Tony Parker" -> "Spurs": (1999, 2018),
                    "Tony Parker" -> "Hornets": (2018, 2019),
                    "Danny Green" -> "Cavaliers": (2009, 2010),
                    "Danny Green" -> "Spurs": (2010, 2018),
                    "Danny Green" -> "Raptors": (2018, 2019),
                    "Rudy Gay" -> "Grizzlies": (2006, 2013),
                    "Rudy Gay" -> "Raptors": (2013, 2013),
                    "Rudy Gay" -> "Kings": (2013, 2017),
                    "Rudy Gay" -> "Spurs": (2017, 2019),
                    "LaMarcus Aldridge" -> "Trail Blazers": (2006, 2015),
                    "LaMarcus Aldridge" -> "Spurs": (2015, 2019),
                    "Tim Duncan" -> "Spurs": (1997, 2016),
                    "Kevin Durant" -> "Thunders": (2007, 2016),
                    "Kevin Durant" -> "Warriors": (2016, 2019),
                    "Stephen Curry" -> "Warriors": (2009, 2019),
                    "Ray Allen" -> "Bucks": (1996, 2003),
                    "Ray Allen" -> "Thunders": (2003, 2007),
                    "Ray Allen" -> "Celtics": (2007, 2012),
                    "Ray Allen" -> "Heat": (2012, 2014),
                    "Tiago Splitter" -> "Spurs": (2010, 2015),
                    "Tiago Splitter" -> "Hawks": (2015, 2017),
                    "Tiago Splitter" -> "76ers": (2017, 2017),
                    "DeAndre Jordan" -> "Clippers": (2008, 2018),
                    "DeAndre Jordan" -> "Mavericks": (2018, 2019),
                    "DeAndre Jordan" -> "Knicks": (2019, 2019),
                    "Paul Gasol" -> "Grizzlies": (2001, 2008),
                    "Paul Gasol" -> "Lakers": (2008, 2014),
                    "Paul Gasol" -> "Bulls": (2014, 2016),
                    "Paul Gasol" -> "Spurs": (2016, 2019),
                    "Paul Gasol" -> "Bucks": (2019, 2020),
                    "Aron Baynes" -> "Spurs": (2013, 2015),
                    "Aron Baynes" -> "Pistons": (2015, 2017),
                    "Aron Baynes" -> "Celtics": (2017, 2019),
                    "Cory Joseph" -> "Spurs": (2011, 2015),
                    "Cory Joseph" -> "Raptors": (2015, 2017),
                    "Cory Joseph" -> "Pacers": (2017, 2019),
                    "Vince Carter" -> "Raptors": (1998, 2004),
                    "Vince Carter" -> "Nets": (2004, 2009),
                    "Vince Carter" -> "Magic": (2009, 2010),
                    "Vince Carter" -> "Suns": (2010, 2011),
                    "Vince Carter" -> "Mavericks": (2011, 2014),
                    "Vince Carter" -> "Grizzlies": (2014, 2017),
                    "Vince Carter" -> "Kings": (2017, 2018),
                    "Vince Carter" -> "Hawks": (2018, 2019),
                    "Marc Gasol" -> "Grizzlies": (2008, 2019),
                    "Marc Gasol" -> "Raptors": (2019, 2019),
                    "Ricky Rubio" -> "Timberwolves": (2011, 2017),
                    "Ricky Rubio" -> "Jazz": (2017, 2019),
                    "Ben Simmons" -> "76ers": (2016, 2019),
                    "Giannis Antetokounmpo" -> "Bucks": (2013, 2019),
                    "Rajon Rondo" -> "Celtics": (2006, 2014),
                    "Rajon Rondo" -> "Mavericks": (2014, 2015),
                    "Rajon Rondo" -> "Kings": (2015, 2016),
                    "Rajon Rondo" -> "Bulls": (2016, 2017),
                    "Rajon Rondo" -> "Pelicans": (2017, 2018),
                    "Rajon Rondo" -> "Lakers": (2018, 2019),
                    "Manu Ginobili" -> "Spurs": (2002, 2018),
                    "Kyrie Irving" -> "Cavaliers": (2011, 2017),
                    "Kyrie Irving" -> "Celtics": (2017, 2019),
                    "Carmelo Anthony" -> "Nuggets": (2003, 2011),
                    "Carmelo Anthony" -> "Knicks": (2011, 2017),
                    "Carmelo Anthony" -> "Thunders": (2017, 2018),
                    "Carmelo Anthony" -> "Rockets": (2018, 2019),
                    "Dwyane Wade" -> "Heat": (2003, 2016),
                    "Dwyane Wade" -> "Bulls": (2016, 2017),
                    "Dwyane Wade" -> "Cavaliers": (2017, 2018),
                    "Dwyane Wade" -> "Heat": (2018, 2019),
                    "Joel Embiid" -> "76ers": (2014, 2019),
                    "Damian Lillard" -> "Trail Blazers": (2012, 2019),
                    "Yao Ming" -> "Rockets": (2002, 2011),
                    "Kyle Anderson" -> "Spurs": (2014, 2018),
                    "Kyle Anderson" -> "Grizzlies": (2018, 2019),
                    "Dejounte Murray" -> "Spurs": (2016, 2019),
                    "Blake Griffin" -> "Clippers": (2009, 2018),
                    "Blake Griffin" -> "Pistons": (2018, 2019),
                    "Steve Nash" -> "Suns": (1996, 1998),
                    "Steve Nash" -> "Mavericks": (1998, 2004),
                    "Steve Nash" -> "Suns": (2004, 2012),
                    "Steve Nash" -> "Lakers": (2012, 2015),
                    "Jason Kidd" -> "Mavericks": (1994, 1996),
                    "Jason Kidd" -> "Suns": (1996, 2001),
                    "Jason Kidd" -> "Nets": (2001, 2008),
                    "Jason Kidd" -> "Mavericks": (2008, 2012),
                    "Jason Kidd" -> "Knicks": (2012, 2013),
                    "Dirk Nowitzki" -> "Mavericks": (1998, 2019),
                    "Paul George" -> "Pacers": (2010, 2017),
                    "Paul George" -> "Thunders": (2017, 2019),
                    "Grant Hill" -> "Pistons": (1994, 2000),
                    "Grant Hill" -> "Magic": (2000, 2007),
                    "Grant Hill" -> "Suns": (2007, 2012),
                    "Grant Hill" -> "Clippers": (2012, 2013),
                    "Shaquile O'Neal" -> "Magic": (1992, 1996),
                    "Shaquile O'Neal" -> "Lakers": (1996, 2004),
                    "Shaquile O'Neal" -> "Heat": (2004, 2008),
                    "Shaquile O'Neal" -> "Suns": (2008, 2009),
                    "Shaquile O'Neal" -> "Cavaliers": (2009, 2010),
                    "Shaquile O'Neal" -> "Celtics": (2010, 2011),
                    "JaVale McGee" -> "Wizards": (2008, 2012),
                    "JaVale McGee" -> "Nuggets": (2012, 2015),
                    "JaVale McGee" -> "Mavericks": (2015, 2016),
                    "JaVale McGee" -> "Warriors": (2016, 2018),
                    "JaVale McGee" -> "Lakers": (2018, 2019),
                    "Dwight Howard" -> "Magic": (2004, 2012),
                    "Dwight Howard" -> "Lakers": (2012, 2013),
                    "Dwight Howard" -> "Rockets": (2013, 2016),
                    "Dwight Howard" -> "Hawks": (2016, 2017),
                    "Dwight Howard" -> "Hornets": (2017, 2018),
                    "Dwight Howard" -> "Wizards": (2018, 2019)
                    ''')

    assert resp.error_code == 0, resp.error_msg

    # insert edge like with uuid
    client.execute('''
                    INSERT EDGE like(likeness) VALUES 
                    "Amar'e Stoudemire" -> "Steve Nash": (90),
                    "Russell Westbrook" -> "Paul George": (90),
                    "Russell Westbrook" -> "James Harden": (90),
                    "James Harden" -> "Russell Westbrook": (80),
                    "Tracy McGrady" -> "Kobe Bryant": (90),
                    "Tracy McGrady" -> "Grant Hill": (90),
                    "Tracy McGrady" -> "Rudy Gay": (90),
                    "Chris Paul" -> "LeBron James": (90),
                    "Chris Paul" -> "Carmelo Anthony": (90),
                    "Chris Paul" -> "Dwyane Wade": (90),
                    "Boris Diaw" -> "Tony Parker": (80),
                    "Boris Diaw" -> "Tim Duncan": (80),
                    "LeBron James" -> "Ray Allen": (100),
                    "Klay Thompson" -> "Stephen Curry": (90),
                    "Kristaps Porzingis" -> "Luka Doncic": (90),
                    "Marco Belinelli" -> "Tony Parker": (50),
                    "Marco Belinelli" -> "Tim Duncan": (55),
                    "Marco Belinelli" -> "Danny Green": (60),
                    "Luka Doncic" -> "Dirk Nowitzki": (90),
                    "Luka Doncic" -> "Kristaps Porzingis": (90),
                    "Luka Doncic" -> "James Harden": (80),
                    "Tony Parker" -> "Tim Duncan": (95),
                    "Tony Parker" -> "Manu Ginobili": (95),
                    "Tony Parker" -> "LaMarcus Aldridge": (90),
                    "Danny Green" -> "Marco Belinelli": (83),
                    "Danny Green" -> "Tim Duncan": (70),
                    "Danny Green" -> "LeBron James": (80),
                    "Rudy Gay" -> "LaMarcus Aldridge": (70),
                    "LaMarcus Aldridge" -> "Tony Parker": (75),
                    "LaMarcus Aldridge" -> "Tim Duncan": (75),
                    "Tim Duncan" -> "Tony Parker": (95),
                    "Tim Duncan" -> "Manu Ginobili": (95),
                    "Ray Allen" -> "Rajon Rondo": (9),
                    "Tiago Splitter" -> "Tim Duncan": (80),
                    "Tiago Splitter" -> "Manu Ginobili": (90),
                    "Paul Gasol" -> "Kobe Bryant": (90),
                    "Paul Gasol" -> "Marc Gasol": (99),
                    "Aron Baynes" -> "Tim Duncan": (80),
                    "Vince Carter" -> "Tracy McGrady": (90),
                    "Vince Carter" -> "Jason Kidd": (70),
                    "Marc Gasol" -> "Paul Gasol": (99),
                    "Ben Simmons" -> "Joel Embiid": (80),
                    "Rajon Rondo" -> "Ray Allen": (-1),
                    "Manu Ginobili" -> "Tim Duncan": (90),
                    "Kyrie Irving" -> "LeBron James": (13),
                    "Carmelo Anthony" -> "LeBron James": (90),
                    "Carmelo Anthony" -> "Chris Paul": (90),
                    "Carmelo Anthony" -> "Dwyane Wade": (90),
                    "Dwyane Wade" -> "LeBron James": (90),
                    "Dwyane Wade" -> "Chris Paul": (90),
                    "Dwyane Wade" -> "Carmelo Anthony": (90),
                    "Joel Embiid" -> "Ben Simmons": (80),
                    "Damian Lillard" -> "LaMarcus Aldridge": (80),
                    "Yao Ming" -> "Tracy McGrady": (90),
                    "Yao Ming" -> "Shaquile O'Neal": (90),
                    "Dejounte Murray" -> "Tim Duncan": (99),
                    "Dejounte Murray" -> "Tony Parker": (99),
                    "Dejounte Murray" -> "Manu Ginobili": (99),
                    "Dejounte Murray" -> "Marco Belinelli": (99),
                    "Dejounte Murray" -> "Danny Green": (99),
                    "Dejounte Murray" -> "LeBron James": (99),
                    "Dejounte Murray" -> "Russell Westbrook": (99),
                    "Dejounte Murray" -> "Chris Paul": (99),
                    "Dejounte Murray" -> "Kyle Anderson": (99),
                    "Dejounte Murray" -> "Kevin Durant": (99),
                    "Dejounte Murray" -> "James Harden": (99),
                    "Dejounte Murray" -> "Tony Parker": (99),
                    "Blake Griffin" -> "Chris Paul": (-1),
                    "Steve Nash" -> "Amar'e Stoudemire": (90),
                    "Steve Nash" -> "Dirk Nowitzki": (88),
                    "Steve Nash" -> "Stephen Curry": (90),
                    "Steve Nash" -> "Jason Kidd": (85),
                    "Jason Kidd" -> "Vince Carter": (80),
                    "Jason Kidd" -> "Steve Nash": (90),
                    "Jason Kidd" -> "Dirk Nowitzki": (85),
                    "Dirk Nowitzki" -> "Steve Nash": (80),
                    "Dirk Nowitzki" -> "Jason Kidd": (80),
                    "Dirk Nowitzki" -> "Dwyane Wade": (10),
                    "Paul George" -> "Russell Westbrook": (95),
                    "Grant Hill" -> "Tracy McGrady": (90),
                    "Shaquile O'Neal" -> "JaVale McGee": (100),
                    "Shaquile O'Neal" -> "Tim Duncan": (80)
                    ''')

    assert resp.error_code == 0, resp.error_msg

    # insert edge teammate with uuid
    client.execute('''
                    INSERT EDGE teammate(start_year, end_year) VALUES 
                    "Tony Parker" -> "Tim Duncan": (2001, 2016),
                    "Tony Parker" -> "Manu Ginobili": (2002, 2018),
                    "Tony Parker" -> "LaMarcus Aldridge": (2015, 2018),
                    "Tony Parker" -> "Kyle Anderson": (2014, 2016),
                    "Tim Duncan" -> "Tony Parker": (2001, 2016),
                    "Tim Duncan" -> "Manu Ginobili": (2002, 2016),
                    "Tim Duncan" -> "LaMarcus Aldridge": (2015, 2016),
                    "Tim Duncan" -> "Danny Green": (2010, 2016),
                    "Manu Ginobili" -> "Tim Duncan": (2002, 2016),
                    "Manu Ginobili" -> "Tony Parker": (2002, 2016)
                    ''')

    assert resp.error_code == 0, resp.error_msg


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
            print('Authenticate failed: {}'.format(auth_resp.error_code))

        insert_data()
        # close connect pool
        connection_pool.close()

    except Exception as x:
        print(x)
        # close connect pool
        connection_pool.close()
        exit(-1)

