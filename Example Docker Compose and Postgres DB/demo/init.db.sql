CREATE TABLE IF NOT EXISTS quotes (
    day_of_week VARCHAR(20) NOT NULL,
    quote VARCHAR(2000) NOT NULL
);

INSERT INTO
    quotes (day_of_week, quote)
VALUES
    (
        'sunday',
        'Life is about making an impact, not making an income. -Kevin Kruse'
    ),
    (
        'monday',
        'Whatever the mind of man can conceive and believe, it can achieve. -Napoleon Hill'
    ),
    (
        'tuesday',
        'Strive not to be a success, but rather to be of value. -Albert Einstein'
    ),
    (
        'wednesday',
        'You miss 100% of the shots you dont take. -Wayne Gretzky'
    ),
    (
        'thursday',
        'Every strike brings me closer to the next home run. -Babe Ruth'
    ),
    (
        'friday',
        'We become what we think about. -Earl Nightingale'
    ),
    (
        'saturday',
        'Life is what happens to you while you are busy making other plans. -John Lennon'
    );