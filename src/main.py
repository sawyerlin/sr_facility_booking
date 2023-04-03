import logging
import click
from firefox_book_utils import get_driver, login, go_to_facility, book, confirm_book
from recaptcha import solve_recaptcha
from utils import get_strtime, wait_until

@click.command()
@click.option('--username', '-u', required=True, help='username')
@click.option('--password', '-p', required=False, help='password')
@click.option('--facility', '-f', required=True, help='facility name, mapping can be found in firefox_book_utils')
@click.option('--date', '-d', required=True, help='date')
@click.option('--is_next_month/--is_current_month', default=False, help='month')
@click.option('--time', '-t', required=True, help='time')
@click.option('--wait', '-w', default="2023-03-31 23:59:58", help='specific datetime on wait')
@click.option('--site_url', '-lu', default="https://app.iplusliving.com/", help='login url')
def main(username, password, facility, date, is_next_month, time, wait, site_url):
    password = password if password else click.prompt('Password', hide_input=True)
    with get_driver(headless=False) as driver:
        try:
            login(driver, username, password, site_url)
            go_to_facility(driver, facility, site_url)
            solve_recaptcha(driver)
            book(driver, is_next_month, date, time, wait)
            confirm_book(driver)
        except Exception as ex:
            logging.error(ex)

if __name__ == '__main__':
    strtime = get_strtime()
    filename = f"logs/sr_facility_book-{strtime}.log"
    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    main()