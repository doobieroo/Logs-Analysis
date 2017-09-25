# Logs Analysis

This project will query a PostgreSQL database (called "news") located on a virtual machine using a Python program in order to answer three questions.

1. What are the most popular three articles of all time?
2. Who are the most popular authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Getting Started
In order to get a copy of the project up and running on your local machine for development and testing please see the instructions below.

### Prerequisites
- Python 3.6.2 installed. To download - go to [Python.org](https://www.python.org/downloads/release/python-362/).
- Data downloaded. To download - go to [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). After downloading, unzip the file and place it in the vagrant directory - or whatever file is shared with your virtual machine.
- Data loaded. To do this - `cd` into your vagrant directory and use the command `psql -d news -f newsdata.sql`.
- Views in database "news" created. Two views are needed (see below).

#### Views Needed
1. Create a view of all error requests in "log" table (anything other than '200 OK').

    `create view err_reqs as select to_char(time, 'YYYY-MM-DD') as date, count(*) as tot_err from log where status <> '200 OK' group by date order by date asc;`

2. Create a view of all requests in "log" table (error and otherwise). 

    `create view tot_reqs as select to_char(time, 'YYYY-MM-DD') as date, count(*) as totals from log group by date order by date asc;`



### Installing
Download [Logs-Analysis](https://github.com/doobieroo/Logs-Analysis).


## Unit Testing
To test this code, ensure you are connected to the virtual machine, then from a console window (like Git Bash) run logs_analysis.py from the vagrant directory (or shared virtual machine directory). You will see the answers to the three questions printed out within the terminal window.

## License
This project is licensed under the GNU General Public License. See the [LICENSE](https://github.com/doobieroo/Logs-Analysis/blob/master/LICENSE) for details.
