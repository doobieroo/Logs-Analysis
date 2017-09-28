#!/usr/bin/env python3

import psycopg2
import sys

DBNAME = "news"


# func to execute db queries
def execute_query(query):
    try:
        # connect to database named "news"
        db = psycopg2.connect(database=DBNAME)
        # open cursor for use with query
        c = db.cursor()
        # execute the query
        c.execute(query)
        # store the results of the query using fetchall
        results = c.fetchall()
        # close db connection
        db.close()
        # return the results of the query
        return (results)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# func to find 3 most accessed articles sorted with most pop article at top
def get_articles():

    # SQL to retrieve most popular three articles
    query = ("""
        SELECT title, count(title)
        FROM log, articles
        WHERE '/article/' || articles.slug = log.path
        GROUP BY title
        ORDER BY count DESC
        LIMIT 3""")
    # call execute_query function to perform query
    pop_articles = execute_query(query)

    # print header for popular articles
    print('\nWhat are the most popular three articles of all time?\n')

    # for every row print article name and nbr of views
    for title, views in pop_articles:
        lst = "  " + '"' + title + '"' + " - " + str(views) + " views\n"
        sys.stdout.write(lst)


# func to find the authors w/ most pg views sorted w/ most pop author at top
def get_authors():

    # SQL to retrieve most popular authors
    query = ("""
        SELECT name, count(title)
        FROM log, articles, authors
        WHERE '/article/' || articles.slug = log.path
        AND authors.id = articles.author
        GROUP BY authors.name
        ORDER BY count DESC""")

    # call execute_query function to perform query
    pop_authors = execute_query(query)

    # print header for popular authors
    print('\nWho are the most popular article authors of all time?\n')

    # for every row print author name and total views
    for name, views in pop_authors:
        print("  ", name, "-", views, "views")


# function to find which days received more than 1% of error requests
def get_errors():

    # SQL to retrieve error codes more than 1% (from 2 diff views)
    query = ("""
        WITH t AS (
            SELECT tot_reqs.date,
                   round((tot_err::numeric / totals::numeric) * 100, 2)
                    AS pct_errs
            FROM err_reqs, tot_reqs
            WHERE err_reqs.date = tot_reqs.date
            )
        SELECT to_char(date, 'TMMonth DD"," YYYY'),
               pct_errs
        FROM t
        WHERE pct_errs > 1.0""")

    # call execute_query function to perform query
    err_days = execute_query(query)

    # print header for error days
    print("\nOn which days did more than 1% of requests lead to errors?\n")

    # for every row print date (Month DD, YYYY) and err %
    for date, pct_errs in err_days:
        bad_status = "  " + date + " - " + str(pct_errs) + "% errors\n"
        sys.stdout.write(bad_status)
        print('\n')


# execute all three functions
if __name__ == '__main__':
    get_articles()

    get_authors()

    get_errors()
