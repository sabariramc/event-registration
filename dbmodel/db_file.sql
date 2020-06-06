-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema event
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema event
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8mb4 ;
USE `event` ;

-- -----------------------------------------------------
-- Table `event`.`d_admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event`.`d_admin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `creation_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_name` VARCHAR(45) NOT NULL,
  `password_hash` BINARY(60) NOT NULL,
  `email` VARCHAR(50) NULL,
  `is_email_verified` BIT(1) NOT NULL DEFAULT b'0',
  `is_active` BIT(1) NOT NULL DEFAULT b'1',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event`.`d_event_registration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event`.`d_event_registration` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `creation_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reg_uuid` VARCHAR(36) NOT NULL,
  `full_name` VARCHAR(200) NOT NULL,
  `mobile_number` VARCHAR(10) NOT NULL,
  `email_address` VARCHAR(100) NOT NULL,
  `mobile_country_code` VARCHAR(4) NULL,
  `registration_date` DATE NOT NULL,
  `registration_type` INT NOT NULL,
  `no_of_ticket` INT UNSIGNED NOT NULL,
  `id_card_path` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `reg_uuid_UNIQUE` (`reg_uuid` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event`.`c_enum`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `event`.`c_enum` (
  `enum_type_code` INT NOT NULL,
  `enum_type_name` VARCHAR(45) NOT NULL,
  `enum_value` INT NOT NULL,
  `enum_name` VARCHAR(45) NOT NULL,
  `enum_code` VARCHAR(45) NOT NULL,
  UNIQUE INDEX `AK_c_enum_01` (`enum_type_code` ASC, `enum_value` ASC),
  UNIQUE INDEX `AK_c_enum_02` (`enum_type_code` ASC, `enum_code` ASC),
  UNIQUE INDEX `AK_c_enum_03` (`enum_type_code` ASC, `enum_code` ASC))
ENGINE = InnoDB;

INSERT INTO `event`.`c_enum` (`enum_type_code`, `enum_type_name`, `enum_value`, `enum_name`, `enum_code`) VALUES (100, 'REGISTRATION_TYPE', 1, 'Self', 'SELF');
INSERT INTO `event`.`c_enum` (`enum_type_code`, `enum_type_name`, `enum_value`, `enum_name`, `enum_code`) VALUES (100, 'REGISTRATION_TYPE', 2, 'Group', 'GROUP');
INSERT INTO `event`.`c_enum` (`enum_type_code`, `enum_type_name`, `enum_value`, `enum_name`, `enum_code`) VALUES (100, 'REGISTRATION_TYPE', 3, 'Corporate', 'CORPORATE');
INSERT INTO `event`.`c_enum` (`enum_type_code`, `enum_type_name`, `enum_value`, `enum_name`, `enum_code`) VALUES (100, 'REGISTRATION_TYPE', 4, 'Others', 'OTHERS');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
