# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sniffapi.scheduler import create_scent_post

@csrf_exempt
def automate_new_scent(request):
    if request.method == 'POST':
        try:
            # Call the Python script to create a new scent post
            new_scent_post = create_scent_post()

            # Serialize the new scent post data
            new_scent_data = {
                'title': new_scent_post.title,
                'description': new_scent_post.description,
                'category': new_scent_post.category.name,
                'tags': [tag.name for tag in new_scent_post.tags.all()],
                # Add any other relevant fields
            }

            # Return the new scent post data as a JSON response
            return JsonResponse(new_scent_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)