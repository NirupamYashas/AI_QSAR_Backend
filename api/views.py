from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import ai_qsar_model

@api_view(['POST'])
def postData(request):
    # {"casNumber": "75184-71-3", "selectedSpecies": "Chicken"}

    CAS = request.data['casNumber']
    Species = request.data['selectedSpecies']

    y_preds_v2 = ai_qsar_model.ai_qsar_predict(CAS, Species)

    return Response(y_preds_v2)