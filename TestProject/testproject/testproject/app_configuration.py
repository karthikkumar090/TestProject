PROJECT_ROOT_FOLDER = "testproject"
SITE_HEADER = "testproject Admin"
REST_API_UI_HEADER = "testproject APIs"

IDENTITY_MESSAGE_SETTINGS = {
    "PASSWORD": {
        "regex": r"^(?=.{8,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$",
        "regex-message": "Password must be at least 8 char.One capital letter,one lower case letter,one number, and one special character.",
        "blank": "Password is mandatory.",
        "mismatch": "Password and Confirm password are not matching. Please re-enter.",
    },
    "EMAIL": {
        "blank": "Email address is mandatory.",
        "email_pass": 'Must include "email" and "password".',
    },
    "FIRST_NAME": {
        "blank": "First name is required",
        "alpha": "First Name field allows only alphabet characters and this is Mandatory.",
    },
    "LAST_NAME": {
        "blank": "First name is required",
        "alpha": "First Name field allows only alphabet characters and this is Mandatory.",
    },
    "PHONE_NUMBER": {
        "blank": "Phone number is required",
        "existed": "A user has already been registered with this phone number",
    },
    "CONFIRM_PASSWORD": {"mismatch": "Confirm password does not match"},
    "USER": {
        "logged-in": "User already logged in",
        "not-match-type-when-login": "Unauthorized",
    },
    "backend": "allauth.account.auth_backends.AuthenticationBackend",
}

ROOT_URLCONF = "testproject.urls"
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "authentication.serializers.RegisterSerializer",
}
REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "authentication.serializers.LoginSerializer",
}

APP_MIDDLEWARE = []
WSGI_APPLICATION = "testproject.wsgi.application"
