CREATE DATABASE /*!32312 IF NOT EXISTS*/`db.OSHES` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `db.OSHES`;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customer` (
`customerID` varchar(15) NOT NULL UNIQUE,
`customerName` varchar(50) NOT NULL,
`customerGender` char(1) NOT NULL,
`email` varchar(50) NOT NULL,
`address` varchar(50) NOT NULL,
`customerPhone` int(10) NOT NULL,
`customerPassword` varchar(50) NOT NULL,
PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `customers`*/

/*insert into `customers`(`customerID`, `customerName`, customerGender`, `email`, `address`, customerPhone`, customerPassword`) values
(*/

/*Table structure for table `administrator` */

DROP TABLE IF EXISTS `administator`;

CREATE TABLE `administrator` (
`adminID` varchar(15) NOT NULL UNIQUE,
`adminName` varchar(50) NOT NULL,
`adminGender` char(1) NOT NULL,
`adminPhone` int(10) NOT NULL,
`adminPassword` varchar(50) NOT NULL,
PRIMARY KEY (`adminID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `request`*/

DROP TABLE IF EXISTS `request`;

CREATE TABLE `request` (
`customerID` varchar(15) DEFAULT NULL,
`requestID` varchar(15) DEFAULT NULL,
`serviceAmount` decimal(10,2) DEFAULT NULL,
`servicePaymentDate` date DEFAULT NULL,
`requestStatus` varchar(50) DEFAULT 'N/A',
`requestDate` date DEFAULT NULL,
`AdminID` varchar(15) DEFAULT NULL,
PRIMARY KEY (`customerID`, `adminID`),
KEY
FOREIGN KEY (`adminID`) REFERENCES `administrator` (`adminID`)
);

DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
`itemID` varchar(15) NOT NULL,
`colour` varchar(50) NOT NULL,
`powerSupply` varchar(50) NOT NULL,
`factory` varchar(50) NOT NULL,
`productionYear` int NOT NULL,
`purchaseStatus` varchar(50) NOT NULL,
`serviceStatus` varchar(50) NOT NULL,
`purchaseDate` date DEFAULT NULL,
`customerID` varchar(15) DEFAULT NULL,
`adminID` varchar(15) DEFAULT NULL,
`productID` varchar(15) NOT NULL,
PRIMARY KEY (`itemID`),
FOREIGN KEY (`customerID`) REFERENCES `customer`(`customerID`),
FOREIGN KEY (`adminID`) REFERENCES `administrator`(`adminID`),
FOREIGN KEY (`productID`) REFERENCES `product`(`productID`) 
);

DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
`productID` varchar(15) NOT NULL,
`category` varchar(50) NOT NULL,
`model` varchar(50) NOT NULL,
`cost` decimal(10,2) NOT NULL,
`price` decimal(10,2) NOT NULL,
`warranty` int NOT NULL,
PRIMARY KEY (`productID`)
);

