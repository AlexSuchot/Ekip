-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  mar. 28 jan. 2020 à 12:23
-- Version du serveur :  5.7.24
-- Version de PHP :  7.2.14
--
-- Base de données :  `blockchain_ekip`
--

-- --------------------------------------------------------

--
-- Structure de la table `block`
--

CREATE TABLE IF NOT EXISTS `block` (
  `contributeur` varchar(255) NOT NULL,
  `previous_hash`varchar(255) NOT NULL,
  `hash` varchar(255) NOT NULL,
  `nonce` varchar(255) NOT NULL
);
