#!/usr/bin/env python3

import psycopg2
import sys

DBNAME = "news"


# func to find 3 most accessed articles sorted with most pop article at top
def get_articles():

    # connect to database named "news"
    db = psycopg2.connect(database=DBNAME)
    # open cursor for use with query
    c = db.cursor()

    # execute sql to retrieve most popular three articles
    c.execute("""
        select title, count(title)
        from log, articles
        where substring(path, 10) = slug
        group by title
        order by count desc
        limit 3""")

    # retrieve data from query using fetchall
    pop_articles = c.fetchall()
    # print header for popular articles
    print('\nWhat are the most popular three articles of all time?\n')

    # for every row print article name and nbr of views
    for row in pop_articles:
        lst = "  " + '"' + row[0] + '"' + " - " + str(row[1]) + " views\n"
        sys.stdout.write(lst)

    # close db connection
    db.close()


# func to find the authors w/ most pg views sorted w/ most pop author at top
def get_authors():

    # connect to a database named "news"
    db = psycopg2.connect(database=DBNAME)
    # open cursor for use with query
    c = db.cursor()

    # execute sql to retrieve most popular authors
    c.execute("""
        select name, count(title)
        from log, articles, authors
        where substring(path, 10) = slug and authors.id = articles.author
        group by authors.name
        order by count desc""")

    # retrieve data from query using fetchall
    pop_authors = c.fetchall()
    # print header for popular authors
    print('\nWho are the most popular article authors of all time?\n')

    # for every row print author name and total views
    for row in pop_authors:
        print("  ", row[0], "-", row[1], "views")

    # close db connection
    db.close()


# function to find which days received more than 1% of error requests
def get_errors():

    # connect to a database named "news"
    db = psycopg2.connect(database=DBNAME)
    # open cursor for use with query
    c = db.cursor()

    # execute sql to retrieve error codes more than 1% (from 2 diff views)
    c.execute("""
        with t as (
            select tot_reqs.date,
                   round((tot_err::numeric / totals::numeric) * 100, 2)
                    as pct_errs
            from err_reqs, tot_reqs
            where err_reqs.date = tot_reqs.date
            )
        select to_char(to_date(date, 'YYYY-MM-DD'), 'TMMonth DD"," YYYY'),
               pct_errs
        from t
        where pct_errs > 1.0""")

    # retrieve data from query using fetchall
    err_days = c.fetchall()
    # print header for error days
    print("\nOn which days did more than 1% of requests lead to errors?\n")

    # for every row print date (Month DD, YYYY) and err %
    for row in err_days:
        bad_status = "  " + row[0] + " - " + str(row[1]) + "% errors\n"
        sys.stdout.write(bad_status)
        print('\n')

    # close db connection
    db.close()


# execute all three functions
if __name__ == '__main__':
    get_articles()

    get_authors()

    get_errors()
