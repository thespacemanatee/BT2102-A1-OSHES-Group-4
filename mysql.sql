CREATE DATABASE /*!32312 IF NOT EXISTS*/`db.OSHES` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `db.OSHES`;


/*table structure for `CUSTOMER`*/
DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
`customerID` varchar(15) NOT NULL UNIQUE,
`customerName` varchar(50) NOT NULL,
`customerGender` char(1) NOT NULL,
`email` varchar(100) NOT NULL,
`address` varchar(50) NOT NULL,
`customerPhone` int(10) NOT NULL,
`customerPassword` varchar(50) NOT NULL,
PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*data for the table `customer`*/
insert into `customer`(`customerID`, `customerName`, customerGender`, `email`, `address`, customerPhone`, customerPassword`) values
('id1', 'Aly', 'F', 'aly@bt.com', 'sg', 1234567890, 'pass1'), 
('id2', 'Ben', 'M', 'ben@bt.com', 'sg', 1234567809, 'pass2'),
('id3', 'Carl', 'M', 'carl@bt.com', 'sg', 1234567980, 'pass3');





/*table structure for table `ADMINISTRATOR` */
DROP TABLE IF EXISTS `administator`;

CREATE TABLE `administrator` (
`adminID` varchar(15) NOT NULL UNIQUE,
`adminName` varchar(50) NOT NULL,
`adminGender` char(1) NOT NULL,
`adminPhone` int(10) NOT NULL,
`adminPassword` varchar(50) NOT NULL,
PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*data for the table `administrator*/
insert into `administrator`(`adminID`, `adminName`, adminGender`, `adminPhone`, `adminPassword`) values
('id4', 'Dina', 'F', 1234568790, 'pass4'),
('id5', 'Ferb', 'M', 1234576890, 'pass5'),
('id6', 'Greg', 'M', 1234657890, 'pass6');





/*table structure for table `REQUEST`*/
DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
`customerID` varchar(15) DEFAULT NULL,
`requestID` varchar(15) DEFAULT NULL,
`serviceAmount` decimal(10,2) DEFAULT NULL,
`servicePaymentDate` date DEFAULT NULL,
`requestStatus` varchar(50) DEFAULT 'N/A',
`requestDate` date DEFAULT NULL,
`adminID` varchar(15) DEFAULT NULL,
PRIMARY KEY (`customerID`, `requestID`),
CONSTRAINT `request_ibfk_1` FOREIGN KEY (`adminID`) REFERENCES `administrator` (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*data for the table `request` */
/*insert into `request` (`customerID`, `requestID`, `serviceAmount`, `servicePaymentDate`, `requestStatus`, `requestDate`, `AdminID`) values */





/*table stucture for table `ITEM`*/
DROP TABLE IF EXISTS `item`;

CREATE TABLE `item` (
`itemID` varchar(15) NOT NULL UNIQUE,
`colour` varchar(50) NOT NULL,
`powerSupply` varchar(50) NOT NULL,
`factory` varchar(50) NOT NULL,
`productionYear` int NOT NULL,
`purchaseStatus` varchar(50) NOT NULL,
`serviceStatus` varchar(50) DEFAULT 'N/A',
`purchaseDate` date DEFAULT NULL,
`customerID` varchar(15) DEFAULT NULL,
`adminID` varchar(15) DEFAULT NULL,
`productID` varchar(15) NOT NULL,
PRIMARY KEY (`itemID`),
KEY `customerID` (`customerID`),
KEY `adminID` (`adminID`),
KEY `productID` (`productID`),
CONSTRAINT `item_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `customer`(`customerID`),
CONSTRAINT `item_ibfk_2` FOREIGN KEY (`adminID`) REFERENCES `administrator`(`adminID`),
CONSTRAINT `item_ibfk_3` FOREIGN KEY (`productID`) REFERENCES `product`(`productID`) 
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*data for the table `item`*/
/*insert into `item`(`itemID`, `colour`, `powerSupply`, `factory`, `productionYear`, `purchaseStatus`, `serviceStatus`, `purchaseDate`, `customerID`, `adminID`, `productID`) values */





/* table structure for `PRODUCT`*/
DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
`productID` varchar(15) NOT NULL UNIQUE,
`category` varchar(50) NOT NULL,
`model` varchar(50) NOT NULL,
`cost` decimal(10,2) NOT NULL,
`price` decimal(10,2) NOT NULL,
`warranty` int NOT NULL,
PRIMARY KEY (`productID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*data for the table `product`*/
/*insert into `product`(`productID`, `category`, `model`, `cost`, `price`, `warranty`) values */

/*to return if the item purchased is still under warranty*/ /*STILL UNSURE*/
SELECT itemID, T2.warranty >= DATEDIFF(month, requestDate, purchaseDate) AS warranty_status from item AS T1 
LEFT JOIN product as T2 ON T1.productID = T2.productID
LEFT JOIN request as T3 ON T1.customerID = T3.customerID;

