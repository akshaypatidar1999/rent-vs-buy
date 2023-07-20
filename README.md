# Rent vs Buy

## Assumption
This simulation is run on the following assumption: The downpayment is invested if renting and the difference in rent and EMI for a year is reinvested at the end of the year

## How to use

```shell
pip3 install -r requirements.txt
python3 buy_vs_rent.py --starting-rent 80000 --flat-cost 25000000 --initial-downpayment 0 --loan-tenure 20 --loan-interest-rate 8 --years 30 --flat-cost-appreciation 7 --log-level DEBUG
```

### Available options
```
--starting-rent: Starting rent per month
--rent-appreciation: Estimated percent rent appreciation per year
--flat-cost: Cost of flat
--flat-cost-appreciation: Estimated percent increase in cost of flat per year
--initial-downpayment: Initial downpayment when buying flat
--loan-interest-rate: Interest rate at which home loan will be procured
--loan-tenure: Tenure in which loan is repaid
--investment-return: If you chose to rent, investment XIRR
--years: Years for which simulation should be run
--log-level: Log level
```
