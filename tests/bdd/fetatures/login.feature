Feature: Logowanie użytkownika
  Scenariusze testują działanie formularza logowania w aplikacji
  https://practicesoftwaretesting.com/auth/login


  Scenario: Poprawne logowanie admina
    Given użytkownik otwiera stronę logowania
    When wpisze email "admin@practicesoftwaretesting.com"
    And wpisze hasło "welcome01"
    And kliknie przycisk Log in
    Then powinien zobaczyć menu użytkownika


  Scenario: Logowanie błędnymi danymi
    Given użytkownik otwiera stronę logowania
    When wpisze email "wrong@mail.com"
    And wpisze hasło "badpassword"
    And kliknie przycisk Log in
    Then powinien zobaczyć komunikat o błędnych danych