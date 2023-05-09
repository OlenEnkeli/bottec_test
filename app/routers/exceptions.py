from fastapi import HTTPException


def rate_not_found(code: str):
    return HTTPException(
        status_code=404,
        detail={
            'Not found': f'Rate for currency {code}'
        }
    )


def rates_not_found():
    return HTTPException(
        status_code=404,
        detail={
            'Not found': 'Rates are empty. \n'
            'Try to recall this method later'
        }
    )
