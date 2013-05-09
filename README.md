About
-----

Oopa is a password/wordlist analyser. It is highly modular, allowing users to write their own analyzers in Python with minimal effort. It supports user-supplied encoding and output can be heavily customized.

Consider this software so in Alpha stage that it's in Omega. In fact, you mine as well just go use Pipal (http://www.digininja.org/projects/pipal.php).

Examples
-------
You specify a module with the --analysis argument. Default output is top 10.

    $ python oopa.py --analysis keyword wordlists/phpbb.txt 
    +----------+-------+
    | Keyword  | Count |
    +----------+-------+
    |  phpbb   |  332  |
    |   php    |  127  |
    | password |   89  |
    |  dragon  |   76  |
    |   pass   |   70  |
    |   mike   |   69  |
    |   blue   |   67  |
    |   test   |   66  |
    |  qwerty  |   59  |
    |   alex   |   58  |
    +----------+-------+

You can view the same data in a more parse-friendly format with --greppable.

    $ python oopa.py --analysis keyword wordlists/phpbb.txt --greppable
    #Keyword:Count
    phpbb:332
    php:127
    password:89
    dragon:76
    pass:70
    mike:69
    blue:67
    test:66
    qwerty:59
    alex:58

You can change the number of results with --top.

    $ python oopa.py --analysis length wordlists/phpbb.txt --top 20
    +--------+------------+-------+
    | Length | Percentage | Count |
    +--------+------------+-------+
    |   1    |    0.02    |   32  |
    |   2    |    0.07    |  137  |
    |   3    |    0.42    |  776  |
    |   4    |    2.49    |  4598 |
    |   5    |    4.45    |  8198 |
    |   6    |   22.82    | 42070 |
    |   7    |   17.75    | 32731 |
    |   8    |   30.01    | 55338 |
    |   9    |   10.41    | 19188 |
    |   10   |    6.45    | 11896 |
    |   11   |    2.68    |  4933 |
    |   12   |    1.36    |  2505 |
    |   13   |    0.55    |  1018 |
    |   14   |    0.28    |  515  |
    |   15   |    0.13    |  232  |
    |   16   |    0.07    |  125  |
    |   17   |    0.02    |   36  |
    |   18   |    0.01    |   27  |
    |   19   |    0.0     |   9   |
    |   20   |    0.0     |   8   |
    +--------+------------+-------+

You can change the column sorting is based on with --sort.

    $ python oopa.py --analysis length wordlists/phpbb.txt  --sort Count
    +--------+------------+-------+
    | Length | Percentage | Count |
    +--------+------------+-------+
    |   8    |   30.01    | 55338 |
    |   6    |   22.82    | 42070 |
    |   7    |   17.75    | 32731 |
    |   9    |   10.41    | 19188 |
    |   10   |    6.45    | 11896 |
    |   5    |    4.45    |  8198 |
    |   11   |    2.68    |  4933 |
    |   4    |    2.49    |  4598 |
    |   12   |    1.36    |  2505 |
    |   13   |    0.55    |  1018 |
    +--------+------------+-------+

Name
----
OOPA was briefly an acronym, before I forgot what it stood for.
