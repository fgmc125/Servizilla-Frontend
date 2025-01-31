from flet import Page


def detect_device_type(page: Page):
    platform = str(page.platform)
    platform = platform.replace("PagePlatform.", "").upper()

    user_agent = page.client_user_agent

    if platform.upper() == "ANDROID" and "DART" in user_agent.upper():
        device_type = "ANDROID APP"
    elif platform.upper() == "ANDROID" and (
            "Mozilla" in user_agent or "AppleWebKit" in user_agent or "Chrome" in user_agent or "Safari" in user_agent):
        device_type = "MOBILE BROWSER"
    elif platform.upper() == "IOS":
        device_type = "IOS APP"
    elif platform.upper() == "WINDOWS" and user_agent == "":
        device_type = "DESKTOP APP"
    elif platform.upper() == "WINDOWS" or platform == "MACOS" and (
            "Mozilla" in user_agent or "AppleWebKit" in user_agent or "Chrome" in user_agent or "Safari" in user_agent):
        device_type = "WEB BROWSER"
    else:
        device_type = "UNKNOWN DEVICE"

    return {
        "platform": platform,
        "user_agent": user_agent,
        "device_type": device_type,
        "is_browser": device_type in ["WEB BROWSER", "MOBILE BROWSER"],
        "is_mobile": platform in ["ANDROID", "IOS"],
    }