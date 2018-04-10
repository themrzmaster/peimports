

-- -----------------------------------------------------
-- Table ``.`files`
-- -----------------------------------------------------


SELECT apis.name, SUM(extract.call_number) as soma FROM apis INNER JOIN extract ON apis.idapis = extract.api GROUP BY apis.name  ORDER BY soma DESC
-- -----------------------------------------------------
<<<<<<< HEAD
=======


SELECT apis.name, SUM(extract.call_number) as soma FROM apis INNER JOIN extract ON apis.idapis = extract.api GROUP BY apis.name  ORDER BY soma DESC
-- -----------------------------------------------------
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c
ALTER TABLE modules ADD 'blacklist' INT;

CREATE TABLE IF NOT EXISTS `files` (
  `idfile` INT NOT NULL AUTO_INCREMENT,
  `hash` VARCHAR(255) NULL,
  `creation_time` DATE NULL,
  PRIMARY KEY (`idfile`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`modules`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `modules` (
  `idmodules` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  `blacklist` INT NULL,
  PRIMARY KEY (`idmodules`))
ENGINE = InnoDB;


<<<<<<< HEAD
<<<<<<< HEAD
-- -----------------------------------------------------
-- Table ``.`apis`
=======
=======
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c

-- Table `mydb`.`apis`
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apis` (
  `idapis` INT NOT NULL AUTO_INCREMENT,
  `module` INT NULL,
  `name` VARCHAR(45) NULL,
  `blacklist` INT NULL,
  PRIMARY KEY (`idapis`),
  INDEX `module_idx` (`module` ASC),
  CONSTRAINT `module`
    FOREIGN KEY (`module`)
    REFERENCES `modules` (`idmodules`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table ``.`extract`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `extract` (
  `idextract` INT NOT NULL AUTO_INCREMENT,
  `hash` INT NULL,
  `api` INT NULL,
  `call_number` INT NULL,
  PRIMARY KEY (`idextract`),
  INDEX `hash_idx` (`hash` ASC),
  INDEX `api_idx` (`api` ASC),
  CONSTRAINT `hash`
    FOREIGN KEY (`hash`)
    REFERENCES `files` (`idfile`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `api`
    FOREIGN KEY (`api`)
    REFERENCES `apis` (`idapis`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


