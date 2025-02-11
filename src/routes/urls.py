# Pages
from contents.miscellaneous import code_401, code_404, code_500, code_503
from contents.login import login_page
from contents.signup import signup_page

from contents.service_list import product_catalog_page
from contents.dashboard import seller_dashboard_page
from contents.add_service import add_service_page
from contents.service_detail import service_detail_page

# Layouts
from layouts.common_layout import CommonLayout
from layouts.basic_layout import BasicLayout
from layouts.dashboard_layout import DashboardLayout


routes = {
    # Common
    "/": {"page": product_catalog_page, "protected": False, "layout": BasicLayout},
    "/home": {"page": product_catalog_page, "protected": False, "layout": BasicLayout},

    # Auth contents
    "/auth/login": {"page": login_page, "protected": False, "layout": BasicLayout},
    "/auth/signup": {"page": signup_page, "protected": False, "layout": BasicLayout},

    # Miscellaneous
    "/401": {"page": code_401, "protected": False, "layout": CommonLayout},
    "/404": {"page": code_404, "protected": False, "layout": CommonLayout},
    "/500": {"page": code_500, "protected": False, "layout": CommonLayout},
    "/503": {"page": code_503, "protected": False, "layout": CommonLayout},

    # Protected - Dashboard profile_page
    "/dashboard": {"page": seller_dashboard_page, "protected": True, "layout": DashboardLayout},
    "/services/new": {"page": add_service_page, "protected": True, "layout": DashboardLayout},
    
    "/services/<int:service_id>": {"page": service_detail_page, "protected": False, "layout": CommonLayout},

    # Protected - Webapp
    
}
