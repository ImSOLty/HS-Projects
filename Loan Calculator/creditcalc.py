from argparse import ArgumentParser
import math

parser = ArgumentParser()
parser.add_argument('--type')
parser.add_argument('--payment')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')

args = parser.parse_args()

if args.type not in ['annuity', 'diff'] or (args.payment is not None and args.type == 'diff') or args.interest is None \
        or any(elem is not None and float(elem) < 0 for elem in
               [args.principal, args.payment, args.principal, args.periods, args.interest]):
    print('Incorrect parameters')
else:
    payment = None if args.payment is None else float(args.payment)
    principal = None if args.principal is None else float(args.principal)
    periods = None if args.periods is None else int(args.periods)
    interest = None if args.interest is None else float(args.interest)
    missing = args.type
    i = interest / (12 * 100)
    if missing != 'diff':
        missing = 'n' if periods is None else 'a' if payment is None else 'p'
        calc = 0
        match missing:
            case 'n':
                months = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
                over = principal - months * payment
                print(f'It will take {int(months / 12)} years and {months % 12} months to repay this loan!')
            case 'a':
                annuity = principal * ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1))
                over = principal - periods * math.ceil(annuity)
                print(f'Your monthly payment = {math.ceil(annuity)}!')
            case "p":
                principal = math.floor(payment / ((i * pow(1 + i, periods)) / (pow(1 + i, periods) - 1)))
                over = payment * periods - principal
                print(f'Your loan principal = {principal}!')
        print(f"Overpayment = {over}")
    else:
        over = 0
        for j in range(1, periods + 1):
            calc = math.ceil(principal / periods + i * (principal - principal * (j - 1) / periods))
            over += calc
            print(f"Month {j}: payment is {calc}")
        print(f"Overpayment: {over-principal}")
