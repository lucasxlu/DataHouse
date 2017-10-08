/*
Navicat MySQL Data Transfer

Source Server         : cvlh
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : qcwy

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2017-10-08 17:30:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 51job
-- ----------------------------
DROP TABLE IF EXISTS `51job`;
CREATE TABLE `51job` (
  `cjobname` varchar(255) DEFAULT NULL,
  `cocname` varchar(255) DEFAULT NULL,
  `coid` varchar(255) DEFAULT NULL,
  `hasposted` varchar(255) DEFAULT NULL,
  `isexpired` varchar(255) DEFAULT NULL,
  `isjump` varchar(255) DEFAULT NULL,
  `jobareaname` varchar(255) DEFAULT NULL,
  `jobid` varchar(255) DEFAULT NULL,
  `jobsalaryname` varchar(255) DEFAULT NULL,
  `jumpurl` varchar(255) DEFAULT NULL,
  `typeid` varchar(255) DEFAULT NULL,
  `placeid` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for dict
-- ----------------------------
DROP TABLE IF EXISTS `dict`;
CREATE TABLE `dict` (
  `tname` varchar(255) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for unit_convert
-- ----------------------------
DROP TABLE IF EXISTS `unit_convert`;
CREATE TABLE `unit_convert` (
  `unit` varchar(255) DEFAULT NULL,
  `ratio` int(10) DEFAULT NULL,
  `model` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Function structure for filter_num
-- ----------------------------
DROP FUNCTION IF EXISTS `filter_num`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `filter_num`(str varchar(100)) RETURNS varchar(100) CHARSET utf8
    READS SQL DATA
return REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(str,'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9',''),'.',''),'-','')
;;
DELIMITER ;
