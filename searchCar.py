import pprint
import requests

token = "Token 41b42b7083e058a39581b4e6e7dcb2bad727638e"
regions = ["il"]

def manipulate_license_plate(license_plate):
    listResult = []
    for license_number in license_plate:
        print("license_number", license_number)
        listResult.append(license_number)
        # if len(license_number) % 2 == 0:
        #     first_three_digits = license_number[:3]
        #     listResult.append(first_three_digits)
        #     last_three_digits = license_number[-3:]
        #     listResult.append(last_three_digits)
        # if len(license_number) % 2 == 1:
        #     mid_index = len(license_number) // 2
        #     three_middle_digits = license_number[mid_index - 1:mid_index + 2]
        #     listResult.append(three_middle_digits)
    return license_number


def searchCar():
    with open('image.jpg', 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),
            files=dict(upload=fp),
            headers={'Authorization': token}
        )

    result = response.json()
    pprint.pprint(result)
    license_plates = []
    if 'results' in result and result['results']:
        for car_result in result['results']:
            if 'plate' in car_result:
                license_plate = car_result['plate']
                license_plates.append(license_plate)
                manipulated_plate = manipulate_license_plate(license_plates)
        return manipulated_plate

    return license_plates if license_plates else None