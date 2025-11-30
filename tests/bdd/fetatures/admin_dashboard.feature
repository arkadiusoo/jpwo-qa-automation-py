Feature: Dashboard administratora
  Testy weryfikują elementy dostępne po zalogowaniu jako administrator.

  Scenario: Widoczność wykresu raportów na dashboardzie admina
    Given administrator otwiera stronę logowania
    When wpisze email "admin@practicesoftwaretesting.com"
    And wpisze hasło "welcome01"
    And kliknie przycisk Log in
    And otworzy menu użytkownika
    And przejdzie do dashboardu administratora
    Then wykres raportów powinien być widoczny