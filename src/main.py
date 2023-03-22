import click
from firefox_book_utils import get_driver, login, go_to_facility, book, confirm_book
from recaptcha import solve_recaptcha

@click.command()
@click.option('--username', '-u', required=True, help='username')
# @click.option('--facility', '-f', default="tennis", help='guid of facility')
@click.option('--facility', '-f', required=True, help='facility name, mapping can be found in firefox_book_utils')
@click.option('--date_slot', '-ds', required=True, help='date slot')
@click.option('--time_slot', '-ts', required=True, help='time slot')
@click.option('--login_url', '-lu', default="https://app.iplusliving.com/site/login", help='login url')
def main(username, facility, date_slot, time_slot, login_url):
    password = click.prompt('Password', hide_input=True)
    driver = get_driver(headless=False)

    login(driver, username, password, login_url)
    go_to_facility(driver, facility)
    solve_recaptcha(driver)
    book(driver, date_slot, time_slot)
    confirm_book(driver)

    driver.close()

if __name__ == '__main__':
    main()