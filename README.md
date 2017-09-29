# Logs Analysis

This project will query a PostgreSQL database (called "news") located on a virtual machine using a python program in order to answer three questions. 

1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?

## news PostgreSQL database
News is a fictional news website. It contains three tables - `articles, authors, and log`. The schema for each can be found below:

```
                           Table "public.articles"
 Column |           Type           |                       Modifiers            
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


                  Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


                                  Table "public.log"
 Column |           Type           |                    Modifiers               
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
```


## Getting Started
In order to get a copy of the project up and running on your local machine for development and testing please see the instructions below.

### Prerequisites
- Python 3.6.2 installed. To download - go to [Python.org](https://www.python.org/downloads/release/python-362/).
- PostgreSQL.
- Virtual machine (if using) configured. See this [Vagrantfile](https://github.com/doobieroo/Logs-Analysis/blob/master/Vagrantfile) for use.
- Data downloaded. To download - go to [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). After downloading, unzip the file and place it in the vagrant directory - or whatever file is shared with your virtual machine.
- Data loaded. To do this - `cd` into your vagrant directory and use the command `psql -d news -f newsdata.sql`.
- Views in database "news" created. Download [create_views.sql](https://github.com/doobieroo/Logs-Analysis/blob/master/create_views.sql) Two views are needed (see below with script to create).

#### Views Needed
Run script `psql -d news -f create_views.sql` after downloading script above to create the necessary views. Views are detailed below. 

1. Create a view of all error requests in "log" table (anything other than '200 OK').

```sql
    CREATE VIEW err_reqs AS 
    SELECT time::date AS date, count(*) AS tot_err
    FROM log
    WHERE status <> '200 OK'
    GROUP BY date
    ORDER BY date ASC;
```

2. Create a view of all requests in "log" table (error and otherwise). 

```sql
    CREATE VIEW tot_reqs AS 
    SELECT time::date AS date, count(*) AS totals
    FROM log
    GROUP BY date
    ORDER BY date ASC;
```


### Installing
Download [Logs-Analysis](https://github.com/doobieroo/Logs-Analysis).


## Unit Testing
To test this code, ensure you are connected to the virtual machine, then from a console window (like Git Bash) run logs_analysis.py from the vagrant directory (or shared virtual machine directory). You will see the answers to the three questions printed out within the terminal window.

## License
This project is licensed under the GNU General Public License. See the [LICENSE](https://github.com/doobieroo/Logs-Analysis/blob/master/LICENSE) for details.