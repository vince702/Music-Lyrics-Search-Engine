#!/usr/bin/python3

import psycopg2
import re
import string
import sys

_PUNCTUATION = frozenset(string.punctuation)

def _remove_punc(token):
    """Removes punctuation from start/end of token."""
    i = 0
    j = len(token) - 1
    idone = False
    jdone = False
    while i <= j and not (idone and jdone):
        if token[i] in _PUNCTUATION and not idone:
            i += 1
        else:
            idone = True
        if token[j] in _PUNCTUATION and not jdone:
            j -= 1
        else:
            jdone = True
    return "" if i > j else token[i:(j+1)]

def _get_tokens(query):
    rewritten_query = []
    tokens = re.split('[ \n\r]+', query)
    for token in tokens:
        cleaned_token = _remove_punc(token)
        if cleaned_token:
            if "'" in cleaned_token:
                cleaned_token = cleaned_token.replace("'", "''")
            rewritten_query.append(cleaned_token)
    return rewritten_query




import hashlib



def search(query, query_type,itemnum):
    
    rewritten_query = _get_tokens(query)
    for i in range(len(rewritten_query)):
        rewritten_query[i] =   rewritten_query[i].lower()
    rewritten_query = set(rewritten_query)


    """TODO
    Your code will go here. Refer to the specification for projects 1A and 1B.
    But your code should do the following:
    1. Connect to the Postgres database.
    2. Graciously handle any errors that may occur (look into try/except/finally).
    3. Close any database connections when you're done.
    4. Write queries so that they are not vulnerable to SQL injections.
    5. The parameters passed to the search function may need to be changed for 1B. 
    """
    viewname = ""
    for i in rewritten_query:
        viewname += (i+'_')

    viewname += query_type


    if query_type == "pagination":
        return [];
    if query_type == 'and':
     
        subquery = """
      



        SELECT song.song_name,artist.artist_name, song.page_link,total_score

        FROM artist INNER JOIN song ON artist.artist_id = song.artist_id
                    INNER JOIN 

            ( SELECT song_id, SUM(score) as total_score, COUNT(score) as num_matches from tfidf 

            WHERE """;

        count = 1

        for i in rewritten_query :
            if count < len(rewritten_query):
                 count += 1;
                 subquery += """ token=%s OR """
            else:
                 subquery += """ token=%s """

        
        subquery += """ GROUP BY song_id  HAVING COUNT(score)={} ORDER BY SUM(score) DESC)  sq ON sq.song_id = song.song_id

        ORDER BY total_score DESC

        """.format(len(rewritten_query))


        dquery = subquery  

    else: 

        subquery = """

    

        SELECT song.song_name,artist.artist_name, song.page_link,total_score

        FROM artist INNER JOIN song ON artist.artist_id = song.artist_id
                    INNER JOIN 

            ( SELECT song_id, SUM(score) as total_score from tfidf 

            WHERE """;

        count = 1

        for i in rewritten_query :
            if count < len(rewritten_query):
                 count += 1;
                 subquery += """ token=%s OR """
            else:
                 subquery += """ token=%s """

        
        subquery += """ GROUP BY song_id  ORDER BY SUM(score) DESC)  sq ON sq.song_id = song.song_id
            ORDER BY total_score DESC



        """


        dquery = subquery     


    connection=0
    cursor=0

    


    mview_name = "mv_"
    for i in rewritten_query:
        mview_name += (i + '_')

    mview_name += query_type;

    mview_name = re.sub(r'[^a-z]', '_', mview_name)

    real_query = """SELECT * FROM {} LIMIT 21 OFFSET %s """.format(mview_name)

    try:
        connection = psycopg2.connect(user="cs143",password="cs143",host="localhost",port=5432,database='searchengine')
        cursor = connection.cursor()

        args = tuple(rewritten_query)

       
        mview_string = "CREATE MATERIALIZED VIEW IF NOT EXISTS {} AS".format(mview_name)

        dquery = mview_string + dquery
        cursor.execute(dquery,args)


        rows = []
        cursor.execute(real_query,(itemnum,))
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        

    except:
        try: 
            connection.close()
        except:
            pass
        try:
            cursor.close()
        except:
            pass


        rows = []
        pass




    return rows

if __name__ == "__main__":
    if len(sys.argv) > 2:
        result = search(' '.join(sys.argv[2:]), sys.argv[1].lower())
        print(result)
    else:
        print("USAGE: python3 search.py [or|and] term1 term2 ...")

