DROP DATABASE IF EXISTS `db.OSHES`;

CREATE DATABASE IF NOT EXISTS `db.OSHES`;

USE `db.OSHES`;

CREATE TABLE `customer`
(
    `id`       varchar(50) NOT NULL,
    `name`     varchar(50) NOT NULL,
    `gender`   varchar(50) NOT NULL,
    `email`    varchar(50) NOT NULL,
    `address`  varchar(50) NOT NULL,
    `phone`    int(20)     NOT NULL,
    `password` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
);

/*test data for the table `customer`*/
/*insert into `customer`(`customerID`, `customerName`, `customerGender`, `email`, `address`, `customerPhone`, `customerPassword`) values
(1, 'Aly', 'F', 'aly@bt.com', 'sg', 1234567890, 'pass1'), 
(2, 'Ben', 'M', 'ben@bt.com', 'sg', 1234567809, 'pass2'),
(3, 'Carl', 'M', 'carl@bt.com', 'sg', 1234567980, 'pass3');*/

CREATE TABLE `administrator`
(
    `id`       varchar(50) NOT NULL,
    `name`     varchar(50) NOT NULL,
    `gender`   varchar(50) NOT NULL,
    `phone`    int(20)     NOT NULL,
    `password` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
);

/*test data for the table `administrator*/
/*insert into `administrator`(`adminID`, `adminName`, `adminGender`, `adminPhone`, `adminPassword`) values
(4, 'Dina', 'F', 1234568790, 'pass4'),
(5, 'Ferb', 'M', 1234576890, 'pass5'),
(6, 'Greg', 'M', 1234657890, 'pass6');*/

CREATE TABLE `request`
(
    `id`                   int            NOT NULL AUTO_INCREMENT,
    `service_amount`       decimal(10, 2) DEFAULT NULL,
    `service_payment_date` date           DEFAULT NULL,
    `request_status`       varchar(50)    NOT NULL,
    `request_date`         date           NOT NULL,
    `customer_id`          varchar(50)    DEFAULT NULL,
    `admin_id`             varchar(50)    DEFAULT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `request_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
    CONSTRAINT `request_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `administrator` (`id`)
);

/*test data for the table `request` */
/*insert into `request` (`customerID`, `requestID`, `serviceAmount`, `servicePaymentDate`, `requestStatus`, `requestDate`, `adminID`) values
('id1', 001, 0.00, '13-01-21', 'submitted', '12-01-21', 'id6');*/

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

/*test data for the table `product`*/
/*insert into `product`(`productID`, `category`, `model`, `cost`, `price`, `warranty`) values
(1, 'light', 'safehome', 89.00, 120.00, 6);*/

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
    `admin_id`        varchar(50) DEFAULT NULL,
    `product_id`      int         NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `item_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
    CONSTRAINT `item_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `administrator` (`id`),
    CONSTRAINT `item_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
);

/*test data for the table `item`*/
/*insert into `item`(`itemID`, `colour`, `powerSupply`, `factory`, `productionYear`, `purchaseStatus`, `serviceStatus`, `purchaseDate`, `customerID`, `adminID`, `productID`) values
('1001', 'black', 'battery', 'malaysia', 2014, 'sold', '', '23-01-21', 'id1', 'id4', 1);*/




