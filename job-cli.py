from cli import Jobcli
import argparse

parser = argparse.ArgumentParser(description='Job cli, tool for finding jobs ')
parser.add_argument('outdir', type=str, help='Output dir for excel')
parser.add_argument('--n',default=10,type=int, help='number of jobs to be scraped')
parser.add_argument('--parser',default='fresher_cooker',type=str,help='Website to be used for scraping')

args = parser.parse_args()


if __name__ == '__main__':
    # TODO: add more websites
    # TODO: add glassdoor salaries
    
    cli = Jobcli(n=args.n,default_scraper=args.parser)
    cli.run()
    cli.generate_excel(args.outdir)
