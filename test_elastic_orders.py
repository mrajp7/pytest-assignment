import pytest
import pytest_check as check
from order_helper import Orders
from validations import validate_non_empty_string, validate_email_address, \
        validate_phone_number, validate_gender, validate_int, \
        validate_date_time, validate_weekdays_value, validate_order_json_schema, \
        validate_order_details_against_product, validate_order_payment_details

ORDERS = Orders.get_instance().list

class TestOrders:

    @pytest.mark.user_details
    def test_user_details_name_validation(self):
        """
        Objective: Validate the User Name fields are having right type values and present

        Steps: 
        1. Check first name does not contains any number and special characters (only allowed ' ', '.')
        2. Check Customer Full Name does not contains any number and special characters (only allowed ' ', '.')
        3. Check the Last name does not contains any number and special characters (only allowed ' ', '.')
        """
        check.is_true(validate_non_empty_string(ORDERS, "customer_first_name"), 
                        "Errors in Customer First Name")
        check.is_true(validate_non_empty_string(ORDERS, "customer_full_name"),
                        "Errors in Customer Full Name")
        check.is_true(validate_non_empty_string(ORDERS, "customer_last_name"),
                        "Errors in Customer Last Name")

    @pytest.mark.user_details
    def test_user_details_contact_info_validation(self):
        """
        Objective: validate the user contact details (email, phone) are having right type, values and present

        Steps:
        1. Check the Email validation of the user
        2. Check the Phone number field is present
        """
        check.is_true(validate_email_address(ORDERS, "email"), "Errors in Email validation")
        check.is_true(validate_phone_number(orders=ORDERS, key="customer_phone", allow_empty=True),
                        "Erros in Phone number validation")

    @pytest.mark.user_details
    def test_user_details_general_validation(self):
        """
        Objective: Validate the general details of the user such as Gender, Customer ID
        """
        check.is_true(validate_gender(ORDERS, "customer_gender"), "Errors in Gender validation")
        check.is_true(validate_int(ORDERS, "customer_id"), "Errors in Customer ID validation")

    @pytest.mark.date_time
    def test_date_time_validation(self):
        """
        Objective: Validate the date time fields of the Order
        """
        check.is_true(validate_date_time(ORDERS, "order_date"), "Errors in order_date validation")
        check.is_true(validate_weekdays_value(ORDERS, "order_date", "day_of_week","day_of_week_i"),
                                                "Errors in Weekday validations")

    @pytest.mark.order
    def test_order_json_schema_validation(self):
        """
        Objective:

        Steps:
        """
        assert validate_order_json_schema(ORDERS,"products")

    @pytest.mark.order
    def test_product_products_order_generic_validation(self):
        """
        Objective:
        """
        assert validate_order_details_against_product(ORDERS)

    @pytest.mark.order
    def test_order_amount_against_products(self):
        """
        Objective: To test the Order Amount is matching with the Products added.
        """
        assert validate_order_payment_details(ORDERS)

        
