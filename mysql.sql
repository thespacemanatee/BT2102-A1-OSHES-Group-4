CREATE DATABASE /*!32312 IF NOT EXISTS*/`db.OSHES` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `db.OSHES`;


/*table structure for `CUSTOMER`*/
DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
`customerID` int AUTO_INCREMENT,
`customerName` varchar(50) NOT NULL,
`customerGender` char(1) NOT NULL,
`email` varchar(100) NOT NULL,
`address` varchar(50) NOT NULL,
`customerPhone` int(10) NOT NULL,
`customerPassword` varchar(50) NOT NULL,
PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*test data for the table `customer`*/
/*insert into `customer`(`customerID`, `customerName`, `customerGender`, `email`, `address`, `customerPhone`, `customerPassword`) values
(1, 'Aly', 'F', 'aly@bt.com', 'sg', 1234567890, 'pass1'), 
(2, 'Ben', 'M', 'ben@bt.com', 'sg', 1234567809, 'pass2'),
(3, 'Carl', 'M', 'carl@bt.com', 'sg', 1234567980, 'pass3');*/





/*table structure for table `ADMINISTRATOR` */
DROP TABLE IF EXISTS `administrator`;

CREATE TABLE `administrator` (
`adminID` int AUTO_INCREMENT,
`adminName` varchar(50) NOT NULL,
`adminGender` char(1) NOT NULL,
`adminPhone` int(10) NOT NULL,
`adminPassword` varchar(50) NOT NULL,
PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*test data for the table `administrator*/
/*insert into `administrator`(`adminID`, `adminName`, `adminGender`, `adminPhone`, `adminPassword`) values
(4, 'Dina', 'F', 1234568790, 'pass4'),
(5, 'Ferb', 'M', 1234576890, 'pass5'),
(6, 'Greg', 'M', 1234657890, 'pass6');*/





/*table structure for table `REQUEST`*/
DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
`requestID` int AUTO_INCREMENT,
`serviceAmount` decimal(10,2) DEFAULT NULL,
`servicePaymentDate` date DEFAULT NULL,
`requestStatus` varchar(50) DEFAULT '',
`requestDate` date DEFAULT NULL,
`adminID` int DEFAULT NULL,
PRIMARY KEY (`requestID`),
CONSTRAINT `request_ibfk_1` FOREIGN KEY (`adminID`) REFERENCES `administrator` (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*test data for the table `request` */
/*insert into `request` (`customerID`, `requestID`, `serviceAmount`, `servicePaymentDate`, `requestStatus`, `requestDate`, `adminID`) values
('id1', 001, 0.00, '13-01-21', 'submitted', '12-01-21', 'id6');*/




/* table structure for `PRODUCT`*/
DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
`productID` int UNIQUE,
`category` varchar(50) NOT NULL,
`model` varchar(50) NOT NULL,
`cost` decimal(10,2) NOT NULL,
`price` decimal(10,2) NOT NULL,
`warranty` int NOT NULL,
PRIMARY KEY (`productID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*test data for the table `product`*/
/*insert into `product`(`productID`, `category`, `model`, `cost`, `price`, `warranty`) values
(1, 'light', 'safehome', 89.00, 120.00, 6);*/





/*table stucture for table `ITEM`*/
DROP TABLE IF EXISTS `item`;

CREATE TABLE `item` (
`itemID` int(4) NOT NULL UNIQUE,
`colour` varchar(50) NOT NULL,
`powerSupply` varchar(50) NOT NULL,
`factory` varchar(50) NOT NULL,
`productionYear` int NOT NULL,
`purchaseStatus` varchar(6) NOT NULL,
`serviceStatus` varchar(50) DEFAULT '',
`purchaseDate` date DEFAULT NULL,
`customerID` int DEFAULT NULL,
`adminID` int DEFAULT NULL,
`productID` int NOT NULL,
PRIMARY KEY (`itemID`),
KEY `customerID` (`customerID`),
KEY `adminID` (`adminID`),
KEY `productID` (`productID`),
CONSTRAINT `item_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `customer`(`customerID`),
CONSTRAINT `item_ibfk_2` FOREIGN KEY (`adminID`) REFERENCES `administrator`(`adminID`),
CONSTRAINT `item_ibfk_3` FOREIGN KEY (`productID`) REFERENCES `product`(`productID`) 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*test data for the table `item`*/
/*insert into `item`(`itemID`, `colour`, `powerSupply`, `factory`, `productionYear`, `purchaseStatus`, `serviceStatus`, `purchaseDate`, `customerID`, `adminID`, `productID`) values
('1001', 'black', 'battery', 'malaysia', 2014, 'sold', '', '23-01-21', 'id1', 'id4', 1);*/




