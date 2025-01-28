# Pages
from contents.miscellaneous import code_401, code_404, code_500, code_503

# Layouts
from layouts.common_layout import CommonLayout


routes = {
    # Common
    # "/": {"page": home_page, "protected": False, "layout": CommonLayout},
    # "/home": {"page": home_page, "protected": False, "layout": CommonLayout},

    # Auth contents

    # Miscellaneous
    "/401": {"page": code_401, "protected": False, "layout": CommonLayout},
    "/404": {"page": code_404, "protected": False, "layout": CommonLayout},
    "/500": {"page": code_500, "protected": False, "layout": CommonLayout},
    "/503": {"page": code_503, "protected": False, "layout": CommonLayout},

    # Protected - Dashboard profile_page

    # Protected - Webapp
}
