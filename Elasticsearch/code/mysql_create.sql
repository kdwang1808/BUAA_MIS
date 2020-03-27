CREATE TABLE news (
    id varchar(255) NOT NULL,
    url varchar(255) NOT NULL,
    datestr varchar(255) NOT NULL,
    title varchar(255) NOT NULL,
    content varchar(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;