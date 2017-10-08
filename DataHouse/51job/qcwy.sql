/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : qcwy

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2017-10-08 15:46:37
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
