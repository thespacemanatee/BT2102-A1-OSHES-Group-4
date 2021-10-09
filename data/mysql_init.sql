DROP
DATABASE IF EXISTS `db.OSHES`;

CREATE
DATABASE IF NOT EXISTS `db.OSHES`;

USE
`db.OSHES`;

CREATE TABLE `customer`
(
    `id`       varchar(50) NOT NULL,
    `name`     varchar(50) NOT NULL,
    `gender`   varchar(50) NOT NULL,
    `email`    varchar(50) NOT NULL,
    `address`  varchar(50) NOT NULL,
    `phone`    int(20) NOT NULL,
    `password` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `administrator`
(
    `id`       varchar(50) NOT NULL,
    `name`     varchar(50) NOT NULL,
    `gender`   varchar(50) NOT NULL,
    `phone`    int(20) NOT NULL,
    `password` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `product`
(
    `id`       int            NOT NULL,
    `category` varchar(50)    NOT NULL,
    `model`    varchar(50)    NOT NULL,
    `cost`     decimal(10, 2) NOT NULL,
    `price`    decimal(10, 2) NOT NULL,
    `warranty` int            NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `item`
(
    `id`              int         NOT NULL,
    `colour`          varchar(50) NOT NULL,
    `power_supply`    varchar(50) NOT NULL,
    `factory`         varchar(50) NOT NULL,
    `production_year` int         NOT NULL,
    `purchase_status` varchar(6)  NOT NULL,
    `service_status`  varchar(50) DEFAULT '',
    `purchase_date`   date        DEFAULT NULL,
    `customer_id`     varchar(50) DEFAULT NULL,
    `product_id`      int         NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `item_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
    CONSTRAINT `item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
);

CREATE TABLE `request`
(
    `id`                   int         NOT NULL AUTO_INCREMENT,
    `service_amount`       decimal(10, 2) DEFAULT 0.00,
    `service_payment_date` date           DEFAULT NULL,
    `request_status`       varchar(50) NOT NULL,
    `request_date`         date        NOT NULL,
    `customer_id`          varchar(50) NOT NULL,
    `item_id`              int         NOT NULL,
    `admin_id`             varchar(50)    DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `request_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
    CONSTRAINT `request_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
    CONSTRAINT `request_ibfk_3` FOREIGN KEY (`admin_id`) REFERENCES `administrator` (`id`)
);
