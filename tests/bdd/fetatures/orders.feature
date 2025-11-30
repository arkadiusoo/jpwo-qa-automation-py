Feature: Sprawdzenie zamówień użytkownika

  Scenario: Sprawdzenie stanu pierwszego zamówienia
    Given użytkownik otwiera stronę logowania
    When wpisze email "admin@practicesoftwaretesting.com"
    And wpisze hasło "welcome01"
    And kliknie przycisk Log in
    And Wybiera pierwsze zamówienie
    Then Numer powinien być widoczny