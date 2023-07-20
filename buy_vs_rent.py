import argparse, logging, sys
from colorlog import ColoredFormatter

def setup_logging(log_level):
	formatter = ColoredFormatter(
	    "%(log_color)s%(message)s%(reset)s",
	    log_colors = {
	    	"INFO": "green",
	        "WARNING": "yellow",
	        "ERROR": "red"    
	    }
	)
	std_out_streaming_handler = logging.StreamHandler(sys.stdout)
	std_out_streaming_handler.setLevel(log_level)
	std_out_streaming_handler.setFormatter(formatter)

	logging.basicConfig(**{
		"level" : log_level,
	    "handlers" : [std_out_streaming_handler]
	})

# Returns monthly EMI
def calculate_emi(principal, rate, tenure):
	monthly_rate = rate / (12 * 100)
	tenure_months = tenure * 12
	return (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)


def appreciate_value(principal, rate, period):
	return principal * ((1 + rate/100) ** period)

def log_stats(year, total_rent, total_emi, current_money_rent, current_money_buy, flat_cost):
	logging.debug(f"\n================================= YEAR {year} =================================")
	logging.debug(f"Total Rent Paid: {total_rent}")
	logging.debug(f"Total EMI Paid: {total_emi}")
	logging.debug(f"Current Money When Renting: {current_money_rent}")
	logging.debug(f"Current Money When Buying excluding flat cost: {current_money_buy}")
	logging.debug(f"Flat cost: {flat_cost}")

def simulate(args):
	# Variables which will not change throughout the simulation
	rent_appreciation = float(args.rent_appreciation)
	flat_cost_appreciation = float(args.flat_cost_appreciation)
	initial_downpayment = int(args.initial_downpayment)
	loan_interest_rate = float(args.loan_interest_rate)
	loan_tenure = int(args.loan_tenure)
	investment_return = float(args.investment_return)
	years = int(args.years)

	# Variables that will change every year
	flat_cost = int(args.flat_cost)
	monthly_rent = int(args.starting_rent)

	# Validations
	if years < loan_tenure:
		logging.error("Number of simulation years should be greater than or equal to loan tenure")
		sys.exit(1)

	logging.info("This simulation is run on the following assumption: The downpayment is invested if renting and the difference in rent and EMI for a year is reinvested at the end of the year\n")

	# Variables denoting current money in case of rent and buying
	current_money_rent = initial_downpayment
	current_money_buy = 0

	monthly_emi = calculate_emi(flat_cost - initial_downpayment, loan_interest_rate, loan_tenure)

	logging.info(f"Monthly EMI Installments: {monthly_emi}")

	for year in range(1, years + 1):
		rental_expense = 12 * monthly_rent
		emi_expense = 0 if year > loan_tenure else 12 * monthly_emi

		current_money_rent = appreciate_value(current_money_rent, investment_return, 1)
		current_money_buy = appreciate_value(current_money_buy, investment_return, 1)

		# Invest difference between rental expense and emi expense
		current_money_buy = current_money_buy + max(0, rental_expense - emi_expense)
		current_money_rent = current_money_rent + max(0, emi_expense - rental_expense)

		# Appreciate rent and flat cost
		monthly_rent = appreciate_value(monthly_rent, rent_appreciation, 1)
		flat_cost = appreciate_value(flat_cost, flat_cost_appreciation, 1)

		# Log stats
		log_stats(year, rental_expense, emi_expense, current_money_rent, current_money_buy, flat_cost)


	rent_networth = current_money_rent
	buy_networth = current_money_buy + flat_cost


	logging.debug(f"\n================================= SUMMARY =================================")
	logging.info(f"Networth when renting: {rent_networth}")
	logging.info(f"Networth when buying: {buy_networth}")
	action = "buy" if buy_networth > rent_networth else "rent"

	logging.info(f"Recommended to {action} flat. Savings: {abs(buy_networth - rent_networth)}")

	return rent_networth, buy_networth

parser = argparse.ArgumentParser()
parser.add_argument("--starting-rent", help="Starting rent per month", required=True)
parser.add_argument("--rent-appreciation", help="Estimated percent rent appreciation per year", default=5)
parser.add_argument("--flat-cost", help="Cost of flat", required=True)
parser.add_argument("--flat-cost-appreciation", help="Estimated percent increase in cost of flat per year", default=5)
parser.add_argument("--initial-downpayment", help="Initial downpayment when buying flat", required=True)
parser.add_argument("--loan-interest-rate", help="Interest rate at which home loan will be procured", default=8)
parser.add_argument("--loan-tenure", help="Tenure in which loan is repaid", required=True)
parser.add_argument("--investment-return", help="If you chose to rent, investment XIRR", default=12)
parser.add_argument("--years", help="Years for which simulation should be run", default=30)
parser.add_argument("--log-level", help="Log level", default="INFO")

args = parser.parse_args()
setup_logging(args.log_level)
simulate(args)
