# Created by Jakub at 30.11.2025
Feature: Dodawanie do koszyka
  # Enter feature description here

  Scenario: Dodawanie do koszyka
    Given Wybiera stronę główną
    When Wybiera pierwszy produkt
    When Dodaje produkt do koszyka
    Then Powinien widzieć koszyk