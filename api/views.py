from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import ai_qsar_model

valid_species = ["Goats", "Swine", "Sheep", "Chickens", "Turkeys", "Cattle"]

def is_valid_cas(cas):
    # CAS format: number-number-number
    parts = cas.split('-')
    if len(parts) == 3 and all(part.isdigit() for part in parts) and len(cas) <= 20:
        return True
    return False

@api_view(['POST'])
def singleinputDatapost(request):
    # {"CAS": "75184-71-3", "Species": "Chicken"}

    CAS = request.data.get('CAS')
    Species = request.data.get('Species')

    if not is_valid_cas(CAS):
        return Response("Invalid CAS Number format", status=400)

    if Species not in valid_species:
        return Response("Invalid Species", status=400)

    data = [[CAS, Species]]

    y_preds_v2 = ai_qsar_model.ai_qsar_predict(data)
    y_pred = "{:.2f}".format(y_preds_v2[0][0])

    return Response(y_pred)

@api_view(['POST'])
def fileinputDatapost(request):
    # [{"CAS": "75184-71-3", "Species": "Chicken"},{"CAS": "317-34-0", "Species": "Cattle"}]
    data = []
    results = []

    for item in request.data:
        CAS = item.get('CAS')
        Species = item.get('Species')

        if not is_valid_cas(CAS):
            return Response(f"Invalid CAS Number format: {CAS}", status=400)

        if Species not in valid_species:
            return Response(f"Invalid Species: {Species}", status=400)

        data.append([CAS, Species])

    y_preds_v2 = ai_qsar_model.ai_qsar_predict(data)

    for i in range(len(y_preds_v2)):
        results.append({'CAS': data[i][0], 'Species': data[i][1], 'LambdaZHl': "{:.2f}".format(y_preds_v2[i][0])})

    return Response(results)

# @api_view(['POST'])
# def singleinputDatapost(request):
#     # {"CAS": "75184-71-3", "Species": "Chicken"}

#     CAS = request.data['CAS']
#     Species = request.data['Species']

#     data = [[CAS, Species]]

#     y_preds_v2 = ai_qsar_model.ai_qsar_predict(data)
#     y_pred = "{:.2f}".format(y_preds_v2[0][0])

#     return Response(y_pred)

# @api_view(['POST'])
# def fileinputDatapost(request):
#     # [{"CAS": "75184-71-3", "Species": "Chicken"},{"CAS": "317-34-0", "Species": "Cattle"}]
#     data = []
#     results = []

#     for item in request.data:
#         CAS = item.get('CAS')
#         Species = item.get('Species')

#         data.append([CAS, Species])

#         # if CAS and Species:
#         #     y_pred = ai_qsar_model.ai_qsar_predict(CAS, Species)
#         #     results.append({'CAS': CAS, 'Species': Species, 'LambdaZHl': "{:.2f}".format(y_pred)})

#     y_preds_v2 = ai_qsar_model.ai_qsar_predict(data)

#     for i in range(len(y_preds_v2)):
#         results.append({'CAS': data[i][0], 'Species': data[i][1], 'LambdaZHl': "{:.2f}".format(y_preds_v2[i][0])})

#     return Response(results)