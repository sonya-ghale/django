from django.shortcuts import render

# This is the function (def) called post_list that take request and will return the values 
def post_list(request):
    return render(request, 'blog/post_list.html', {})