import logging
import click
from firefox_book_utils import get_driver, login, go_to_facility, book, confirm_book
from recaptcha import solve_recaptcha
from utils import get_strtime, wait_until

@click.command()
@click.option('--username', '-u', required=True, help='username')
@click.option('--password', '-p', required=False, help='password')
# @click.option('--facility', '-f', default="tennis", help='guid of facility')
@click.option('--facility', '-f', required=True, help='facility name, mapping can be found in firefox_book_utils')
@click.option('--date_slot', '-ds', required=True, help='date slot')
@click.option('--time_slot', '-ts', required=True, help='time slot')
@click.option('--time_until', '-tu', default="23:59:58", help='specific time on when the facility booking start')
@click.option('--site_url', '-lu', default="https://app.iplusliving.com/", help='login url')
def main(username, password, facility, date_slot, time_slot, time_until, site_url):
    password = password if password else click.prompt('Password', hide_input=True)
    # driver = get_driver(headless=False)
    # login(driver, username, password, site_url)
    # go_to_facility(driver, facility, site_url)
    # solve_recaptcha(driver)
    with get_driver(headless=False) as driver:
        try:
            login(driver, username, password, site_url)
            wait_until(time_until) # start the following code after the until time reached
            logging.info(f"{time_until} has been reached")
            go_to_facility(driver, facility, site_url)
            solve_recaptcha(driver)
            book(driver, date_slot, time_slot)
            confirm_book(driver)
        except Exception as ex:
            logging.error(ex)

if __name__ == '__main__':
    strtime = get_strtime()
    filename = f"logs/sr_facility_book-{strtime}.log"
    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    main()