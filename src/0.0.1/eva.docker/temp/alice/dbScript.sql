DROP TABLE AuthurMaster;
CREATE TABLE IF NOT EXISTS `aflatun`.`AuthurMaster` (
  `AuthurID` VARCHAR(56) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `reference` VARCHAR(128) NULL,
  `description` VARCHAR(128) NULL,
  PRIMARY KEY (`AuthurID`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `aflatun`.`MetaContentMaster` (
  `ContentHash` VARCHAR(128) NOT NULL,
  `ContentKey` MEDIUMTEXT NOT NULL,
  `AuthurID` VARCHAR(56) NOT NULL,
  `source` VARCHAR(32) NULL,
  `contentIndex` INT(10) NULL,
  `excerpt` MEDIUMTEXT NULL,
  `body` LONGTEXT NULL,
  `fetchedOn` DATETIME NULL,
  `imageFileName` TEXT(512) NULL,
  `imageURL` MEDIUMTEXT NULL,
  `detailURL` MEDIUMTEXT NULL,
  PRIMARY KEY (`ContentHash`),
  INDEX `fk_MetaContentMaster_AuthurMaster_idx` (`AuthurID` ASC),
  CONSTRAINT `fk_MetaContentMaster_AuthurMaster`
    FOREIGN KEY (`AuthurID`)
    REFERENCES `aflatun`.`AuthurMaster` (`AuthurID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

DROP TABLE ContentEntities;
CREATE TABLE IF NOT EXISTS `aflatun`.`ContentEntities` (
  `entityID` VARCHAR(56) NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `type` TEXT NULL,
  `reference` TEXT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`entityID`))
ENGINE = InnoDB;

DROP TABLE MetaContentTOEntities;
CREATE TABLE IF NOT EXISTS `aflatun`.`MetaContentTOEntities` (
  `entityID` VARCHAR(56) NOT NULL,
  `ContentHash` VARCHAR(128) NOT NULL,
  `salience` DECIMAL NULL,
  INDEX `fk_MetaContentTOEntities_MetaContentMaster1_idx` (`ContentHash` ASC),
  PRIMARY KEY (`ContentHash`, `entityID`),
  INDEX `fk_MetaContentTOEntities_ContentEntities1_idx` (`entityID` ASC),
  CONSTRAINT `fk_MetaContentTOEntities_MetaContentMaster1`
    FOREIGN KEY (`ContentHash`)
    REFERENCES `aflatun`.`MetaContentMaster` (`ContentHash`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MetaContentTOEntities_ContentEntities1`
    FOREIGN KEY (`entityID`)
    REFERENCES `aflatun`.`ContentEntities` (`entityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;