import unittest
from dataclasses import dataclass
from typing import Optional

from lib.salary import DAY, HOUR, WEEK, YEAR, extract_salary, salary_unit


@dataclass
class salarytest:
    """test case for salary parser"""

    text: str
    min: Optional[float] = None
    max: Optional[float] = None
    unit: Optional[int] = None
    super: Optional[bool] = None


salary_tests = [
    salarytest("Attractive renumeration"),
    salarytest("Competitive"),
    salarytest("A04 level"),
    salarytest("$NEG"),
    # salarytest("Daily/Hourly rate"),
    salarytest("Daily rate", unit=DAY),
    salarytest("Highly Lucrative Call out $"),
    salarytest("13% Super"),
    salarytest("$55 - $65 per hour", 55, 65, HOUR),
    salarytest("$35-$40/h +Super, Car, Fuel Card, Tablet, Phone", 35, 40, HOUR, False),
    salarytest("Paid at an hourly rate of $46.75", 46.75, unit=HOUR),
    salarytest("$31.39 per hour plus superannuation", 31.39, unit=HOUR, super=False),
    salarytest(
        "$26.76 per hour (level 2) PLUS other benefits and allowances", 26.76, unit=HOUR
    ),
    salarytest("$45.00 hourly rate plus superannuation", 45, unit=HOUR, super=False),
    salarytest("$40.01 /hour", 40.01, unit=HOUR),
    salarytest("$40.01 ph", 40.01, unit=HOUR),
    salarytest(
        "25.98 p/hr excluding casual allowance and penalities", 25.98, unit=HOUR
    ),
    salarytest("$700 - $800 per day", 700, 800, DAY),
    salarytest("$0 - $650 per day", 0, 650, DAY),
    salarytest("1800+ Weekly", 1_800, unit=WEEK),
    salarytest("$300-$2000 weekly", 300, 2_000, unit=WEEK),
    salarytest("$1,266.18 to $1,349.08 per week", 1_266.18, 1_349.08, WEEK),
    salarytest("$100000 - $130000 per annum", 100_000, 130_000, YEAR),
    salarytest("$53000 per annum", 53_000, unit=YEAR),
    salarytest("$57,000 incl Super + bonuses", 57_000, super=True),
    salarytest("$110k + bonus", 110_000),
    # TODO: Currency
    salarytest("£110000 - £120000 per annum", 110_000, 120_000, YEAR),
    salarytest("Up to $220K Package", 220_000),
    salarytest("$170-180k + Profit Share", 170_000, 180_000),
    salarytest("$55K - $70K + Superannuation", 55_000, 70_000),
    salarytest("$130 to $160K", 130_000, 160_000),
    salarytest("$70-80k", 70_000, 80_000),
    salarytest("$75,000 inclusive of super", 75_000, super=True),
    salarytest("100 to $120K", 100_000, 120_000),
    salarytest("$100-130k+", 100_000, 130_000),
    salarytest("$119,557 - $131,967", 119557, 131967),
    salarytest(
        "Total remuneration package valued to $72,969. Package includes salary ($59,636 - $65,827) employer's contribution to superannuation and annual leave loading",
        59636,
        65827,
        YEAR,
        False,
    ),
    salarytest("$0 - $79000 per annum", 0, 79_000, YEAR),
    salarytest("$140 - $160000 per annum", 140_000, 160_000, YEAR),
    # salarytest("$150 - $170 per annum"),
    salarytest("Band 7 ($90,632 - $100,666 pa)", 90_632, 100_666, YEAR),
    salarytest("84000 - 99,601.85", 84000, 99_601.85),
    salarytest(
        "$67,100 - $92,150 plus 15.4% superannuation", 67_100, 92_150, super=False
    ),
    salarytest("73,636 - $78,873 (plus super)", 73_636, 78_873, super=False),
    salarytest("$146,116 plus 15% Superannuation", 146_116, super=False),
    salarytest("From $95k + Super + 3.5% CLA", 95_000, super=False),
    salarytest(
        "$67k - $73k pa (Level 4 - Award) plus salary packaging to $18,000pa",
        67_000,
        73_000,
        YEAR,
    ),
    salarytest("Starting from $58,692 pa (4 days per week)", 58_692, unit=YEAR),
    salarytest("40000-60000 per Year", 40_000, 60_000, YEAR),
    salarytest(
        "Band 6: $87,041.24 - $94,749 per annum + super",
        87_041.24,
        94_749,
        YEAR,
        super=False,
    ),
    salarytest("$70,000 - 76,000 p/a", 70_000, 76_000, YEAR),
    salarytest("$70,000 - $80,000(based on skill and experience)", 70_000, 80_000),
    salarytest("$73,796pa", 73_796, unit=YEAR),
    salarytest(
        "Level 7 - 8 salary range is $94,266.12 - $119,401.50 per annum (pro-rata) + superannuation",
        94_266.12,
        119_401.50,
        YEAR,
        False,
    ),
    salarytest("$100,000 (0.6 FTE)", 100_000),
    salarytest(
        "AU$83964 - AU$96350 per annum + super + salary sacrifice",
        83_964,
        96_350,
        YEAR,
        False,
    ),
    salarytest(
        "SCHADS Level 4.4 (SACS Grade 4 Year 4), $75661.04 pro-rata p.a.",
        75_661.04,
        unit=YEAR,
    ),
    # salarytest("Level 6 - $94,409 to $103,497 / Level 7- $107,134 to $118,283", 94_409, 118_283),
    salarytest("$100,000 +", 100_000),
    salarytest("80-90k pro rata", 80_000, 90_000),
    salarytest("Express Process You Could Be Working In 3 Days"),
    salarytest("Competitive Salary + 17.5% Leave Loading + RDO"),
    # Hard
    #salarytest("Please call 08 7729 1352 for further information"),
    #salarytest("Children's Services Award Victoria 2010 3.1-3.4"),
    salarytest("4 nights Mon -Thu, night shift (10pm to 8am)"),
    salarytest("$85k _$95k Base +Package", 85_000, 95_000, super=False),
    #salarytest("$115,824  $156,740", 115_824, 156_740),
    #salarytest("Up to $100000.00 p.a. + Car + $15 - $20k Commission", 100_000, unit=YEAR),
    #salarytest("$30000 plus if working 4 shifts a week", 30_000),
    salarytest("Subject to QLD Anglican Schools EBA 2018"),

]


def create_salary_unit_test(test):
    def _salary_unit_test(self):
        self.assertEqual(salary_unit(test.text), test.unit)

    return _salary_unit_test


def create_salary_value_test(test):
    def _salary_value_test(self):
        low, hi = extract_salary(test.text)
        self.assertEqual(test.min, low)
        self.assertEqual(test.max, hi)

    return _salary_value_test


class TestSalary(unittest.TestCase):
    pass


for idx, test in enumerate(salary_tests):
    setattr(TestSalary, f"test_unit_{idx}", create_salary_unit_test(test))
    setattr(TestSalary, f"test_value_{idx}", create_salary_value_test(test))

if __name__ == "__main__":
    unittest.main()
